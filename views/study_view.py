import flet as ft
import json
import asyncio


class StudyView:
    """Central de Estudos — Quiz com questões do banco de dados."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._mode = "menu"  # menu | quiz | results
        self._questions = []
        self._q_index = 0
        self._correct = 0
        self._total = 0
        self._category = "enem"
        self._subject = None

    def on_show(self):
        pass  # Não resetar modo — preserva estado do quiz quando cacheado

    def build(self):
        if self._mode == "quiz":
            return self._build_quiz()
        elif self._mode == "results":
            return self._build_results()
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
            topics = self.db.get_topics(self._category, subj, "quiz")
            topic_count = len(topics) if topics else 0
            subject_tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12,
                    padding=15,
                    on_click=lambda _, s=subj: self._start_quiz(s),
                    content=ft.Row([
                        ft.Column([
                            ft.Text(
                                f"📖 {subj}", size=15, weight=ft.FontWeight.BOLD, color=t["text"]),
                            ft.Text(f"{topic_count} tópicos",
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
                            on_click=lambda _, y=year: self._start_enem_quiz(
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
            self._category, subject, limit=10)
        if not self._questions:
            self.app.show_snackbar(
                "⚠️ Nenhuma questão disponível para essa matéria.")
            return
        self._q_index = 0
        self._correct = 0
        self._total = len(self._questions)
        self._mode = "quiz"
        self.app.show_view("study")

    def _start_enem_quiz(self, year, e=None):
        self._subject = f"ENEM {year}"
        questions_raw = self.db.get_enem_questions(year, limit=10)
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
            self.app.show_snackbar("✅ Correto!", bgcolor="#4CAF50")
        else:
            self.app.show_snackbar(
                f"❌ Errado! Resposta: {correct}", bgcolor="#F44336")

        # XP
        uid = self.app.get_user_id()
        if uid:
            xp = 10 if is_correct else 3
            self.db.add_xp(uid, xp, "quiz", f"Quiz: {self._subject}")
            self.db.update_daily_goal_progress(uid, "quiz")
            self.db.update_daily_goal_progress(uid, "xp", xp)

        self._q_index += 1

        async def _next():
            await asyncio.sleep(0.6)
            self.app.show_view("study")
        self.app.page.run_task(_next)

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
