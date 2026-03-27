import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class LoginView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._mode = "login"  # login | register
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.card = ctk.CTkFrame(self, width=420, height=480, corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)

        self.title_lb = ctk.CTkLabel(
            self.card, text="🔑 Entrar",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.pack(pady=(30, 5))

        self.subtitle = ctk.CTkLabel(
            self.card, text="Acesse sua conta para sincronizar dados",
            font=ctk.CTkFont(size=12),
        )
        self.subtitle.pack(pady=(0, 25))

        self.username_entry = ctk.CTkEntry(
            self.card, placeholder_text="Usuário", width=300, height=42,
        )
        self.username_entry.pack(pady=6)

        self.password_entry = ctk.CTkEntry(
            self.card, placeholder_text="Senha", show="•", width=300, height=42,
        )
        self.password_entry.pack(pady=6)

        self.name_entry = ctk.CTkEntry(
            self.card, placeholder_text="Nome de exibição", width=300, height=42,
        )
        # Escondido no modo login

        self.action_btn = ctk.CTkButton(
            self.card, text="Entrar", width=300, height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._do_action,
        )
        self.action_btn.pack(pady=(20, 8))

        self.toggle_btn = ctk.CTkButton(
            self.card, text="Não tem conta? Cadastre-se",
            width=300, height=36, fg_color="transparent",
            font=ctk.CTkFont(size=12),
            command=self._toggle_mode,
        )
        self.toggle_btn.pack(pady=2)

        self.skip_btn = ctk.CTkButton(
            self.card, text="Continuar como convidado →",
            width=300, height=36, fg_color="transparent",
            font=ctk.CTkFont(size=12),
            command=lambda: self.app.show_frame("pomodoro"),
        )
        self.skip_btn.pack(pady=2)

    def _toggle_mode(self):
        if self._mode == "login":
            self._mode = "register"
            self.title_lb.configure(text="📝 Cadastrar")
            self.subtitle.configure(
                text="Crie sua conta para salvar seu progresso")
            self.action_btn.configure(text="Cadastrar")
            self.toggle_btn.configure(text="Já tem conta? Faça login")
            self.name_entry.pack(after=self.password_entry, pady=6)
        else:
            self._mode = "login"
            self.title_lb.configure(text="🔑 Entrar")
            self.subtitle.configure(
                text="Acesse sua conta para sincronizar dados")
            self.action_btn.configure(text="Entrar")
            self.toggle_btn.configure(text="Não tem conta? Cadastre-se")
            self.name_entry.pack_forget()

    def _do_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            CTkMessagebox(title="Atenção",
                          message="Preencha todos os campos.", icon="warning")
            return

        if self._mode == "login":
            user = self.db.authenticate(username, password)
            if user:
                self.app.set_user(user)
                self._clear()
                self.app.show_frame("pomodoro")
            else:
                CTkMessagebox(
                    title="Erro", message="Usuário ou senha inválidos.", icon="cancel")
        else:
            display = self.name_entry.get().strip() or username
            user = self.db.create_user(username, password, display)
            if user:
                self.app.set_user(user)
                self._clear()
                CTkMessagebox(
                    title="Sucesso", message="Conta criada com sucesso!", icon="check")
                self.app.show_frame("pomodoro")
            else:
                CTkMessagebox(
                    title="Erro", message="Usuário já existe.", icon="cancel")

    def _clear(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.name_entry.delete(0, "end")

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.card.configure(fg_color=t["card"])
        self.title_lb.configure(text_color=t["primary"])
        self.subtitle.configure(text_color=t["text_sec"])
        self.username_entry.configure(
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self.password_entry.configure(
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self.name_entry.configure(
            fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"],
        )
        self.action_btn.configure(
            fg_color=t["button"], hover_color=t["button_hover"])
        self.toggle_btn.configure(
            text_color=t["primary"], hover_color=t["card"])
        self.skip_btn.configure(
            text_color=t["text_sec"], hover_color=t["card"])
