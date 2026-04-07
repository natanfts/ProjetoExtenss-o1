import flet as ft


class FlashcardsView:
    """Flashcards com repetição espaçada (SM-2)."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._mode = "menu"  # menu | review | create | results
        self._cards = []
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}

    def on_show(self):
        self._mode = "menu"

    def build(self):
        if self._mode == "review":
            return self._build_review()
        elif self._mode == "create":
            return self._build_create()
        elif self._mode == "results":
            return self._build_results()
        return self._build_menu()

    def _build_menu(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()
        stats = self.db.get_flashcard_stats(uid)

        stat_cards = []
        for emoji, label, value in [
            ("🃏", "Total", str(stats["total"])),
            ("📖", "Revisados", str(stats["reviewed"])),
            ("📬", "Pendentes", str(stats["due"])),
        ]:
            stat_cards.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, expand=True,
                    padding=ft.padding.symmetric(vertical=15, horizontal=10),
                    content=ft.Column([
                        ft.Text(f"{emoji} {value}", size=22,
                                weight=ft.FontWeight.BOLD, color=t["primary"]),
                        ft.Text(label, size=11, color=t["text_sec"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                )
            )

        due = stats["due"]
        review_text = f"📬 Revisar Agora ({due} pendentes)" if due > 0 else "✅ Tudo revisado!"

        # Matérias
        subjects = self.db.get_flashcard_subjects(uid)
        subject_tiles = []
        for subj in subjects:
            cards = self.db.get_flashcards(uid, subject=subj)
            subject_tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=10, padding=12,
                    on_click=lambda _, s=subj: self._start_review_subject(s),
                    content=ft.Row([
                        ft.Column([
                            ft.Text(
                                f"📚 {subj}", size=13, weight=ft.FontWeight.BOLD, color=t["text"]),
                            ft.Text(f"{len(cards)} cards",
                                    size=11, color=t["text_sec"]),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.PLAY_ARROW, color=t["primary"]),
                    ]),
                )
            )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row(stat_cards, spacing=6),
                ft.ElevatedButton(
                    content=ft.Text(review_text), height=50, width=400,
                    bgcolor=t["success"] if due > 0 else t["card"],
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12)),
                    disabled=due == 0,
                    on_click=lambda _: self._start_review(),
                ),
                ft.ElevatedButton(
                    content=ft.Text("➕ Criar Novo Flashcard"), height=45, width=400,
                    bgcolor=t["button"], color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=lambda _: self._show_create(),
                ),
                ft.ElevatedButton(
                    content=ft.Text("📖 Ver Todos"), height=40, width=400,
                    bgcolor=t["card"], color=t["text"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=lambda _: self._show_browse(),
                ),
                ft.Container(height=5),
                ft.Text("📂 Por Matéria", size=16,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                *subject_tiles,
            ], spacing=8, scroll=ft.ScrollMode.AUTO),
        )

    # ── Revisão ──────────────────────────────────────────────
    def _start_review(self):
        uid = self.app.get_user_id()
        self._cards = self.db.get_flashcards_for_review(uid, limit=20)
        if not self._cards:
            self.app.show_snackbar("✅ Nenhum flashcard para revisar agora!")
            return
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}
        self._mode = "review"
        self.app.show_view("flashcards")

    def _start_review_subject(self, subject):
        uid = self.app.get_user_id()
        self._cards = self.db.get_flashcards(uid, subject=subject)
        if not self._cards:
            self.app.show_snackbar("⚠️ Nenhum flashcard nesta matéria!")
            return
        self._card_index = 0
        self._showing_back = False
        self._review_results = {"total": 0, "easy": 0,
                                "medium": 0, "hard": 0, "forgot": 0}
        self._mode = "review"
        self.app.show_view("flashcards")

    def _build_review(self):
        t = self.app.theme_mgr.get_theme()

        if self._card_index >= len(self._cards):
            self._mode = "results"
            return self._build_results()

        card = self._cards[self._card_index]
        progress = self._card_index / len(self._cards) if self._cards else 0

        if not self._showing_back:
            # Frente
            card_content = ft.Container(
                bgcolor=t["card"], border_radius=20, height=280,
                padding=30, alignment=ft.Alignment.CENTER,
                on_click=lambda _: self._flip_card(),
                content=ft.Column([
                    ft.Text("PERGUNTA", size=12,
                            weight=ft.FontWeight.BOLD, color=t["accent"]),
                    ft.Text(card["front"], size=20, weight=ft.FontWeight.BOLD,
                            color=t["text"], text_align=ft.TextAlign.CENTER),
                    ft.Container(height=15),
                    ft.Text("👁️ Toque para ver resposta",
                            size=13, color=t["text_sec"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER),
            )
            quality_row = ft.Container()
        else:
            # Verso
            card_content = ft.Container(
                bgcolor=t["card"], border_radius=20, height=280,
                padding=30, alignment=ft.Alignment.CENTER,
                content=ft.Column([
                    ft.Text("RESPOSTA", size=12,
                            weight=ft.FontWeight.BOLD, color=t["success"]),
                    ft.Text(card["back"], size=18, color=t["text"],
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER),
            )
            quality_row = ft.Column([
                ft.Text("Como foi?", size=14, color=t["text_sec"],
                        text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.ElevatedButton("😵 Esqueci", bgcolor=t["danger"], color="#FFF", expand=True,
                                      on_click=lambda _: self._rate(0)),
                    ft.ElevatedButton("😅 Difícil", bgcolor=t["warning"], color="#000", expand=True,
                                      on_click=lambda _: self._rate(3)),
                    ft.ElevatedButton("🙂 Bom", bgcolor=t["primary"], color="#FFF", expand=True,
                                      on_click=lambda _: self._rate(4)),
                    ft.ElevatedButton("😎 Fácil", bgcolor=t["success"], color="#FFF", expand=True,
                                      on_click=lambda _: self._rate(5)),
                ], spacing=6),
            ], spacing=8)

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row([
                    ft.TextButton("← Voltar", on_click=lambda _: self._back_to_menu(),
                                  style=ft.ButtonStyle(color=t["text_sec"])),
                    ft.Text(f"{self._card_index + 1}/{len(self._cards)}",
                            size=14, color=t["text_sec"]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=progress, height=6, color=t["accent"],
                               bgcolor=t["secondary"], border_radius=3),
                ft.Text(f"📚 {card.get('subject', '')} — {card.get('topic', '')}",
                        size=13, color=t["text_sec"]),
                card_content,
                quality_row,
            ], spacing=10),
        )

    def _flip_card(self):
        self._showing_back = True
        self.app.show_view("flashcards")

    def _rate(self, quality):
        card = self._cards[self._card_index]
        uid = self.app.get_user_id()

        # Registrar review no banco
        if uid:
            self.db.review_flashcard(uid, card["id"], quality)
            self.db.add_xp(uid, 5, "flashcard", "Revisão de flashcard")
            self.db.update_daily_goal_progress(uid, "xp", 5)

        # Atualizar resultados
        self._review_results["total"] += 1
        if quality >= 5:
            self._review_results["easy"] += 1
        elif quality >= 4:
            self._review_results["medium"] += 1
        elif quality >= 3:
            self._review_results["hard"] += 1
        else:
            self._review_results["forgot"] += 1

        self._card_index += 1
        self._showing_back = False
        self.app.show_view("flashcards")

    def _build_results(self):
        t = self.app.theme_mgr.get_theme()
        r = self._review_results
        total = r["total"] or 1

        uid = self.app.get_user_id()
        if uid:
            self.db.check_and_grant_achievements(uid)
            self.app.refresh_xp_sidebar()

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            alignment=ft.Alignment.CENTER, padding=30,
            content=ft.Column([
                ft.Text("🎉 Revisão Concluída!", size=24,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                ft.Container(height=10),
                ft.Text(f"📊 {r['total']} cards revisados",
                        size=16, color=t["text"]),
                ft.Container(height=10),
                ft.Row([
                    ft.Container(bgcolor=t["success"], border_radius=8, padding=12, expand=True,
                                 content=ft.Column([
                                     ft.Text(
                                         f"😎 {r['easy']}", size=18, weight=ft.FontWeight.BOLD, color="#FFF"),
                                     ft.Text("Fácil", size=11, color="#FFF"),
                                 ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(bgcolor=t["primary"], border_radius=8, padding=12, expand=True,
                                 content=ft.Column([
                                     ft.Text(
                                         f"🙂 {r['medium']}", size=18, weight=ft.FontWeight.BOLD, color="#FFF"),
                                     ft.Text("Bom", size=11, color="#FFF"),
                                 ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(bgcolor=t["warning"], border_radius=8, padding=12, expand=True,
                                 content=ft.Column([
                                     ft.Text(
                                         f"😅 {r['hard']}", size=18, weight=ft.FontWeight.BOLD, color="#000"),
                                     ft.Text("Difícil", size=11, color="#000"),
                                 ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(bgcolor=t["danger"], border_radius=8, padding=12, expand=True,
                                 content=ft.Column([
                                     ft.Text(
                                         f"😵 {r['forgot']}", size=18, weight=ft.FontWeight.BOLD, color="#FFF"),
                                     ft.Text("Esqueci", size=11, color="#FFF"),
                                 ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ], spacing=6),
                ft.Container(height=20),
                ft.ElevatedButton("🃏 Voltar ao Menu", height=45, width=250,
                                  bgcolor=t["button"], color="#FFF",
                                  on_click=lambda _: self._back_to_menu()),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
        )

    # ── Criar ────────────────────────────────────────────────
    def _show_create(self):
        self._mode = "create"
        self.app.show_view("flashcards")

    def _build_create(self):
        t = self.app.theme_mgr.get_theme()

        subject_f = ft.TextField(label="Matéria", width=350, height=50,
                                 bgcolor=t["entry_bg"], border_color=t["entry_border"],
                                 color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]))
        topic_f = ft.TextField(label="Tópico", width=350, height=50,
                               bgcolor=t["entry_bg"], border_color=t["entry_border"],
                               color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]))
        front_f = ft.TextField(label="Frente (Pergunta)", width=350, height=80, multiline=True,
                               bgcolor=t["entry_bg"], border_color=t["entry_border"],
                               color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]))
        back_f = ft.TextField(label="Verso (Resposta)", width=350, height=80, multiline=True,
                              bgcolor=t["entry_bg"], border_color=t["entry_border"],
                              color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]))

        def save(e):
            if not front_f.value or not back_f.value or not subject_f.value:
                self.app.show_snackbar("⚠️ Preencha matéria, frente e verso.")
                return
            uid = self.app.get_user_id()
            self.db.create_flashcard(
                uid, "enem", subject_f.value.strip(),
                topic_f.value.strip() if topic_f.value else "",
                front_f.value.strip(), back_f.value.strip(),
            )
            self.app.show_snackbar("✅ Flashcard criado!")
            self._back_to_menu()

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row([
                    ft.TextButton("← Voltar", on_click=lambda _: self._back_to_menu(),
                                  style=ft.ButtonStyle(color=t["text_sec"])),
                ]),
                ft.Text("➕ Novo Flashcard", size=20,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                subject_f, topic_f, front_f, back_f,
                ft.ElevatedButton("💾 Salvar", height=45, width=350,
                                  bgcolor=t["button"], color="#FFF",
                                  on_click=save),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
        )

    # ── Browse ───────────────────────────────────────────────
    def _show_browse(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()
        cards = self.db.get_flashcards(uid)

        tiles = []
        for card in cards[:50]:
            tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=10, padding=12,
                    content=ft.Column([
                        ft.Text(card["front"], size=14,
                                weight=ft.FontWeight.BOLD, color=t["text"]),
                        ft.Text(card["back"], size=12, color=t["text_sec"]),
                        ft.Text(f"📚 {card.get('subject', '')}  •  {card.get('difficulty', '')}",
                                size=10, color=t["text_sec"]),
                    ], spacing=4),
                )
            )

        bs = ft.BottomSheet(
            content=ft.Container(
                height=500, padding=20, bgcolor=t["bg"],
                content=ft.Column([
                    ft.Text(f"📖 Todos os Flashcards ({len(cards)})", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    *tiles,
                ], scroll=ft.ScrollMode.AUTO, spacing=8),
            ),
        )
        self.app.page.overlay.append(bs)
        bs.open = True
        self.app.page.update()

    def _back_to_menu(self):
        self._mode = "menu"
        self.app.show_view("flashcards")
