import customtkinter as ctk
import csv
import os
from datetime import datetime, timedelta
from tkinter import filedialog


class HistoryView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.db = app.db
        self._filter_period = "tudo"  # hoje | semana | mes | tudo
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ── Linha 0: Título temático ─────────────────────────
        self.title_lb = ctk.CTkLabel(
            self, text="📊 Histórico & Estatísticas",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_lb.grid(row=0, column=0, pady=(20, 4), padx=25, sticky="w")

        self.subtitle_lb = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=13),
        )
        self.subtitle_lb.grid(
            row=1, column=0, pady=(0, 10), padx=25, sticky="w")

        # ── Linha 1: Cards de estatísticas (grid responsivo) ─
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(
            row=2, column=0, sticky="ew", padx=25, pady=(0, 10))
        for i in range(6):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        # ── Linha 2: Scroll com histórico ────────────────────
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=3, column=0, sticky="nswe", padx=25, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

    # ══════════════════════════════════════════════════════════
    # ── HELPERS ──────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _stat_card(self, parent, emoji, value, label, t, col, row=0,
                   value_color=None):
        """Cria um card de estatística no grid responsivo."""
        card = ctk.CTkFrame(parent, corner_radius=12,
                            fg_color=t["card"], height=90)
        card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text=f"{emoji} {value}",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=value_color or t["primary"],
                     ).grid(row=0, column=0, pady=(15, 1), sticky="n")
        ctk.CTkLabel(card, text=label,
                     font=ctk.CTkFont(size=11),
                     text_color=t["text_sec"],
                     ).grid(row=1, column=0, sticky="n")
        return card

    def _section_title(self, parent, text, t, pady=(20, 8)):
        ctk.CTkLabel(parent, text=text,
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=t["primary"]).pack(anchor="w", pady=pady)

    def _filter_date(self):
        """Retorna data ISO mínima conforme filtro selecionado."""
        now = datetime.now()
        if self._filter_period == "hoje":
            return now.strftime("%Y-%m-%d")
        elif self._filter_period == "semana":
            return (now - timedelta(days=7)).strftime("%Y-%m-%d")
        elif self._filter_period == "mes":
            return (now - timedelta(days=30)).strftime("%Y-%m-%d")
        return None  # tudo

    # ══════════════════════════════════════════════════════════
    # ── CARREGAMENTO PRINCIPAL ───────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _load(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        # ── Título temático (melhoria 5) ─────────────────────
        xp_info = self.db.get_xp_info(uid)
        streak_info = self.db.get_streak(uid)
        level_prefix = t.get("level_prefix", "Nível")
        xp_name = t.get("xp_name", "XP")
        level = xp_info.get("level", 1)
        xp = xp_info.get("xp", 0)
        streak = streak_info.get("streak", 0)

        # Mensagem motivacional dinâmica
        if streak >= 7 and level >= 5:
            motiv = f"🔥 Imparável! {streak} dias seguidos no {level_prefix} {level}!"
        elif streak >= 3:
            motiv = t.get("streak_msg", "🔥 {dias} dias seguidos!").format(
                dias=streak)
        elif xp > 500:
            motiv = f"⭐ {xp} {xp_name} acumulados — continue assim!"
        elif level > 1:
            motiv = f"📈 {level_prefix} {level} — sua evolução está aqui!"
        else:
            motiv = "📊 Acompanhe seu progresso e evolua nos estudos!"

        self.title_lb.configure(text=f"📊 Histórico & Estatísticas")
        self.subtitle_lb.configure(text=motiv, text_color=t["text_sec"])

        # ── Cards de estatísticas (melhoria 6 + 8 + 9) ──────
        for w in self.stats_frame.winfo_children():
            w.destroy()

        stats = self.db.get_session_stats(uid)
        focus_hrs = (stats.get("focus_minutes") or 0) / 60
        theory_stats = self.db.get_theory_stats(uid)
        theory_total = sum(s.get("completed", 0)
                           for s in theory_stats.values())

        self._stat_card(self.stats_frame, "⭐", f"{level_prefix} {level}", "Nível Atual",
                        t, col=0, value_color=t["accent"])
        self._stat_card(self.stats_frame, "✨", f"{xp} {xp_name}", "XP Total",
                        t, col=1, value_color=t["primary"])
        self._stat_card(self.stats_frame, "🔥",
                        f"{streak} {'dia' if streak == 1 else 'dias'}",
                        f"Streak (rec: {streak_info.get('longest', 0)})",
                        t, col=2, value_color=t["danger"] if streak >= 7 else t["warning"])
        self._stat_card(self.stats_frame, "🍅", str(stats.get("focus_count") or 0),
                        "Sessões de Foco", t, col=3)
        self._stat_card(self.stats_frame, "⏱️", f"{focus_hrs:.1f}h",
                        "Horas Estudadas", t, col=4)
        self._stat_card(self.stats_frame, "📖", str(theory_total),
                        "Tópicos Concluídos", t, col=5, value_color=t["success"])

        # ── Conteúdo principal (scroll) ──────────────────────
        for w in self.scroll.winfo_children():
            w.destroy()

        # ── Filtros de período (melhoria 2) ──────────────────
        filter_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(filter_frame, text="📅 Período:",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=t["text"]).pack(side="left", padx=(0, 8))

        for period_key, period_label in [("hoje", "Hoje"), ("semana", "Semana"),
                                         ("mes", "Mês"), ("tudo", "Tudo")]:
            is_active = self._filter_period == period_key
            ctk.CTkButton(
                filter_frame, text=period_label, width=70, height=30,
                font=ctk.CTkFont(
                    size=12, weight="bold" if is_active else "normal"),
                fg_color=t["primary"] if is_active else t["card"],
                hover_color=t["button_hover"],
                text_color=t["text"] if is_active else t["text_sec"],
                command=lambda k=period_key: self._set_filter(k),
            ).pack(side="left", padx=2)

        # Botões de ação à direita
        ctk.CTkButton(
            filter_frame, text="📤 Exportar CSV", width=120, height=30,
            font=ctk.CTkFont(size=12),
            fg_color=t["card"], hover_color=t["secondary"],
            text_color=t["text_sec"],
            command=self._export_csv,
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            filter_frame, text="🗑️ Limpar", width=90, height=30,
            font=ctk.CTkFont(size=12),
            fg_color=t["card"], hover_color=t["danger"],
            text_color=t["danger"],
            command=self._confirm_clear,
        ).pack(side="right", padx=(5, 0))

        # ── Gráfico de atividade semanal (melhoria 4) ────────
        self._draw_activity_chart(t, uid)

        # ── Progresso de Teoria (melhoria 1) ─────────────────
        self._draw_theory_progress(t, uid, theory_stats)

        # ── Desempenho ENEM Real (melhoria 3) ────────────────
        self._draw_enem_stats(t, uid)

        # ── Progresso por matéria ────────────────────────────
        self._draw_study_stats(t, uid)

        # ── Flashcards ───────────────────────────────────────
        self._draw_flashcard_stats(t, uid)

        # ── Sessões recentes ─────────────────────────────────
        self._draw_sessions(t, uid)

    # ══════════════════════════════════════════════════════════
    # ── GRÁFICO DE ATIVIDADE (melhoria 4) ────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_activity_chart(self, t, uid):
        self._section_title(
            self.scroll, "📊 Atividade dos Últimos 7 Dias", t, pady=(10, 8))

        chart_card = ctk.CTkFrame(
            self.scroll, corner_radius=12, fg_color=t["card"])
        chart_card.pack(fill="x", pady=(0, 5))
        chart_inner = ctk.CTkFrame(chart_card, fg_color="transparent")
        chart_inner.pack(fill="x", padx=20, pady=15)

        # Calcular sessões dos últimos 7 dias
        sessions = self.db.get_sessions(uid, limit=200)
        today = datetime.now().date()
        day_names = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        counts = {}
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            counts[d.isoformat()] = 0

        for s in sessions:
            completed = s.get("completed_at", "")
            if completed:
                date_str = completed[:10]
                if date_str in counts:
                    counts[date_str] += 1

        max_count = max(counts.values()) if counts.values() else 1
        if max_count == 0:
            max_count = 1

        # Desenhar barras simples com frames
        bars_frame = ctk.CTkFrame(
            chart_inner, fg_color="transparent", height=120)
        bars_frame.pack(fill="x")
        bars_frame.pack_propagate(False)

        for i in range(7):
            bars_frame.grid_columnconfigure(i, weight=1)

        for i, (date_key, count) in enumerate(counts.items()):
            d = datetime.fromisoformat(date_key).date()
            day_label = day_names[d.weekday()]
            is_today = d == today

            col_frame = ctk.CTkFrame(bars_frame, fg_color="transparent")
            col_frame.grid(row=0, column=i, sticky="nsew", padx=3)
            col_frame.grid_rowconfigure(0, weight=1)

            # Contagem
            ctk.CTkLabel(col_frame, text=str(count),
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=t["primary"] if count > 0 else t["text_sec"],
                         ).pack(side="top", pady=(0, 2))

            # Barra
            bar_height = max(int(70 * count / max_count), 4)
            bar_color = t["primary"] if count > 0 else t["secondary"]
            if is_today and count > 0:
                bar_color = t["success"]

            bar = ctk.CTkFrame(col_frame, fg_color=bar_color,
                               corner_radius=4, height=bar_height, width=30)
            bar.pack(side="bottom", pady=(0, 0))
            bar.pack_propagate(False)

            # Label do dia
            ctk.CTkLabel(col_frame, text=day_label,
                         font=ctk.CTkFont(
                             size=10, weight="bold" if is_today else "normal"),
                         text_color=t["success"] if is_today else t["text_sec"],
                         ).pack(side="bottom", pady=(2, 0))

    # ══════════════════════════════════════════════════════════
    # ── PROGRESSO DE TEORIA (melhoria 1) ─────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_theory_progress(self, t, uid, theory_stats):
        if not theory_stats:
            return

        self._section_title(self.scroll, "📖 Progresso de Teoria", t)

        # Importar dados do syllabus para saber totais por área
        try:
            from enem_syllabus import ENEM_SYLLABUS
        except ImportError:
            return

        for area_key, area_data in ENEM_SYLLABUS.items():
            total_topics = len(area_data.get("topics", []))
            stat = theory_stats.get(area_key, {"read": 0, "completed": 0})
            completed = stat.get("completed", 0)
            pct = int(completed / total_topics *
                      100) if total_topics > 0 else 0

            card = ctk.CTkFrame(
                self.scroll, corner_radius=10, fg_color=t["card"])
            card.pack(fill="x", pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            inner.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(inner,
                         text=f"{area_data['emoji']} {area_key}",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=t["text"]).grid(row=0, column=0, sticky="w")

            ctk.CTkLabel(inner,
                         text=f"{completed}/{total_topics} tópicos ({pct}%)",
                         font=ctk.CTkFont(size=12),
                         text_color=t["success"] if pct == 100 else t["text_sec"],
                         ).grid(row=1, column=0, sticky="w")

            bar = ctk.CTkProgressBar(inner, width=140, height=10)
            bar.set(pct / 100)
            bar.configure(
                progress_color=t["success"] if pct >= 70 else t["warning"] if pct >= 30 else t["danger"])
            bar.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))

    # ══════════════════════════════════════════════════════════
    # ── STATS ENEM REAL (melhoria 3) ─────────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_enem_stats(self, t, uid):
        enem_stats = self.db.get_enem_quiz_stats_by_year(uid)
        if not enem_stats:
            return

        self._section_title(self.scroll, "🎯 Desempenho ENEM Real", t)

        for s in enem_stats:
            disc_name = s.get("discipline") or "Todas"
            avg = s.get("avg_score") or 0
            best = s.get("best_score") or 0
            correct = s.get("total_correct") or 0
            total_q = s.get("total_q") or 0

            card = ctk.CTkFrame(
                self.scroll, corner_radius=10, fg_color=t["card"])
            card.pack(fill="x", pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            inner.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(inner,
                         text=f"📋 ENEM {s['year']} — {disc_name}",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=t["text"]).grid(row=0, column=0, sticky="w")

            info = (f"Tentativas: {s.get('attempts', 0)}  |  "
                    f"Acertos: {correct}/{total_q}  |  "
                    f"Média: {avg:.0f}%  |  Melhor: {best:.0f}%")
            ctk.CTkLabel(inner, text=info,
                         font=ctk.CTkFont(size=12),
                         text_color=t["text_sec"]).grid(row=1, column=0, sticky="w")

            bar = ctk.CTkProgressBar(inner, width=120, height=10)
            bar.set(avg / 100 if avg else 0)
            bar.configure(
                progress_color=t["success"] if avg >= 70 else t["warning"] if avg >= 50 else t["danger"])
            bar.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))

    # ══════════════════════════════════════════════════════════
    # ── PROGRESSO POR MATÉRIA ────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_study_stats(self, t, uid):
        study_stats = self.db.get_study_stats(uid)
        if not study_stats:
            return

        self._section_title(self.scroll, "📚 Desempenho por Matéria", t)

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
            bar.configure(
                progress_color=t["success"] if avg >= 70 else t["warning"] if avg >= 50 else t["danger"])
            bar.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))

    # ══════════════════════════════════════════════════════════
    # ── FLASHCARDS ───────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_flashcard_stats(self, t, uid):
        fc_stats = self.db.get_flashcard_stats(uid)
        if not fc_stats or fc_stats.get("total", 0) == 0:
            return

        self._section_title(self.scroll, "🃏 Flashcards", t)

        card = ctk.CTkFrame(self.scroll, corner_radius=10, fg_color=t["card"])
        card.pack(fill="x", pady=3)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)

        total = fc_stats.get("total", 0)
        reviewed = fc_stats.get("reviewed", 0)
        due = fc_stats.get("due", 0)

        ctk.CTkLabel(inner,
                     text=f"🃏 {total} flashcards  •  ✅ {reviewed} revisados  •  📋 {due} pendentes",
                     font=ctk.CTkFont(size=14),
                     text_color=t["text"]).pack(side="left")

        if total > 0:
            pct = int(reviewed / total * 100)
            bar = ctk.CTkProgressBar(inner, width=120, height=10)
            bar.set(pct / 100)
            bar.configure(progress_color=t["success"]
                          if pct >= 70 else t["warning"])
            bar.pack(side="right", padx=(15, 0))

    # ══════════════════════════════════════════════════════════
    # ── SESSÕES RECENTES ─────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _draw_sessions(self, t, uid):
        sessions = self.db.get_sessions(uid, limit=100)
        min_date = self._filter_date()

        # Filtrar por período
        if min_date:
            sessions = [s for s in sessions
                        if (s.get("completed_at") or "") >= min_date]

        self._section_title(
            self.scroll, f"🕐 Sessões Recentes ({len(sessions)})", t)

        if not sessions:
            ctk.CTkLabel(
                self.scroll,
                text="Nenhuma sessão registrada neste período.\nInicie um Pomodoro para começar!",
                font=ctk.CTkFont(size=14), text_color=t["text_sec"],
            ).pack(pady=20)
            return

        types = {"foco": "🍅 Foco", "pausa_curta": "☕ Pausa Curta",
                 "pausa_longa": "🌿 Pausa Longa"}

        for s in sessions[:30]:  # Limitar exibição a 30
            card = ctk.CTkFrame(self.scroll, corner_radius=8,
                                fg_color=t["card"], height=50)
            card.pack(fill="x", pady=2)
            card.pack_propagate(False)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=8)

            stype = types.get(s["session_type"], s["session_type"])
            task_info = f"  •  📋 {s['task_title']}" if s.get(
                "task_title") else ""

            ctk.CTkLabel(inner, text=f"{stype}  •  {s['duration']} min{task_info}",
                         font=ctk.CTkFont(size=13),
                         text_color=t["text"]).pack(side="left")

            date_str = (s.get("completed_at") or "")[:16].replace("T", " ")
            ctk.CTkLabel(inner, text=date_str,
                         font=ctk.CTkFont(size=11),
                         text_color=t["text_sec"]).pack(side="right")

    # ══════════════════════════════════════════════════════════
    # ── FILTRO DE PERÍODO (melhoria 2) ───────────────────────
    # ══════════════════════════════════════════════════════════
    def _set_filter(self, period):
        self._filter_period = period
        self._load()

    # ══════════════════════════════════════════════════════════
    # ── EXPORTAR CSV (melhoria 7) ────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _export_csv(self):
        uid = self.app.get_user_id()

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exportar Histórico",
            initialfile=f"switch_focus_historico_{datetime.now().strftime('%Y%m%d')}.csv",
        )
        if not filepath:
            return

        try:
            sessions = self.db.get_sessions(uid, limit=9999)
            study_stats = self.db.get_study_stats(uid)
            xp_info = self.db.get_xp_info(uid)
            streak_info = self.db.get_streak(uid)

            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)

                # Resumo geral
                writer.writerow(["=== RESUMO GERAL ==="])
                writer.writerow(["XP Total", xp_info.get("xp", 0)])
                writer.writerow(["Nível", xp_info.get("level", 1)])
                writer.writerow(["Streak Atual", streak_info.get("streak", 0)])
                writer.writerow(
                    ["Maior Streak", streak_info.get("longest", 0)])
                writer.writerow([])

                # Sessões Pomodoro
                writer.writerow(["=== SESSÕES POMODORO ==="])
                writer.writerow(["Tipo", "Duração (min)", "Tarefa", "Data"])
                for s in sessions:
                    writer.writerow([
                        s.get("session_type", ""),
                        s.get("duration", 0),
                        s.get("task_title", ""),
                        s.get("completed_at", ""),
                    ])
                writer.writerow([])

                # Desempenho por matéria
                if study_stats:
                    writer.writerow(["=== DESEMPENHO POR MATÉRIA ==="])
                    writer.writerow(
                        ["Matéria", "Sessões", "Acertos", "Total Questões", "Média (%)"])
                    for ss in study_stats:
                        writer.writerow([
                            ss.get("subject", ""),
                            ss.get("sessions", 0),
                            ss.get("total_correct", 0),
                            ss.get("total_q", 0),
                            f"{ss.get('avg_score', 0):.1f}",
                        ])

            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(
                title="Exportação Concluída ✅",
                message=f"Histórico exportado com sucesso!\n📁 {os.path.basename(filepath)}",
                icon="check",
            )
        except Exception as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(
                title="Erro", message=f"Erro ao exportar: {e}", icon="cancel")

    # ══════════════════════════════════════════════════════════
    # ── LIMPAR HISTÓRICO (melhoria 10) ───────────────────────
    # ══════════════════════════════════════════════════════════
    def _confirm_clear(self):
        from CTkMessagebox import CTkMessagebox
        msg = CTkMessagebox(
            title="Limpar Histórico",
            message="⚠️ Tem certeza que deseja limpar todo o histórico de sessões Pomodoro?\n\n"
                    "Isso apagará as sessões registradas.\n"
                    "XP, nível, conquistas e progresso de estudo NÃO serão afetados.",
            icon="warning",
            option_1="Cancelar",
            option_2="Limpar",
        )
        if msg.get() == "Limpar":
            self._clear_sessions()

    def _clear_sessions(self):
        """Limpa sessões Pomodoro do usuário."""
        uid = self.app.get_user_id()
        if not uid:
            return
        try:
            self.db.clear_pomodoro_sessions(uid)

            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(
                title="Concluído ✅",
                message="Histórico de sessões limpo com sucesso!",
                icon="check",
            )
            self._load()
        except Exception as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title="Erro", message=f"Erro: {e}", icon="cancel")

    # ══════════════════════════════════════════════════════════
    # ── EVENTOS ──────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def on_show(self):
        self._load()

    def apply_theme(self, t):
        self.configure(fg_color=t["bg"])
        self.title_lb.configure(text_color=t["primary"])
        self.subtitle_lb.configure(text_color=t["text_sec"])
        self.scroll.configure(fg_color=t["bg"])
        # Recarregar conteúdo com novas cores
        self._load()
