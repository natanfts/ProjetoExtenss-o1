"""
ShortsView — Feed estilo TikTok com vídeos educativos curtos do YouTube.

Navega verticalmente entre vídeos curtos sobre tópicos do ENEM,
com thumbnails grandes, informações do vídeo e abertura no navegador.
"""

import customtkinter as ctk
import threading
import webbrowser
import random
import io
import urllib.request
from PIL import Image

from youtubesearchpython import VideosSearch
from api_service import APIService


# ── Tópicos de busca organizados por área ENEM ──────────────
SHORTS_TOPICS = {
    "🔤 Linguagens": [
        "interpretação de texto ENEM shorts",
        "gramática dica rápida ENEM",
        "literatura brasileira resumo rápido",
        "figuras de linguagem ENEM shorts",
        "variação linguística resumo",
        "funções da linguagem resumo rápido",
        "redação ENEM dica rápida",
        "gêneros textuais resumo ENEM",
        "intertextualidade ENEM shorts",
        "movimentos literários resumo",
    ],
    "📐 Matemática": [
        "matemática ENEM dica rápida shorts",
        "porcentagem truque rápido ENEM",
        "geometria dica ENEM shorts",
        "probabilidade resumo rápido ENEM",
        "função primeiro grau resumo",
        "equação segundo grau dica rápida",
        "regra de três ENEM shorts",
        "trigonometria resumo rápido ENEM",
        "análise combinatória dica ENEM",
        "logaritmo resumo rápido",
        "progressão aritmética geométrica shorts",
        "estatística média moda mediana resumo",
    ],
    "🔬 Ciências da Natureza": [
        "física ENEM dica rápida shorts",
        "cinemática resumo rápido ENEM",
        "leis de Newton resumo shorts",
        "termodinâmica dica rápida",
        "óptica física resumo ENEM",
        "eletricidade circuitos resumo shorts",
        "ondulatória resumo rápido ENEM",
        "química ENEM dica rápida shorts",
        "tabela periódica resumo rápido",
        "estequiometria dica ENEM shorts",
        "ligações químicas resumo rápido",
        "química orgânica resumo shorts",
        "biologia ENEM dica rápida shorts",
        "ecologia resumo rápido ENEM",
        "genética resumo shorts ENEM",
        "citologia célula resumo rápido",
        "evolução Darwin resumo shorts",
        "fisiologia humana resumo ENEM",
    ],
    "🏛️ Ciências Humanas": [
        "história ENEM dica rápida shorts",
        "revolução industrial resumo rápido",
        "Brasil Colônia resumo shorts",
        "Era Vargas resumo rápido ENEM",
        "ditadura militar Brasil resumo shorts",
        "guerras mundiais resumo rápido",
        "Guerra Fria resumo shorts ENEM",
        "geografia ENEM dica rápida shorts",
        "globalização resumo rápido",
        "urbanização brasileira resumo shorts",
        "biomas brasileiros resumo rápido",
        "clima do Brasil resumo shorts",
        "filosofia ENEM resumo rápido shorts",
        "sociologia ENEM resumo rápido shorts",
    ],
    "✏️ Redação": [
        "redação ENEM nota 1000 dica rápida",
        "proposta intervenção redação ENEM shorts",
        "conectivos redação ENEM resumo rápido",
        "repertório sociocultural redação ENEM",
        "competências redação ENEM resumo shorts",
        "introdução redação ENEM como fazer",
        "temas redação ENEM previsão shorts",
        "argumentação redação dica rápida",
    ],
}

# Nomes curtos para filtro
AREA_NAMES = list(SHORTS_TOPICS.keys())
ALL_LABEL = "🎯 Todas"


