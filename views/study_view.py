import customtkinter as ctk
import json
import webbrowser
import threading
from api_service import APIService


class StudyView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self.api = APIService()

        self._category = "enem_real"
        self._subject = None
        self._fmt = "quiz"
        self._questions = []
        self._q_index = 0
        self._correct = 0
        self._answered = False

        # Estado do quiz ENEM real
        self._enem_year = None
        self._enem_discipline = None
        self._enem_questions = []
        self._enem_q_index = 0
        self._enem_correct = 0
        self._enem_answered = False
        self._loading = False

        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(
            self, text="📚 Central de Estudos",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.header.grid(row=0, column=0, pady=(20, 10), padx=25, sticky="w")

        # Conteúdo principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(
            row=1, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self._show_menu()

    # ══════════════════════════════════════════════════════════
    # ── MENU PRINCIPAL ───────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_menu(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        # Abas: ENEM Real | Questões Próprias | Concursos | Vídeos | Pesquisar
        tabs = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tabs.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tab_items = [
            ("enem_real", "🎯 ENEM Real"),
            ("enem", "📝 Quiz ENEM"),
            ("concursos", "📑 Concursos"),
            ("videos", "🎬 Vídeos"),
            ("pesquisar", "🔍 Pesquisar"),
        ]
        for cat, label in tab_items:
            btn = ctk.CTkButton(
                tabs, text=label, width=130, height=38,
                font=ctk.CTkFont(
                    size=13, weight="bold" if self._category == cat else "normal"),
                fg_color=t["primary"] if self._category == cat else t["card"],
                hover_color=t["button_hover"],
                text_color=t["text"] if self._category == cat else t["text_sec"],
                command=lambda c=cat: self._switch_category(c),
            )
            btn.pack(side="left", padx=3)

        if self._category == "enem_real":
            self._show_enem_real_menu()
        elif self._category == "pesquisar":
            self._show_search()
        elif self._category == "videos":
            self._show_videos_menu()
        elif self._category in ("enem", "concursos"):
            self._show_quiz_menu()

    # ══════════════════════════════════════════════════════════
    # ── ENEM REAL — Seleção de Ano ───────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_enem_real_menu(self):
        t = self.app.theme_mgr.get_theme()

        scroll = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nswe")
        scroll.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(
            scroll,
            text="🎯 Questões Reais do ENEM — Provas Oficiais",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            scroll,
            text="Questões reais das provas do ENEM de 2009 a 2023.\n"
                 "Selecione o ano desejado para começar. As questões são baixadas da API oficial e salvas localmente.",
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
            justify="left", wraplength=700,
        ).pack(anchor="w", pady=(0, 15))

        # Grid de anos
        cached_years = self.db.get_cached_enem_years()

        years_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        years_frame.pack(fill="x", pady=5)

        row_frame = None
        for i, year in enumerate(range(2023, 2008, -1)):
            if i % 5 == 0:
                row_frame = ctk.CTkFrame(years_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=4)

            is_cached = year in cached_years
            cached_count = self.db.get_cached_enem_year_count(
                year) if is_cached else 0

            card = ctk.CTkFrame(
                row_frame, corner_radius=12,
                fg_color=t["card"], height=100, width=140,
            )
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card, text=f"📋 {year}",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=t["text"],
            ).pack(pady=(12, 2))

            if is_cached:
                ctk.CTkLabel(
                    card, text=f"✅ {cached_count} questões",
                    font=ctk.CTkFont(size=10),
                    text_color=t["success"],
                ).pack(pady=(0, 4))
            else:
                ctk.CTkLabel(
                    card, text="📥 Baixar",
                    font=ctk.CTkFont(size=10),
                    text_color=t["text_sec"],
                ).pack(pady=(0, 4))

            ctk.CTkButton(
                card, text="Iniciar" if is_cached else "Baixar",
                width=90, height=26,
                font=ctk.CTkFont(size=11),
                fg_color=t["primary"] if is_cached else t["accent"],
                hover_color=t["button_hover"],
                command=lambda y=year: self._select_enem_year(y),
            ).pack(pady=(0, 8))

        # Estatísticas do usuário
        stats = self.db.get_enem_quiz_stats_by_year(self.app.get_user_id())
        if stats:
            ctk.CTkLabel(
                scroll, text="📊 Seu Desempenho por Ano",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=t["primary"],
            ).pack(anchor="w", pady=(25, 10))

            for s in stats:
                disc_name = self.api.ENEM_DISCIPLINES.get(
                    s.get("discipline", ""), s.get("discipline", "Todas"))
                stat_card = ctk.CTkFrame(
                    scroll, corner_radius=10, fg_color=t["card"])
                stat_card.pack(fill="x", pady=3)
                inner = ctk.CTkFrame(stat_card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=10)

                ctk.CTkLabel(
                    inner,
                    text=f"📋 ENEM {s['year']} — {disc_name}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=t["text"],
                ).pack(side="left")

                avg = s.get("avg_score", 0) or 0
                best = s.get("best_score", 0) or 0
                attempts = s.get("attempts", 0)
                score_color = t["success"] if avg >= 70 else t["accent"] if avg >= 50 else t["danger"]
                ctk.CTkLabel(
                    inner,
                    text=f"Média: {avg:.0f}%  |  Melhor: {best:.0f}%  |  {attempts}x",
                    font=ctk.CTkFont(size=13),
                    text_color=score_color,
                ).pack(side="right")

    # ── Selecionar ano do ENEM ───────────────────────────────
    def _select_enem_year(self, year: int):
        self._enem_year = year

        if self.db.has_enem_year_cached(year):
            self._show_enem_disciplines(year)
        else:
            self._download_enem_year(year)

    # ── Baixar questões de um ano ────────────────────────────
    def _download_enem_year(self, year: int):
        if self._loading:
            return
        self._loading = True

        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        loading_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        loading_frame.grid(row=1, column=0, sticky="nswe")
        loading_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            loading_frame,
            text=f"📥 Baixando questões do ENEM {year}...",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(80, 10))

        self._dl_status = ctk.CTkLabel(
            loading_frame,
            text="Conectando à API enem.dev...",
            font=ctk.CTkFont(size=14),
            text_color=t["text_sec"],
        )
        self._dl_status.pack(pady=5)

        self._dl_progress = ctk.CTkProgressBar(
            loading_frame, width=400, height=14,
            progress_color=t["accent"],
        )
        self._dl_progress.pack(pady=15)
        self._dl_progress.set(0)

        ctk.CTkLabel(
            loading_frame,
            text="Isso pode levar alguns segundos na primeira vez.\n"
                 "As questões são salvas localmente para uso offline.",
            font=ctk.CTkFont(size=12),
            text_color=t["text_sec"],
            justify="center",
        ).pack(pady=10)

        # Baixar em background thread
        def _download():
            try:
                self._update_dl_status("Buscando questões...")
                self._update_dl_progress(0.1)
                questions = self.api.fetch_enem_questions(year, limit=200)
                self._update_dl_progress(0.7)

                if questions:
                    self._update_dl_status(
                        f"Salvando {len(questions)} questões no cache...")
                    self._update_dl_progress(0.85)
                    self.db.cache_enem_questions(questions)
                    self._update_dl_progress(1.0)
                    self._update_dl_status(
                        f"✅ {len(questions)} questões baixadas com sucesso!")
                    self.after(800, lambda: self._show_enem_disciplines(year))
                else:
                    self._update_dl_status(
                        "❌ Não foi possível baixar as questões. Verifique sua conexão.")
                    self.after(2000, self._show_menu)
            except Exception as e:
                self._update_dl_status(f"❌ Erro: {e}")
                self.after(2000, self._show_menu)
            finally:
                self._loading = False

        threading.Thread(target=_download, daemon=True).start()

    def _update_dl_status(self, text):
        try:
            self._dl_status.configure(text=text)
        except Exception:
            pass

    def _update_dl_progress(self, value):
        try:
            self._dl_progress.set(value)
        except Exception:
            pass

    # ── Seleção de disciplina ────────────────────────────────
    def _show_enem_disciplines(self, year: int):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        # Header
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkButton(
            top, text="← Voltar", width=90, height=32,
            fg_color=t["card"], hover_color=t["secondary"],
            command=self._show_menu,
        ).pack(side="left")

        ctk.CTkLabel(
            top, text=f"🎯 ENEM {year} — Escolha a Área",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(side="left", padx=15)

        total_cached = self.db.get_cached_enem_year_count(year)
        ctk.CTkLabel(
            top, text=f"📋 {total_cached} questões",
            font=ctk.CTkFont(size=13),
            text_color=t["success"],
        ).pack(side="right")

        scroll = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nswe")

        disciplines = self.db.get_enem_disciplines_for_year(year)

        # Card "Todas as Questões"
        all_card = ctk.CTkFrame(scroll, corner_radius=14,
                                fg_color=t["card"], height=90)
        all_card.pack(fill="x", pady=6, padx=4)
        all_card.pack_propagate(False)
        all_inner = ctk.CTkFrame(all_card, fg_color="transparent")
        all_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            all_inner, text=f"🎯 Todas as Áreas — {total_cached} questões",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t["text"],
        ).pack(side="left")

        # Seletor de quantidade
        qty_frame = ctk.CTkFrame(all_inner, fg_color="transparent")
        qty_frame.pack(side="right")

        for qty_label, qty_val in [("10", 10), ("20", 20), ("45", 45), ("Todas", 200)]:
            ctk.CTkButton(
                qty_frame, text=qty_label, width=55, height=30,
                font=ctk.CTkFont(size=12),
                fg_color=t["primary"], hover_color=t["button_hover"],
                command=lambda n=qty_val: self._start_enem_quiz(year, None, n),
            ).pack(side="left", padx=2)

        # Cards por disciplina
        disc_emojis = {
            "linguagens": "📖",
            "ciencias-humanas": "🏛️",
            "ciencias-natureza": "🔬",
            "matematica": "📐",
        }

        for disc in disciplines:
            emoji = disc_emojis.get(disc["discipline"], "📋")
            card = ctk.CTkFrame(scroll, corner_radius=14,
                                fg_color=t["card"], height=85)
            card.pack(fill="x", pady=4, padx=4)
            card.pack_propagate(False)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=20, pady=12)

            ctk.CTkLabel(
                inner,
                text=f"{emoji} {disc['discipline_name']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=t["text"],
            ).pack(side="left")

            ctk.CTkLabel(
                inner,
                text=f"{disc['count']} questões",
                font=ctk.CTkFont(size=12),
                text_color=t["text_sec"],
            ).pack(side="left", padx=15)

            btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
            btn_frame.pack(side="right")

            for qty_label, qty_val in [("10", 10), ("20", 20), ("Todas", disc["count"])]:
                ctk.CTkButton(
                    btn_frame, text=qty_label, width=55, height=28,
                    font=ctk.CTkFont(size=11),
                    fg_color=t["accent"], hover_color=t["button_hover"],
                    text_color="#000",
                    command=lambda d=disc["discipline"], n=qty_val, y=year:
                        self._start_enem_quiz(y, d, n),
                ).pack(side="left", padx=2)

        # Botão para re-baixar
        ctk.CTkButton(
            scroll, text="🔄 Re-baixar questões deste ano",
            height=36, fg_color=t["card"], hover_color=t["secondary"],
            text_color=t["text_sec"],
            command=lambda: self._redownload_year(year),
        ).pack(pady=15)

    def _redownload_year(self, year: int):
        """Remove cache do ano e baixa novamente."""
        conn = self.db._conn()
        conn.execute("DELETE FROM enem_questions WHERE year=?", (year,))
        conn.commit()
        conn.close()
        self._download_enem_year(year)

    # ══════════════════════════════════════════════════════════
    # ── QUIZ ENEM REAL ───────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _start_enem_quiz(self, year: int, discipline: str = None, limit: int = 10):
        self._enem_year = year
        self._enem_discipline = discipline
        self._enem_questions = self.db.get_enem_questions(
            year, discipline, limit=limit)

        if not self._enem_questions:
            return

        self._enem_q_index = 0
        self._enem_correct = 0
        self._show_enem_question()

    def _show_enem_question(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()
        self._enem_answered = False
        q = self._enem_questions[self._enem_q_index]
        total = len(self._enem_questions)

        # ── Header ───────────────────────────────────────────
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkButton(
            top, text="✕ Sair", width=70, height=30,
            fg_color=t["danger"], hover_color="#EF5350",
            font=ctk.CTkFont(size=12),
            command=self._confirm_exit_quiz,
        ).pack(side="left")

        disc_name = q.get("discipline_name", "")
        title_text = f"ENEM {self._enem_year}"
        if disc_name:
            title_text += f" — {disc_name}"

        ctk.CTkLabel(
            top, text=title_text,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=t["primary"],
        ).pack(side="left", padx=12)

        # Progresso
        progress_text = f"Questão {self._enem_q_index + 1}/{total}"
        ctk.CTkLabel(
            top, text=progress_text,
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
        ).pack(side="left", padx=8)

        score_text = f"✅ {self._enem_correct}/{self._enem_q_index}"
        ctk.CTkLabel(
            top, text=score_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=t["success"],
        ).pack(side="right")

        # Barra de progresso
        prog_bar = ctk.CTkProgressBar(
            top, width=120, height=8,
            progress_color=t["accent"],
        )
        prog_bar.pack(side="right", padx=10)
        prog_bar.set((self._enem_q_index) / total)

        # ── Corpo da questão ─────────────────────────────────
        body = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nswe")

        # Título da questão
        q_title = q.get("title", f"Questão {q.get('question_index', '?')}")
        ctk.CTkLabel(
            body, text=q_title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=t["accent"],
        ).pack(anchor="w", pady=(8, 5))

        # Contexto / texto-base
        context = q.get("context", "")
        if context and len(context) > 5:
            ctx_frame = ctk.CTkFrame(
                body, corner_radius=10, fg_color=t["card"])
            ctx_frame.pack(fill="x", pady=(0, 10), padx=5)

            ctk.CTkLabel(
                ctx_frame, text="📄 Texto-base:",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=t["text_sec"],
            ).pack(anchor="w", padx=12, pady=(8, 2))

            # Limitar tamanho do contexto para exibição
            display_ctx = context[:2000] + \
                "..." if len(context) > 2000 else context
            ctk.CTkLabel(
                ctx_frame, text=display_ctx,
                font=ctk.CTkFont(size=13),
                text_color=t["text"],
                wraplength=680, justify="left",
            ).pack(anchor="w", padx=12, pady=(0, 10))

        # Imagens (se houver)
        images = q.get("images", [])
        if images:
            ctk.CTkLabel(
                body,
                text="🖼️ Esta questão contém imagem(ns). Clique para visualizar:",
                font=ctk.CTkFont(size=11),
                text_color=t["text_sec"],
            ).pack(anchor="w", padx=5, pady=(0, 3))
            for img_url in images:
                ctk.CTkButton(
                    body, text=f"🔗 Ver imagem", width=130, height=26,
                    font=ctk.CTkFont(size=11),
                    fg_color=t["card"], hover_color=t["secondary"],
                    text_color=t["accent"],
                    command=lambda url=img_url: webbrowser.open(url),
                ).pack(anchor="w", padx=5, pady=2)

        # Enunciado
        intro = q.get("question_intro", "")
        if intro and intro != context:
            ctk.CTkLabel(
                body, text=intro,
                font=ctk.CTkFont(size=15),
                text_color=t["text"],
                wraplength=680, justify="left",
            ).pack(anchor="w", pady=(8, 15), padx=5)

        # ── Alternativas ─────────────────────────────────────
        options = q["options"]
        self._enem_option_buttons = []

        for opt in options:
            btn = ctk.CTkButton(
                body, text=f"  {opt}", height=50, anchor="w",
                font=ctk.CTkFont(size=14),
                fg_color=t["card"], hover_color=t["secondary"],
                text_color=t["text"],
                corner_radius=10,
                command=lambda o=opt: self._answer_enem(o),
            )
            btn.pack(fill="x", pady=3, padx=15)
            self._enem_option_buttons.append((btn, opt))

        # Área de feedback
        self._enem_feedback_frame = ctk.CTkFrame(body, fg_color="transparent")
        self._enem_feedback_frame.pack(fill="x", pady=15, padx=15)

    def _answer_enem(self, selected: str):
        if self._enem_answered:
            return
        self._enem_answered = True

        t = self.app.theme_mgr.get_theme()
        q = self._enem_questions[self._enem_q_index]
        correct = q["correct_answer"]
        is_correct = selected == correct

        if is_correct:
            self._enem_correct += 1

        # Colorir botões
        for btn, opt in self._enem_option_buttons:
            if opt == correct:
                btn.configure(fg_color=t["success"], text_color="#FFF")
            elif opt == selected and not is_correct:
                btn.configure(fg_color=t["danger"], text_color="#FFF")
            btn.configure(state="disabled")

        # Feedback
        icon = "✅ Correto!" if is_correct else f"❌ Incorreto! Resposta: {q.get('correct_letter', '')}"
        ctk.CTkLabel(
            self._enem_feedback_frame, text=icon,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=t["success"] if is_correct else t["danger"],
        ).pack(anchor="w")

        # Botão próxima / resultado
        if self._enem_q_index + 1 < len(self._enem_questions):
            ctk.CTkButton(
                self._enem_feedback_frame, text="Próxima →", width=150, height=40,
                fg_color=t["primary"], hover_color=t["button_hover"],
                font=ctk.CTkFont(size=14, weight="bold"),
                command=self._next_enem_question,
            ).pack(pady=(12, 0))
        else:
            self._show_enem_result()

    def _next_enem_question(self):
        self._enem_q_index += 1
        self._show_enem_question()

    def _confirm_exit_quiz(self):
        """Salva progresso parcial e volta ao menu."""
        total_answered = self._enem_q_index
        if self._enem_answered:
            total_answered += 1
        if total_answered > 0:
            score = (self._enem_correct / total_answered * 100)
            self.db.save_enem_quiz_progress(
                self._enem_year, self._enem_discipline or "todas",
                total_answered, self._enem_correct, score,
                self.app.get_user_id(),
            )
        self._category = "enem_real"
        self._show_menu()

    def _show_enem_result(self):
        t = self.app.theme_mgr.get_theme()
        total = len(self._enem_questions)
        score = (self._enem_correct / total * 100) if total else 0

        # Salvar progresso
        self.db.save_enem_quiz_progress(
            self._enem_year, self._enem_discipline or "todas",
            total, self._enem_correct, score,
            self.app.get_user_id(),
        )

        # Resultado
        ctk.CTkLabel(
            self._enem_feedback_frame,
            text=f"\n🏆 Resultado Final — ENEM {self._enem_year}",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["accent"],
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self._enem_feedback_frame,
            text=f"Acertos: {self._enem_correct} de {total}  ({score:.0f}%)",
            font=ctk.CTkFont(size=18),
            text_color=t["text"],
        ).pack(pady=5)

        # Barra visual
        result_bar = ctk.CTkProgressBar(
            self._enem_feedback_frame, width=350, height=16,
            progress_color=t["success"] if score >= 70 else t["accent"] if score >= 50 else t["danger"],
        )
        result_bar.pack(pady=10)
        result_bar.set(score / 100)

        msg = ("🌟 Excelente! Você está muito bem preparado!" if score >= 80
               else "👍 Bom trabalho! Continue praticando!" if score >= 60
               else "💪 Continue estudando! A prática leva à perfeição!" if score >= 40
               else "📚 Foque nos estudos! Revise os conteúdos dessa área.")
        ctk.CTkLabel(
            self._enem_feedback_frame, text=msg,
            font=ctk.CTkFont(size=15),
            text_color=t["text_sec"],
        ).pack(pady=8)

        btn_frame = ctk.CTkFrame(
            self._enem_feedback_frame, fg_color="transparent")
        btn_frame.pack(pady=12)

        ctk.CTkButton(
            btn_frame, text="🔄 Refazer Quiz", width=160, height=40,
            fg_color=t["primary"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._start_enem_quiz(
                self._enem_year, self._enem_discipline, len(self._enem_questions)),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="📋 Outro Ano", width=160, height=40,
            fg_color=t["accent"], hover_color=t["button_hover"],
            text_color="#000",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._switch_category("enem_real"),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="← Menu", width=100, height=40,
            fg_color=t["card"], hover_color=t["secondary"],
            command=self._show_menu,
        ).pack(side="left", padx=5)

    # ══════════════════════════════════════════════════════════
    # ── QUIZ DE QUESTÕES PRÓPRIAS (enem/concursos) ───────────
    # ══════════════════════════════════════════════════════════
    def _show_quiz_menu(self):
        t = self.app.theme_mgr.get_theme()
        cat = self._category

        scroll = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nswe")

        subjects = self.db.get_subjects(cat, "quiz")
        if not subjects:
            ctk.CTkLabel(
                scroll, text="Nenhum conteúdo disponível para esta categoria.",
                font=ctk.CTkFont(size=14), text_color=t["text_sec"],
            ).pack(pady=40)
            return

        row_frame = None
        for i, subj in enumerate(subjects):
            if i % 2 == 0:
                row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                row_frame.pack(fill="x", pady=4)

            card = ctk.CTkFrame(row_frame, corner_radius=12,
                                fg_color=t["card"], height=110)
            card.pack(side="left", fill="x", expand=True, padx=6)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card, text=subj, font=ctk.CTkFont(size=16, weight="bold"),
                text_color=t["text"],
            ).pack(pady=(15, 5))

            ctk.CTkButton(
                card, text="📝 Iniciar Quiz", width=130, height=30,
                font=ctk.CTkFont(size=12),
                fg_color=t["primary"], hover_color=t["button_hover"],
                command=lambda s=subj: self._start_quiz(s),
            ).pack(pady=5)

        # Botão buscar na API
        ctk.CTkButton(
            scroll, text="🌐 Buscar questões extras online (inglês)",
            height=38, fg_color=t["card"], hover_color=t["secondary"],
            text_color=t["text_sec"],
            command=self._fetch_api,
        ).pack(pady=15)

    # ── Vídeos ───────────────────────────────────────────────
    def _show_videos_menu(self):
        t = self.app.theme_mgr.get_theme()

        scroll = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nswe")

        # Listar todas as matérias que têm vídeos
        for cat_key, cat_label in [("enem", "🎓 ENEM"), ("concursos", "📑 Concursos")]:
            video_subjects = self.db.get_subjects(cat_key, "video")
            if not video_subjects:
                continue

            ctk.CTkLabel(
                scroll, text=cat_label,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=t["primary"],
            ).pack(anchor="w", pady=(15, 8))

            row_frame = None
            for i, subj in enumerate(video_subjects):
                if i % 3 == 0:
                    row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                    row_frame.pack(fill="x", pady=3)

                card = ctk.CTkFrame(row_frame, corner_radius=10,
                                    fg_color=t["card"], height=70)
                card.pack(side="left", fill="x", expand=True, padx=4)
                card.pack_propagate(False)

                ctk.CTkLabel(
                    card, text=f"🎬 {subj}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=t["text"],
                ).pack(pady=(12, 3))

                ctk.CTkButton(
                    card, text="Ver Vídeos", width=100, height=24,
                    font=ctk.CTkFont(size=11),
                    fg_color=t["accent"], hover_color=t["button_hover"],
                    text_color="#000",
                    command=lambda s=subj, c=cat_key: self._show_videos(s, c),
                ).pack(pady=(0, 8))

    # ── pesquisa ─────────────────────────────────────────────
    def _show_search(self):
        t = self.app.theme_mgr.get_theme()
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="nswe")
        search_frame.grid_columnconfigure(0, weight=1)

        bar = ctk.CTkFrame(search_frame, fg_color="transparent")
        bar.pack(fill="x", pady=(10, 15))

        self._search_entry = ctk.CTkEntry(
            bar, placeholder_text="Busque qualquer tema: ex. 'fotossíntese', 'trigonometria'...",
            width=500, height=42,
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self._search_entry.pack(
            side="left", padx=(0, 10), fill="x", expand=True)
        self._search_entry.bind("<Return>", lambda e: self._do_search())

        ctk.CTkButton(
            bar, text="Buscar", width=100, height=42,
            fg_color=t["button"], hover_color=t["button_hover"],
            command=self._do_search,
        ).pack(side="left")

        ctk.CTkButton(
            bar, text="▶ YouTube", width=100, height=42,
            fg_color=t["danger"], hover_color="#EF5350",
            command=self._search_youtube,
        ).pack(side="left", padx=6)

        self._search_results = ctk.CTkScrollableFrame(
            search_frame, fg_color="transparent")
        self._search_results.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self._search_results,
            text="Digite um assunto e pressione Enter para buscar\nem nosso banco de questões e videoaulas.",
            font=ctk.CTkFont(size=14), text_color=t["text_sec"],
        ).pack(pady=40)

    def _do_search(self):
        query = self._search_entry.get().strip()
        if not query:
            return

        for w in self._search_results.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()
        results = self.db.search_content(query)

        if not results:
            ctk.CTkLabel(
                self._search_results,
                text=f"Nenhum resultado para '{query}'.\nTente buscar no YouTube!",
                font=ctk.CTkFont(size=14), text_color=t["text_sec"],
            ).pack(pady=40)
            return

        quizzes = [r for r in results if r["content_type"] == "quiz"]
        videos = [r for r in results if r["content_type"] == "video"]

        if quizzes:
            ctk.CTkLabel(self._search_results, text=f"📝 {len(quizzes)} questão(ões) encontrada(s)",
                         font=ctk.CTkFont(size=15, weight="bold"), text_color=t["primary"]).pack(anchor="w", pady=(10, 5))
            for q in quizzes[:10]:
                card = ctk.CTkFrame(self._search_results,
                                    corner_radius=10, fg_color=t["card"])
                card.pack(fill="x", pady=3)
                ctk.CTkLabel(card, text=f"[{q['subject']}] {q['question'][:80]}...",
                             font=ctk.CTkFont(size=13), text_color=t["text"], anchor="w",
                             wraplength=600).pack(padx=12, pady=8, anchor="w")

        if videos:
            ctk.CTkLabel(self._search_results, text=f"🎬 {len(videos)} vídeo(s) encontrado(s)",
                         font=ctk.CTkFont(size=15, weight="bold"), text_color=t["primary"]).pack(anchor="w", pady=(15, 5))
            for v in videos:
                card = ctk.CTkFrame(self._search_results,
                                    corner_radius=10, fg_color=t["card"])
                card.pack(fill="x", pady=3)
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=12, pady=8)
                ctk.CTkLabel(inner, text=f"🎬 {v['video_title']} — {v['video_channel']}",
                             font=ctk.CTkFont(size=13), text_color=t["text"], anchor="w").pack(side="left")
                ctk.CTkButton(inner, text="Assistir ▶", width=90, height=28,
                              fg_color=t["danger"], hover_color="#EF5350",
                              command=lambda url=v["video_url"]: webbrowser.open(url)).pack(side="right")

    def _search_youtube(self):
        query = self._search_entry.get().strip()
        if query:
            url = self.api.get_youtube_search_url(query)
            webbrowser.open(url)

    # ══════════════════════════════════════════════════════════
    # ── QUIZ QUESTÕES PRÓPRIAS ───────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _start_quiz(self, subject):
        self._subject = subject
        cat = self._category if self._category in (
            "enem", "concursos") else "enem"
        self._questions = self.db.get_questions(cat, subject)
        if not self._questions:
            return
        self._q_index = 0
        self._correct = 0
        self._show_question()

    def _show_question(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()
        self._answered = False
        q = self._questions[self._q_index]

        # Header do quiz
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkButton(top, text="← Voltar", width=90, height=32,
                      fg_color=t["card"], hover_color=t["secondary"],
                      command=self._show_menu).pack(side="left")

        ctk.CTkLabel(
            top, text=f"📝 {self._subject} — Questão {self._q_index + 1}/{len(self._questions)}",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=t["primary"],
        ).pack(side="left", padx=15)

        score_text = f"✅ {self._correct}/{self._q_index}"
        ctk.CTkLabel(top, text=score_text, font=ctk.CTkFont(size=14),
                     text_color=t["success"]).pack(side="right")

        # Corpo da questão
        body = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nswe")

        diff_colors = {"fácil": t["success"],
                       "médio": t.get("warning", t["accent"]), "difícil": t["danger"]}
        diff = q.get("difficulty", "médio")

        ctk.CTkLabel(
            body, text=f"Dificuldade: {diff}",
            font=ctk.CTkFont(size=12),
            text_color=diff_colors.get(diff, t["text_sec"]),
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            body, text=q["question"],
            font=ctk.CTkFont(size=16),
            text_color=t["text"], wraplength=650, justify="left",
        ).pack(anchor="w", pady=(5, 20))

        options = json.loads(q["options"]) if isinstance(
            q["options"], str) else q["options"]
        self._option_buttons = []

        for opt in options:
            btn = ctk.CTkButton(
                body, text=f"  {opt}", height=48, anchor="w",
                font=ctk.CTkFont(size=14),
                fg_color=t["card"], hover_color=t["secondary"],
                text_color=t["text"],
                corner_radius=10,
                command=lambda o=opt: self._answer(o, q),
            )
            btn.pack(fill="x", pady=4, padx=20)
            self._option_buttons.append((btn, opt))

        # Feedback area
        self._feedback_frame = ctk.CTkFrame(body, fg_color="transparent")
        self._feedback_frame.pack(fill="x", pady=15, padx=20)

    def _answer(self, selected, question):
        if self._answered:
            return
        self._answered = True
        t = self.app.theme_mgr.get_theme()
        correct = question["correct_answer"]
        is_correct = selected == correct

        if is_correct:
            self._correct += 1

        # Colorir botões
        for btn, opt in self._option_buttons:
            if opt == correct:
                btn.configure(fg_color=t["success"], text_color="#FFF")
            elif opt == selected and not is_correct:
                btn.configure(fg_color=t["danger"], text_color="#FFF")
            btn.configure(state="disabled")

        # Feedback
        icon = "✅ Correto!" if is_correct else "❌ Incorreto!"
        ctk.CTkLabel(
            self._feedback_frame, text=icon,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["success"] if is_correct else t["danger"],
        ).pack(anchor="w")

        if question.get("explanation"):
            ctk.CTkLabel(
                self._feedback_frame, text=f"💡 {question['explanation']}",
                font=ctk.CTkFont(size=13), text_color=t["text_sec"],
                wraplength=600, justify="left",
            ).pack(anchor="w", pady=(5, 0))

        # Botão próxima
        if self._q_index + 1 < len(self._questions):
            ctk.CTkButton(
                self._feedback_frame, text="Próxima →", width=140, height=38,
                fg_color=t["primary"], hover_color=t["button_hover"],
                command=self._next_question,
            ).pack(pady=(15, 0))
        else:
            self._show_result()

    def _next_question(self):
        self._q_index += 1
        self._show_question()

    def _show_result(self):
        t = self.app.theme_mgr.get_theme()
        total = len(self._questions)
        score = (self._correct / total * 100) if total else 0

        cat = self._category if self._category in (
            "enem", "concursos") else "enem"
        self.db.save_study_progress(
            self._subject, "", "quiz", score, total, self._correct,
            cat, self.app.get_user_id(),
        )

        ctk.CTkLabel(
            self._feedback_frame,
            text=f"\n🏆 Resultado Final: {self._correct}/{total} ({score:.0f}%)",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["accent"],
        ).pack(pady=(15, 5))

        msg = "Excelente! 🌟" if score >= 80 else "Bom trabalho! 👍" if score >= 60 else "Continue praticando! 💪"
        ctk.CTkLabel(
            self._feedback_frame, text=msg,
            font=ctk.CTkFont(size=16), text_color=t["text_sec"],
        ).pack()

        ctk.CTkButton(
            self._feedback_frame, text="🔄 Refazer Quiz", width=160, height=38,
            fg_color=t["primary"], hover_color=t["button_hover"],
            command=lambda: self._start_quiz(self._subject),
        ).pack(pady=(15, 5))

        ctk.CTkButton(
            self._feedback_frame, text="← Voltar ao Menu", width=160, height=38,
            fg_color=t["card"], hover_color=t["secondary"],
            command=self._show_menu,
        ).pack(pady=3)

    # ── vídeos ───────────────────────────────────────────────
    def _show_videos(self, subject, category=None):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()
        cat = category or self._category
        if cat not in ("enem", "concursos"):
            cat = "enem"

        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkButton(top, text="← Voltar", width=90, height=32,
                      fg_color=t["card"], hover_color=t["secondary"],
                      command=self._show_menu).pack(side="left")

        ctk.CTkLabel(top, text=f"🎬 Videoaulas — {subject}",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=t["primary"]).pack(side="left", padx=15)

        scroll = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nswe")

        videos = self.db.get_videos(cat, subject)

        if not videos:
            ctk.CTkLabel(scroll, text="Nenhuma videoaula encontrada para esta matéria.",
                         font=ctk.CTkFont(size=14), text_color=t["text_sec"]).pack(pady=40)
            return

        for video in videos:
            card = ctk.CTkFrame(scroll, corner_radius=12, fg_color=t["card"])
            card.pack(fill="x", pady=5)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)
            inner.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                inner, text=f"🎬 {video['video_title']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=t["text"], anchor="w",
            ).grid(row=0, column=0, sticky="w")

            info = f"📺 {video['video_channel']}  •  📂 {video.get('topic', '')}"
            ctk.CTkLabel(
                inner, text=info,
                font=ctk.CTkFont(size=12),
                text_color=t["text_sec"], anchor="w",
            ).grid(row=1, column=0, sticky="w", pady=(2, 0))

            ctk.CTkButton(
                inner, text="▶ Assistir", width=100, height=34,
                fg_color=t["danger"], hover_color="#EF5350",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=lambda url=video["video_url"]: webbrowser.open(url),
            ).grid(row=0, column=1, rowspan=2, padx=(10, 0))

        ctk.CTkButton(
            scroll, text=f"🔎 Buscar mais videoaulas de {subject} no YouTube",
            height=38, fg_color=t["card"], hover_color=t["secondary"],
            text_color=t["text_sec"],
            command=lambda: webbrowser.open(
                self.api.get_youtube_search_url(f"{subject} aula")),
        ).pack(pady=15)

    # ── API fetch ────────────────────────────────────────────
    def _fetch_api(self):
        questions = self.api.fetch_trivia_questions("Ciências da Natureza", 5)
        if questions:
            self._questions = questions
            self._q_index = 0
            self._correct = 0
            self._subject = "Questões Online"
            self._show_question()

    # ── utils ────────────────────────────────────────────────
    def _switch_category(self, cat):
        self._category = cat
        self._show_menu()

    def on_show(self):
        self._show_menu()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.header.configure(text_color=t["primary"])
