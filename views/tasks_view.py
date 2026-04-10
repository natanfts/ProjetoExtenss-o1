import flet as ft
from datetime import datetime


class TasksView:
    """Gerenciador de Tarefas com CRUD completo."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._filter = "todas"

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()
        self._theme = t

        # Filtro
        filter_dd = ft.Dropdown(
            value="Todas", width=140, height=45,
            options=[ft.dropdown.Option(v) for v in
                     ["Todas", "Pendentes", "Concluídas", "Alta", "Média", "Baixa"]],
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], text_size=13,
            on_select=self._on_filter,
        )

        add_btn = ft.ElevatedButton(
            content=ft.Text("＋ Nova Tarefa"), height=42,
            bgcolor=t["button"], color="#FFFFFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda _: self._open_add_dialog(),
        )

        self._task_list = ft.Column(
            spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)
        self._load_tasks()

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row([filter_dd, add_btn],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self._task_list,
            ], expand=True, spacing=10),
        )

    # ── listagem ─────────────────────────────────────────────
    def _load_tasks(self):
        t = self._theme
        self._task_list.controls.clear()

        status = None
        if self._filter == "pendentes":
            status = "pendente"
        elif self._filter == "concluídas":
            status = "concluída"

        tasks = self.db.get_tasks(
            user_id=self.app.get_user_id(), status=status)

        if self._filter in ("alta", "média", "baixa"):
            tasks = [tk for tk in tasks if tk.get("priority") == self._filter]

        if not tasks:
            self._task_list.controls.append(
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=40,
                    content=ft.Text(
                        "Nenhuma tarefa encontrada.\nToque em '＋ Nova Tarefa' para começar!",
                        size=14, color=t["text_sec"], text_align=ft.TextAlign.CENTER,
                    ),
                )
            )
            return

        for task in tasks:
            self._task_list.controls.append(self._render_task(task, t))

    def _render_task(self, task, t):
        done = task["status"] == "concluída"
        prio = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}.get(
            task["priority"], "⚪")

        # Deadline
        deadline_text = ""
        deadline = task.get("deadline")
        if deadline:
            try:
                dl = datetime.strptime(deadline, "%Y-%m-%d")
                days_left = (dl.date() - datetime.now().date()).days
                if days_left < 0:
                    deadline_text = f" ⚠️ Atrasada ({abs(days_left)}d)"
                elif days_left == 0:
                    deadline_text = " 🚨 Vence hoje!"
                elif days_left <= 3:
                    deadline_text = f" ⏳ {days_left}d"
                else:
                    deadline_text = f" 📅 {dl.strftime('%d/%m')}"
            except ValueError:
                pass

        pom_text = f"🍅 {task['pomodoros_done']}/{task['pomodoros_est']}"
        desc = task.get("description") or ""
        sub_text = f"{desc}  {pom_text}{deadline_text}".strip()

        return ft.Container(
            bgcolor=t["card"], border_radius=12,
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            on_click=lambda _, tk=task: self._open_edit_dialog(tk),
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.CHECK_CIRCLE if done else ft.Icons.CIRCLE_OUTLINED,
                    icon_color=t["success"] if done else t["text_sec"],
                    icon_size=28,
                    on_click=lambda _, tid=task["id"], d=done: self._toggle_complete(
                        tid, d),
                ),
                ft.Column([
                    ft.Text(
                        f"{prio} {task['title']}",
                        size=15, weight=ft.FontWeight.BOLD,
                        color=t["text_sec"] if done else t["text"],
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.LINE_THROUGH) if done else None,
                    ),
                    ft.Text(sub_text, size=12, color=t["text_sec"]),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=t["danger"], icon_size=22,
                    on_click=lambda _, tid=task["id"]: self._delete(tid),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )

    # ── ações ────────────────────────────────────────────────
    def _toggle_complete(self, task_id, currently_done):
        if currently_done:
            self.db.update_task(task_id, status="pendente", completed_at=None)
        else:
            self.db.complete_task(task_id)
            uid = self.app.get_user_id()
            if uid:
                self.db.add_xp(uid, 15, "task", "Tarefa concluída")
                self.db.update_daily_goal_progress(uid, "xp", 15)
                self.db.check_and_grant_achievements(uid)
                self.app.refresh_xp_sidebar()
        self._load_tasks()
        self.app.page.update()

    def _delete(self, task_id):
        self.app.show_confirm(
            "Confirmar", "Deseja excluir esta tarefa?",
            on_confirm=lambda: self._do_delete(task_id),
        )

    def _do_delete(self, task_id):
        self.db.delete_task(task_id)
        self._load_tasks()
        self.app.page.update()

    def _on_filter(self, e):
        self._filter = e.control.value.lower()
        self._load_tasks()
        self.app.page.update()

    # ── diálogo adicionar / editar ───────────────────────────
    def _open_add_dialog(self):
        self._task_dialog("Adicionar Tarefa")

    def _open_edit_dialog(self, task):
        self._task_dialog("Editar Tarefa", task)

    def _task_dialog(self, title, task=None):
        t = self._theme

        title_field = ft.TextField(
            label="Título da tarefa", width=320, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            value=task["title"] if task else "",
        )
        desc_field = ft.TextField(
            label="Descrição (opcional)", width=320, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            value=task.get("description", "") if task else "",
        )
        prio_dd = ft.Dropdown(
            label="Prioridade", width=320, height=55,
            value=task["priority"] if task else "média",
            options=[ft.dropdown.Option(v)
                     for v in ["alta", "média", "baixa"]],
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
        )
        pom_field = ft.TextField(
            label="Pomodoros estimados", width=320, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            value=str(task["pomodoros_est"]) if task else "1",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        dl_field = ft.TextField(
            label="📅 Prazo (dd/mm/aaaa)", width=320, height=50,
            bgcolor=t["entry_bg"], border_color=t["entry_border"],
            color=t["text"], label_style=ft.TextStyle(color=t["text_sec"]),
            value="",
        )
        if task and task.get("deadline"):
            try:
                dl = datetime.strptime(task["deadline"], "%Y-%m-%d")
                dl_field.value = dl.strftime("%d/%m/%Y")
            except ValueError:
                pass

        def save(e):
            t_title = title_field.value.strip() if title_field.value else ""
            if not t_title:
                self.app.show_snackbar("⚠️ Título é obrigatório.")
                return
            try:
                pom_val = int(pom_field.value)
            except (ValueError, TypeError):
                pom_val = 1

            deadline_val = None
            dl_text = dl_field.value.strip() if dl_field.value else ""
            if dl_text:
                try:
                    deadline_val = datetime.strptime(
                        dl_text, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    self.app.show_snackbar("⚠️ Use formato dd/mm/aaaa")
                    return

            if task:
                self.db.update_task(
                    task["id"], title=t_title,
                    description=desc_field.value.strip() if desc_field.value else "",
                    priority=prio_dd.value,
                    pomodoros_est=pom_val, deadline=deadline_val,
                )
            else:
                self.db.create_task(
                    t_title, desc_field.value.strip() if desc_field.value else "",
                    prio_dd.value, pom_val,
                    user_id=self.app.get_user_id(), deadline=deadline_val,
                )

            dlg.open = False
            self.app.page.update()
            self._load_tasks()
            self.app.page.update()

        def close(e):
            dlg.open = False
            self.app.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                title_field, desc_field, prio_dd, pom_field, dl_field,
            ], tight=True, spacing=8),
            actions=[
                ft.TextButton("Cancelar", on_click=close),
                ft.ElevatedButton(
                    "💾 Salvar", bgcolor=t["button"], color="#FFFFFF", on_click=save),
            ],
        )
        self.app.page.overlay.append(dlg)
        dlg.open = True
        self.app.page.update()
