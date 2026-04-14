import flet as ft
import logging
import re

logger = logging.getLogger("ShortsView")

# WebView disponível em iOS, Android, macOS e Web
try:
    import flet_webview as fwv
    _HAS_WEBVIEW = True
except ImportError:
    _HAS_WEBVIEW = False

_YT_ID_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([a-zA-Z0-9_-]{11})"
)


def _extract_video_id(url: str) -> str | None:
    m = _YT_ID_RE.search(url)
    return m.group(1) if m else None


class ShortsView:
    """Vídeos educativos — listagem por matéria."""

    def __init__(self, app):
        self.app = app
        self.db = app.db
        self._category = "enem"
        self._playing_url = None  # URL do vídeo em reprodução (modo embutido)

    def on_show(self):
        pass

    def build(self):
        t = self.app.theme_mgr.get_theme()

        # Se há vídeo em reprodução (modo embutido), mostra o player
        if self._playing_url and self._can_embed():
            return self._build_player(t)

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
        self._playing_url = None
        self.app.show_view("shorts")

    def _can_embed(self) -> bool:
        """Verifica se WebView está disponível na plataforma atual."""
        if not _HAS_WEBVIEW:
            return False
        # WebView não funciona no Windows/Linux desktop
        platform = self.app.page.platform
        if platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX):
            return False
        return True

    def _open_video(self, url):
        if not url:
            return
        if self._can_embed() and _extract_video_id(url):
            self._playing_url = url
            self.app.show_view("shorts")
        else:
            import webbrowser
            webbrowser.open(url)

    def _close_player(self, e=None):
        self._playing_url = None
        self.app.show_view("shorts")

    def _build_player(self, t):
        """Constrói o player embutido com WebView do YouTube."""
        video_id = _extract_video_id(self._playing_url)
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"

        return ft.Container(
            expand=True, bgcolor=t["bg"],
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=t["text"],
                        on_click=self._close_player,
                    ),
                    ft.Text("📱 Player", size=18,
                            weight=ft.FontWeight.BOLD, color=t["text"],
                            expand=True),
                    ft.IconButton(
                        icon=ft.Icons.OPEN_IN_BROWSER,
                        icon_color=t["text_sec"],
                        tooltip="Abrir no navegador",
                        on_click=lambda _: __import__('webbrowser').open(
                            self._playing_url),
                    ),
                ]),
                ft.Container(
                    expand=True,
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=fwv.WebView(
                        url=embed_url,
                        expand=True,
                    ),
                ),
            ], spacing=8),
        )
