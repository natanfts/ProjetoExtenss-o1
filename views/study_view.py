import flet as ft
import json
import asyncio


class StudyView:
    """Central de Estudos — Quiz com questões do banco de dados."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._mode = "menu"  # menu | quiz | feedback | results
        self._questions = []
        self._q_index = 0
        self._correct = 0
        self._total = 0
        self._category = "enem"
        self._subject = None
        self._enem_year = None
        self._last_chosen = None
        self._last_is_correct = False

    def on_show(self):
        pass  # Não resetar modo — preserva estado do quiz quando cacheado

    def build(self):
        if self._mode == "quiz":
            return self._build_quiz()
        elif self._mode == "feedback":
            return self._build_feedback()
        elif self._mode == "results":
            return self._build_results()
        elif self._mode == "enem_select":
            return self._build_enem_select()
        return self._build_menu()

    def _build_menu(self):
        t = self.app.theme_mgr.get_theme()

        # Categorias
        cat_btns = []
        for cat_label, cat_key in [("📚 ENEM", "enem"), ("📋 Concursos", "concursos")]:
            is_active = self._category == cat_key
            cat_btns.append(
                ft.ElevatedButton(
                    content=ft.Text(cat_label), height=40, expand=True,
                    bgcolor=t["primary"] if is_active else t["card"],
                    color="#FFFFFF" if is_active else t["text_sec"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _, c=cat_key: self._set_category(c),
                )
            )

        # Matérias disponíveis
        subjects = self.db.get_subjects(self._category, "quiz")
        subject_tiles = []
        for subj in subjects:
            q_count = len(self.db.get_questions(
                self._category, subj, limit=500))
            subject_tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12,
                    padding=15,
                    on_click=lambda _, s=subj: self._start_quiz(s),
                    content=ft.Row([
                        ft.Column([
                            ft.Text(
                                f"📖 {subj}", size=15, weight=ft.FontWeight.BOLD, color=t["text"]),
                            ft.Text(f"{q_count} questões",
                                    size=12, color=t["text_sec"]),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.PLAY_CIRCLE_FILLED,
                                color=t["primary"], size=32),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                )
            )

        # ENEM Real
        enem_section = []
        if self._category == "enem":
            cached_years = self.db.get_cached_enem_years()
            if cached_years:
                enem_section.append(
                    ft.Text("🎯 ENEM Real — Questões Oficiais", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                )
                for year in cached_years[:5]:
                    count = self.db.get_cached_enem_year_count(year)
                    enem_section.append(
                        ft.Container(
                            bgcolor=t["card"], border_radius=12, padding=15,
                            on_click=lambda _, y=year: self._show_enem_select(
                                y),
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"📋 ENEM {year}", size=15,
                                            weight=ft.FontWeight.BOLD, color=t["text"]),
                                    ft.Text(f"{count} questões em cache",
                                            size=12, color=t["text_sec"]),
                                ], spacing=2, expand=True),
                                ft.Icon(ft.Icons.QUIZ,
                                        color=t["accent"], size=28),
                            ]),
                        )
                    )

        # Card para Teorias
        theory_card = ft.Container(
            bgcolor=t["card"], border_radius=14, padding=15,
            on_click=lambda _: self.app.show_view("theory"),
            ink=True,
            content=ft.Row([
                ft.Icon(ft.Icons.MENU_BOOK_ROUNDED,
                        color=t["primary"], size=28),
                ft.Column([
                    ft.Text("📖 Teorias do ENEM", size=15,
                            weight=ft.FontWeight.BOLD, color=t["text"]),
                    ft.Text("Resumos, fórmulas, conceitos e artigos",
                            size=12, color=t["text_sec"]),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS,
                        color=t["text_sec"], size=16),
            ], spacing=10),
        )

        # Card para Editais do ENEM
        editais_card = ft.Container(
            bgcolor=t["card"], border_radius=14, padding=15,
            on_click=lambda _: self.app.show_view("enem_editais"),
            ink=True,
            content=ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION_ROUNDED,
                        color=t["accent"], size=28),
                ft.Column([
                    ft.Text("📋 Editais do ENEM", size=15,
                            weight=ft.FontWeight.BOLD, color=t["text"]),
                    ft.Text("Todos os anos + temas de redação",
                            size=12, color=t["text_sec"]),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS,
                        color=t["text_sec"], size=16),
            ], spacing=10),
        )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column(
                controls=[
                    ft.Row(cat_btns, spacing=8),
                    theory_card,
                    editais_card,
                    ft.Text(f"📚 Matérias — {self._category.upper()}", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    *subject_tiles,
                    *enem_section,
                ],
                spacing=10, scroll=ft.ScrollMode.AUTO,
            ),
        )

    # ── quiz ─────────────────────────────────────────────────
    def _start_quiz(self, subject, e=None):
        self._subject = subject
        self._questions = self.db.get_questions(
            self._category, subject, limit=500)
        if not self._questions:
            self.app.show_snackbar(
                "⚠️ Nenhuma questão disponível para essa matéria.")
            return
        self._q_index = 0
        self._correct = 0
        self._total = len(self._questions)
        self._mode = "quiz"
        self.app.show_view("study")

    # ── ENEM Real — seleção de disciplina ────────────────────
    def _show_enem_select(self, year, e=None):
        self._enem_year = year
        self._mode = "enem_select"
        self.app.show_view("study")

    def _build_enem_select(self):
        t = self.app.theme_mgr.get_theme()
        year = self._enem_year
        disciplines = self.db.get_enem_disciplines_for_year(year)
        total_count = self.db.get_cached_enem_year_count(year)

        tiles = []
        # Opção: prova completa
        tiles.append(
            ft.Container(
                bgcolor=t["primary"], border_radius=12, padding=15,
                on_click=lambda _: self._start_enem_quiz(year),
                ink=True,
                content=ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=28),
                    ft.Column([
                        ft.Text("📝 Prova Completa", size=15,
                                weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text(f"{total_count} questões",
                                size=12, color="#FFFFFFCC"),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS,
                            color="#FFFFFF", size=16),
                ], spacing=10),
            )
        )

        # Opção: por disciplina
        for disc in disciplines:
            name = disc["discipline_name"] or disc["discipline"]
            count = disc["count"]
            tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, padding=15,
                    on_click=lambda _, d=disc["discipline"]: self._start_enem_quiz(
                        year, discipline=d),
                    ink=True,
                    content=ft.Row([
                        ft.Icon(ft.Icons.QUIZ, color=t["accent"], size=24),
                        ft.Column([
                            ft.Text(f"📖 {name}", size=14,
                                    weight=ft.FontWeight.BOLD, color=t["text"]),
                            ft.Text(f"{count} questões", size=12,
                                    color=t["text_sec"]),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD_IOS,
                                color=t["text_sec"], size=16),
                    ], spacing=10),
                )
            )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row([
                    ft.TextButton("← Voltar",
                                  on_click=lambda _: self._back_to_menu(),
                                  style=ft.ButtonStyle(color=t["text_sec"])),
                ]),
                ft.Text(f"🎯 ENEM {year}", size=22,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                ft.Text("Escolha a prova completa ou uma área de conhecimento:",
                        size=13, color=t["text_sec"]),
                ft.Container(height=5),
                *tiles,
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
        )

    def _start_enem_quiz(self, year, discipline=None, e=None):
        self._enem_year = year
        self._subject = f"ENEM {year}"
        questions_raw = self.db.get_enem_questions(
            year, discipline=discipline, limit=500)
        if discipline and questions_raw:
            disc_name = questions_raw[0].get("discipline_name", discipline)
            self._subject += f" — {disc_name}"
        if not questions_raw:
            self.app.show_snackbar(
                "⚠️ Nenhuma questão em cache para esse ano.")
            return
        # Adaptar formato
        self._questions = []
        for q in questions_raw:
            opts = q["options"] if isinstance(
                q["options"], list) else json.loads(q["options"])
            self._questions.append({
                "question": q["question_text"],
                "options": json.dumps(opts) if isinstance(opts, list) else q["options"],
                "correct_answer": q["correct_answer"],
                "explanation": q.get("context", ""),
                "subject": q.get("discipline_name", ""),
                "topic": "",
            })
        self._q_index = 0
        self._correct = 0
        self._total = len(self._questions)
        self._mode = "quiz"
        self.app.show_view("study")

    def _build_quiz(self):
        t = self.app.theme_mgr.get_theme()

        if self._q_index >= len(self._questions):
            self._mode = "results"
            return self._build_results()

        q = self._questions[self._q_index]
        options = json.loads(q["options"]) if isinstance(
            q["options"], str) else q["options"]

        progress_val = self._q_index / self._total if self._total > 0 else 0

        option_btns = []
        for opt in options:
            option_btns.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=10,
                    padding=ft.padding.symmetric(horizontal=15, vertical=12),
                    on_click=lambda _, o=opt: self._answer(o),
                    ink=True,
                    content=ft.Text(opt, size=14, color=t["text"]),
                )
            )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row([
                    ft.TextButton("← Voltar", on_click=lambda _: self._back_to_menu(),
                                  style=ft.ButtonStyle(color=t["text_sec"])),
                    ft.Text(f"{self._q_index + 1}/{self._total}",
                            size=14, color=t["text_sec"]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=progress_val, height=6, color=t["accent"],
                               bgcolor=t["secondary"], border_radius=3),
                ft.Container(height=10),
                ft.Text(f"📖 {q.get('subject', self._subject)}",
                        size=13, color=t["text_sec"]),
                ft.Container(
                    bgcolor=t["card"], border_radius=14, padding=20,
                    content=ft.Text(q["question"], size=16, color=t["text"]),
                ),
                ft.Container(height=5),
                *option_btns,
            ], spacing=8, scroll=ft.ScrollMode.AUTO),
        )

    def _answer(self, chosen):
        q = self._questions[self._q_index]
        correct = q["correct_answer"]
        is_correct = chosen.strip() == correct.strip()

        if is_correct:
            self._correct += 1

        # XP
        uid = self.app.get_user_id()
        if uid:
            xp = 10 if is_correct else 3
            self.db.add_xp(uid, xp, "quiz", f"Quiz: {self._subject}")
            self.db.update_daily_goal_progress(uid, "quiz")
            self.db.update_daily_goal_progress(uid, "xp", xp)

        self._last_chosen = chosen
        self._last_is_correct = is_correct
        self._mode = "feedback"
        self.app.show_view("study")

    def _build_feedback(self):
        """Tela de feedback após responder — mostra se acertou/errou e a explicação."""
        t = self.app.theme_mgr.get_theme()
        q = self._questions[self._q_index]
        correct = q["correct_answer"]
        explanation = q.get("explanation", "")
        options = json.loads(q["options"]) if isinstance(
            q["options"], str) else q["options"]

        is_correct = self._last_is_correct
        chosen = self._last_chosen

        # Header
        header_color = t["success"] if is_correct else t["danger"]
        header_emoji = "✅" if is_correct else "❌"
        header_text = "Resposta Correta!" if is_correct else "Resposta Incorreta"

        # Opções com destaque visual
        option_rows = []
        for opt in options:
            is_chosen = opt.strip() == chosen.strip()
            is_answer = opt.strip() == correct.strip()

            if is_answer:
                bg = "#1B5E20"  # verde escuro
                border = ft.border.all(2, t["success"])
                icon = ft.Icon(ft.Icons.CHECK_CIRCLE,
                               color=t["success"], size=20)
            elif is_chosen and not is_correct:
                bg = "#4E1A1A"  # vermelho escuro
                border = ft.border.all(2, t["danger"])
                icon = ft.Icon(ft.Icons.CANCEL, color=t["danger"], size=20)
            else:
                bg = t["card"]
                border = None
                icon = ft.Container(width=20)

            option_rows.append(
                ft.Container(
                    bgcolor=bg, border_radius=10, border=border,
                    padding=ft.padding.symmetric(horizontal=15, vertical=12),
                    content=ft.Row([
                        icon,
                        ft.Text(opt, size=14, color=t["text"], expand=True),
                    ], spacing=10),
                )
            )

        # Explicação
        explanation_section = []
        if explanation and explanation.strip():
            explanation_section.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, padding=15,
                    border=ft.border.all(1, t["accent"]),
                    content=ft.Column([
                        ft.Text("💡 Explicação", size=15,
                                weight=ft.FontWeight.BOLD, color=t["accent"]),
                        ft.Text(explanation, size=13, color=t["text"],
                                selectable=True),
                    ], spacing=6),
                )
            )

        # Botão próxima
        is_last = self._q_index >= len(self._questions) - 1
        next_label = "📊 Ver Resultado" if is_last else "➡️ Próxima Questão"

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                # Status header
                ft.Container(
                    bgcolor=header_color, border_radius=12,
                    padding=ft.padding.symmetric(horizontal=20, vertical=12),
                    content=ft.Row([
                        ft.Text(header_emoji, size=28),
                        ft.Text(header_text, size=18,
                                weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ),
                ft.Container(height=5),
                # Pergunta
                ft.Container(
                    bgcolor=t["card"], border_radius=12, padding=15,
                    content=ft.Text(q["question"], size=14,
                                    color=t["text_sec"]),
                ),
                # Opções com feedback visual
                *option_rows,
                # Explicação
                *explanation_section,
                ft.Container(height=10),
                # Botão próxima
                ft.ElevatedButton(
                    content=ft.Text(next_label, size=15),
                    height=48, width=300,
                    bgcolor=t["button"], color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self._next_question(),
                ),
            ], spacing=8, scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )

    def _next_question(self):
        self._q_index += 1
        if self._q_index >= len(self._questions):
            self._mode = "results"
        else:
            self._mode = "quiz"
        self.app.show_view("study")

    def _build_results(self):
        t = self.app.theme_mgr.get_theme()
        score = (self._correct / self._total * 100) if self._total > 0 else 0

        # Salvar progresso
        uid = self.app.get_user_id()
        if uid and self._total > 0:
            self.db.save_study_progress(
                self._subject or "", "", "quiz", score,
                self._total, self._correct, self._category, uid,
            )
            self.db.check_and_grant_achievements(uid)
            self.app.refresh_xp_sidebar()

        emoji = "🏆" if score >= 80 else "👍" if score >= 50 else "📚"

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            alignment=ft.Alignment.CENTER,
            padding=30,
            content=ft.Column([
                ft.Text(emoji, size=60),
                ft.Text("Resultado do Quiz", size=24,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                ft.Text(f"{self._subject}", size=14, color=t["text_sec"]),
                ft.Container(height=10),
                ft.Text(f"{score:.0f}%", size=48, weight=ft.FontWeight.BOLD,
                        color=t["success"] if score >= 70 else t["warning"]),
                ft.Text(f"{self._correct}/{self._total} questões corretas",
                        size=16, color=t["text"]),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "🔄 Tentar Novamente", height=45, width=250,
                    bgcolor=t["button"], color="#FFFFFF",
                    on_click=lambda _: self._retry(),
                ),
                ft.ElevatedButton(
                    "📚 Voltar ao Menu", height=45, width=250,
                    bgcolor=t["card"], color=t["text"],
                    on_click=lambda _: self._back_to_menu(),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        )

    def _retry(self):
        if self._subject:
            self._start_quiz(self._subject)

    def _back_to_menu(self):
        self._mode = "menu"
        self.app.show_view("study")

    def _set_category(self, cat):
        self._category = cat
        self.app.show_view("study")
