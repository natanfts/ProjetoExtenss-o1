"""
ContentUpdater – Sistema de atualização automática de conteúdo.

Busca vídeos frescos no YouTube diariamente para cada matéria/tópico,
substituindo os antigos no banco de dados. Roda em background thread
para não travar a interface.
"""

import threading
import time
import logging
from datetime import datetime

from api_service import APIService
from database import DatabaseManager

logger = logging.getLogger("ContentUpdater")

# ── Mapa de buscas para cada (category, subject, topic) ──────
# Cada entrada define a query de busca usada no YouTube.
SEARCH_QUERIES = {
    # ── ENEM ──────────────────────────────────────────────────
    ("enem", "Linguagens", "Interpretação de Texto"):
        "interpretação de texto ENEM aula",
    ("enem", "Linguagens", "Gramática"):
        "gramática para ENEM aula completa",
    ("enem", "Linguagens", "Literatura"):
        "literatura brasileira ENEM aula",
    ("enem", "Matemática", "Porcentagem"):
        "porcentagem matemática ENEM aula",
    ("enem", "Matemática", "Geometria"):
        "geometria plana ENEM aula",
    ("enem", "Matemática", "Funções"):
        "função primeiro grau função afim ENEM aula",
    ("enem", "Matemática", "Probabilidade"):
        "probabilidade ENEM aula",
    ("enem", "Matemática", "Estatística"):
        "estatística média moda mediana ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Cinemática"):
        "cinemática movimento uniforme física ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Leis de Newton"):
        "leis de Newton física ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Termodinâmica"):
        "termodinâmica física ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Estequiometria"):
        "estequiometria química ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Tabela Periódica"):
        "tabela periódica química ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Reações"):
        "reações químicas combustão ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Ecologia"):
        "ecologia biologia ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Genética"):
        "genética DNA biologia ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Citologia"):
        "citologia célula biologia ENEM aula",
    ("enem", "Ciências Humanas", "História - Rev. Industrial"):
        "revolução industrial história ENEM aula",
    ("enem", "Ciências Humanas", "História - Brasil Colônia"):
        "Brasil Colônia história ENEM aula",
    ("enem", "Ciências Humanas", "História - Brasil"):
        "história do Brasil república ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Globalização"):
        "globalização geografia ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Urbanização"):
        "urbanização brasileira geografia ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Brasil"):
        "biomas brasileiros geografia ENEM aula",
    ("enem", "Ciências Humanas", "Filosofia"):
        "filosofia Sócrates Platão Aristóteles ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia"):
        "sociologia Durkheim Weber Marx ENEM aula",
    ("enem", "Redação", "Estrutura"):
        "redação nota 1000 ENEM como fazer aula",
    ("enem", "Redação", "Competências"):
        "competências redação ENEM dicas aula",

    # ── Concursos ─────────────────────────────────────────────
    ("concursos", "Português", "Concordância"):
        "concordância verbal nominal concursos aula",
    ("concursos", "Português", "Interpretação"):
        "interpretação de texto concursos aula",
    ("concursos", "Raciocínio Lógico", "Proposições"):
        "raciocínio lógico proposições concursos aula",
    ("concursos", "Raciocínio Lógico", "Sequências"):
        "raciocínio lógico sequências concursos aula",
    ("concursos", "Informática", "Hardware"):
        "informática hardware concursos aula",
    ("concursos", "Informática", "Internet"):
        "informática internet protocolos concursos aula",
    ("concursos", "Informática", "Conceitos Básicos"):
        "informática básica concursos aula completa",
    ("concursos", "Direito Constitucional", "Direitos Fundamentais"):
        "direitos fundamentais constituição concursos aula",
    ("concursos", "Direito Constitucional", "Princípios"):
        "princípios fundamentais direito constitucional concursos aula",
    ("concursos", "Atualidades", "Brasil"):
        "atualidades Brasil concursos aula",
}


