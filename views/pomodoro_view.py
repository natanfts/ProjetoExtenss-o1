import customtkinter as ctk
from datetime import datetime
import platform
import threading

# Guard: winsound só existe no Windows
if platform.system() == "Windows":
    import winsound
else:
    winsound = None


class PomodoroView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db

        # Estado do timer
        self._focus_min = 25
        self._short_min = 5
        self._long_min = 15
        self._seconds_left = self._focus_min * 60
        self._running = False
        self._session_type = "foco"       # foco | pausa_curta | pausa_longa
        self._sessions_done = 0
        self._started_at = None
        self._selected_task = None        # dict da tarefa
        self._timer_id = None

        self._build()

    # ── construção da interface ──────────────────────────────
    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título
        self.header = ctk.CTkLabel(
            self, text="🍅 Pomodoro Timer",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.header.grid(row=0, column=0, pady=(25, 10))

        # Container central
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=1, column=0, sticky="n", pady=10)

        # Timer card
        self.timer_card = ctk.CTkFrame(
            center, width=340, height=340, corner_radius=20)
        self.timer_card.pack(pady=10)
        self.timer_card.pack_propagate(False)

        self.session_label = ctk.CTkLabel(
            self.timer_card, text="Sessão de Foco",
            font=ctk.CTkFont(size=16),
        )
        self.session_label.pack(pady=(30, 5))

        self.time_label = ctk.CTkLabel(
            self.timer_card, text="25:00",
            font=ctk.CTkFont(size=72, weight="bold"),
        )
        self.time_label.pack(pady=(10, 5))

        self.counter_label = ctk.CTkLabel(
            self.timer_card, text="Sessão 0/4",
            font=ctk.CTkFont(size=14),
        )
        self.counter_label.pack(pady=(0, 5))

        # Barra de progresso
        self.progress = ctk.CTkProgressBar(
            self.timer_card, width=260, height=10)
        self.progress.pack(pady=(5, 15))
        self.progress.set(1.0)

        # Botões de controle
        btn_frame = ctk.CTkFrame(center, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            btn_frame, text="▶  Iniciar", width=120, height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._start,
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = ctk.CTkButton(
            btn_frame, text="⏸  Pausar", width=120, height=44,
            font=ctk.CTkFont(size=15), state="disabled",
            command=self._pause,
        )
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ctk.CTkButton(
            btn_frame, text="🔄  Reiniciar", width=120, height=44,
            font=ctk.CTkFont(size=15),
            command=self._reset,
        )
        self.reset_btn.grid(row=0, column=2, padx=5)

        self.skip_btn = ctk.CTkButton(
            btn_frame, text="⏭  Pular", width=120, height=44,
            font=ctk.CTkFont(size=15),
            command=self._skip_break,
        )
        self.skip_btn.grid(row=0, column=3, padx=5)
        self.skip_btn.grid_remove()  # Inicialmente oculto

        # Tarefa vinculada
        task_frame = ctk.CTkFrame(center, fg_color="transparent")
        task_frame.pack(pady=(15, 5))

        self.task_label = ctk.CTkLabel(
            task_frame, text="📋 Tarefa: Nenhuma selecionada",
            font=ctk.CTkFont(size=13),
        )
        self.task_label.pack(side="left", padx=(0, 10))

        self.pick_task_btn = ctk.CTkButton(
            task_frame, text="Selecionar Tarefa", width=140, height=32,
            font=ctk.CTkFont(size=12),
            command=self._pick_task,
        )
        self.pick_task_btn.pack(side="left")

        # Atalho: tipo manual
        type_frame = ctk.CTkFrame(center, fg_color="transparent")
        type_frame.pack(pady=5)

        for txt, stype in [("Foco", "foco"), ("Pausa Curta", "pausa_curta"), ("Pausa Longa", "pausa_longa")]:
            ctk.CTkButton(
                type_frame, text=txt, width=110, height=30,
                font=ctk.CTkFont(size=12),
                fg_color="transparent",
                command=lambda s=stype: self._set_type(s),
            ).pack(side="left", padx=4)

    # ── controle do timer ────────────────────────────────────
    def _start(self):
        if not self._running:
            self._running = True
            self._started_at = self._started_at or datetime.now().isoformat()
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self._tick()

    def _pause(self):
        self._running = False
        self.start_btn.configure(state="normal", text="▶  Continuar")
        self.pause_btn.configure(state="disabled")
        if self._timer_id:
            self.after_cancel(self._timer_id)

    def _reset(self):
        self._running = False
        if self._timer_id:
            self.after_cancel(self._timer_id)
        self._load_durations()
        self._seconds_left = self._get_duration() * 60
        self._started_at = None
        self._update_display()
        self.start_btn.configure(state="normal", text="▶  Iniciar")
        self.pause_btn.configure(state="disabled")
        self.progress.set(1.0)
        # Restaurar título da janela
        self.app.title("🔀 Switch Focus – Estude com Foco!")

    def _tick(self):
        if not self._running:
            return
        if self._seconds_left > 0:
            self._seconds_left -= 1
            self._update_display()
            total = self._get_duration() * 60
            self.progress.set(self._seconds_left / total if total else 0)
            self._timer_id = self.after(1000, self._tick)
        else:
            self._session_complete()

    def _session_complete(self):
        self._running = False
        self.start_btn.configure(state="normal", text="▶  Iniciar")
        self.pause_btn.configure(state="disabled")

        duration = self._get_duration()
        # Salvar sessão no banco
        self.db.save_session(
            self._session_type, duration,
            self._started_at or datetime.now().isoformat(),
            user_id=self.app.get_user_id(),
            task_id=self._selected_task["id"] if self._selected_task else None,
        )

        if self._session_type == "foco":
            self._sessions_done += 1
            if self._selected_task:
                self.db.increment_task_pomodoro(self._selected_task["id"])
            # Gamificação: XP + metas
            uid = self.app.get_user_id()
            if uid:
                self.db.add_xp(uid, 25, "pomodoro",
                               f"Pomodoro de {duration} min")
                self.db.update_streak(uid)
                self.db.update_daily_goal_progress(uid, "pomodoro")
                self.db.update_daily_goal_progress(uid, "xp", 25)
                self.db.check_and_grant_achievements(uid)
                self.app.refresh_xp_sidebar()

        # Notificação sonora em thread separada (cross-platform)
        def _beep():
            if winsound:
                winsound.Beep(800, 600)
            else:
                print("\a")  # Fallback: terminal bell
        threading.Thread(target=_beep, daemon=True).start()

        # Restaurar título da janela
        self.app.title("🔀 Switch Focus – Estude com Foco!")

        # Auto-switch
        if self._session_type == "foco":
            if self._sessions_done % 4 == 0:
                self._set_type("pausa_longa")
            else:
                self._set_type("pausa_curta")
        else:
            self._set_type("foco")

        self._started_at = None

    def _set_type(self, stype):
        self._session_type = stype
        self._load_durations()
        self._seconds_left = self._get_duration() * 60
        t = self.app.theme_mgr.get_theme()
        labels = {
            "foco": t.get("focus_label", "Sessão de Foco"),
            "pausa_curta": t.get("short_break_label", "Pausa Curta"),
            "pausa_longa": t.get("long_break_label", "Pausa Longa"),
        }
        self.session_label.configure(text=labels.get(stype, stype))
        self._update_display()
        self.progress.set(1.0)
        self.start_btn.configure(state="normal", text="▶  Iniciar")
        self.pause_btn.configure(state="disabled")
        self._running = False
        self._started_at = None
        # Mostrar botão Pular apenas durante pausas
        if hasattr(self, "skip_btn"):
            if stype in ("pausa_curta", "pausa_longa"):
                self.skip_btn.grid()
            else:
                self.skip_btn.grid_remove()

    def _get_duration(self):
        return {"foco": self._focus_min, "pausa_curta": self._short_min, "pausa_longa": self._long_min}.get(
            self._session_type, self._focus_min
        )

    def _load_durations(self):
        user = self.app.current_user
        if user:
            self._focus_min = user.get("pomodoro_focus", 25)
            self._short_min = user.get("pomodoro_short", 5)
            self._long_min = user.get("pomodoro_long", 15)

    def _update_display(self):
        m, s = divmod(self._seconds_left, 60)
        time_str = f"{m:02d}:{s:02d}"
        self.time_label.configure(text=time_str)
        self.counter_label.configure(text=f"Sessão {self._sessions_done}/4")
        # Mostrar timer no título da janela
        if self._running:
            stype_names = {"foco": "Foco", "pausa_curta": "Pausa",
                           "pausa_longa": "Pausa Longa"}
            sname = stype_names.get(self._session_type, "")
            self.app.title(f"⏱ {time_str} — {sname} | Switch Focus")

    # ── seleção de tarefa ────────────────────────────────────
    def _pick_task(self):
        tasks = self.db.get_tasks(
            user_id=self.app.get_user_id(), status="pendente")
        if not tasks:
            self.task_label.configure(text="📋 Nenhuma tarefa pendente")
            return

        win = ctk.CTkToplevel(self)
        win.title("Selecionar Tarefa")
        win.geometry("400x350")
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(win, text="Selecione uma tarefa:",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=12)

        scroll = ctk.CTkScrollableFrame(win, width=360, height=240)
        scroll.pack(padx=15, fill="both", expand=True)

        for task in tasks:
            btn = ctk.CTkButton(
                scroll,
                text=f"{'🔴' if task['priority']=='alta' else '🟡' if task['priority']=='média' else '🟢'} {task['title']}",
                anchor="w", height=36,
                command=lambda t=task, w=win: self._select_task(t, w),
            )
            btn.pack(fill="x", pady=2)

    def _select_task(self, task, win):
        self._selected_task = task
        self.task_label.configure(text=f"📋 Tarefa: {task['title']}")
        win.destroy()

    def _skip_break(self):
        """Pula a pausa e volta direto ao foco."""
        if self._session_type in ("pausa_curta", "pausa_longa"):
            self._running = False
            if self._timer_id:
                self.after_cancel(self._timer_id)
            self._set_type("foco")

    # ── on_show ──────────────────────────────────────────────
    def on_show(self):
        self._load_durations()
        self._update_display()
        # Atalho de teclado: Space para iniciar/pausar
        self.app.bind("<space>", self._on_space_key)

    def _on_space_key(self, event=None):
        """Atalho: Espaço para iniciar/pausar o timer."""
        # Verificar se o Pomodoro está visível
        if not self.winfo_ismapped():
            return
        if self._running:
            self._pause()
        else:
            self._start()

    # ── tema ─────────────────────────────────────────────────────
    def _update_themed_header(self):
        t = self.app.theme_mgr.get_theme()
        self.header.configure(text=t.get("timer_title", "🍅 Pomodoro Timer"))
        # Atualizar labels da sessão atual
        if hasattr(self, "session_label"):
            labels = {
                "foco": t.get("focus_label", "Sessão de Foco"),
                "pausa_curta": t.get("short_break_label", "Pausa Curta"),
                "pausa_longa": t.get("long_break_label", "Pausa Longa"),
            }
            self.session_label.configure(text=labels.get(
                self._session_type, self._session_type))

    def apply_theme(self, t):
        self._update_themed_header()
        self.configure(fg_color=t["bg"])
        self.header.configure(text_color=t["primary"])
        self.timer_card.configure(fg_color=t["card"])
        self.session_label.configure(text_color=t["accent"])
        self.time_label.configure(text_color=t["text"])
        self.counter_label.configure(text_color=t["text_sec"])
        self.progress.configure(
            progress_color=t["progress"], fg_color=t["secondary"])
        self.start_btn.configure(fg_color=t["success"], hover_color="#5DBF60")
        self.pause_btn.configure(
            fg_color=t["warning"], hover_color="#FFD54F", text_color="#000")
        self.reset_btn.configure(fg_color=t["danger"], hover_color="#EF5350")
        self.task_label.configure(text_color=t["text_sec"])
        self.pick_task_btn.configure(
            fg_color=t["button"], hover_color=t["button_hover"])
        if hasattr(self, "skip_btn"):
            self.skip_btn.configure(
                fg_color=t["accent"], hover_color=t["button_hover"], text_color="#000")
