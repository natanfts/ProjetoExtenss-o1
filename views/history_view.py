import flet as ft
from datetime import datetime, timedelta


class HistoryView:
    """Histórico — Estatísticas de estudo e sessões."""

    def __init__(self, app):
        self.app = app
        self.db = app.db

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()
        uid = self.app.get_user_id()

        if not uid:
            return ft.Container(
                expand=True, bgcolor=t["bg"],
                alignment=ft.Alignment.CENTER,
                content=ft.Column([
                    ft.Text("📊", size=48),
                    ft.Text("Faça login para ver seu histórico",
                            size=16, color=t["text_sec"]),
                    ft.ElevatedButton("🔑 Entrar", bgcolor=t["button"], color="#FFF",
                                      on_click=lambda _: self.app.show_view("login")),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            )

        # ── Estatísticas gerais ──────────────────────────────
        stats = self.db.get_session_stats(uid) or {}
        xp_info = self.db.get_xp_info(uid) or {"level": 1}
        streak = self.db.get_streak(uid) or {"streak": 0, "longest": 0}

        stat_cards = []
        stat_data = [
            ("🍅", "Pomodoros", str(stats.get("focus_count", 0))),
            ("⏱️", "Min. Foco", str(stats.get("focus_minutes", 0))),
            ("📅", "Dias Ativos", str(stats.get("days_active", 0))),
            ("⭐", "Nível", str(xp_info.get("level", 1))),
        ]
        for emoji, label, value in stat_data:
            stat_cards.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=12, expand=True,
                    padding=ft.padding.symmetric(vertical=12, horizontal=8),
                    content=ft.Column([
                        ft.Text(f"{emoji} {value}", size=20,
                                weight=ft.FontWeight.BOLD, color=t["primary"]),
                        ft.Text(label, size=10, color=t["text_sec"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                )
            )

        # ── Progresso por matéria ────────────────────────────
        study_stats = self.db.get_study_stats(uid)
        study_rows = []
        for s in study_stats:
            avg = s.get("avg_score", 0) or 0
            study_rows.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=10, padding=12,
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"📖 {s['subject']}", size=14,
                                    weight=ft.FontWeight.BOLD, color=t["text"]),
                            ft.Text(f"{s['sessions']} sessões  •  {s.get('total_correct', 0)}/{s.get('total_q', 0)} acertos",
                                    size=12, color=t["text_sec"]),
                        ], spacing=2, expand=True),
                        ft.Text(f"{avg:.0f}%", size=16, weight=ft.FontWeight.BOLD,
                                color=t["success"] if avg >= 70 else t["warning"]),
                    ]),
                )
            )

        # ── Sessões recentes ─────────────────────────────────
        sessions = self.db.get_sessions(uid, limit=20)
        session_tiles = []
        for s in sessions:
            stype_labels = {
                "foco": "🍅 Foco", "pausa_curta": "☕ Pausa", "pausa_longa": "🌿 Pausa Longa"}
            stype = stype_labels.get(
                s.get("session_type", ""), s.get("session_type", ""))
            completed = s.get("completed_at", "")
            time_str = ""
            if completed:
                try:
                    dt = datetime.fromisoformat(completed)
                    time_str = dt.strftime("%d/%m %H:%M")
                except (ValueError, TypeError):
                    time_str = completed[:16]

            task_title = s.get("task_title", "")
            task_text = f" — {task_title}" if task_title else ""

            session_tiles.append(
                ft.Container(
                    bgcolor=t["card"], border_radius=8, padding=10,
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"{stype}{task_text}",
                                    size=13, color=t["text"]),
                            ft.Text(f"{s.get('duration', 0)} min  •  {time_str}",
                                    size=11, color=t["text_sec"]),
                        ], spacing=2, expand=True),
                    ]),
                )
            )

        # ── Exportar CSV ─────────────────────────────────────
        export_btn = ft.ElevatedButton(
            content=ft.Text("📥 Exportar CSV"), height=40,
            bgcolor=t["card"], color=t["text"],
            on_click=lambda _: self._export_csv(uid),
        )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row(stat_cards, spacing=6),
                ft.Text("📊 Desempenho por Matéria", size=18,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                *(study_rows if study_rows else [
                    ft.Text("Nenhum quiz realizado ainda.",
                            size=14, color=t["text_sec"])
                ]),
                ft.Text("🕐 Sessões Recentes", size=18,
                        weight=ft.FontWeight.BOLD, color=t["primary"]),
                *(session_tiles if session_tiles else [
                    ft.Text("Nenhuma sessão registrada.",
                            size=14, color=t["text_sec"])
                ]),
                ft.Container(height=5),
                export_btn,
                ft.Container(height=10),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
        )

    def _export_csv(self, uid):
        try:
            sessions = self.db.get_sessions(uid, limit=500)
            import csv
            import os
            path = os.path.join(os.path.expanduser("~"),
                                "switch_focus_export.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Tipo", "Duração (min)", "Tarefa", "Data"])
                for s in sessions:
                    writer.writerow([
                        s.get("session_type", ""),
                        s.get("duration", 0),
                        s.get("task_title", ""),
                        s.get("completed_at", ""),
                    ])
            self.app.show_snackbar(f"✅ Exportado: {path}")
        except Exception as e:
            self.app.show_snackbar(
                f"❌ Erro ao exportar: {e}", bgcolor="#F44336")