class ContentUpdater:
    """
    Gerencia atualização automática de vídeos do YouTube no banco de dados.
    Busca vídeos frescos diariamente para cada matéria/tópico configurado.
    """

    def __init__(self, db: DatabaseManager, interval_hours: int = 24):
        self.db = db
        self.api = APIService()
        self.interval_hours = interval_hours
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._status = "idle"           # idle | updating | done | error
        self._progress = ""             # mensagem de progresso
        self._progress_pct = 0.0        # 0.0 a 1.0
        self._last_error = ""
        self._videos_per_topic = 3      # quantos vídeos por tópico

    # ── propriedades de status ───────────────────────────────
    @property
    def status(self):
        return self._status

    @property
    def progress(self):
        return self._progress

    @property
    def progress_pct(self):
        return self._progress_pct

    @property
    def is_running(self):
        return self._status == "updating"

    # ── iniciar atualização em background ────────────────────
    def start_update(self, force=False):
        """
        Verifica se precisa atualizar e, se sim, roda em thread background.
        Se force=True, atualiza mesmo que não tenha passado o intervalo.
        """
        if self._status == "updating":
            return False  # já está rodando

        if not force and not self.db.needs_update("videos", self.interval_hours):
            self._status = "done"
            self._progress = "Conteúdo atualizado (última atualização recente)"
            return False

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_update, daemon=True)
        self._thread.start()
        return True

    def stop(self):
        """Para a atualização em andamento."""
        self._stop_event.set()

    # ── lógica principal de atualização ──────────────────────
    def _run_update(self):
        self._status = "updating"
        self._progress = "Iniciando atualização de conteúdo..."
        self._progress_pct = 0.0

        log_id = self.db.log_update_start("videos")
        total_updated = 0

        try:
            # Coletar todos os tópicos que precisam de vídeo
            topics = list(SEARCH_QUERIES.items())
            total = len(topics)

            for i, ((category, subject, topic), query) in enumerate(topics):
                if self._stop_event.is_set():
                    break

                self._progress = f"🔄 Buscando: {subject} → {topic}"
                self._progress_pct = i / total

                # Buscar vídeos no YouTube
                results = self.api.search_youtube_videos(
                    query, limit=self._videos_per_topic)

                if results:
                    # Substituir vídeos antigos pelos novos
                    new_videos = [
                        {"url": v["url"], "title": v["title"],
                            "channel": v["channel"]}
                        for v in results if v.get("url")
                    ]
                    if new_videos:
                        count = self.db.replace_videos_for_topic(
                            category, subject, topic, new_videos
                        )
                        total_updated += count

                # Pequena pausa para não sobrecarregar
                time.sleep(0.5)

            self._progress_pct = 1.0
            self._status = "done"
            self._progress = f"✅ Atualização concluída! {total_updated} vídeos atualizados."
            self.db.log_update_finish(log_id, "success", total_updated)

            logger.info(
                "Atualização concluída: %d vídeos atualizados", total_updated)

        except Exception as e:
            self._status = "error"
            self._last_error = str(e)
            self._progress = f"❌ Erro na atualização: {e}"
            self.db.log_update_finish(log_id, "error", total_updated, str(e))
            logger.error("Erro na atualização: %s", e)

    # ── atualizar um único tópico sob demanda ────────────────
    def update_single_topic(self, category, subject, topic):
        """Atualiza vídeos de um único tópico imediatamente."""
        key = (category, subject, topic)
        query = SEARCH_QUERIES.get(key)
        if not query:
            # Gerar query genérica
            query = f"{subject} {topic} aula"

        results = self.api.search_youtube_videos(
            query, limit=self._videos_per_topic)
        if results:
            new_videos = [
                {"url": v["url"], "title": v["title"], "channel": v["channel"]}
                for v in results if v.get("url")
            ]
            if new_videos:
                return self.db.replace_videos_for_topic(
                    category, subject, topic, new_videos
                )
        return 0

    # ── busca livre sob demanda ──────────────────────────────
    def search_and_add_videos(self, category, subject, topic, custom_query=None):
        """
        Busca vídeos para um tema personalizado e adiciona ao banco.
        Permite que o usuário pesquise qualquer assunto.
        """
        query = custom_query or f"{topic} {subject} aula"
        results = self.api.search_youtube_videos(query, limit=5)
        added = 0
        for v in results:
            if v.get("url"):
                self.db.upsert_video(
                    category, subject, topic,
                    v["url"], v["title"], v["channel"],
                )
                added += 1
        return added, results
