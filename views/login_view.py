import flet as ft


class LoginView:
    """Tela de Login / Cadastro."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._mode = "login"

    def build(self):
        t = self.app.theme_mgr.get_theme()

        self._username = ft.TextField(
            label="Usuário", width=300, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._password = ft.TextField(
            label="Senha", width=300, height=50, password=True, can_reveal_password=True,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
        )
        self._display_name = ft.TextField(
            label="Nome de exibição", width=300, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            visible=False,
        )

        self._title = ft.Text("🔑 Entrar", size=24,
                              weight=ft.FontWeight.BOLD, color=t["primary"])
        self._subtitle = ft.Text(
            "Acesse sua conta para sincronizar dados",
            size=12, color=t["text_sec"],
        )

        self._action_btn = ft.ElevatedButton(
            content=ft.Text("Entrar"), width=300, height=45,
            bgcolor=t["button"], color="#FFFFFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self._do_action,
        )

        self._toggle_btn = ft.TextButton(
            content=ft.Text("Não tem conta? Cadastre-se"), width=300,
            on_click=self._toggle_mode,
            style=ft.ButtonStyle(color=t["text_sec"]),
        )

        self._skip_btn = ft.TextButton(
            content=ft.Text("Continuar como convidado →"), width=300,
            on_click=lambda _: self.app.show_view("pomodoro"),
            style=ft.ButtonStyle(color=t["text_sec"]),
        )

        card = ft.Container(
            width=380,
            padding=30,
            border_radius=16,
            bgcolor=t["card"],
            content=ft.Column(
                controls=[
                    self._title,
                    self._subtitle,
                    ft.Container(height=15),
                    self._username,
                    self._password,
                    self._display_name,
                    ft.Container(height=10),
                    self._action_btn,
                    self._toggle_btn,
                    self._skip_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor=t["bg"],
            alignment=ft.Alignment.CENTER,
            content=card,
        )

    def on_show(self):
        self._mode = "login"

    def _toggle_mode(self, e=None):
        if self._mode == "login":
            self._mode = "register"
            self._title.value = "📝 Cadastrar"
            self._subtitle.value = "Crie sua conta para salvar seu progresso"
            self._action_btn.content = ft.Text("Cadastrar")
            self._toggle_btn.content = ft.Text("Já tem conta? Faça login")
            self._display_name.visible = True
        else:
            self._mode = "login"
            self._title.value = "🔑 Entrar"
            self._subtitle.value = "Acesse sua conta para sincronizar dados"
            self._action_btn.content = ft.Text("Entrar")
            self._toggle_btn.content = ft.Text("Não tem conta? Cadastre-se")
            self._display_name.visible = False
        self.app.page.update()

    def _do_action(self, e=None):
        username = self._username.value.strip() if self._username.value else ""
        password = self._password.value.strip() if self._password.value else ""

        if not username or not password:
            self.app.show_snackbar("⚠️ Preencha todos os campos.")
            return

        if self._mode == "register" and len(password) < 8:
            self.app.show_snackbar(
                "⚠️ A senha deve ter pelo menos 8 caracteres.")
            return

        if self._mode == "login":
            user = self.db.authenticate(username, password)
            if user:
                self.app.set_user(user)
                self.app.show_snackbar("✅ Login realizado com sucesso!")
                self.app.show_view("dashboard")
            else:
                self.app.show_snackbar(
                    "❌ Usuário ou senha inválidos.", bgcolor="#F44336")
        else:
            display = (self._display_name.value or "").strip() or username
            user = self.db.create_user(username, password, display)
            if user:
                self.app.set_user(user)
                self.app.show_snackbar("✅ Conta criada com sucesso!")
                self.app.show_view("dashboard")
            else:
                self.app.show_snackbar(
                    "❌ Usuário já existe.", bgcolor="#F44336")
