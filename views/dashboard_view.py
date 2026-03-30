import customtkinter as ctk
from datetime import datetime


class DashboardView(ctk.CTkFrame):
    """Tela inicial — Dashboard com resumo do dia, XP, streak, metas e conquistas."""

    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_lb = ctk.CTkLabel(
            self, text="🏠 Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.grid(row=0, column=0, pady=(20, 10), padx=25, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

    def _load(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        if not uid:
            self._show_guest_message(t)
            return

        # Atualizar streak
        self.db.update_streak(uid)

        # ── Saudação ─────────────────────────────────────────
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Bom dia"
        elif hour < 18:
            greeting = "Boa tarde"
        else:
            greeting = "Boa noite"
        name = self.app.current_user.get("display_name", "Estudante")

        greeting_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        greeting_frame.pack(fill="x", pady=(10, 15))

        ctk.CTkLabel(
            greeting_frame,
            text=f"👋 {greeting}, {name}!",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["text"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            greeting_frame,
            text=datetime.now().strftime("%A, %d de %B de %Y").capitalize(),
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
        ).pack(anchor="w")

        # ── Barra de XP e Nível ──────────────────────────────
        xp_info = self.db.get_xp_info(uid)
        streak_info = self.db.get_streak(uid)

        xp_card = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color=t["card"])
        xp_card.pack(fill="x", pady=8)

        xp_inner = ctk.CTkFrame(xp_card, fg_color="transparent")
        xp_inner.pack(fill="x", padx=20, pady=15)

        # Nível + XP
        level_frame = ctk.CTkFrame(xp_inner, fg_color="transparent")
        level_frame.pack(fill="x")

        ctk.CTkLabel(
            level_frame,
            text=f"⭐ Nível {xp_info['level']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t["accent"],
        ).pack(side="left")

        ctk.CTkLabel(
            level_frame,
            text=f"🔥 {streak_info['streak']} dias seguidos",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t["danger"] if streak_info["streak"] >= 7 else t["warning"],
        ).pack(side="right")

        # Barra de progresso do nível
        xp_bar_frame = ctk.CTkFrame(xp_inner, fg_color="transparent")
        xp_bar_frame.pack(fill="x", pady=(8, 2))

        xp_bar = ctk.CTkProgressBar(xp_bar_frame, height=14, corner_radius=7)
        xp_bar.set(xp_info["progress"])
        xp_bar.configure(progress_color=t["accent"], fg_color=t["secondary"])
        xp_bar.pack(fill="x")

        ctk.CTkLabel(
            xp_inner,
            text=f"{xp_info['xp']} / {xp_info['xp_next_level']} XP  •  Recorde de streak: {streak_info['longest']} dias",
            font=ctk.CTkFont(size=11),
            text_color=t["text_sec"],
        ).pack(anchor="w", pady=(2, 0))

        # ── Metas do Dia ─────────────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="🎯 Metas de Hoje",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(18, 8))

        goals_summary = self.db.get_daily_goals_summary(uid)
        goals = goals_summary["goals"]
        today_stats = self.db.get_today_stats(uid)

        goals_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        goals_frame.pack(fill="x")

        goal_configs = {
            "pomodoro": ("🍅", "Pomodoros", today_stats["pomodoros"]),
            "xp":       ("⚡", "XP Ganho", today_stats["xp_today"]),
            "quiz":     ("📝", "Questões", today_stats["questions"]),
        }

        for goal in goals:
            gtype = goal["goal_type"]
            config = goal_configs.get(gtype, ("📌", gtype, goal["current_value"]))
            emoji, label, current = config

            # Atualizar valor real
            current = max(current, goal["current_value"])
            target = goal["target_value"]
            done = current >= target
            pct = min(current / target, 1.0) if target > 0 else 0

            card = ctk.CTkFrame(goals_frame, corner_radius=12, fg_color=t["card"])
            card.pack(fill="x", pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)
            inner.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                inner,
                text=f"{emoji} {label}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=t["success"] if done else t["text"],
            ).grid(row=0, column=0, sticky="w")

            status_text = f"✅ {current}/{target}" if done else f"{current}/{target}"
            ctk.CTkLabel(
                inner, text=status_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=t["success"] if done else t["text_sec"],
            ).grid(row=0, column=2, sticky="e")

            bar = ctk.CTkProgressBar(inner, height=8, corner_radius=4)
            bar.set(pct)
            bar.configure(
                progress_color=t["success"] if done else t["accent"],
                fg_color=t["secondary"],
            )
            bar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0))

        if goals_summary["all_done"]:
            ctk.CTkLabel(
                self.scroll,
                text="🎉 Parabéns! Todas as metas de hoje foram cumpridas!",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=t["success"],
            ).pack(anchor="w", pady=(8, 0))

        # ── Estatísticas de Hoje ─────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="📊 Resumo de Hoje",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(18, 8))

        stats_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        stats_frame.pack(fill="x")

        stat_items = [
            ("🍅", "Pomodoros", str(today_stats["pomodoros"])),
            ("⏱️", "Min. de Foco", str(today_stats["focus_min"])),
            ("📝", "Questões", str(today_stats["questions"])),
            ("⚡", "XP Ganho", str(today_stats["xp_today"])),
        ]

        row_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        row_frame.pack(fill="x")

        for emoji, label, value in stat_items:
            card = ctk.CTkFrame(row_frame, corner_radius=12, fg_color=t["card"],
                                height=90)
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)
            ctk.CTkLabel(
                card, text=f"{emoji} {value}",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=t["primary"],
            ).pack(pady=(18, 2))
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=11),
                text_color=t["text_sec"],
            ).pack()

        # ── Conquistas Recentes ──────────────────────────────
        # Verificar novas conquistas
        new_achs = self.db.check_and_grant_achievements(uid)

        earned = self.db.get_user_achievements(uid)
        all_achs = self.db.get_all_achievements()

        ctk.CTkLabel(
            self.scroll, text=f"🏆 Conquistas ({len(earned)}/{len(all_achs)})",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(18, 8))

        # Mostrar novas conquistas com destaque
        if new_achs:
            for ach in new_achs:
                new_card = ctk.CTkFrame(self.scroll, corner_radius=12,
                                        fg_color=t["accent"], border_width=2, border_color=t["accent"])
                new_card.pack(fill="x", pady=4)
                inner = ctk.CTkFrame(new_card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=10)

                ctk.CTkLabel(
                    inner,
                    text=f"🎉 NOVA CONQUISTA: {ach['emoji']} {ach['title']}",
                    font=ctk.CTkFont(size=15, weight="bold"),
                    text_color=t["bg"],
                ).pack(anchor="w")
                ctk.CTkLabel(
                    inner,
                    text=f"{ach['description']}  (+{ach['xp_reward']} XP)",
                    font=ctk.CTkFont(size=12),
                    text_color=t["bg"],
                ).pack(anchor="w")

        # Grid de conquistas
        earned_keys = {a["key"] for a in earned}
        achs_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        achs_frame.pack(fill="x")

        row_frame = None
        for i, ach in enumerate(all_achs):
            if i % 4 == 0:
                row_frame = ctk.CTkFrame(achs_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=3)

            is_earned = ach["key"] in earned_keys
            card = ctk.CTkFrame(
                row_frame, corner_radius=10,
                fg_color=t["card"] if is_earned else t["secondary"],
                border_width=2 if is_earned else 0,
                border_color=t["success"] if is_earned else t["card"],
                height=100,
            )
            card.pack(side="left", fill="x", expand=True, padx=3)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card,
                text=ach["emoji"] if is_earned else "🔒",
                font=ctk.CTkFont(size=24),
            ).pack(pady=(10, 2))

            ctk.CTkLabel(
                card,
                text=ach["title"] if is_earned else "???",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=t["text"] if is_earned else t["text_sec"],
                wraplength=120,
            ).pack()

            if is_earned:
                ctk.CTkLabel(
                    card,
                    text=f"+{ach['xp_reward']} XP",
                    font=ctk.CTkFont(size=9),
                    text_color=t["success"],
                ).pack()

        # ── Ações Rápidas ────────────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="⚡ Ações Rápidas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(18, 8))

        actions_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 15))

        actions = [
            ("🍅  Iniciar Pomodoro", "pomodoro"),
            ("📝  Fazer Quiz", "study"),
            ("🃏  Revisar Flashcards", "flashcards"),
            ("📋  Ver Tarefas", "tasks"),
        ]

        for text, target in actions:
            ctk.CTkButton(
                actions_frame, text=text, height=42, width=200,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=t["button"], hover_color=t["button_hover"],
                corner_radius=10,
                command=lambda f=target: self.app.show_frame(f),
            ).pack(side="left", padx=4, fill="x", expand=True)

    def _show_guest_message(self, t):
        """Mostra mensagem para convidados."""
        ctk.CTkLabel(
            self.scroll,
            text="👋 Bem-vindo ao PomodoroStudy!",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self.scroll,
            text="Faça login ou cadastre-se para desbloquear:\n\n"
                 "⭐ Sistema de XP e Níveis\n"
                 "🔥 Streak de dias consecutivos\n"
                 "🏆 Conquistas e badges\n"
                 "🎯 Metas diárias personalizáveis\n"
                 "🃏 Flashcards com repetição espaçada\n"
                 "📊 Dashboard completo",
            font=ctk.CTkFont(size=14),
            text_color=t["text_sec"],
            justify="left",
        ).pack(pady=10)

        ctk.CTkButton(
            self.scroll, text="🔑  Entrar / Cadastrar",
            width=250, height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=t["button"], hover_color=t["button_hover"],
            command=lambda: self.app.show_frame("login"),
        ).pack(pady=20)

    def on_show(self):
        self._load()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.scroll.configure(fg_color=t["bg"])
