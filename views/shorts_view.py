import flet as ft


class ShortsView:
    """Vídeos educativos — listagem por matéria."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._category = "enem"

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()

        # Tabs de categoria
        cat_btns = []
        for label, key in [("📚 ENEM", "enem"), ("📋 Concursos", "concursos")]:
            is_active = self._category == key
            cat_btns.append(
                ft.ElevatedButton(
                    content=ft.Text(label), height=38, expand=True,
                    bgcolor=t["primary"] if is_active else t["card"],
                    color="#FFFFFF" if is_active else t["text_sec"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _, c=key: self._set_category(c),
                )
            )

        # Matérias com vídeos
        subjects = self.db.get_subjects(self._category, "video")
        subject_sections = []

        for subj in subjects:
            videos = self.db.get_videos(self._category, subj)
            if not videos:
                continue

            video_cards = []
            for v in videos[:6]:  # Máx 6 por matéria
                video_cards.append(
                    ft.Container(
                        bgcolor=t["card"], border_radius=12, padding=12, width=280,
                        on_click=lambda _, url=v.get(
                            "video_url", ""): self._open_video(url),
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.PLAY_CIRCLE,
                                        color=t["primary"], size=36),
                                ft.Column([
                                    ft.Text(
                                        v.get("video_title", "Vídeo")[:50],
                                        size=13, weight=ft.FontWeight.BOLD, color=t["text"],
                                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Text(
                                        v.get("video_channel", ""),
                                        size=11, color=t["text_sec"],
                                    ),
                                ], spacing=2, expand=True),
                            ]),
                            ft.Text(v.get("topic", ""), size=10,
                                    color=t["text_sec"]),
                        ], spacing=6),
                    )
                )

            subject_sections.append(
                ft.Column([
                    ft.Text(f"📖 {subj}", size=16,
                            weight=ft.FontWeight.BOLD, color=t["primary"]),
                    ft.Row(video_cards, scroll=ft.ScrollMode.AUTO, spacing=8),
                ], spacing=6)
            )

        if not subject_sections:
            subject_sections.append(
                ft.Container(
                    alignment=ft.Alignment.CENTER, padding=40,
                    content=ft.Column([
                        ft.Text("📱", size=48),
                        ft.Text("Nenhum vídeo disponível ainda.",
                                size=16, color=t["text_sec"]),
                        ft.Text("Os vídeos são atualizados automaticamente.",
                                size=13, color=t["text_sec"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                )
            )

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            content=ft.Column([
                ft.Row(cat_btns, spacing=8),
                *subject_sections,
            ], spacing=12, scroll=ft.ScrollMode.AUTO),
        )

    def _set_category(self, cat):
        self._category = cat
        self.app.show_view("shorts")

    def _open_video(self, url):
        if url:
            import webbrowser
            webbrowser.open(url)
