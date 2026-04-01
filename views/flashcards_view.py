import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class FlashcardsView(ctk.CTkFrame):
    """Sistema de Flashcards com repetição espaçada (SM-2)."""

    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db

        self._mode = "menu"  # menu | review | create | browse
        self._cards = []
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}

        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_lb = ctk.CTkLabel(
            self, text="🃏 Flashcards",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.grid(row=0, column=0, pady=(20, 10), padx=25, sticky="w")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(
            row=1, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════
    # ── MENU PRINCIPAL ───────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_menu(self):
        self._mode = "menu"
        self._clear_content()
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        # Estatísticas
        stats = self.db.get_flashcard_stats(uid)

        stats_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(10, 15))

        stat_items = [
            ("🃏", "Total de Cards", str(stats["total"])),
            ("📖", "Já Revisados", str(stats["reviewed"])),
            ("📬", "Para Revisar", str(stats["due"])),
        ]

        for emoji, label, value in stat_items:
            card = ctk.CTkFrame(stats_frame, corner_radius=12, fg_color=t["card"],
                                height=90)
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)
            ctk.CTkLabel(
                card, text=f"{emoji} {value}",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=t["primary"],
            ).pack(pady=(18, 2))
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=11),
                text_color=t["text_sec"],
            ).pack()

        # Botões de ação
        ctk.CTkLabel(
            scroll, text="📚 Ações",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(15, 10))

        actions_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        actions_frame.pack(fill="x", pady=5)

        # Botão Revisar
        due_count = stats["due"]
        review_text = f"📬  Revisar Agora ({due_count} pendentes)" if due_count > 0 else "✅  Tudo revisado!"

        ctk.CTkButton(
            actions_frame, text=review_text,
            height=50, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=t["success"] if due_count > 0 else t["card"],
            hover_color=t["button_hover"],
            state="normal" if due_count > 0 else "disabled",
            command=self._start_review,
        ).pack(fill="x", pady=4)

        ctk.CTkButton(
            actions_frame, text="➕  Criar Novo Flashcard",
            height=45, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=t["button"], hover_color=t["button_hover"],
            command=self._show_create,
        ).pack(fill="x", pady=4)

        ctk.CTkButton(
            actions_frame, text="📖  Ver Todos os Flashcards",
            height=45, font=ctk.CTkFont(size=14),
            fg_color=t["card"], hover_color=t["button_hover"],
            command=self._show_browse,
        ).pack(fill="x", pady=4)

        if stats["total"] > 0:
            ctk.CTkButton(
                actions_frame, text="🗑️  Limpar Todos os Flashcards",
                height=40, font=ctk.CTkFont(size=13),
                fg_color=t["card"], hover_color=t["danger"],
                text_color=t["danger"],
                command=self._confirm_clear_all,
            ).pack(fill="x", pady=4)

        # Revisar por matéria
        subjects = self.db.get_flashcard_subjects(uid)
        if subjects:
            ctk.CTkLabel(
                scroll, text="📂 Revisar por Matéria",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=t["primary"],
            ).pack(anchor="w", pady=(20, 10))

            subjects_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            subjects_frame.pack(fill="x")

            row_frame = None
            for i, subj in enumerate(subjects):
                if i % 3 == 0:
                    row_frame = ctk.CTkFrame(
                        subjects_frame, fg_color="transparent")
                    row_frame.pack(fill="x", pady=3)

                cards = self.db.get_flashcards(uid, subject=subj)

                card = ctk.CTkFrame(
                    row_frame, corner_radius=10, fg_color=t["card"])
                card.pack(side="left", fill="x", expand=True, padx=3)

                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=12, pady=10)

                ctk.CTkLabel(
                    inner, text=f"📚 {subj}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=t["text"],
                ).pack(anchor="w")

                ctk.CTkLabel(
                    inner, text=f"{len(cards)} cards",
                    font=ctk.CTkFont(size=11),
                    text_color=t["text_sec"],
                ).pack(anchor="w")

                ctk.CTkButton(
                    inner, text="Revisar", height=28, width=80,
                    font=ctk.CTkFont(size=11),
                    fg_color=t["primary"], hover_color=t["button_hover"],
                    command=lambda s=subj: self._start_review_subject(s),
                ).pack(anchor="w", pady=(5, 0))

    # ══════════════════════════════════════════════════════════
    # ── LIMPAR TODOS OS FLASHCARDS ───────────────────────────
    # ══════════════════════════════════════════════════════════
    def _confirm_clear_all(self):
        uid = self.app.get_user_id()
        stats = self.db.get_flashcard_stats(uid)
        total = stats.get("total", 0)

        msg = CTkMessagebox(
            title="Limpar Flashcards",
            message=f"⚠️ Tem certeza que deseja apagar TODOS os {total} flashcards?\n\n"
                    "Esta ação não pode ser desfeita.\n"
                    "Todas as revisões e progresso serão perdidos.",
            icon="warning",
            option_1="Cancelar",
            option_2="Apagar Todos",
        )
        if msg.get() == "Apagar Todos":
            removed = self.db.delete_all_flashcards(uid)
            CTkMessagebox(
                title="Concluído ✅",
                message=f"🗑️ {removed} flashcards removidos com sucesso!",
                icon="check",
            )
            self._show_menu()

    # ══════════════════════════════════════════════════════════
    # ── MODO REVISÃO ─────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _start_review(self):
        uid = self.app.get_user_id()
        self._cards = self.db.get_flashcards_for_review(uid, limit=20)
        if not self._cards:
            CTkMessagebox(
                title="Info", message="Nenhum flashcard para revisar agora!", icon="check")
            return
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}
        self._show_review_card()

    def _start_review_subject(self, subject):
        uid = self.app.get_user_id()
        cards = self.db.get_flashcards(uid, subject=subject)
        if not cards:
            CTkMessagebox(
                title="Info", message="Nenhum flashcard nesta matéria!", icon="warning")
            return
        self._cards = cards
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}
        self._show_review_card()

    def _show_review_card(self):
        self._clear_content()
        t = self.app.theme_mgr.get_theme()

        if self._card_index >= len(self._cards):
            self._show_review_results()
            return

        card_data = self._cards[self._card_index]

        # Header com progresso
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", pady=(10, 5))

        ctk.CTkLabel(
            header,
            text=f"Card {self._card_index + 1} de {len(self._cards)}",
            font=ctk.CTkFont(size=14),
            text_color=t["text_sec"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=f"📚 {card_data.get('subject', '')} — {card_data.get('topic', '')}",
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
        ).pack(side="right")

        progress = ctk.CTkProgressBar(
            self.content_frame, height=6, corner_radius=3)
        progress.set(self._card_index / len(self._cards))
        progress.configure(progress_color=t["accent"], fg_color=t["secondary"])
        progress.pack(fill="x", pady=(0, 15))

        # Card principal
        card_frame = ctk.CTkFrame(
            self.content_frame, corner_radius=20,
            fg_color=t["card"], height=300,
        )
        card_frame.pack(fill="x", pady=10, padx=40)
        card_frame.pack_propagate(False)

        if not self._showing_back:
            # Frente do card
            ctk.CTkLabel(
                card_frame, text="PERGUNTA",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=t["accent"],
            ).pack(pady=(30, 10))

            ctk.CTkLabel(
                card_frame,
                text=card_data["front"],
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=t["text"],
                wraplength=500,
                justify="center",
            ).pack(expand=True, padx=30)

            ctk.CTkButton(
                card_frame, text="👁️  Mostrar Resposta",
                height=45, width=250,
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=t["primary"], hover_color=t["button_hover"],
                command=self._flip_card,
            ).pack(pady=(10, 30))
        else:
            # Verso do card
            ctk.CTkLabel(
                card_frame, text="RESPOSTA",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=t["success"],
            ).pack(pady=(25, 5))

            ctk.CTkLabel(
                card_frame,
                text=card_data["back"],
                font=ctk.CTkFont(size=18),
                text_color=t["text"],
                wraplength=500,
                justify="center",
            ).pack(expand=True, padx=30)

            # Pergunta original (menor)
            ctk.CTkLabel(
                card_frame,
                text=f"❓ {card_data['front']}",
                font=ctk.CTkFont(size=12),
                text_color=t["text_sec"],
                wraplength=500,
            ).pack(pady=(0, 15))

        # Botões de avaliação (só no verso)
        if self._showing_back:
            eval_frame = ctk.CTkFrame(
                self.content_frame, fg_color="transparent")
            eval_frame.pack(fill="x", padx=40, pady=15)

            ctk.CTkLabel(
                eval_frame, text="Como foi? Avalie sua lembrança:",
                font=ctk.CTkFont(size=14),
                text_color=t["text_sec"],
            ).pack(pady=(0, 10))

            btns_frame = ctk.CTkFrame(eval_frame, fg_color="transparent")
            btns_frame.pack()

            eval_buttons = [
                ("❌ Esqueci", 1, t["danger"], "forgot"),
                ("😐 Difícil", 3, t["warning"], "hard"),
                ("👍 Médio", 4, "#2196F3", "medium"),
                ("⭐ Fácil", 5, t["success"], "easy"),
            ]

            for text, quality, color, key in eval_buttons:
                ctk.CTkButton(
                    btns_frame, text=text, width=120, height=45,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color=color, hover_color=t["button_hover"],
                    command=lambda q=quality, k=key: self._rate_card(q, k),
                ).pack(side="left", padx=4)

        # Botão sair
        ctk.CTkButton(
            self.content_frame, text="← Voltar ao Menu",
            height=32, width=150,
            font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color=t["card"],
            text_color=t["text_sec"],
            command=self._show_menu,
        ).pack(pady=(10, 5))

    def _flip_card(self):
        self._showing_back = True
        self._show_review_card()

    def _rate_card(self, quality, key):
        uid = self.app.get_user_id()
        card = self._cards[self._card_index]

        # Salvar revisão
        self.db.save_flashcard_review(card["id"], quality, uid)

        # Estatísticas
        self._review_results["total"] += 1
        self._review_results[key] += 1

        # XP pela revisão
        xp = {1: 2, 3: 5, 4: 8, 5: 10}.get(quality, 5)
        if uid:
            self.db.add_xp(uid, xp, "flashcard", f"Revisão de flashcard")
            self.db.update_daily_goal_progress(uid, "xp", xp)

        # Próximo card
        self._card_index += 1
        self._showing_back = False
        self._show_review_card()

    def _show_review_results(self):
        self._clear_content()
        t = self.app.theme_mgr.get_theme()

        results_card = ctk.CTkFrame(
            self.content_frame, corner_radius=16, fg_color=t["card"])
        results_card.pack(fill="x", pady=30, padx=40)

        ctk.CTkLabel(
            results_card, text="🎉 Revisão Concluída!",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(25, 15))

        total = self._review_results["total"]
        items = [
            ("⭐ Fácil", self._review_results["easy"], t["success"]),
            ("👍 Médio", self._review_results["medium"], "#2196F3"),
            ("😐 Difícil", self._review_results["hard"], t["warning"]),
            ("❌ Esquecido", self._review_results["forgot"], t["danger"]),
        ]

        for label, count, color in items:
            row = ctk.CTkFrame(results_card, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=3)

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(size=14),
                text_color=t["text"],
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=str(count),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=color,
            ).pack(side="right")

        ctk.CTkLabel(
            results_card,
            text=f"📊 Total: {total} cards revisados",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=t["accent"],
        ).pack(pady=(15, 20))

        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, text="🃏  Voltar ao Menu",
            height=42, width=200,
            fg_color=t["button"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._show_menu,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="🏠  Dashboard",
            height=42, width=200,
            fg_color=t["card"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14),
            command=lambda: self.app.show_frame("dashboard"),
        ).pack(side="left", padx=5)

    # ══════════════════════════════════════════════════════════
    # ── CRIAR FLASHCARD ──────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_create(self):
        self._clear_content()
        t = self.app.theme_mgr.get_theme()

        card = ctk.CTkFrame(self.content_frame,
                            corner_radius=16, fg_color=t["card"])
        card.pack(fill="x", pady=20, padx=40)

        ctk.CTkLabel(
            card, text="➕ Criar Novo Flashcard",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(20, 15))

        # Matéria
        ctk.CTkLabel(card, text="Matéria:", font=ctk.CTkFont(size=13),
                     text_color=t["text"]).pack(anchor="w", padx=30)
        self._create_subject = ctk.CTkEntry(
            card, placeholder_text="Ex: Matemática", width=400, height=38,
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self._create_subject.pack(padx=30, pady=(2, 8))

        # Tópico
        ctk.CTkLabel(card, text="Tópico (opcional):", font=ctk.CTkFont(size=13),
                     text_color=t["text"]).pack(anchor="w", padx=30)
        self._create_topic = ctk.CTkEntry(
            card, placeholder_text="Ex: Fórmulas", width=400, height=38,
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self._create_topic.pack(padx=30, pady=(2, 8))

        # Frente
        ctk.CTkLabel(card, text="Pergunta (frente):", font=ctk.CTkFont(size=13),
                     text_color=t["text"]).pack(anchor="w", padx=30)
        self._create_front = ctk.CTkTextbox(
            card, width=400, height=80,
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self._create_front.pack(padx=30, pady=(2, 8))

        # Verso
        ctk.CTkLabel(card, text="Resposta (verso):", font=ctk.CTkFont(size=13),
                     text_color=t["text"]).pack(anchor="w", padx=30)
        self._create_back = ctk.CTkTextbox(
            card, width=400, height=80,
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self._create_back.pack(padx=30, pady=(2, 8))

        # Dificuldade
        self._create_diff = ctk.CTkOptionMenu(
            card, values=["fácil", "médio", "difícil"], width=200,
            fg_color=t["button"], button_color=t["button_hover"],
        )
        self._create_diff.set("médio")
        self._create_diff.pack(padx=30, pady=(2, 10))

        # Botões
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(5, 20))

        ctk.CTkButton(
            btn_frame, text="💾  Salvar", width=150, height=40,
            fg_color=t["success"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._save_flashcard,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="← Cancelar", width=150, height=40,
            fg_color=t["card"], hover_color=t["secondary"],
            font=ctk.CTkFont(size=14),
            command=self._show_menu,
        ).pack(side="left", padx=5)

    def _save_flashcard(self):
        subject = self._create_subject.get().strip()
        topic = self._create_topic.get().strip()
        front = self._create_front.get("1.0", "end").strip()
        back = self._create_back.get("1.0", "end").strip()
        diff = self._create_diff.get()

        if not subject or not front or not back:
            CTkMessagebox(
                title="Atenção", message="Preencha a matéria, pergunta e resposta.", icon="warning")
            return

        uid = self.app.get_user_id()
        self.db.create_flashcard(front, back, subject,
                                 topic, difficulty=diff, user_id=uid)

        # XP por criar flashcard
        if uid:
            self.db.add_xp(uid, 5, "flashcard_create", "Flashcard criado")
            self.db.check_and_grant_achievements(uid)

        CTkMessagebox(title="Sucesso",
                      message="Flashcard criado com sucesso! 🃏", icon="check")
        self._show_menu()

    # ══════════════════════════════════════════════════════════
    # ── NAVEGAR FLASHCARDS ───────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_browse(self):
        self._clear_content()
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(10, 15))

        ctk.CTkLabel(
            header, text="📖 Todos os Flashcards",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["primary"],
        ).pack(side="left")

        ctk.CTkButton(
            header, text="← Voltar", width=100, height=32,
            fg_color=t["card"], hover_color=t["secondary"],
            font=ctk.CTkFont(size=12),
            command=self._show_menu,
        ).pack(side="right")

        cards = self.db.get_flashcards(uid)

        if not cards:
            ctk.CTkLabel(
                scroll,
                text="Nenhum flashcard ainda.\nClique em 'Criar Novo Flashcard' para começar!",
                font=ctk.CTkFont(size=14),
                text_color=t["text_sec"],
            ).pack(pady=40)
            return

        # Agrupar por matéria
        by_subject = {}
        for c in cards:
            subj = c.get("subject", "Outros")
            by_subject.setdefault(subj, []).append(c)

        for subj, subj_cards in by_subject.items():
            ctk.CTkLabel(
                scroll, text=f"📚 {subj} ({len(subj_cards)})",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=t["accent"],
            ).pack(anchor="w", pady=(15, 5))

            for card_data in subj_cards:
                card = ctk.CTkFrame(
                    scroll, corner_radius=10, fg_color=t["card"])
                card.pack(fill="x", pady=3)
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=10)
                inner.grid_columnconfigure(0, weight=1)

                # Frente
                ctk.CTkLabel(
                    inner,
                    text=f"❓ {card_data['front']}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=t["text"],
                    anchor="w", wraplength=500,
                ).grid(row=0, column=0, sticky="w")

                # Verso
                ctk.CTkLabel(
                    inner,
                    text=f"💡 {card_data['back']}",
                    font=ctk.CTkFont(size=12),
                    text_color=t["text_sec"],
                    anchor="w", wraplength=500,
                ).grid(row=1, column=0, sticky="w")

                # Deletar (só se for do usuário)
                if card_data.get("user_id") == uid:
                    ctk.CTkButton(
                        inner, text="🗑️", width=34, height=34,
                        fg_color="transparent", hover_color=t["danger"],
                        command=lambda fid=card_data["id"]: self._delete_card(
                            fid),
                    ).grid(row=0, column=1, rowspan=2, sticky="e")

    def _delete_card(self, flashcard_id):
        msg = CTkMessagebox(
            title="Confirmar", message="Deseja excluir este flashcard?",
            icon="question", option_1="Cancelar", option_2="Excluir",
        )
        if msg.get() == "Excluir":
            self.db.delete_flashcard(flashcard_id)
            self._show_browse()

    # ── lifecycle ────────────────────────────────────────────
    def on_show(self):
        self._show_menu()
        # Atalhos de teclado para flashcards
        self.app.bind("<Left>", self._on_key_left)
        self.app.bind("<Right>", self._on_key_right)

    def _on_key_left(self, event=None):
        """Atalho: seta esquerda para virar card."""
        if not self.winfo_ismapped() or self._mode != "review":
            return
        if not self._showing_back:
            self._flip_card()

    def _on_key_right(self, event=None):
        """Atalho: seta direita para próximo (avaliar como Médio)."""
        if not self.winfo_ismapped() or self._mode != "review":
            return
        if self._showing_back:
            self._rate_card(4, "medium")

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.content_frame.configure(fg_color=t["bg"])
