import customtkinter as ctk
from datetime import datetime
from themes import THEMES, ThemeManager
from CTkMessagebox import CTkMessagebox


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._update_poll_id = None
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_lb = ctk.CTkLabel(
            self, text="⚙️ Configurações",
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

        # ── Temas ────────────────────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="🎨 Temas — Escolha seu Anime/Série",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(10, 12))

        themes_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        themes_grid.pack(fill="x")

        row_frame = None
        for i, (name, theme) in enumerate(THEMES.items()):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(themes_grid, fg_color="transparent")
                row_frame.pack(fill="x", pady=4)

            is_active = name == self.app.theme_mgr.current_theme
            border_color = theme["accent"] if is_active else theme["card"]

            card = ctk.CTkFrame(
                row_frame, corner_radius=12,
                fg_color=theme["card"],
                border_width=3 if is_active else 0,
                border_color=border_color,
                height=130,
            )
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)

            # Preview de cores
            colors_frame = ctk.CTkFrame(
                card, fg_color="transparent", height=20)
            colors_frame.pack(fill="x", padx=10, pady=(10, 0))
            for color_key in ["primary", "accent", "success", "danger"]:
                c = ctk.CTkFrame(colors_frame, width=25, height=12, corner_radius=6,
                                 fg_color=theme[color_key])
                c.pack(side="left", padx=2)

            # Nome + emoji
            ctk.CTkLabel(
                card, text=f"{theme['emoji']} {name}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=theme["text"],
            ).pack(pady=(8, 2))

            ctk.CTkLabel(
                card, text=theme["desc"][:50],
                font=ctk.CTkFont(size=10),
                text_color=theme["text_sec"],
                wraplength=200,
            ).pack(pady=(0, 3))

            if not is_active:
                ctk.CTkButton(
                    card, text="Aplicar", width=80, height=26,
                    font=ctk.CTkFont(size=11),
                    fg_color=theme["primary"],
                    hover_color=theme["button_hover"],
                    command=lambda n=name: self._apply_theme(n),
                ).pack(pady=(0, 8))
            else:
                ctk.CTkLabel(
                    card, text="✓ Ativo",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=theme["accent"],
                ).pack(pady=(0, 8))

        # ── Configurações do Pomodoro ────────────────────────
        ctk.CTkLabel(
            self.scroll, text="🍅 Configurações do Pomodoro",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(25, 12))

        pom_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        pom_card.pack(fill="x", pady=5)

        user = self.app.current_user
        focus_val = user.get("pomodoro_focus", 25) if user else 25
        short_val = user.get("pomodoro_short", 5) if user else 5
        long_val = user.get("pomodoro_long", 15) if user else 15

        self._pom_entries = {}
        for label, key, val in [
            ("⏱️ Foco (minutos):", "focus", focus_val),
            ("☕ Pausa curta (minutos):", "short", short_val),
            ("🌿 Pausa longa (minutos):", "long", long_val),
        ]:
            row = ctk.CTkFrame(pom_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=14),
                         text_color=t["text"]).pack(side="left")
            entry = ctk.CTkEntry(row, width=80, height=36,
                                 fg_color=t["entry_bg"], border_color=t["entry_border"],
                                 text_color=t["text"])
            entry.insert(0, str(val))
            entry.pack(side="right")
            self._pom_entries[key] = entry

        ctk.CTkButton(
            pom_card, text="💾 Salvar Configurações do Pomodoro",
            width=300, height=38,
            fg_color=t["button"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._save_pomodoro_settings,
        ).pack(pady=(10, 18))

        # ── Metas Diárias ────────────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="🎯 Metas Diárias",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(25, 12))

        goals_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        goals_card.pack(fill="x", pady=5)

        user = self.app.current_user
        pom_goal = user.get("daily_pomodoro_goal", 4) if user else 4
        xp_goal = user.get("daily_xp_goal", 100) if user else 100
        quiz_goal = user.get("daily_quiz_goal", 10) if user else 10

        self._goal_entries = {}
        for label, key, val in [
            ("🍅 Pomodoros por dia:", "pomodoro", pom_goal),
            ("⚡ XP por dia:", "xp", xp_goal),
            ("📝 Questões por dia:", "quiz", quiz_goal),
        ]:
            row = ctk.CTkFrame(goals_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=14),
                         text_color=t["text"]).pack(side="left")
            entry = ctk.CTkEntry(row, width=80, height=36,
                                 fg_color=t["entry_bg"], border_color=t["entry_border"],
                                 text_color=t["text"])
            entry.insert(0, str(val))
            entry.pack(side="right")
            self._goal_entries[key] = entry

        ctk.CTkButton(
            goals_card, text="💾 Salvar Metas Diárias",
            width=300, height=38,
            fg_color=t["button"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._save_goals_settings,
        ).pack(pady=(10, 18))

        # ── Sobre ────────────────────────────────────────────
        ctk.CTkLabel(
            self.scroll, text="ℹ️ Sobre o PomodoroStudy",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(25, 12))

        about_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        about_card.pack(fill="x", pady=5)

        about_text = (
            "🍅 PomodoroStudy v2.0\n\n"
            "Aplicativo de estudos com método Pomodoro integrado.\n"
            "Preparação para ENEM e Concursos com quizzes e videoaulas.\n"
            "Sistema de gamificação com XP, níveis e conquistas!\n"
            "Flashcards com repetição espaçada e metas diárias.\n"
            "Personalize com temas de seus animes e séries favoritos!\n\n"
            "Desenvolvido com Python + CustomTkinter + SQLite"
        )
        ctk.CTkLabel(
            about_card, text=about_text,
            font=ctk.CTkFont(size=13), text_color=t["text_sec"],
            justify="left", wraplength=600,
        ).pack(padx=20, pady=18, anchor="w")

        # ── Atualização de Conteúdo ──────────────────────────
        ctk.CTkLabel(
            self.scroll, text="🔄 Atualização de Conteúdo (YouTube)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(25, 12))

        update_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        update_card.pack(fill="x", pady=5)

        # Status da última atualização
        last_update = self.db.get_last_update("videos")
        if last_update:
            status_text = f"✅ Última atualização: {last_update.strftime('%d/%m/%Y às %H:%M')}"
            status_color = t["success"]
        else:
            status_text = "⚠️ Nenhuma atualização realizada ainda"
            status_color = t["warning"] if "warning" in t else t["accent"]

        self._update_status_lb = ctk.CTkLabel(
            update_card, text=status_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=status_color,
        )
        self._update_status_lb.pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            update_card,
            text="Os vídeos de aula são atualizados automaticamente a cada 24 horas.\n"
                 "Você pode forçar uma atualização manual clicando no botão abaixo.",
            font=ctk.CTkFont(size=12), text_color=t["text_sec"],
            justify="left", wraplength=600,
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # Barra de progresso (invisível até atualizar)
        self._update_progress = ctk.CTkProgressBar(
            update_card, width=400, height=12,
            progress_color=t["accent"],
            fg_color=t["entry_bg"],
        )
        self._update_progress.pack(padx=20, pady=(0, 5))
        self._update_progress.set(0)

        self._update_progress_lb = ctk.CTkLabel(
            update_card, text="",
            font=ctk.CTkFont(size=11),
            text_color=t["text_sec"],
        )
        self._update_progress_lb.pack(anchor="w", padx=20, pady=(0, 8))

        # Botões de ação
        btn_frame = ctk.CTkFrame(update_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 15))

        updater = self.app.updater
        is_running = updater.is_running

        self._force_update_btn = ctk.CTkButton(
            btn_frame, text="🔄  Atualizar Agora" if not is_running else "⏳ Atualizando...",
            width=220, height=40,
            fg_color=t["button"], hover_color=t["button_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled" if is_running else "normal",
            command=self._force_update,
        )
        self._force_update_btn.pack(side="left", padx=(0, 10))

        if is_running:
            self._update_progress.set(updater.progress_pct)
            self._update_progress_lb.configure(text=updater.progress)
            self._start_poll_update()

        # ── Histórico de Atualizações ────────────────────────
        ctk.CTkLabel(
            self.scroll, text="📜 Histórico de Atualizações",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(anchor="w", pady=(25, 12))

        history_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        history_card.pack(fill="x", pady=(5, 20))

        history = self.db.get_update_history(limit=10)

        if not history:
            ctk.CTkLabel(
                history_card, text="Nenhuma atualização registrada.",
                font=ctk.CTkFont(size=13), text_color=t["text_sec"],
            ).pack(padx=20, pady=18)
        else:
            # Cabeçalho
            header = ctk.CTkFrame(history_card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=(12, 4))
            for col, w in [("Data", 160), ("Status", 100), ("Vídeos", 80), ("Duração", 100)]:
                ctk.CTkLabel(
                    header, text=col, width=w,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=t["text_sec"], anchor="w",
                ).pack(side="left")

            for row_data in history:
                row = ctk.CTkFrame(history_card, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=2)

                # Data
                started = row_data.get("started_at", "")
                if isinstance(started, str) and started:
                    try:
                        dt = datetime.fromisoformat(started)
                        started = dt.strftime("%d/%m/%Y %H:%M")
                    except Exception:
                        pass
                ctk.CTkLabel(
                    row, text=str(started), width=160,
                    font=ctk.CTkFont(size=12), text_color=t["text"], anchor="w",
                ).pack(side="left")

                # Status
                status = row_data.get("status", "?")
                s_color = t["success"] if status == "success" else t["danger"]
                s_icon = "✅" if status == "success" else "❌"
                ctk.CTkLabel(
                    row, text=f"{s_icon} {status}", width=100,
                    font=ctk.CTkFont(size=12), text_color=s_color, anchor="w",
                ).pack(side="left")

                # Vídeos atualizados
                count = row_data.get("items_updated", 0)
                ctk.CTkLabel(
                    row, text=str(count), width=80,
                    font=ctk.CTkFont(size=12), text_color=t["text"], anchor="w",
                ).pack(side="left")

                # Duração
                finished = row_data.get("finished_at", "")
                duration_text = "—"
                if isinstance(started, str) and isinstance(finished, str) and finished:
                    try:
                        dt_s = datetime.fromisoformat(
                            row_data.get("started_at", ""))
                        dt_f = datetime.fromisoformat(finished)
                        delta = dt_f - dt_s
                        mins = int(delta.total_seconds() // 60)
                        secs = int(delta.total_seconds() % 60)
                        duration_text = f"{mins}m {secs}s" if mins else f"{secs}s"
                    except Exception:
                        pass
                ctk.CTkLabel(
                    row, text=duration_text, width=100,
                    font=ctk.CTkFont(size=12), text_color=t["text_sec"], anchor="w",
                ).pack(side="left")

    def _apply_theme(self, name):
        self.app.theme_mgr.set_theme(name)
        if self.app.current_user:
            self.db.update_user_theme(self.app.current_user["id"], name)
        self.app.refresh_theme()
        self._load()

    def _save_pomodoro_settings(self):
        try:
            focus = int(self._pom_entries["focus"].get())
            short = int(self._pom_entries["short"].get())
            long_ = int(self._pom_entries["long"].get())
        except ValueError:
            CTkMessagebox(
                title="Erro", message="Insira valores numéricos válidos.", icon="cancel")
            return

        if focus < 1 or short < 1 or long_ < 1:
            CTkMessagebox(
                title="Erro", message="Os valores devem ser maiores que zero.", icon="cancel")
            return

        if self.app.current_user:
            self.db.update_user_pomodoro(
                self.app.current_user["id"], focus, short, long_)
            self.app.current_user["pomodoro_focus"] = focus
            self.app.current_user["pomodoro_short"] = short
            self.app.current_user["pomodoro_long"] = long_
            CTkMessagebox(
                title="Salvo", message="Configurações do Pomodoro salvas!", icon="check")
        else:
            CTkMessagebox(
                title="Aviso",
                message="Faça login para salvar as configurações permanentemente.\nAs alterações serão temporárias.",
                icon="info",
            )

    def _save_goals_settings(self):
        try:
            pom = int(self._goal_entries["pomodoro"].get())
            xp = int(self._goal_entries["xp"].get())
            quiz = int(self._goal_entries["quiz"].get())
        except ValueError:
            CTkMessagebox(
                title="Erro", message="Insira valores numéricos válidos.", icon="cancel")
            return

        if pom < 1 or xp < 1 or quiz < 1:
            CTkMessagebox(
                title="Erro", message="Os valores devem ser maiores que zero.", icon="cancel")
            return

        if self.app.current_user:
            uid = self.app.current_user["id"]
            conn = self.db._conn()
            conn.execute(
                "UPDATE users SET daily_pomodoro_goal=?, daily_xp_goal=?, daily_quiz_goal=? WHERE id=?",
                (pom, xp, quiz, uid),
            )
            conn.commit()
            conn.close()
            self.app.current_user["daily_pomodoro_goal"] = pom
            self.app.current_user["daily_xp_goal"] = xp
            self.app.current_user["daily_quiz_goal"] = quiz
            CTkMessagebox(
                title="Salvo", message="Metas diárias salvas! 🎯", icon="check")
        else:
            CTkMessagebox(
                title="Aviso",
                message="Faça login para salvar as metas.",
                icon="info",
            )

    # ── Atualização de conteúdo ──────────────────────────────
    def _force_update(self):
        """Força uma atualização manual de vídeos."""
        updater = self.app.updater
        started = updater.start_update(force=True)
        if started:
            self._force_update_btn.configure(
                text="⏳ Atualizando...", state="disabled")
            self._update_progress.set(0)
            self._update_progress_lb.configure(text="Iniciando...")
            self._start_poll_update()
        else:
            CTkMessagebox(
                title="Aviso",
                message="Uma atualização já está em andamento.",
                icon="info",
            )

    def _start_poll_update(self):
        """Inicia polling periódico do progresso da atualização."""
        self._stop_poll_update()
        self._poll_update_progress()

    def _poll_update_progress(self):
        """Verifica o progresso e atualiza a UI."""
        updater = self.app.updater
        try:
            self._update_progress.set(updater.progress_pct)
            self._update_progress_lb.configure(text=updater.progress)
        except Exception:
            pass  # widget pode ter sido destruído

        if updater.is_running:
            self._update_poll_id = self.after(1000, self._poll_update_progress)
        else:
            # Atualização terminou
            self._update_poll_id = None
            t = self.app.theme_mgr.get_theme()
            color = t["success"] if updater.status == "done" else t["danger"]
            try:
                self._update_progress.set(1.0)
                self._update_progress_lb.configure(
                    text=updater.progress, text_color=color)
                self._force_update_btn.configure(
                    text="🔄  Atualizar Agora", state="normal")
                # Atualizar label de status
                last_update = self.db.get_last_update("videos")
                if last_update:
                    self._update_status_lb.configure(
                        text=f"✅ Última atualização: {last_update.strftime('%d/%m/%Y às %H:%M')}",
                        text_color=t["success"],
                    )
            except Exception:
                pass

    def _stop_poll_update(self):
        """Cancela o polling de progresso."""
        if self._update_poll_id is not None:
            self.after_cancel(self._update_poll_id)
            self._update_poll_id = None

    def on_show(self):
        self._load()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.scroll.configure(fg_color=t["bg"])
