import flet as ft
from datetime import datetime
import logging
import platform
import threading
import asyncio

logger = logging.getLogger("PomodoroView")

# Guard: winsound só existe no Windows
if platform.system() == "Windows":
    import winsound
else:
    winsound = None


class PomodoroView:
    """Timer Pomodoro com controles e seleção de tarefa."""

    def __init__(self, app):
        self.app = app
        self.db = app.db

        self._focus_min = 25
        self._short_min = 5
        self._long_min = 15
        self._seconds_left = self._focus_min * 60
        self._running = False
        self._session_type = "foco"
        self._sessions_done = 0
        self._started_at = None
        self._selected_task = None
        self._built = False

        # Controles persistentes
        self._time_label = ft.Text("25:00", size=72, weight=ft.FontWeight.BOLD)
        self._session_label = ft.Text("Sessão de Foco", size=16)
        self._counter_label = ft.Text("Sessão 0/4", size=14)
        self._progress_bar = ft.ProgressBar(
            value=1.0, height=10, border_radius=5)
        self._task_label = ft.Text("📋 Nenhuma tarefa selecionada", size=13)

        self._start_btn = ft.Button(content=ft.Text(
            "▶ Iniciar"), height=44, width=130, on_click=self._start)
        self._pause_btn = ft.Button(content=ft.Text("⏸ Pausar"), height=44, width=130,
                                    disabled=True, on_click=self._pause)
        self._reset_btn = ft.Button(content=ft.Text(
            "🔄 Reset"), height=44, width=130, on_click=self._reset)
        self._skip_btn = ft.Button(content=ft.Text("⏭ Pular"), height=44, width=130,
                                   visible=False, on_click=self._skip_break)

    def on_show(self):
        self._load_durations()
        self._update_display()

    def build(self):
        t = self.app.theme_mgr.get_theme()

        # Aplicar cores
        self._time_label.color = t["text"]
        self._session_label.color = t["accent"]
        self._counter_label.color = t["text_sec"]
        self._progress_bar.color = t["progress"]
        self._progress_bar.bgcolor = t["secondary"]
        self._task_label.color = t["text_sec"]

        self._start_btn.bgcolor = t["success"]
        self._start_btn.color = "#FFFFFF"
        self._pause_btn.bgcolor = t["warning"]
        self._pause_btn.color = "#000000"
        self._reset_btn.bgcolor = t["danger"]
        self._reset_btn.color = "#FFFFFF"
        self._skip_btn.bgcolor = t["accent"]
        self._skip_btn.color = "#000000"

        # Atualizar label de sessão
        labels = {
            "foco": t.get("focus_label", "Sessão de Foco"),
            "pausa_curta": t.get("short_break_label", "Pausa Curta"),
            "pausa_longa": t.get("long_break_label", "Pausa Longa"),
        }
        self._session_label.value = labels.get(
            self._session_type, "Sessão de Foco")

        pick_task_btn = ft.TextButton(
            content=ft.Text("Selecionar Tarefa"), on_click=self._pick_task,
            style=ft.ButtonStyle(color=t["primary"]),
        )

        # Seletor de tipo
        type_btns = []
        for txt, stype in [("Foco", "foco"), ("Pausa Curta", "pausa_curta"), ("Pausa Longa", "pausa_longa")]:
            type_btns.append(
                ft.TextButton(
                    content=ft.Text(txt),
                    on_click=lambda _, s=stype: self._set_type(s),
                    style=ft.ButtonStyle(color=t["text_sec"]),
                )
            )

        timer_card = ft.Container(
            width=340, height=320, border_radius=20,
            bgcolor=t["card"],
            alignment=ft.Alignment.CENTER,
            content=ft.Column([
                self._session_label,
                self._time_label,
                self._counter_label,
                ft.Container(
                    content=self._progress_bar,
                    width=260, padding=ft.padding.only(top=10),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            alignment=ft.Alignment.TOP_CENTER,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                timer_card,
                ft.Row([
                    self._start_btn, self._pause_btn,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([
                    self._reset_btn, self._skip_btn,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([self._task_label, pick_task_btn],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(type_btns, alignment=ft.MainAxisAlignment.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        )

    # ── timer ────────────────────────────────────────────────
    def _start(self, e=None):
        if not self._running:
            self._running = True
            self._started_at = self._started_at or datetime.now().isoformat()
            self._start_btn.disabled = True
            self._pause_btn.disabled = False
            self.app.page.update()
            self.app.page.run_task(self._tick_loop)

    def _pause(self, e=None):
        self._running = False
        self._start_btn.disabled = False
        self._start_btn.content = ft.Text("▶ Continuar")
        self._pause_btn.disabled = True
        self.app.page.update()

    def _reset(self, e=None):
        self._running = False
        self._load_durations()
        self._seconds_left = self._get_duration() * 60
        self._started_at = None
        self._start_btn.disabled = False
        self._start_btn.content = ft.Text("▶ Iniciar")
        self._pause_btn.disabled = True
        self._progress_bar.value = 1.0
        self._update_display()
        self.app.page.update()

    async def _tick_loop(self):
        while self._running and self._seconds_left > 0:
            await asyncio.sleep(1)
            if not self._running:
                break
            self._seconds_left -= 1
            total = self._get_duration() * 60
            self._progress_bar.value = self._seconds_left / total if total else 0
            self._update_display()
            try:
                self.app.page.update()
            except Exception:
                logger.debug("page.update() falhou no tick_loop, encerrando")
                break

        if self._seconds_left <= 0 and self._running:
            self._running = False
            self._session_complete()

    def _session_complete(self):
        self._start_btn.disabled = False
        self._start_btn.content = ft.Text("▶ Iniciar")
        self._pause_btn.disabled = True

        duration = self._get_duration()
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
            uid = self.app.get_user_id()
            if uid:
                self.db.add_xp(uid, 25, "pomodoro",
                               f"Pomodoro de {duration} min")
                self.db.update_streak(uid)
                self.db.update_daily_goal_progress(uid, "pomodoro")
                self.db.update_daily_goal_progress(uid, "xp", 25)
                self.db.check_and_grant_achievements(uid)
                self.app.refresh_xp_sidebar()

        # Beep
        def _beep():
            if winsound:
                winsound.Beep(800, 600)
            else:
                logger.debug("Beep sonoro não disponível (sem winsound)")
        threading.Thread(target=_beep, daemon=True).start()

        # Auto-switch
        if self._session_type == "foco":
            if self._sessions_done % 4 == 0:
                self._set_type("pausa_longa")
            else:
                self._set_type("pausa_curta")
        else:
            self._set_type("foco")

        self._started_at = None
        self.app.show_snackbar("⏰ Sessão concluída!")
        try:
            self.app.page.update()
        except Exception:
            logger.debug("page.update() falhou em _session_complete")

    def _set_type(self, stype, e=None):
        self._running = False
        self._session_type = stype
        self._load_durations()
        self._seconds_left = self._get_duration() * 60
        self._progress_bar.value = 1.0
        self._start_btn.disabled = False
        self._start_btn.content = ft.Text("▶ Iniciar")
        self._pause_btn.disabled = True
        self._started_at = None

        t = self.app.theme_mgr.get_theme()
        labels = {
            "foco": t.get("focus_label", "Sessão de Foco"),
            "pausa_curta": t.get("short_break_label", "Pausa Curta"),
            "pausa_longa": t.get("long_break_label", "Pausa Longa"),
        }
        self._session_label.value = labels.get(stype, stype)

        # Mostrar/ocultar botão pular
        self._skip_btn.visible = stype in ("pausa_curta", "pausa_longa")

        self._update_display()
        try:
            self.app.page.update()
        except Exception:
            logger.debug("page.update() falhou em _set_type")

    def _skip_break(self, e=None):
        if self._session_type in ("pausa_curta", "pausa_longa"):
            self._running = False
            self._set_type("foco")

    def _get_duration(self):
        return {"foco": self._focus_min, "pausa_curta": self._short_min,
                "pausa_longa": self._long_min}.get(self._session_type, self._focus_min)

    def _load_durations(self):
        user = self.app.current_user
        if user:
            self._focus_min = user.get("pomodoro_focus", 25)
            self._short_min = user.get("pomodoro_short", 5)
            self._long_min = user.get("pomodoro_long", 15)

    def _update_display(self):
        m, s = divmod(self._seconds_left, 60)
        self._time_label.value = f"{m:02d}:{s:02d}"
        self._counter_label.value = f"Sessão {self._sessions_done}/4"

    # ── seleção de tarefa ────────────────────────────────────
    def _pick_task(self, e=None):
        tasks = self.db.get_tasks(
            user_id=self.app.get_user_id(), status="pendente")
        if not tasks:
            self.app.show_snackbar("📋 Nenhuma tarefa pendente")
            return

        t = self.app.theme_mgr.get_theme()
        task_tiles = []
        for task in tasks:
            prio_icon = {"alta": "🔴", "média": "🟡",
                         "baixa": "🟢"}.get(task["priority"], "⚪")
            task_tiles.append(
                ft.ListTile(
                    title=ft.Text(
                        f"{prio_icon} {task['title']}", color=t["text"]),
                    on_click=lambda _, tk=task: self._select_task(tk),
                )
            )

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Selecionar Tarefa", size=18,
                                weight=ft.FontWeight.BOLD, color=t["primary"]),
                        *task_tiles,
                    ],
                    tight=True, scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=t["card"],
            ),
        )
        self.app.page.overlay.append(bs)
        bs.open = True
        self.app.page.update()

    def _select_task(self, task):
        self._selected_task = task
        self._task_label.value = f"📋 Tarefa: {task['title']}"
        # Fechar bottom sheet
        if self.app.page.overlay:
            self.app.page.overlay[-1].open = False
        self.app.page.update()
