import flet as ft
from themes import THEMES


class SettingsView:
    """Configurações — Temas, Pomodoro, Metas, Perfil."""

    def __init__(self, app):
        self.app = app
        self.db = app.db

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()
        user = self.app.current_user

        controls = []

        # ── Temas ────────────────────────────────────────────
        controls.append(
            ft.Text("🎨 Temas — Escolha seu Anime/Série", size=18,
                    weight=ft.FontWeight.BOLD, color=t["primary"]),
        )

        theme_cards = []
        for name, theme in THEMES.items():
            is_active = name == self.app.theme_mgr.current_theme

            # Preview de cores
            color_dots = ft.Row([
                ft.Container(width=20, height=10, border_radius=5,
                             bgcolor=theme["primary"]),
                ft.Container(width=20, height=10, border_radius=5,
                             bgcolor=theme["accent"]),
                ft.Container(width=20, height=10, border_radius=5,
                             bgcolor=theme["success"]),
                ft.Container(width=20, height=10, border_radius=5,
                             bgcolor=theme["danger"]),
            ], spacing=3)

            card_content = ft.Column([
                color_dots,
                ft.Text(f"{theme['emoji']} {name}", size=14, weight=ft.FontWeight.BOLD,
                        color=theme["text"]),
                ft.Text(theme["desc"][:45], size=10, color=theme["text_sec"], max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS),
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            if is_active:
                card_content.controls.append(
                    ft.Text("✓ Ativo", size=11,
                            weight=ft.FontWeight.BOLD, color=theme["accent"]),
                )
            else:
                card_content.controls.append(
                    ft.TextButton("Aplicar", on_click=lambda _, n=name: self._apply_theme(n),
                                  style=ft.ButtonStyle(color=theme["primary"])),
                )

            theme_cards.append(
                ft.Container(
                    width=170, border_radius=12, padding=12,
                    bgcolor=theme["card"],
                    border=ft.border.all(
                        3, theme["accent"]) if is_active else None,
                    content=card_content,
                )
            )

        controls.append(
            ft.Row(theme_cards, wrap=True, spacing=8, run_spacing=8),
        )

        # ── Pomodoro ─────────────────────────────────────────
        controls.append(
            ft.Text("🍅 Configurações do Pomodoro", size=18,
                    weight=ft.FontWeight.BOLD, color=t["primary"]),
        )

        focus_val = user.get("pomodoro_focus", 25) if user else 25
        short_val = user.get("pomodoro_short", 5) if user else 5
        long_val = user.get("pomodoro_long", 15) if user else 15

        self._pom_focus = ft.TextField(
            label="⏱️ Foco (min)", value=str(focus_val), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._pom_short = ft.TextField(
            label="☕ Pausa curta", value=str(short_val), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._pom_long = ft.TextField(
            label="🌿 Pausa longa", value=str(long_val), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )

        controls.append(
            ft.Container(
                bgcolor=t["card"], border_radius=12, padding=15,
                content=ft.Column([
                    ft.Row([self._pom_focus, self._pom_short,
                           self._pom_long], spacing=8),
                    ft.ElevatedButton(
                        "💾 Salvar Pomodoro", height=38, width=300,
                        bgcolor=t["button"], color="#FFF",
                        on_click=self._save_pomodoro,
                    ),
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ),
        )

        # ── Metas Diárias ────────────────────────────────────
        controls.append(
            ft.Text("🎯 Metas Diárias", size=18,
                    weight=ft.FontWeight.BOLD, color=t["primary"]),
        )

        pom_goal = user.get("daily_pomodoro_goal", 4) if user else 4
        xp_goal = user.get("daily_xp_goal", 100) if user else 100
        quiz_goal = user.get("daily_quiz_goal", 10) if user else 10

        self._goal_pom = ft.TextField(
            label="🍅 Pomodoros/dia", value=str(pom_goal), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._goal_xp = ft.TextField(
            label="⚡ XP/dia", value=str(xp_goal), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._goal_quiz = ft.TextField(
            label="📝 Questões/dia", value=str(quiz_goal), width=100, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], keyboard_type=ft.KeyboardType.NUMBER,
            label_style=ft.TextStyle(color=t["text_sec"]),
        )

        controls.append(
            ft.Container(
                bgcolor=t["card"], border_radius=12, padding=15,
                content=ft.Column([
                    ft.Row([self._goal_pom, self._goal_xp,
                           self._goal_quiz], spacing=8),
                    ft.ElevatedButton(
                        "💾 Salvar Metas", height=38, width=300,
                        bgcolor=t["button"], color="#FFF",
                        on_click=self._save_goals,
                    ),
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ),
        )

        # ── Perfil ───────────────────────────────────────────
        if user:
            controls.append(
                ft.Text("👤 Perfil", size=18,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
            )

            self._name_field = ft.TextField(
                label="📛 Nome de exibição",
                value=user.get("display_name", ""), width=350, height=50,
                bgcolor=t["entry_bg"], border_color=t["entry_border"],
                color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            )
            self._old_pw = ft.TextField(
                label="Senha atual", width=350, height=50, password=True, can_reveal_password=True,
                bgcolor=t["entry_bg"], border_color=t["entry_border"],
                color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            )
            self._new_pw = ft.TextField(
                label="Nova senha", width=350, height=50, password=True, can_reveal_password=True,
                bgcolor=t["entry_bg"], border_color=t["entry_border"],
                color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            )

            controls.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, padding=15,
                    content=ft.Column([
                        self._name_field,
                        ft.ElevatedButton("💾 Salvar Nome", height=36, width=200,
                                          bgcolor=t["button"], color="#FFF",
                                          on_click=self._save_name),
                        ft.Divider(color=t["secondary"]),
                        ft.Text("🔒 Alterar Senha", size=14,
                                weight=ft.FontWeight.BOLD, color=t["text"]),
                        self._old_pw,
                        self._new_pw,
                        ft.ElevatedButton("🔒 Alterar Senha", height=36, width=200,
                                          bgcolor=t["button"], color="#FFF",
                                          on_click=self._save_password),
                    ], spacing=8),
                ),
            )

        # ── Sobre ────────────────────────────────────────────
        controls.append(
            ft.Text("ℹ️ Sobre", size=18,
                    weight=ft.FontWeight.BOLD, color=t["primary"]),
        )
        controls.append(
            ft.Container(
                bgcolor=t["card"], border_radius=12, padding=18,
                content=ft.Text(
                    "🔀 Switch Focus v3.0 (Flet)\n\n"
                    "Aplicativo de estudos com método Pomodoro.\n"
                    "ENEM e Concursos com quizzes e vídeos.\n"
                    "Gamificação com XP, níveis e conquistas!\n"
                    "Flashcards com repetição espaçada.\n"
                    "Temas de animes e séries favoritos!\n\n"
                    "Desenvolvido com Python + Flet + SQLite",
                    size=13, color=t["text_sec"],
                ),
            ),
        )

        controls.append(ft.Container(height=20))

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column(controls, spacing=12, scroll=ft.ScrollMode.AUTO),
        )

    # ── ações ────────────────────────────────────────────────
    def _apply_theme(self, name):
        self.app.theme_mgr.set_theme(name)
        if self.app.current_user:
            self.db.update_user_theme(self.app.current_user["id"], name)
        self.app.refresh_theme()

    def _save_pomodoro(self, e=None):
        try:
            focus = int(self._pom_focus.value)
            short = int(self._pom_short.value)
            long_ = int(self._pom_long.value)
        except (ValueError, TypeError):
            self.app.show_snackbar("⚠️ Insira valores numéricos válidos.")
            return
        if focus < 1 or short < 1 or long_ < 1:
            self.app.show_snackbar("⚠️ Valores devem ser maiores que zero.")
            return
        if self.app.current_user:
            self.db.update_user_pomodoro(
                self.app.current_user["id"], focus, short, long_)
            self.app.current_user["pomodoro_focus"] = focus
            self.app.current_user["pomodoro_short"] = short
            self.app.current_user["pomodoro_long"] = long_
            self.app.show_snackbar("✅ Configurações do Pomodoro salvas!")
        else:
            self.app.show_snackbar("⚠️ Faça login para salvar.")

    def _save_goals(self, e=None):
        try:
            pom = int(self._goal_pom.value)
            xp = int(self._goal_xp.value)
            quiz = int(self._goal_quiz.value)
        except (ValueError, TypeError):
            self.app.show_snackbar("⚠️ Insira valores numéricos válidos.")
            return
        if pom < 1 or xp < 1 or quiz < 1:
            self.app.show_snackbar("⚠️ Valores devem ser maiores que zero.")
            return
        if self.app.current_user:
            uid = self.app.current_user["id"]
            self.db.update_user_goals(uid, pom, xp, quiz)
            self.app.current_user["daily_pomodoro_goal"] = pom
            self.app.current_user["daily_xp_goal"] = xp
            self.app.current_user["daily_quiz_goal"] = quiz
            self.app.show_snackbar("✅ Metas diárias salvas! 🎯")
        else:
            self.app.show_snackbar("⚠️ Faça login para salvar.")

    def _save_name(self, e=None):
        new_name = self._name_field.value.strip() if self._name_field.value else ""
        if not new_name:
            self.app.show_snackbar("⚠️ Nome não pode ser vazio.")
            return
        uid = self.app.current_user["id"]
        self.db.update_user_display_name(uid, new_name)
        self.app.current_user["display_name"] = new_name
        self.app.show_snackbar("✅ Nome atualizado!")

    def _save_password(self, e=None):
        old_pw = self._old_pw.value.strip() if self._old_pw.value else ""
        new_pw = self._new_pw.value.strip() if self._new_pw.value else ""
        if not old_pw or not new_pw:
            self.app.show_snackbar("⚠️ Preencha ambos os campos.")
            return
        if len(new_pw) < 4:
            self.app.show_snackbar(
                "⚠️ Nova senha deve ter pelo menos 4 caracteres.")
            return
        uid = self.app.current_user["id"]
        success = self.db.update_user_password(uid, old_pw, new_pw)
        if success:
            self.app.show_snackbar("✅ Senha alterada com sucesso!")
        else:
            self.app.show_snackbar(
                "❌ Senha atual incorreta.", bgcolor="#F44336")
