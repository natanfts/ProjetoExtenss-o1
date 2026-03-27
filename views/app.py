import customtkinter as ctk
from database import DatabaseManager
from themes import ThemeManager, THEMES
from content_updater import ContentUpdater


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🍅 PomodoroStudy – Estude com Foco!")
        self.geometry("1120x700")
        self.minsize(900, 600)

        self.db = DatabaseManager()
        self.theme_mgr = ThemeManager()
        self.updater = ContentUpdater(self.db, interval_hours=24)
        self.current_user = None  # None = convidado

        ctk.set_appearance_mode("dark")

        # frames registrados
        self._frames: dict[str, ctk.CTkFrame] = {}
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._active_frame = None

        self._build_layout()
        self._register_views()
        self._apply_theme()
        self.show_frame("pomodoro")

        # Iniciar atualização automática de conteúdo em background
        self.after(2000, self._auto_update_content)

    # ── layout principal ─────────────────────────────────────
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        # Logo / título
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="🍅 PomodoroStudy",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.pack(pady=(25, 5))

        self.user_label = ctk.CTkLabel(
            self.sidebar, text="👤 Convidado",
            font=ctk.CTkFont(size=13),
        )
        self.user_label.pack(pady=(0, 20))

        # Botões de navegação
        nav_items = [
            ("pomodoro", "🍅  Pomodoro"),
            ("tasks",    "📋  Tarefas"),
            ("study",    "📚  Estudar"),
            ("history",  "📊  Histórico"),
            ("settings", "⚙️  Configurações"),
        ]
        for key, label in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, height=42,
                anchor="w", font=ctk.CTkFont(size=14),
                corner_radius=8,
                command=lambda k=key: self.show_frame(k),
            )
            btn.pack(fill="x", padx=14, pady=3)
            self._nav_buttons[key] = btn

        # Espaçador
        ctk.CTkLabel(self.sidebar, text="").pack(expand=True)

        # Botão Login
        self.login_btn = ctk.CTkButton(
            self.sidebar, text="🔑  Entrar / Cadastrar", height=40,
            corner_radius=8, font=ctk.CTkFont(size=13),
            command=lambda: self.show_frame("login"),
        )
        self.login_btn.pack(fill="x", padx=14, pady=(3, 8))

        # Indicador de status de atualização
        self.update_status_label = ctk.CTkLabel(
            self.sidebar, text="",
            font=ctk.CTkFont(size=10),
            wraplength=200,
        )
        self.update_status_label.pack(fill="x", padx=14, pady=(0, 12))

        # Content area
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nswe")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    # ── registrar views ──────────────────────────────────────
    def _register_views(self):
        from views.login_view import LoginView
        from views.pomodoro_view import PomodoroView
        from views.tasks_view import TasksView
        from views.study_view import StudyView
        from views.history_view import HistoryView
        from views.settings_view import SettingsView

        for ViewClass, key in [
            (PomodoroView, "pomodoro"),
            (TasksView, "tasks"),
            (StudyView, "study"),
            (HistoryView, "history"),
            (SettingsView, "settings"),
            (LoginView, "login"),
        ]:
            frame = ViewClass(self.content, self)
            frame.grid(row=0, column=0, sticky="nswe")
            self._frames[key] = frame

    # ── navegação ────────────────────────────────────────────
    def show_frame(self, name):
        frame = self._frames.get(name)
        if frame is None:
            return
        if self._active_frame == name:
            return
        self._active_frame = name

        # Highlight botão ativo
        theme = self.theme_mgr.get_theme()
        for k, btn in self._nav_buttons.items():
            if k == name:
                btn.configure(
                    fg_color=theme["primary"], text_color=theme["text"])
            else:
                btn.configure(fg_color="transparent",
                              text_color=theme["text_sec"])

        # Atualizar conteúdo se o frame tiver refresh
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # ── tema ─────────────────────────────────────────────────
    def _apply_theme(self):
        t = self.theme_mgr.get_theme()
        self.configure(fg_color=t["bg"])
        self.sidebar.configure(fg_color=t["sidebar"])
        self.content.configure(fg_color=t["bg"])
        self.logo_label.configure(text_color=t["primary"])
        self.user_label.configure(text_color=t["text_sec"])

        for btn in self._nav_buttons.values():
            btn.configure(
                fg_color="transparent",
                hover_color=t["card"],
                text_color=t["text_sec"],
            )
        self.login_btn.configure(
            fg_color=t["card"],
            hover_color=t["primary"],
            text_color=t["text"],
        )
        # Propagar para frames
        for frame in self._frames.values():
            if hasattr(frame, "apply_theme"):
                frame.apply_theme(t)

    def refresh_theme(self):
        self._apply_theme()
        if self._active_frame:
            self.show_frame(self._active_frame)

    # ── login / logout ───────────────────────────────────────
    def set_user(self, user_dict):
        self.current_user = user_dict
        if user_dict:
            self.user_label.configure(text=f"👤 {user_dict['display_name']}")
            self.login_btn.configure(text="🚪  Sair")
            self.login_btn.configure(command=self.logout)
            # carregar tema do usuário
            if user_dict.get("theme"):
                self.theme_mgr.set_theme(user_dict["theme"])
                self.refresh_theme()
        else:
            self.user_label.configure(text="👤 Convidado")
            self.login_btn.configure(text="🔑  Entrar / Cadastrar")
            self.login_btn.configure(command=lambda: self.show_frame("login"))

    def logout(self):
        self.current_user = None
        self.set_user(None)
        self.show_frame("pomodoro")

    def get_user_id(self):
        return self.current_user["id"] if self.current_user else None

    # ── atualização automática de conteúdo ───────────────────
    def _auto_update_content(self):
        """Inicia atualização de vídeos em background ao abrir o app."""
        started = self.updater.start_update()
        if started:
            self.update_status_label.configure(
                text="🔄 Atualizando conteúdo...")
            self._check_update_status()
        else:
            last = self.db.get_last_update("videos")
            if last:
                self.update_status_label.configure(
                    text=f"✅ Atualizado: {last.strftime('%d/%m %H:%M')}"
                )

    def _check_update_status(self):
        """Verifica o progresso da atualização periodicamente."""
        if self.updater.is_running:
            t = self.theme_mgr.get_theme()
            self.update_status_label.configure(
                text=self.updater.progress,
                text_color=t["accent"],
            )
            self.after(1500, self._check_update_status)
        else:
            t = self.theme_mgr.get_theme()
            color = t["success"] if self.updater.status == "done" else t["danger"]
            self.update_status_label.configure(
                text=self.updater.progress,
                text_color=color,
            )
            # Limpar a mensagem após 10 segundos
            self.after(10000, lambda: self.update_status_label.configure(
                text=f"✅ Conteúdo atualizado",
                text_color=t["text_sec"],
            ))
