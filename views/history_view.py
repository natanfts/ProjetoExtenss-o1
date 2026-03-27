import customtkinter as ctk


class HistoryView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title_lb = ctk.CTkLabel(
            self, text="📊 Histórico & Estatísticas",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.grid(row=0, column=0, pady=(20, 10), padx=25, sticky="w")

        # Cards de estatísticas
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(
            row=1, column=0, sticky="ew", padx=25, pady=(0, 10))

        # Scroll com histórico
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=2, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

    def _load(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        # ── Estatísticas ─────────────────────────────────────
        for w in self.stats_frame.winfo_children():
            w.destroy()

        stats = self.db.get_session_stats(uid)
        focus_hrs = (stats.get("focus_minutes") or 0) / 60

        stat_data = [
            ("🍅", "Sessões de Foco", str(stats.get("focus_count") or 0)),
            ("⏱️", "Horas Estudadas", f"{focus_hrs:.1f}h"),
            ("📅", "Dias Ativos", str(stats.get("days_active") or 0)),
            ("🔥", "Total de Sessões", str(stats.get("total") or 0)),
        ]

        for emoji, label, value in stat_data:
            card = ctk.CTkFrame(self.stats_frame, corner_radius=12,
                                fg_color=t["card"], width=180, height=90)
            card.pack(side="left", padx=6, fill="x", expand=True)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=f"{emoji} {value}",
                         font=ctk.CTkFont(size=24, weight="bold"),
                         text_color=t["primary"]).pack(pady=(15, 2))
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=12),
                         text_color=t["text_sec"]).pack()

        # ── Progresso por matéria ────────────────────────────
        for w in self.scroll.winfo_children():
            w.destroy()

        study_stats = self.db.get_study_stats(uid)
        if study_stats:
            ctk.CTkLabel(
                self.scroll, text="📚 Desempenho por Matéria",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=t["primary"],
            ).pack(anchor="w", pady=(10, 8))

            for ss in study_stats:
                card = ctk.CTkFrame(
                    self.scroll, corner_radius=10, fg_color=t["card"])
                card.pack(fill="x", pady=3)
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=10)
                inner.grid_columnconfigure(1, weight=1)

                ctk.CTkLabel(inner, text=ss["subject"],
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=t["text"]).grid(row=0, column=0, sticky="w")

                avg = ss.get("avg_score") or 0
                correct = ss.get("total_correct") or 0
                total_q = ss.get("total_q") or 0

                info = f"Sessões: {ss['sessions']}  |  Acertos: {correct}/{total_q}  |  Média: {avg:.0f}%"
                ctk.CTkLabel(inner, text=info,
                             font=ctk.CTkFont(size=12),
                             text_color=t["text_sec"]).grid(row=1, column=0, sticky="w")

                bar = ctk.CTkProgressBar(inner, width=120, height=10)
                bar.set(avg / 100 if avg else 0)
                bar.configure(progress_color=t["success"] if avg >=
                              70 else t["warning"] if avg >= 50 else t["danger"])
                bar.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))

        # ── Histórico de sessões Pomodoro ────────────────────
        sessions = self.db.get_sessions(uid, limit=30)

        ctk.CTkLabel(
            self.scroll, text="🕐 Sessões Recentes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(20, 8))

        if not sessions:
            ctk.CTkLabel(
                self.scroll,
                text="Nenhuma sessão registrada ainda.\nInicie um Pomodoro para começar!",
                font=ctk.CTkFont(size=14), text_color=t["text_sec"],
            ).pack(pady=20)
            return

        for s in sessions:
            card = ctk.CTkFrame(self.scroll, corner_radius=8,
                                fg_color=t["card"], height=50)
            card.pack(fill="x", pady=2)
            card.pack_propagate(False)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=8)

            types = {"foco": "🍅 Foco", "pausa_curta": "☕ Pausa Curta",
                     "pausa_longa": "🌿 Pausa Longa"}
            stype = types.get(s["session_type"], s["session_type"])

            task_info = f"  •  📋 {s['task_title']}" if s.get(
                "task_title") else ""

            ctk.CTkLabel(inner, text=f"{stype}  •  {s['duration']} min{task_info}",
                         font=ctk.CTkFont(size=13), text_color=t["text"]).pack(side="left")

            date_str = (s.get("completed_at") or "")[:16].replace("T", " ")
            ctk.CTkLabel(inner, text=date_str,
                         font=ctk.CTkFont(size=11), text_color=t["text_sec"]).pack(side="right")

    def on_show(self):
        self._load()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.scroll.configure(fg_color=t["bg"])
