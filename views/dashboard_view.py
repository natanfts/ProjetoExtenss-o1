import flet as ft
from datetime import datetime, timedelta


class DashboardView:
    """Dashboard — resumo do dia, XP, streak, metas e conquistas."""

    def __init__(self, app):
        self.app = app
        self.db = app.db

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        if not uid:
            return self._build_guest(t)

        # Atualizar streak
        self.db.update_streak(uid)

        # ── Saudação ─────────────────────────────────────────
        hour = datetime.now().hour
        greeting = "Bom dia" if hour < 12 else (
            "Boa tarde" if hour < 18 else "Boa noite")
        name = self.app.current_user.get("display_name", "Estudante")
        greeting_template = t.get("greeting", "👋 {saudacao}, {nome}!")
        greeting_text = greeting_template.format(saudacao=greeting, nome=name)

        # ── XP / Nível ───────────────────────────────────────
        xp_info = self.db.get_xp_info(
            uid) or {"xp": 0, "level": 1, "progress": 0.0, "xp_next_level": 120}
        streak_info = self.db.get_streak(uid) or {"streak": 0, "longest": 0}
        level_prefix = t.get("level_prefix", "Nível")
        xp_name = t.get("xp_name", "XP")
        streak_msg = t.get("streak_msg", "🔥 {dias} dias seguidos!").format(
            dias=streak_info.get("streak", 0))

        xp_card = ft.Container(
            bgcolor=t["card"], border_radius=14, padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text(f"⭐ {level_prefix} {xp_info.get('level', 1)}",
                            size=20, weight=ft.FontWeight.BOLD, color=t["accent"]),
                    ft.Text(streak_msg, size=14, weight=ft.FontWeight.BOLD,
                            color=t["danger"] if streak_info.get("streak", 0) >= 7 else t["warning"]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(
                    value=xp_info.get("progress", 0.0), height=12,
                    color=t["accent"], bgcolor=t["secondary"],
                    border_radius=6,
                ),
                ft.Text(
                    f"{xp_info.get('xp', 0)} / {xp_info.get('xp_next_level', 120)} {xp_name}  •  Recorde: {streak_info.get('longest', 0)} dias",
                    size=11, color=t["text_sec"],
                ),
            ], spacing=8),
        )

        # ── Metas do Dia ─────────────────────────────────────
        goals_summary = self.db.get_daily_goals_summary(uid)
        goals = goals_summary["goals"]
        today_stats = self.db.get_today_stats(uid)

        goal_configs = {
            "pomodoro": ("🍅", "Pomodoros", today_stats["pomodoros"]),
            "xp":       ("⚡", "XP Ganho", today_stats["xp_today"]),
            "quiz":     ("📝", "Questões", today_stats["questions"]),
        }

        goal_cards = []
        for goal in goals:
            gtype = goal["goal_type"]
            config = goal_configs.get(
                gtype, ("📌", gtype, goal["current_value"]))
            emoji, label, current = config
            current = max(current, goal["current_value"])
            target = goal["target_value"]
            done = current >= target
            pct = min(current / target, 1.0) if target > 0 else 0

            goal_cards.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, padding=15,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{emoji} {label}", size=14, weight=ft.FontWeight.BOLD,
                                    color=t["success"] if done else t["text"]),
                            ft.Text(f"{'✅ ' if done else ''}{current}/{target}",
                                    size=13, weight=ft.FontWeight.BOLD,
                                    color=t["success"] if done else t["text_sec"]),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(
                            value=pct, height=8, border_radius=4,
                            color=t["success"] if done else t["accent"],
                            bgcolor=t["secondary"],
                        ),
                    ], spacing=6),
                )
            )

        celebration_row = []
        if goals_summary["all_done"]:
            celebration = t.get(
                "celebration", "Parabéns! Todas as metas cumpridas!")
            celebration_row.append(
                ft.Text(f"🎉 {celebration}", size=14,
                        weight=ft.FontWeight.BOLD, color=t["success"])
            )

        # ── Estatísticas de Hoje ─────────────────────────────
        stat_items = [
            ("🍅", "Pomodoros", str(today_stats["pomodoros"])),
            ("⏱️", "Min. Foco", str(today_stats["focus_min"])),
            ("📝", "Questões", str(today_stats["questions"])),
            ("⚡", "XP Ganho", str(today_stats["xp_today"])),
        ]

        stat_cards = []
        for emoji, label, value in stat_items:
            stat_cards.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12,
                    padding=ft.padding.symmetric(vertical=15, horizontal=10),
                    expand=True,
                    content=ft.Column([
                        ft.Text(f"{emoji} {value}", size=22,
                                weight=ft.FontWeight.BOLD, color=t["primary"]),
                        ft.Text(label, size=11, color=t["text_sec"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                )
            )

        # ── Conquistas Recentes ──────────────────────────────
        new_achs = self.db.check_and_grant_achievements(uid)
        earned = self.db.get_user_achievements(uid)
        all_achs = self.db.get_all_achievements()
        earned_keys = {a["key"] for a in earned}

        ach_badges = []
        for ach in all_achs[:12]:  # Mostrar até 12
            is_earned = ach["key"] in earned_keys
            ach_badges.append(
                ft.Container(
                    bgcolor=t["card"] if is_earned else t["secondary"],
                    border_radius=10, width=70, height=70,
                    border=ft.border.all(
                        2, t["success"]) if is_earned else None,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column([
                        ft.Text(ach["emoji"] if is_earned else "🔒", size=22),
                        ft.Text(ach["title"][:8] if is_earned else "???",
                                size=8, color=t["text"] if is_earned else t["text_sec"],
                                text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                )
            )

        new_ach_cards = []
        for ach in new_achs:
            ach_msg = t.get("new_achievement",
                            "🎉 NOVA CONQUISTA: {emoji} {title}")
            new_ach_cards.append(
                ft.Container(
                    bgcolor=t["accent"], border_radius=12, padding=12,
                    content=ft.Column([
                        ft.Text(ach_msg.format(emoji=ach["emoji"], title=ach["title"]),
                                size=14, weight=ft.FontWeight.BOLD, color=t["bg"]),
                        ft.Text(f"{ach['description']}  (+{ach['xp_reward']} XP)",
                                size=12, color=t["bg"]),
                    ]),
                )
            )

        # ── Atividade Semanal ────────────────────────────────
        sessions = self.db.get_sessions(uid, limit=200)
        today_date = datetime.now().date()
        day_names = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        counts = {}
        for i in range(6, -1, -1):
            d = today_date - timedelta(days=i)
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

        week_bars = []
        for date_key, count in counts.items():
            d = datetime.fromisoformat(date_key).date()
            day_label = day_names[d.weekday()]
            is_today = d == today_date
            bar_height = max(int(40 * count / max_count), 4)
            bar_color = t["success"] if is_today and count > 0 else t["primary"] if count > 0 else t["secondary"]

            week_bars.append(
                ft.Column([
                    ft.Text(str(count), size=10, weight=ft.FontWeight.BOLD,
                            color=t["primary"] if count > 0 else t["text_sec"]),
                    ft.Container(width=24, height=bar_height,
                                 bgcolor=bar_color, border_radius=3),
                    ft.Text(day_label, size=9,
                            weight=ft.FontWeight.BOLD if is_today else ft.FontWeight.NORMAL,
                            color=t["success"] if is_today else t["text_sec"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
            )

        # ── Ações Rápidas ────────────────────────────────────
        actions = [
            ("🍅 Pomodoro", "pomodoro"),
            ("📝 Quiz", "study"),
            ("🃏 Cards", "flashcards"),
            ("📋 Tarefas", "tasks"),
        ]
        action_btns = []
        for text, target in actions:
            action_btns.append(
                ft.ElevatedButton(
                    content=ft.Text(text), height=42, expand=True,
                    bgcolor=t["button"], color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _, f=target: self.app.show_view(f),
                )
            )

        # ── Layout completo ──────────────────────────────────
        return ft.Container(
            expand=True, bgcolor=t["bg"],
            content=ft.Column(
                controls=[
                    # Saudação
                    ft.Text(greeting_text, size=20,
                            weight=ft.FontWeight.BOLD, color=t["text"]),
                    ft.Text(datetime.now().strftime("%A, %d de %B de %Y").capitalize(),
                            size=12, color=t["text_sec"]),
                    # XP
                    xp_card,
                    # Metas
                    ft.Text("🎯 Metas de Hoje", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    *goal_cards,
                    *celebration_row,
                    # Stats
                    ft.Text("📊 Resumo de Hoje", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    ft.Row(stat_cards, spacing=6),
                    # Conquistas
                    *new_ach_cards,
                    ft.Text(f"🏆 Conquistas ({len(earned)}/{len(all_achs)})",
                            size=18, weight=ft.FontWeight.BOLD, color=t["primary"]),
                    ft.Row(ach_badges, wrap=True, spacing=6, run_spacing=6),
                    # Atividade semanal
                    ft.Text("📈 Atividade Semanal", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    ft.Container(
                        bgcolor=t["card"], border_radius=12, padding=15,
                        content=ft.Row(
                            week_bars, alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ),
                    # Ações rápidas
                    ft.Text("⚡ Ações Rápidas", size=18,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    ft.Row(action_btns, spacing=6),
                    ft.Container(height=10),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        )

    def _build_guest(self, t):
        welcome_msg = t.get("welcome", "👋 Bem-vindo ao Switch Focus!")
        return ft.Container(
            expand=True, bgcolor=t["bg"],
            alignment=ft.Alignment.CENTER,
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Text(welcome_msg, size=22, weight=ft.FontWeight.BOLD, color=t["primary"],
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.Text(
                        "Faça login ou cadastre-se para desbloquear:\n\n"
                        "⭐ Sistema de XP e Níveis\n"
                        "🔥 Streak de dias consecutivos\n"
                        "🏆 Conquistas e badges\n"
                        "🎯 Metas diárias personalizáveis\n"
                        "🃏 Flashcards com repetição espaçada\n"
                        "📊 Dashboard completo",
                        size=14, color=t["text_sec"],
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        content=ft.Text("🔑 Entrar / Cadastrar"),
                        width=250, height=45,
                        bgcolor=t["button"], color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=lambda _: self.app.show_view("login"),
                    ),
                    ft.TextButton(
                        content=ft.Text("Continuar como convidado →"),
                        on_click=lambda _: self.app.show_view("pomodoro"),
                        style=ft.ButtonStyle(color=t["text_sec"]),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