class ShortsView(ctk.CTkFrame):
    """Feed vertical estilo TikTok com vídeos educativos do YouTube."""

    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0)
        self.app = app
        self.api = APIService()

        self._videos: list[dict] = []
        self._current_idx = 0
        self._selected_area = ALL_LABEL
        self._loading = False
        self._loading_more = False
        self._thumbnail_cache: dict[str, ctk.CTkImage] = {}

        # ── Estado de paginação (feed infinito) ─────────────
        self._seen_urls: set[str] = set()          # URLs já exibidas (dedup)
        # Buscas ativas com .next()
        self._search_objects: list[VideosSearch] = []
        self._query_queue: list[str] = []           # Queries ainda não usadas
        # Queries já com search ativo
        self._active_queries: list[str] = []
        self._page_count = 0                        # Páginas carregadas

        self._build()

    # ══════════════════════════════════════════════════════════
    # ── BUILD ────────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        self.header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.header, text="📱 Shorts Educativos",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.header, text="Vídeos curtos estilo TikTok sobre o ENEM",
            font=ctk.CTkFont(size=13),
        ).grid(row=1, column=0, sticky="w", pady=(0, 0))

        # Área de conteúdo principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self._show_feed_layout()

    # ══════════════════════════════════════════════════════════
    # ── LAYOUT DO FEED ───────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_feed_layout(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        # Layout: [filtros à esquerda] [card central grande] [controles à direita]
        container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # ── Painel de filtros (esquerda) ─────────────────────
        filters = ctk.CTkFrame(container, width=160, corner_radius=14,
                               fg_color=t["card"])
        filters.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=5)
        filters.grid_propagate(False)

        ctk.CTkLabel(
            filters, text="📂 Área",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(15, 8))

        # Botão "Todas"
        self._filter_buttons = {}
        all_btn = ctk.CTkButton(
            filters, text=ALL_LABEL, height=34, width=130,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            fg_color=t["primary"] if self._selected_area == ALL_LABEL else "transparent",
            text_color=t["text"],
            hover_color=t["button_hover"],
            command=lambda: self._select_area(ALL_LABEL),
        )
        all_btn.pack(padx=10, pady=2)
        self._filter_buttons[ALL_LABEL] = all_btn

        for area in AREA_NAMES:
            btn = ctk.CTkButton(
                filters, text=area, height=34, width=130,
                font=ctk.CTkFont(size=11),
                corner_radius=8,
                fg_color=t["primary"] if self._selected_area == area else "transparent",
                text_color=t["text"],
                hover_color=t["button_hover"],
                command=lambda a=area: self._select_area(a),
            )
            btn.pack(padx=10, pady=2)
            self._filter_buttons[area] = btn

        # Separador
        ctk.CTkLabel(filters, text="").pack(expand=True)

        # Info
        self._counter_label = ctk.CTkLabel(
            filters, text="",
            font=ctk.CTkFont(size=11),
            text_color=t["text_sec"],
        )
        self._counter_label.pack(pady=(0, 5))

        # Indicador feed infinito
        self._feed_status = ctk.CTkLabel(
            filters, text="♾️ Feed infinito",
            font=ctk.CTkFont(size=10),
            text_color=t["accent"],
        )
        self._feed_status.pack(pady=(0, 5))

        # Botão recarregar
        ctk.CTkButton(
            filters, text="🔄 Novos vídeos", height=32, width=130,
            font=ctk.CTkFont(size=11),
            fg_color=t["accent"], hover_color=t["button_hover"],
            text_color="#000",
            command=self._load_videos,
        ).pack(padx=10, pady=(0, 15))

        # ── Card central (vídeo atual) ───────────────────────
        self._card_frame = ctk.CTkFrame(
            container, corner_radius=18,
            fg_color=t["card"],
        )
        self._card_frame.grid(row=0, column=1, sticky="nswe", pady=5)
        self._card_frame.grid_columnconfigure(0, weight=1)
        self._card_frame.grid_rowconfigure(1, weight=1)

        # ── Controles laterais (direita) ─────────────────────
        controls = ctk.CTkFrame(container, width=60, fg_color="transparent")
        controls.grid(row=0, column=2, sticky="ns", padx=(12, 0), pady=5)

        ctk.CTkLabel(controls, text="").pack(expand=True)

        # Botão subir (anterior)
        self._btn_prev = ctk.CTkButton(
            controls, text="⬆️", width=50, height=50,
            font=ctk.CTkFont(size=22),
            corner_radius=25,
            fg_color=t["card"], hover_color=t["secondary"],
            command=self._prev_video,
        )
        self._btn_prev.pack(pady=5)

        # Contador central
        self._nav_label = ctk.CTkLabel(
            controls, text="0/0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t["accent"],
        )
        self._nav_label.pack(pady=5)

        # Botão descer (próximo)
        self._btn_next = ctk.CTkButton(
            controls, text="⬇️", width=50, height=50,
            font=ctk.CTkFont(size=22),
            corner_radius=25,
            fg_color=t["primary"], hover_color=t["button_hover"],
            command=self._next_video,
        )
        self._btn_next.pack(pady=5)

        # Botão abrir no YouTube
        self._btn_open = ctk.CTkButton(
            controls, text="▶️", width=50, height=50,
            font=ctk.CTkFont(size=22),
            corner_radius=25,
            fg_color=t["accent"], hover_color=t["button_hover"],
            text_color="#000",
            command=self._open_current_video,
        )
        self._btn_open.pack(pady=(15, 5))

        # Botão curtir / salvar (XP)
        self._btn_like = ctk.CTkButton(
            controls, text="⭐", width=50, height=50,
            font=ctk.CTkFont(size=22),
            corner_radius=25,
            fg_color=t["card"], hover_color=t["secondary"],
            command=self._like_video,
        )
        self._btn_like.pack(pady=5)

        ctk.CTkLabel(controls, text="").pack(expand=True)

        # Bind scroll do mouse para navegar (via tk root, pois CTk não permite bind_all)
        self.app.bind("<MouseWheel>", self._on_mousewheel)

        # Carregar vídeos iniciais
        self._show_empty_state()
        self.after(500, self._load_videos)

    # ══════════════════════════════════════════════════════════
    # ── SELEÇÃO DE ÁREA ──────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _select_area(self, area: str):
        self._selected_area = area
        t = self.app.theme_mgr.get_theme()

        # Atualizar visual dos filtros
        for name, btn in self._filter_buttons.items():
            if name == area:
                btn.configure(fg_color=t["primary"])
            else:
                btn.configure(fg_color="transparent")

        self._load_videos()

    # ══════════════════════════════════════════════════════════
    # ── CARREGAR VÍDEOS ──────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _load_videos(self):
        """Carrega feed inicial: usa TODAS as queries da área selecionada."""
        if self._loading:
            return
        self._loading = True
        self._show_loading()

        # Resetar estado
        self._videos.clear()
        self._seen_urls.clear()
        self._search_objects.clear()
        self._active_queries.clear()
        self._current_idx = 0
        self._page_count = 0

        # Pegar TODAS as queries da área (ou de todas as áreas)
        if self._selected_area == ALL_LABEL:
            all_queries = []
            for queries in SHORTS_TOPICS.values():
                all_queries.extend(queries)
            random.shuffle(all_queries)
            self._query_queue = all_queries
        else:
            area_queries = list(SHORTS_TOPICS.get(self._selected_area, []))
            random.shuffle(area_queries)
            self._query_queue = area_queries

        def _fetch():
            try:
                self._fetch_batch(initial=True)
                self.after(0, self._show_current_video)
            except Exception as e:
                self.after(0, lambda: self._show_error(str(e)))
            finally:
                self._loading = False

        threading.Thread(target=_fetch, daemon=True).start()

    def _fetch_batch(self, initial: bool = False):
        """Busca um lote de vídeos do YouTube em tempo real.

        - Na carga inicial: cria buscas para as primeiras queries
        - Em cargas subsequentes: pagina buscas existentes + novas queries
        """
        new_videos = []
        batch_target = 15 if initial else 10  # Quantos novos vídeos queremos
        queries_per_batch = 5 if initial else 3

        # 1) Criar novas buscas a partir da fila de queries
        queries_to_start = min(queries_per_batch, len(self._query_queue))
        for _ in range(queries_to_start):
            query = self._query_queue.pop(0)
            try:
                search = VideosSearch(query, limit=10)
                results = search.result().get("result", [])
                self._search_objects.append(search)
                self._active_queries.append(query)
                new_videos.extend(
                    self._parse_results(results, query)
                )
            except Exception:
                continue

        # 2) Se ainda precisamos de mais, paginar buscas existentes
        if len(new_videos) < batch_target and self._search_objects:
            for i, search in enumerate(list(self._search_objects)):
                if len(new_videos) >= batch_target:
                    break
                try:
                    has_next = search.next()
                    if has_next:
                        results = search.result().get("result", [])
                        query = self._active_queries[i] if i < len(
                            self._active_queries) else ""
                        new_videos.extend(
                            self._parse_results(results, query)
                        )
                    else:
                        # Busca esgotou, remover
                        self._search_objects[i] = None
                except Exception:
                    self._search_objects[i] = None

            # Limpar buscas esgotadas
            pairs = [(s, q) for s, q in zip(self._search_objects,
                                            self._active_queries) if s is not None]
            if pairs:
                self._search_objects, self._active_queries = map(
                    list, zip(*pairs))
            else:
                self._search_objects, self._active_queries = [], []

        # Embaralhar novos e adicionar ao feed
        random.shuffle(new_videos)
        self._videos.extend(new_videos)
        self._page_count += 1

    def _parse_results(self, results: list[dict], query: str) -> list[dict]:
        """Converte resultados do YouTube em formato do feed, com dedup."""
        parsed = []
        for item in results:
            url = item.get("link", "")
            if not url or url in self._seen_urls:
                continue

            duration = item.get("duration", "")
            if not self._is_short_video(duration):
                continue

            self._seen_urls.add(url)
            thumbs = item.get("thumbnails", [])
            parsed.append({
                "url": url,
                "title": item.get("title", ""),
                "channel": item.get("channel", {}).get("name", ""),
                "duration": duration,
                "views": item.get("viewCount", {}).get("short", ""),
                "published": item.get("publishedTime", ""),
                "thumbnail": thumbs[0].get("url", "") if thumbs else "",
                "search_topic": query,
            })
        return parsed

    def _load_more(self):
        """Carrega mais vídeos em background (feed infinito)."""
        if self._loading_more or self._loading:
            return
        # Verificar se ainda tem fonte de dados
        if not self._search_objects and not self._query_queue:
            return
        self._loading_more = True

        def _fetch():
            try:
                self._fetch_batch(initial=False)
                total = len(self._videos)
                self.after(0, lambda: self._update_counter(total))
            except Exception:
                pass
            finally:
                self._loading_more = False

        threading.Thread(target=_fetch, daemon=True).start()

    def _update_counter(self, total: int):
        """Atualiza o contador na UI."""
        try:
            self._counter_label.configure(text=f"📹 {total} vídeos carregados")
            self._nav_label.configure(
                text=f"{self._current_idx + 1}/{total}")
        except Exception:
            pass

    @staticmethod
    def _is_short_video(duration: str) -> bool:
        """Verifica se a duração indica um vídeo curto (< 5 min)."""
        if not duration:
            return True  # Sem duração = provavelmente short
        parts = duration.split(":")
        try:
            if len(parts) == 1:
                return int(parts[0]) <= 300  # segundos
            elif len(parts) == 2:
                minutes = int(parts[0])
                return minutes < 5
            elif len(parts) >= 3:
                return False  # Tem horas
        except ValueError:
            return True
        return True

    # ══════════════════════════════════════════════════════════
    # ── RENDERIZAR VÍDEO ATUAL ───────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_current_video(self):
        for w in self._card_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        if not self._videos:
            self._show_empty_state()
            return

        video = self._videos[self._current_idx]
        total = len(self._videos)

        # Atualizar contador
        self._nav_label.configure(text=f"{self._current_idx + 1}/{total}")
        self._counter_label.configure(text=f"📹 {total} vídeos carregados")

        # ── Thumbnail grande ─────────────────────────────────
        thumb_url = video.get("thumbnail", "")
        thumb_container = ctk.CTkFrame(
            self._card_frame, fg_color=t["secondary"],
            corner_radius=14, height=300,
        )
        thumb_container.grid(row=0, column=0, sticky="ew",
                             padx=15, pady=(15, 8))
        thumb_container.grid_propagate(False)
        thumb_container.grid_columnconfigure(0, weight=1)
        thumb_container.grid_rowconfigure(0, weight=1)

        # Placeholder enquanto carrega
        self._thumb_label = ctk.CTkLabel(
            thumb_container, text="🎬\nCarregando...",
            font=ctk.CTkFont(size=40),
            text_color=t["text_sec"],
        )
        self._thumb_label.grid(row=0, column=0, sticky="nswe")

        # Carregar thumbnail em background
        if thumb_url:
            self._load_thumbnail(thumb_url, self._thumb_label)

        # Botão de play sobre a thumbnail
        play_btn = ctk.CTkButton(
            thumb_container, text="▶️  Assistir",
            width=140, height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=22,
            fg_color=t["danger"], hover_color="#EF5350",
            command=self._open_current_video,
        )
        play_btn.grid(row=0, column=0)  # sobrepõe a thumbnail

        # ── Informações do vídeo ─────────────────────────────
        info_frame = ctk.CTkFrame(self._card_frame, fg_color="transparent")
        info_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=(5, 10))
        info_frame.grid_columnconfigure(0, weight=1)

        # Título
        title = video.get("title", "Sem título")
        if len(title) > 80:
            title = title[:77] + "..."

        ctk.CTkLabel(
            info_frame, text=title,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=t["text"],
            wraplength=450, justify="left",
        ).grid(row=0, column=0, sticky="w", pady=(8, 4))

        # Canal + duração
        channel = video.get("channel", "Canal desconhecido")
        duration = video.get("duration", "")
        views = video.get("views", "")
        published = video.get("published", "")

        meta_parts = [f"📺 {channel}"]
        if duration:
            meta_parts.append(f"⏱️ {duration}")
        if views:
            meta_parts.append(f"👁️ {views}")

        ctk.CTkLabel(
            info_frame, text="  •  ".join(meta_parts),
            font=ctk.CTkFont(size=12),
            text_color=t["text_sec"],
            wraplength=450, justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 4))

        if published:
            ctk.CTkLabel(
                info_frame, text=f"📅 {published}",
                font=ctk.CTkFont(size=11),
                text_color=t["text_sec"],
            ).grid(row=2, column=0, sticky="w", pady=(0, 4))

        # Tag do tópico
        topic_query = video.get("search_topic", "")
        if topic_query:
            tag_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            tag_frame.grid(row=3, column=0, sticky="w", pady=(5, 5))

            ctk.CTkLabel(
                tag_frame,
                text=f"🏷️ {self._area_from_query(topic_query)}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=t["accent"],
                fg_color=t["secondary"],
                corner_radius=8,
                padx=10, pady=3,
            ).pack(side="left", padx=(0, 5))

        # ── Barra inferior com ações ─────────────────────────
        actions = ctk.CTkFrame(self._card_frame, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))

        ctk.CTkButton(
            actions, text="▶️  Assistir no YouTube",
            height=42, width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF0000", hover_color="#CC0000",
            corner_radius=10,
            command=self._open_current_video,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            actions, text="⬇️ Próximo",
            height=42, width=120,
            font=ctk.CTkFont(size=13),
            fg_color=t["primary"], hover_color=t["button_hover"],
            corner_radius=10,
            command=self._next_video,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            actions, text="🔀 Aleatório",
            height=42, width=120,
            font=ctk.CTkFont(size=13),
            fg_color=t["card"], hover_color=t["secondary"],
            corner_radius=10,
            border_width=1, border_color=t["primary"],
            command=self._random_video,
        ).pack(side="left")

    # ══════════════════════════════════════════════════════════
    # ── THUMBNAIL LOADING ────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _load_thumbnail(self, url: str, label: ctk.CTkLabel):
        """Carrega thumbnail do YouTube em background thread."""
        if url in self._thumbnail_cache:
            try:
                label.configure(image=self._thumbnail_cache[url], text="")
            except Exception:
                pass
            return

        def _fetch():
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0"
                })
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = response.read()

                img = Image.open(io.BytesIO(data))

                # Redimensionar para caber no card
                target_w, target_h = 520, 290
                img_ratio = img.width / img.height
                target_ratio = target_w / target_h

                if img_ratio > target_ratio:
                    new_h = target_h
                    new_w = int(new_h * img_ratio)
                else:
                    new_w = target_w
                    new_h = int(new_w / img_ratio)

                img = img.resize((new_w, new_h), Image.LANCZOS)

                # Crop central
                left = (new_w - target_w) // 2
                top = (new_h - target_h) // 2
                img = img.crop((left, top, left + target_w, top + target_h))

                ctk_img = ctk.CTkImage(
                    light_image=img, dark_image=img,
                    size=(target_w, target_h),
                )
                self._thumbnail_cache[url] = ctk_img

                self.after(0, lambda: self._set_thumb(label, ctk_img))

            except Exception:
                pass  # Manter placeholder

        threading.Thread(target=_fetch, daemon=True).start()

    def _set_thumb(self, label, img):
        """Define a thumbnail no label (thread-safe)."""
        try:
            label.configure(image=img, text="")
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════
    # ── NAVEGAÇÃO ────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _next_video(self):
        if not self._videos:
            return
        self._current_idx += 1
        # Se chegou ao fim, voltar ao início
        if self._current_idx >= len(self._videos):
            self._current_idx = 0
        self._show_current_video()

        # Feed infinito: carregar mais ao se aproximar do fim
        remaining = len(self._videos) - self._current_idx
        if remaining <= 5:
            self._load_more()

    def _prev_video(self):
        if not self._videos:
            return
        self._current_idx -= 1
        if self._current_idx < 0:
            self._current_idx = len(self._videos) - 1
        self._show_current_video()

    def _random_video(self):
        if len(self._videos) < 2:
            return
        old = self._current_idx
        while self._current_idx == old:
            self._current_idx = random.randint(0, len(self._videos) - 1)
        self._show_current_video()

    def _open_current_video(self):
        if not self._videos:
            return
        video = self._videos[self._current_idx]
        url = video.get("url", "")
        if url:
            webbrowser.open(url)

    def _like_video(self):
        """Marca vídeo como favorito e dá XP."""
        uid = self.app.get_user_id()
        if uid and self._videos:
            self.app.db.add_xp(uid, 5, "shorts", "Assistiu short educativo")
            self.app.refresh_xp_sidebar()
            t = self.app.theme_mgr.get_theme()
            self._btn_like.configure(
                fg_color=t["accent"], text_color="#000", text="⭐")
            self.after(1500, lambda: self._btn_like.configure(
                fg_color=t["card"], text="⭐"))

    def _on_mousewheel(self, event):
        """Navegar com scroll do mouse."""
        # Verificar se o ShortsView está visível
        if not self.winfo_ismapped():
            return
        if event.delta > 0:
            self._prev_video()
        else:
            self._next_video()

    # ══════════════════════════════════════════════════════════
    # ── ESTADOS ──────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _show_loading(self):
        for w in self._card_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        ctk.CTkLabel(
            self._card_frame, text="",
        ).pack(expand=True)

        ctk.CTkLabel(
            self._card_frame, text="🔍",
            font=ctk.CTkFont(size=60),
        ).pack()

        ctk.CTkLabel(
            self._card_frame,
            text="Buscando vídeos educativos...",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(10, 5))

        self._loading_dots = ctk.CTkLabel(
            self._card_frame,
            text="Conectando ao YouTube",
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
        )
        self._loading_dots.pack()

        progress = ctk.CTkProgressBar(
            self._card_frame, width=250, height=6,
            progress_color=t["accent"],
            mode="indeterminate",
        )
        progress.pack(pady=20)
        progress.start()

        ctk.CTkLabel(
            self._card_frame, text="",
        ).pack(expand=True)

    def _show_empty_state(self):
        for w in self._card_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        ctk.CTkLabel(self._card_frame, text="").pack(expand=True)

        ctk.CTkLabel(
            self._card_frame, text="📱",
            font=ctk.CTkFont(size=60),
        ).pack()

        ctk.CTkLabel(
            self._card_frame,
            text="Shorts Educativos",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["primary"],
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self._card_frame,
            text="Vídeos curtos sobre todos os tópicos do ENEM\n"
                 "Navegue como no TikTok — um vídeo por vez!\n\n"
                 "🎯 Selecione uma área ao lado ou clique abaixo",
            font=ctk.CTkFont(size=14),
            text_color=t["text_sec"],
            justify="center",
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            self._card_frame,
            text="🚀 Carregar Shorts",
            height=45, width=200,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=t["primary"], hover_color=t["button_hover"],
            corner_radius=12,
            command=self._load_videos,
        ).pack(pady=5)

        ctk.CTkLabel(self._card_frame, text="").pack(expand=True)

    def _show_error(self, msg: str):
        for w in self._card_frame.winfo_children():
            w.destroy()

        t = self.app.theme_mgr.get_theme()

        ctk.CTkLabel(self._card_frame, text="").pack(expand=True)
        ctk.CTkLabel(
            self._card_frame, text="❌",
            font=ctk.CTkFont(size=50),
        ).pack()
        ctk.CTkLabel(
            self._card_frame,
            text="Não foi possível carregar os vídeos",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t["danger"],
        ).pack(pady=5)
        ctk.CTkLabel(
            self._card_frame,
            text="Verifique sua conexão com a internet",
            font=ctk.CTkFont(size=13),
            text_color=t["text_sec"],
        ).pack()
        ctk.CTkButton(
            self._card_frame,
            text="🔄 Tentar novamente",
            height=38, fg_color=t["primary"],
            hover_color=t["button_hover"],
            command=self._load_videos,
        ).pack(pady=15)
        ctk.CTkLabel(self._card_frame, text="").pack(expand=True)

        self._loading = False

    # ══════════════════════════════════════════════════════════
    # ── HELPERS ──────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    @staticmethod
    def _area_from_query(query: str) -> str:
        """Tenta identificar a área ENEM a partir da query de busca."""
        q = query.lower()
        if any(w in q for w in ["gramática", "linguagem", "literatura", "texto", "gênero", "intertextualidade"]):
            return "Linguagens"
        elif any(w in q for w in ["matemática", "porcentagem", "geometria", "equação", "trigonometria",
                                  "logaritmo", "progressão", "combinatória", "regra de três", "estatística"]):
            return "Matemática"
        elif any(w in q for w in ["física", "cinemática", "newton", "termodinâmica", "óptica", "eletricidade",
                                  "ondulatória", "química", "tabela periódica", "estequiometria", "orgânica",
                                  "biologia", "ecologia", "genética", "citologia", "evolução", "fisiologia"]):
            return "Ciências da Natureza"
        elif any(w in q for w in ["história", "geografia", "globalização", "urbanização", "bioma", "clima",
                                  "filosofia", "sociologia", "guerra", "vargas", "ditadura", "colônia"]):
            return "Ciências Humanas"
        elif any(w in q for w in ["redação", "proposta", "conectivo", "repertório", "competência", "argumentação"]):
            return "Redação"
        return "ENEM"

    def on_show(self):
        """Chamado quando a view é exibida."""
        pass  # Vídeos já estão carregados; não recarregar toda vez
