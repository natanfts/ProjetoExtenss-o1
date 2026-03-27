import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class TasksView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._filter = "todas"
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
        top.grid_columnconfigure(1, weight=1)

        self.title_lb = ctk.CTkLabel(
            top, text="📋 Gerenciador de Tarefas",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.grid(row=0, column=0, sticky="w")

        btn_area = ctk.CTkFrame(top, fg_color="transparent")
        btn_area.grid(row=0, column=2, sticky="e")

        self.filter_menu = ctk.CTkOptionMenu(
            btn_area, values=["Todas", "Pendentes", "Concluídas"],
            width=130, command=self._on_filter,
        )
        self.filter_menu.grid(row=0, column=0, padx=5)

        self.add_btn = ctk.CTkButton(
            btn_area, text="＋ Nova Tarefa", width=140, height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._open_add_dialog,
        )
        self.add_btn.grid(row=0, column=1, padx=5)

        # Lista de tarefas
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

        self.empty_label = ctk.CTkLabel(
            self.scroll, text="Nenhuma tarefa encontrada.\nClique em '＋ Nova Tarefa' para começar!",
            font=ctk.CTkFont(size=14),
        )

    # ── listagem ─────────────────────────────────────────────
    def _load_tasks(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        status = None
        if self._filter == "pendentes":
            status = "pendente"
        elif self._filter == "concluídas":
            status = "concluída"

        tasks = self.db.get_tasks(
            user_id=self.app.get_user_id(), status=status)

        if not tasks:
            self.empty_label = ctk.CTkLabel(
                self.scroll,
                text="Nenhuma tarefa encontrada.\nClique em '＋ Nova Tarefa' para começar!",
                font=ctk.CTkFont(size=14),
            )
            self.empty_label.pack(pady=40)
            return

        for task in tasks:
            self._render_task(task)

    def _render_task(self, task):
        t = self.app.theme_mgr.get_theme()
        card = ctk.CTkFrame(self.scroll, corner_radius=12,
                            fg_color=t["card"], height=80)
        card.pack(fill="x", pady=4)
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        inner.grid_columnconfigure(1, weight=1)

        # Checkbox concluir
        done = task["status"] == "concluída"
        check_text = "✅" if done else "⬜"
        check_btn = ctk.CTkButton(
            inner, text=check_text, width=36, height=36,
            fg_color="transparent", hover_color=t["card"],
            font=ctk.CTkFont(size=18),
            command=lambda tid=task["id"]: self._toggle_complete(tid, done),
        )
        check_btn.grid(row=0, column=0, rowspan=2, padx=(0, 10))

        # Prioridade emoji
        prio = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}.get(
            task["priority"], "⚪")

        title_text = f"{prio} {task['title']}"
        if done:
            title_text = f"~~{task['title']}~~"

        title = ctk.CTkLabel(
            inner, text=title_text,
            font=ctk.CTkFont(size=15, weight="bold", overstrike=done),
            anchor="w", text_color=t["text_sec"] if done else t["text"],
        )
        title.grid(row=0, column=1, sticky="w")

        desc_text = task.get("description", "") or ""
        pom_text = f"🍅 {task['pomodoros_done']}/{task['pomodoros_est']}"
        sub = ctk.CTkLabel(
            inner, text=f"{desc_text}  {pom_text}".strip(),
            font=ctk.CTkFont(size=12),
            anchor="w", text_color=t["text_sec"],
        )
        sub.grid(row=1, column=1, sticky="w")

        # Ações
        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.grid(row=0, column=2, rowspan=2, sticky="e")

        ctk.CTkButton(
            actions, text="✏️", width=34, height=34,
            fg_color="transparent", hover_color=t["secondary"],
            command=lambda tid=task: self._open_edit_dialog(tid),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions, text="🗑️", width=34, height=34,
            fg_color="transparent", hover_color=t["danger"],
            command=lambda tid=task["id"]: self._delete(tid),
        ).pack(side="left", padx=2)

    # ── ações ────────────────────────────────────────────────
    def _toggle_complete(self, task_id, currently_done):
        if currently_done:
            self.db.update_task(task_id, status="pendente", completed_at=None)
        else:
            self.db.complete_task(task_id)
        self._load_tasks()

    def _delete(self, task_id):
        msg = CTkMessagebox(
            title="Confirmar", message="Deseja excluir esta tarefa?",
            icon="question", option_1="Cancelar", option_2="Excluir",
        )
        if msg.get() == "Excluir":
            self.db.delete_task(task_id)
            self._load_tasks()

    def _on_filter(self, value):
        self._filter = value.lower()
        self._load_tasks()

    # ── diálogo adicionar ────────────────────────────────────
    def _open_add_dialog(self):
        self._task_dialog("Adicionar Tarefa")

    def _open_edit_dialog(self, task):
        self._task_dialog("Editar Tarefa", task)

    def _task_dialog(self, title, task=None):
        t = self.app.theme_mgr.get_theme()
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("440x420")
        win.transient(self)
        win.grab_set()
        win.configure(fg_color=t["bg"])

        ctk.CTkLabel(win, text=title, font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=t["primary"]).pack(pady=(18, 12))

        title_e = ctk.CTkEntry(win, placeholder_text="Título da tarefa", width=360, height=40,
                               fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"])
        title_e.pack(pady=6)

        desc_e = ctk.CTkEntry(win, placeholder_text="Descrição (opcional)", width=360, height=40,
                              fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"])
        desc_e.pack(pady=6)

        prio_var = ctk.StringVar(value="média")
        prio = ctk.CTkOptionMenu(win, variable=prio_var, values=[
                                 "alta", "média", "baixa"], width=360)
        prio.configure(fg_color=t["button"], button_color=t["button_hover"])
        prio.pack(pady=6)

        pom_frame = ctk.CTkFrame(win, fg_color="transparent")
        pom_frame.pack(pady=6)
        ctk.CTkLabel(pom_frame, text="Pomodoros estimados:",
                     text_color=t["text"]).pack(side="left", padx=5)
        pom_e = ctk.CTkEntry(pom_frame, width=60, height=36,
                             fg_color=t["entry_bg"], border_color=t["entry_border"], text_color=t["text"])
        pom_e.insert(0, "1")
        pom_e.pack(side="left")

        if task:
            title_e.insert(0, task["title"])
            desc_e.insert(0, task.get("description") or "")
            prio_var.set(task["priority"])
            pom_e.delete(0, "end")
            pom_e.insert(0, str(task["pomodoros_est"]))

        def save():
            t_title = title_e.get().strip()
            if not t_title:
                CTkMessagebox(title="Atenção",
                              message="Título é obrigatório.", icon="warning")
                return
            try:
                pom_val = int(pom_e.get())
            except ValueError:
                pom_val = 1

            if task:
                self.db.update_task(
                    task["id"], title=t_title,
                    description=desc_e.get().strip(),
                    priority=prio_var.get(),
                    pomodoros_est=pom_val,
                )
            else:
                self.db.create_task(
                    t_title, desc_e.get().strip(),
                    prio_var.get(), pom_val,
                    user_id=self.app.get_user_id(),
                )
            win.destroy()
            self._load_tasks()

        ctk.CTkButton(
            win, text="💾 Salvar", width=360, height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=t["button"], hover_color=t["button_hover"],
            command=save,
        ).pack(pady=(18, 10))

    # ── hooks ────────────────────────────────────────────────
    def on_show(self):
        self._load_tasks()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.add_btn.configure(
            fg_color=t["button"], hover_color=t["button_hover"])
        self.scroll.configure(fg_color=t["bg"])
        self.filter_menu.configure(
            fg_color=t["button"], button_color=t["button_hover"])
        self._load_tasks()
