import sqlite3
import hashlib
import json
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            base = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base, "pomodoro_study.db")
        self.db_path = db_path
        self._init_database()

    # ── conexão ──────────────────────────────────────────────
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ── criação de tabelas ───────────────────────────────────
    def _init_database(self):
        conn = self._conn()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT,
                theme TEXT DEFAULT 'Naruto',
                pomodoro_focus INTEGER DEFAULT 25,
                pomodoro_short INTEGER DEFAULT 5,
                pomodoro_long INTEGER DEFAULT 15,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'pendente',
                priority TEXT DEFAULT 'média',
                pomodoros_est INTEGER DEFAULT 1,
                pomodoros_done INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_id INTEGER,
                session_type TEXT DEFAULT 'foco',
                duration INTEGER,
                started_at TIMESTAMP,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS study_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT DEFAULT 'enem',
                subject TEXT NOT NULL,
                topic TEXT,
                format TEXT DEFAULT 'quiz',
                score REAL DEFAULT 0,
                total_questions INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT,
                question TEXT,
                options TEXT,
                correct_answer TEXT,
                explanation TEXT,
                difficulty TEXT DEFAULT 'médio',
                video_url TEXT,
                video_title TEXT,
                video_channel TEXT,
                content_type TEXT DEFAULT 'quiz',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS update_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                update_type TEXT NOT NULL,
                category TEXT,
                subject TEXT,
                status TEXT DEFAULT 'success',
                videos_updated INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        # Cache de questões reais do ENEM (API enem.dev)
        c.execute("""
            CREATE TABLE IF NOT EXISTS enem_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                question_index INTEGER NOT NULL,
                title TEXT,
                discipline TEXT,
                discipline_name TEXT,
                language TEXT,
                context TEXT,
                question_intro TEXT,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                correct_letter TEXT,
                images TEXT,
                alt_images TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, question_index)
            )
        """)

        # Progresso do quiz ENEM real (por ano)
        c.execute("""
            CREATE TABLE IF NOT EXISTS enem_quiz_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                year INTEGER NOT NULL,
                discipline TEXT,
                total_questions INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                score REAL DEFAULT 0,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()

        c.execute("SELECT COUNT(*) FROM content")
        if c.fetchone()[0] == 0:
            self._seed_content(conn)

        conn.close()

    # ── SEED de conteúdo ─────────────────────────────────────
    def _seed_content(self, conn):
        questions = [
            # ── ENEM – Linguagens ───────────────────────────
            ("enem", "Linguagens", "Interpretação de Texto",
             "Qual figura de linguagem consiste em atribuir características humanas a seres inanimados?",
             json.dumps(["Metáfora", "Prosopopeia", "Hipérbole", "Metonímia"]),
             "Prosopopeia",
             "Prosopopeia (ou personificação) atribui qualidades humanas a objetos, animais ou fenômenos.",
             "fácil"),
            ("enem", "Linguagens", "Gramática",
             "Na oração 'Os alunos cujos pais compareceram foram elogiados', a palavra 'cujos' é:",
             json.dumps(["Pronome relativo", "Conjunção",
                        "Pronome demonstrativo", "Advérbio"]),
             "Pronome relativo",
             "'Cujos' é pronome relativo que estabelece relação de posse entre antecedente e consequente.",
             "médio"),
            ("enem", "Linguagens", "Literatura",
             "O Modernismo brasileiro teve como marco inicial a Semana de Arte Moderna de:",
             json.dumps(["1920", "1922", "1925", "1930"]),
             "1922",
             "A Semana de Arte Moderna aconteceu em fevereiro de 1922 no Teatro Municipal de São Paulo.",
             "fácil"),
            ("enem", "Linguagens", "Literatura",
             "Qual autor é considerado o principal representante do Realismo no Brasil?",
             json.dumps(["José de Alencar", "Machado de Assis",
                        "Castro Alves", "Gonçalves Dias"]),
             "Machado de Assis",
             "Machado de Assis é o maior nome do Realismo brasileiro, com obras como Dom Casmurro e Memórias Póstumas de Brás Cubas.",
             "fácil"),
            ("enem", "Linguagens", "Gramática",
             "Qual alternativa apresenta um exemplo correto de crase?",
             json.dumps(["Fui à escola", "Fui à casa",
                        "Refiro-me à você", "Chegou à pé"]),
             "Fui à escola",
             "Usa-se crase antes de palavras femininas determinadas. 'À escola' está correto pois há artigo definido.",
             "médio"),

            # ── ENEM – Matemática ──────────────────────────
            ("enem", "Matemática", "Porcentagem",
             "Um produto que custava R$ 200,00 teve um desconto de 15%. Qual o novo preço?",
             json.dumps(["R$ 170,00", "R$ 180,00", "R$ 175,00", "R$ 185,00"]),
             "R$ 170,00",
             "15% de 200 = 30. Portanto: 200 - 30 = R$ 170,00.",
             "fácil"),
            ("enem", "Matemática", "Geometria",
             "Qual a área de um triângulo com base 10 cm e altura 6 cm?",
             json.dumps(["60 cm²", "30 cm²", "16 cm²", "36 cm²"]),
             "30 cm²",
             "Área do triângulo = (base × altura) / 2 = (10 × 6) / 2 = 30 cm².",
             "fácil"),
            ("enem", "Matemática", "Probabilidade",
             "Ao lançar dois dados, qual a probabilidade de obter soma igual a 7?",
             json.dumps(["1/6", "1/12", "1/4", "1/36"]),
             "1/6",
             "Existem 6 combinações que somam 7 de um total de 36 possibilidades: 6/36 = 1/6.",
             "médio"),
            ("enem", "Matemática", "Funções",
             "Dada f(x) = 2x + 3, qual o valor de f(5)?",
             json.dumps(["10", "13", "15", "8"]),
             "13",
             "f(5) = 2(5) + 3 = 10 + 3 = 13.",
             "fácil"),
            ("enem", "Matemática", "Estatística",
             "A média aritmética de 4, 6, 8, 10 e 12 é:",
             json.dumps(["7", "8", "9", "10"]),
             "8",
             "Média = (4+6+8+10+12)/5 = 40/5 = 8.",
             "fácil"),
            ("enem", "Matemática", "Geometria",
             "O volume de um cubo com aresta de 3 cm é:",
             json.dumps(["9 cm³", "18 cm³", "27 cm³", "81 cm³"]),
             "27 cm³",
             "Volume do cubo = a³ = 3³ = 27 cm³.",
             "fácil"),

            # ── ENEM – Ciências da Natureza ─────────────────
            ("enem", "Ciências da Natureza", "Física - Leis de Newton",
             "A Primeira Lei de Newton é conhecida como Lei da:",
             json.dumps(["Ação e Reação", "Inércia",
                        "Gravitação", "Conservação"]),
             "Inércia",
             "A 1ª Lei de Newton (Lei da Inércia) afirma que um corpo em repouso tende a permanecer em repouso.",
             "fácil"),
            ("enem", "Ciências da Natureza", "Química - Tabela Periódica",
             "Qual elemento químico tem o símbolo 'Fe'?",
             json.dumps(["Flúor", "Ferro", "Fósforo", "Frâncio"]),
             "Ferro",
             "Fe vem do latim 'Ferrum', que significa ferro. Número atômico 26.",
             "fácil"),
            ("enem", "Ciências da Natureza", "Biologia - Ecologia",
             "O conjunto de seres vivos de uma mesma espécie que vivem em determinada região é chamado de:",
             json.dumps(["Comunidade", "Ecossistema", "População", "Bioma"]),
             "População",
             "População é o conjunto de indivíduos da mesma espécie em uma determinada área.",
             "fácil"),
            ("enem", "Ciências da Natureza", "Biologia - Genética",
             "Qual é a molécula responsável por carregar a informação genética?",
             json.dumps(["RNA", "DNA", "Proteína", "Lipídio"]),
             "DNA",
             "O DNA (ácido desoxirribonucleico) carrega toda a informação genética dos seres vivos.",
             "fácil"),
            ("enem", "Ciências da Natureza", "Física - Termodinâmica",
             "A escala de temperatura em que a água ferve a 373 K é:",
             json.dumps(["Celsius", "Fahrenheit", "Kelvin", "Rankine"]),
             "Kelvin",
             "Na escala Kelvin, a água ferve a 373 K (equivalente a 100°C).",
             "médio"),
            ("enem", "Ciências da Natureza", "Química - Reações",
             "Uma reação de combustão completa de um hidrocarboneto produz:",
             json.dumps(["CO e H2", "CO2 e H2O", "CO e H2O", "C e H2O"]),
             "CO2 e H2O",
             "Combustão completa: hidrocarboneto + O2 → CO2 + H2O.",
             "médio"),
            ("enem", "Ciências da Natureza", "Biologia - Citologia",
             "A organela responsável pela respiração celular é:",
             json.dumps(["Ribossomo", "Complexo de Golgi",
                        "Mitocôndria", "Lisossomo"]),
             "Mitocôndria",
             "A mitocôndria é a organela responsável pela respiração celular aeróbica e produção de ATP.",
             "fácil"),

            # ── ENEM – Ciências Humanas ────────────────────
            ("enem", "Ciências Humanas", "História - Rev. Industrial",
             "A Revolução Industrial teve início em qual país?",
             json.dumps(
                 ["França", "Alemanha", "Inglaterra", "Estados Unidos"]),
             "Inglaterra",
             "A Revolução Industrial começou na Inglaterra no século XVIII.",
             "fácil"),
            ("enem", "Ciências Humanas", "Geografia - Globalização",
             "Qual bloco econômico o Brasil faz parte como membro fundador?",
             json.dumps(["União Europeia", "NAFTA", "Mercosul", "APEC"]),
             "Mercosul",
             "O Mercosul foi fundado em 1991 pelo Tratado de Assunção, com Brasil, Argentina, Paraguai e Uruguai.",
             "fácil"),
            ("enem", "Ciências Humanas", "Filosofia",
             "O filósofo grego considerado o 'pai da filosofia ocidental' é:",
             json.dumps(["Platão", "Aristóteles",
                        "Sócrates", "Tales de Mileto"]),
             "Sócrates",
             "Sócrates é considerado o pai da filosofia ocidental. Seu método era baseado no diálogo e questionamento.",
             "fácil"),
            ("enem", "Ciências Humanas", "Sociologia",
             "Qual sociólogo é autor do conceito de 'fato social'?",
             json.dumps(["Max Weber", "Karl Marx",
                        "Émile Durkheim", "Auguste Comte"]),
             "Émile Durkheim",
             "Durkheim definiu fato social como maneiras de agir, pensar e sentir exteriores ao indivíduo.",
             "médio"),
            ("enem", "Ciências Humanas", "História - Brasil",
             "A Proclamação da República do Brasil aconteceu em:",
             json.dumps(["1822", "1889", "1891", "1888"]),
             "1889",
             "A República foi proclamada em 15 de novembro de 1889 pelo Marechal Deodoro da Fonseca.",
             "fácil"),
            ("enem", "Ciências Humanas", "Geografia - Brasil",
             "Qual é o maior bioma brasileiro em extensão territorial?",
             json.dumps(["Cerrado", "Mata Atlântica", "Amazônia", "Caatinga"]),
             "Amazônia",
             "A Amazônia ocupa cerca de 49% do território brasileiro, sendo o maior bioma do país.",
             "fácil"),

            # ── ENEM – Redação ─────────────────────────────
            ("enem", "Redação", "Estrutura",
             "Quantos parágrafos tem a estrutura padrão de uma redação dissertativa-argumentativa do ENEM?",
             json.dumps(["3", "4", "5", "6"]),
             "5",
             "Introdução + 2 parágrafos de desenvolvimento + conclusão com proposta de intervenção = ~4-5 parágrafos. O padrão recomendado é 5.",
             "fácil"),
            ("enem", "Redação", "Competências",
             "Quantas competências são avaliadas na redação do ENEM?",
             json.dumps(["3", "4", "5", "6"]),
             "5",
             "São 5 competências, cada uma valendo até 200 pontos, totalizando 1000 pontos.",
             "fácil"),

            # ── Concursos ──────────────────────────────────
            ("concursos", "Português", "Concordância",
             "Na frase 'Faz dois anos que não o vejo', o verbo 'fazer' está:",
             json.dumps(["No plural", "No singular (impessoal)",
                        "No gerúndio", "No subjuntivo"]),
             "No singular (impessoal)",
             "O verbo 'fazer' indicando tempo decorrido é impessoal, ficando sempre na 3ª pessoa do singular.",
             "médio"),
            ("concursos", "Raciocínio Lógico", "Proposições",
             "A negação de 'Todos os alunos passaram' é:",
             json.dumps(["Nenhum aluno passou", "Pelo menos um aluno não passou",
                        "Todos reprovaram", "Alguns passaram"]),
             "Pelo menos um aluno não passou",
             "A negação de 'Todo A é B' é 'Existe pelo menos um A que não é B'.",
             "médio"),
            ("concursos", "Informática", "Hardware",
             "Qual componente é responsável pelo processamento de dados no computador?",
             json.dumps(["HD", "CPU", "RAM", "Placa-mãe"]),
             "CPU",
             "A CPU (Unidade Central de Processamento) é o 'cérebro' do computador.",
             "fácil"),
            ("concursos", "Direito Constitucional", "Direitos Fundamentais",
             "Os direitos e garantias fundamentais estão previstos no artigo 5º da Constituição Federal de:",
             json.dumps(["1967", "1946", "1988", "1891"]),
             "1988",
             "A Constituição Federal de 1988, conhecida como 'Constituição Cidadã', traz os direitos fundamentais.",
             "fácil"),
            ("concursos", "Atualidades", "Brasil",
             "O Sistema Único de Saúde (SUS) foi criado pela Constituição de:",
             json.dumps(["1946", "1967", "1988", "1991"]),
             "1988",
             "O SUS foi criado pela CF/88 e regulamentado pelas Leis 8.080/90 e 8.142/90.",
             "médio"),
            ("concursos", "Raciocínio Lógico", "Sequências",
             "Qual o próximo número da sequência: 2, 6, 18, 54, ...?",
             json.dumps(["108", "162", "72", "216"]),
             "162",
             "É uma progressão geométrica de razão 3: 54 × 3 = 162.",
             "médio"),
            ("concursos", "Português", "Interpretação",
             "A coesão textual é garantida pelo uso de:",
             json.dumps(["Parágrafos longos", "Conectivos e pronomes",
                        "Palavras difíceis", "Repetição de ideias"]),
             "Conectivos e pronomes",
             "Conectivos (conjunções, preposições) e pronomes são os principais elementos de coesão textual.",
             "fácil"),
            ("concursos", "Informática", "Internet",
             "O protocolo utilizado para navegação segura na web é:",
             json.dumps(["HTTP", "FTP", "HTTPS", "SMTP"]),
             "HTTPS",
             "HTTPS (Hyper Text Transfer Protocol Secure) usa criptografia SSL/TLS para navegação segura.",
             "fácil"),
        ]

        for q in questions:
            conn.execute("""
                INSERT INTO content (category, subject, topic, question, options,
                    correct_answer, explanation, difficulty, content_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'quiz')
            """, q)

        videos = [
            # ── ENEM Videos ─────────────────────────────────
            ("enem", "Linguagens", "Interpretação de Texto",
             "https://www.youtube.com/watch?v=7YBA9h2-438",
             "Leitura e Interpretação de Textos - ENEM", "Brasil Escola"),
            ("enem", "Linguagens", "Gramática",
             "https://www.youtube.com/watch?v=-rKt0k-BXZ0",
             "Gramática para PASSAR no ENEM", "Stoodi"),
            ("enem", "Matemática", "Porcentagem",
             "https://www.youtube.com/watch?v=CERiIwParX4",
             "Porcentagem: Teoria e Exemplos - Aula 29", "Professor Ferretto"),
            ("enem", "Matemática", "Geometria",
             "https://www.youtube.com/watch?v=0CnUdzmpO8E",
             "Geometria Plana: Introdução – Ângulos", "Professor Ferretto"),
            ("enem", "Matemática", "Funções",
             "https://www.youtube.com/watch?v=hdMFlAv5GkU",
             "Função do 1º Grau (Função Afim): Conceitos Iniciais", "Professor Ferretto"),
            ("enem", "Ciências da Natureza", "Física - Cinemática",
             "https://www.youtube.com/watch?v=M2urmZToedM",
             "Movimento Uniforme – Teoria e Exemplos", "Me Salva!"),
            ("enem", "Ciências da Natureza", "Química - Estequiometria",
             "https://www.youtube.com/watch?v=8FVJXszOmUw",
             "Introdução à Estequiometria / Cálculo Estequiométrico", "Marcelão da Química"),
            ("enem", "Ciências da Natureza", "Biologia - Ecologia",
             "https://www.youtube.com/watch?v=XvdePktAui8",
             "Conceitos Básicos da Ecologia", "Biologia Total (Paulo Jubilut)"),
            ("enem", "Ciências Humanas", "História - Brasil Colônia",
             "https://www.youtube.com/watch?v=VofLIlRK6vI",
             "Brasil Colônia – Economia Colonial (Revisão ENEM)", "Se Liga Nessa História"),
            ("enem", "Ciências Humanas", "Geografia - Urbanização",
             "https://www.youtube.com/watch?v=v15_Y7oQ9K8",
             "Urbanização Brasileira: Causas, Consequências e Problemas", "Geografilia"),
            ("enem", "Ciências Humanas", "Filosofia",
             "https://www.youtube.com/watch?v=NCVQKQuVXmA",
             "Filósofos no ENEM: Sócrates, Platão, Tales e Aristóteles", "Descomplica"),
            ("enem", "Redação", "Estrutura",
             "https://www.youtube.com/watch?v=dcna77bVXAU",
             "Dicas para Escrever uma Redação Nota 1000 no ENEM", "Descomplica"),
            # ── Concursos Videos ────────────────────────────
            ("concursos", "Português", "Concordância",
             "https://www.youtube.com/watch?v=jdqhnVUvqOc",
             "Concordância Verbal – Teoria e Questões para Concurso", "Prof. Álvaro Ferreira"),
            ("concursos", "Raciocínio Lógico", "Proposições",
             "https://www.youtube.com/watch?v=Q-6-lJhawNA",
             "Raciocínio Lógico para Concursos", "Estratégia Concursos"),
            ("concursos", "Direito Constitucional", "Princípios",
             "https://www.youtube.com/watch?v=4JE6E9-7CdU",
             "Princípios Fundamentais – Direito Constitucional", "Estratégia Concursos"),
            ("concursos", "Informática", "Conceitos Básicos",
             "https://www.youtube.com/watch?v=pY7pM6JOxMU",
             "Informática para Concursos – Aula Completa", "Gran Cursos Online"),
        ]

        for v in videos:
            conn.execute("""
                INSERT INTO content (category, subject, topic, video_url,
                    video_title, video_channel, content_type)
                VALUES (?, ?, ?, ?, ?, ?, 'video')
            """, v)

        conn.commit()

    # ── Usuários ─────────────────────────────────────────────
    @staticmethod
    def _hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, display_name=None):
        conn = self._conn()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, display_name) VALUES (?,?,?)",
                (username, self._hash(password), display_name or username),
            )
            conn.commit()
            user = conn.execute(
                "SELECT * FROM users WHERE username=?", (username,)
            ).fetchone()
            return dict(user)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def authenticate(self, username, password):
        conn = self._conn()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password_hash=?",
            (username, self._hash(password)),
        ).fetchone()
        conn.close()
        return dict(user) if user else None

    def update_user_theme(self, user_id, theme):
        conn = self._conn()
        conn.execute("UPDATE users SET theme=? WHERE id=?", (theme, user_id))
        conn.commit()
        conn.close()

    def update_user_pomodoro(self, user_id, focus, short_break, long_break):
        conn = self._conn()
        conn.execute(
            "UPDATE users SET pomodoro_focus=?, pomodoro_short=?, pomodoro_long=? WHERE id=?",
            (focus, short_break, long_break, user_id),
        )
        conn.commit()
        conn.close()

    def get_user(self, user_id):
        conn = self._conn()
        user = conn.execute("SELECT * FROM users WHERE id=?",
                            (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    # ── Tarefas ──────────────────────────────────────────────
    def create_task(self, title, description="", priority="média", pomodoros_est=1, user_id=None):
        conn = self._conn()
        conn.execute(
            """INSERT INTO tasks (user_id, title, description, priority, pomodoros_est)
               VALUES (?,?,?,?,?)""",
            (user_id, title, description, priority, pomodoros_est),
        )
        conn.commit()
        task_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return task_id

    def get_tasks(self, user_id=None, status=None):
        conn = self._conn()
        q = "SELECT * FROM tasks WHERE user_id IS ?"
        params = [user_id]
        if status:
            q += " AND status=?"
            params.append(status)
        q += " ORDER BY CASE priority WHEN 'alta' THEN 1 WHEN 'média' THEN 2 ELSE 3 END, created_at DESC"
        rows = conn.execute(q, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_task(self, task_id, **kwargs):
        conn = self._conn()
        sets = ", ".join(f"{k}=?" for k in kwargs)
        vals = list(kwargs.values()) + [task_id]
        conn.execute(f"UPDATE tasks SET {sets} WHERE id=?", vals)
        conn.commit()
        conn.close()

    def complete_task(self, task_id):
        conn = self._conn()
        conn.execute(
            "UPDATE tasks SET status='concluída', completed_at=? WHERE id=?",
            (datetime.now().isoformat(), task_id),
        )
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = self._conn()
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

    def increment_task_pomodoro(self, task_id):
        conn = self._conn()
        conn.execute(
            "UPDATE tasks SET pomodoros_done = pomodoros_done + 1 WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

    # ── Sessões Pomodoro ─────────────────────────────────────
    def save_session(self, session_type, duration, started_at, user_id=None, task_id=None):
        conn = self._conn()
        conn.execute(
            """INSERT INTO pomodoro_sessions
               (user_id, task_id, session_type, duration, started_at)
               VALUES (?,?,?,?,?)""",
            (user_id, task_id, session_type, duration, started_at),
        )
        conn.commit()
        conn.close()

    def get_sessions(self, user_id=None, limit=50):
        conn = self._conn()
        rows = conn.execute(
            """SELECT ps.*, t.title as task_title
               FROM pomodoro_sessions ps
               LEFT JOIN tasks t ON ps.task_id = t.id
               WHERE ps.user_id IS ?
               ORDER BY ps.completed_at DESC LIMIT ?""",
            (user_id, limit),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_session_stats(self, user_id=None):
        conn = self._conn()
        row = conn.execute(
            """SELECT
                COUNT(*) as total,
                SUM(CASE WHEN session_type='foco' THEN 1 ELSE 0 END) as focus_count,
                SUM(CASE WHEN session_type='foco' THEN duration ELSE 0 END) as focus_minutes,
                COUNT(DISTINCT DATE(completed_at)) as days_active
               FROM pomodoro_sessions WHERE user_id IS ?""",
            (user_id,),
        ).fetchone()
        conn.close()
        return dict(row)

    # ── Progresso de Estudo ──────────────────────────────────
    def save_study_progress(self, subject, topic, fmt, score, total, correct, category="enem", user_id=None):
        conn = self._conn()
        conn.execute(
            """INSERT INTO study_progress
               (user_id, category, subject, topic, format, score, total_questions, correct_answers)
               VALUES (?,?,?,?,?,?,?,?)""",
            (user_id, category, subject, topic, fmt, score, total, correct),
        )
        conn.commit()
        conn.close()

    def get_study_stats(self, user_id=None, category=None):
        conn = self._conn()
        q = """SELECT subject,
                      COUNT(*) as sessions,
                      AVG(score) as avg_score,
                      SUM(total_questions) as total_q,
                      SUM(correct_answers) as total_correct
               FROM study_progress WHERE user_id IS ?"""
        params = [user_id]
        if category:
            q += " AND category=?"
            params.append(category)
        q += " GROUP BY subject ORDER BY sessions DESC"
        rows = conn.execute(q, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ── Conteúdo ─────────────────────────────────────────────
    def get_subjects(self, category="enem", content_type="quiz"):
        conn = self._conn()
        rows = conn.execute(
            "SELECT DISTINCT subject FROM content WHERE category=? AND content_type=? ORDER BY subject",
            (category, content_type),
        ).fetchall()
        conn.close()
        return [r["subject"] for r in rows]

    def get_topics(self, category, subject, content_type="quiz"):
        conn = self._conn()
        rows = conn.execute(
            "SELECT DISTINCT topic FROM content WHERE category=? AND subject=? AND content_type=? ORDER BY topic",
            (category, subject, content_type),
        ).fetchall()
        conn.close()
        return [r["topic"] for r in rows]

    def get_questions(self, category, subject, topic=None, limit=10):
        conn = self._conn()
        q = "SELECT * FROM content WHERE category=? AND subject=? AND content_type='quiz'"
        params = [category, subject]
        if topic:
            q += " AND topic=?"
            params.append(topic)
        q += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_videos(self, category, subject, topic=None):
        conn = self._conn()
        q = "SELECT * FROM content WHERE category=? AND subject=? AND content_type='video'"
        params = [category, subject]
        if topic:
            q += " AND topic=?"
            params.append(topic)
        q += " ORDER BY topic"
        rows = conn.execute(q, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def search_content(self, query, content_type=None):
        conn = self._conn()
        q = """SELECT * FROM content
               WHERE (question LIKE ? OR topic LIKE ? OR subject LIKE ?
                      OR video_title LIKE ?)"""
        params = [f"%{query}%"] * 4
        if content_type:
            q += " AND content_type=?"
            params.append(content_type)
        q += " ORDER BY category, subject LIMIT 50"
        rows = conn.execute(q, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ── Controle de Atualização ──────────────────────────────
    def get_last_update(self, update_type="videos"):
        """Retorna a data/hora da última atualização bem-sucedida."""
        conn = self._conn()
        row = conn.execute(
            """SELECT completed_at FROM update_log
               WHERE update_type=? AND status='success'
               ORDER BY completed_at DESC LIMIT 1""",
            (update_type,),
        ).fetchone()
        conn.close()
        if row and row["completed_at"]:
            try:
                return datetime.fromisoformat(row["completed_at"])
            except (ValueError, TypeError):
                return None
        return None

    def needs_update(self, update_type="videos", interval_hours=24):
        """Verifica se já passou o intervalo desde a última atualização."""
        last = self.get_last_update(update_type)
        if last is None:
            return True
        diff = datetime.now() - last
        return diff.total_seconds() >= interval_hours * 3600

    def log_update_start(self, update_type, category=None, subject=None):
        """Registra início de uma atualização."""
        conn = self._conn()
        conn.execute(
            """INSERT INTO update_log (update_type, category, subject, status)
               VALUES (?, ?, ?, 'running')""",
            (update_type, category, subject),
        )
        conn.commit()
        log_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return log_id

    def log_update_finish(self, log_id, status="success", videos_updated=0, error_message=None):
        """Registra fim de uma atualização."""
        conn = self._conn()
        conn.execute(
            """UPDATE update_log
               SET status=?, videos_updated=?, error_message=?, completed_at=?
               WHERE id=?""",
            (status, videos_updated, error_message,
             datetime.now().isoformat(), log_id),
        )
        conn.commit()
        conn.close()

    def get_update_history(self, limit=20):
        """Retorna histórico de atualizações."""
        conn = self._conn()
        rows = conn.execute(
            """SELECT * FROM update_log
               ORDER BY started_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ── CRUD de vídeos (para o atualizador) ──────────────────
    def upsert_video(self, category, subject, topic, url, title, channel):
        """Insere ou atualiza um vídeo no banco."""
        conn = self._conn()
        existing = conn.execute(
            """SELECT id FROM content
               WHERE category=? AND subject=? AND topic=?
                     AND content_type='video' AND video_url=?""",
            (category, subject, topic, url),
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE content SET video_title=?, video_channel=?, updated_at=?
                   WHERE id=?""",
                (title, channel, datetime.now().isoformat(), existing["id"]),
            )
        else:
            conn.execute(
                """INSERT INTO content
                   (category, subject, topic, video_url, video_title, video_channel,
                    content_type, updated_at)
                   VALUES (?,?,?,?,?,?,'video',?)""",
                (category, subject, topic, url, title, channel,
                 datetime.now().isoformat()),
            )
        conn.commit()
        conn.close()

    def replace_videos_for_topic(self, category, subject, topic, new_videos):
        """Remove vídeos antigos de um tópico e insere os novos."""
        conn = self._conn()
        conn.execute(
            """DELETE FROM content
               WHERE category=? AND subject=? AND topic=? AND content_type='video'""",
            (category, subject, topic),
        )
        for v in new_videos:
            conn.execute(
                """INSERT INTO content
                   (category, subject, topic, video_url, video_title, video_channel,
                    content_type, updated_at)
                   VALUES (?,?,?,?,?,?,'video',?)""",
                (category, subject, topic, v["url"], v["title"], v["channel"],
                 datetime.now().isoformat()),
            )
        conn.commit()
        conn.close()
        return len(new_videos)

    def get_all_video_topics(self):
        """Retorna todos os (category, subject, topic) que possuem vídeos."""
        conn = self._conn()
        rows = conn.execute(
            """SELECT DISTINCT category, subject, topic
               FROM content WHERE content_type='video'
               ORDER BY category, subject, topic"""
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ── Questões Reais do ENEM (Cache) ───────────────────────
    def cache_enem_questions(self, questions: list[dict]) -> int:
        """Salva questões do ENEM no cache local. Retorna quantas foram inseridas."""
        conn = self._conn()
        inserted = 0
        for q in questions:
            try:
                conn.execute(
                    """INSERT OR REPLACE INTO enem_questions
                       (year, question_index, title, discipline, discipline_name,
                        language, context, question_intro, question_text,
                        options, correct_answer, correct_letter, images, alt_images)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        q["year"], q["index"], q.get("title", ""),
                        q.get("discipline", ""), q.get("discipline_name", ""),
                        q.get("language"), q.get("context", ""),
                        q.get("question_intro", ""), q["question_text"],
                        json.dumps(q["options"], ensure_ascii=False),
                        q["correct_answer"], q.get("correct_letter", ""),
                        json.dumps(q.get("images", []), ensure_ascii=False),
                        json.dumps(q.get("alt_images", []),
                                   ensure_ascii=False),
                    ),
                )
                inserted += 1
            except Exception:
                continue
        conn.commit()
        conn.close()
        return inserted

    def get_cached_enem_years(self) -> list[int]:
        """Retorna os anos que já têm questões em cache."""
        conn = self._conn()
        rows = conn.execute(
            "SELECT DISTINCT year FROM enem_questions ORDER BY year DESC"
        ).fetchall()
        conn.close()
        return [r["year"] for r in rows]

    def get_cached_enem_year_count(self, year: int) -> int:
        """Retorna quantas questões estão em cache para um ano."""
        conn = self._conn()
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM enem_questions WHERE year=?", (year,)
        ).fetchone()
        conn.close()
        return row["cnt"] if row else 0

    def get_enem_disciplines_for_year(self, year: int) -> list[dict]:
        """Retorna disciplinas disponíveis para um ano com contagem de questões."""
        conn = self._conn()
        rows = conn.execute(
            """SELECT discipline, discipline_name, COUNT(*) as count
               FROM enem_questions
               WHERE year=? AND discipline != ''
               GROUP BY discipline
               ORDER BY discipline_name""",
            (year,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_enem_questions(
        self, year: int, discipline: str = None,
        limit: int = 45, randomize: bool = True
    ) -> list[dict]:
        """Retorna questões do ENEM do cache por ano e disciplina."""
        conn = self._conn()
        q = "SELECT * FROM enem_questions WHERE year=?"
        params: list = [year]
        if discipline:
            q += " AND discipline=?"
            params.append(discipline)
        if randomize:
            q += " ORDER BY RANDOM()"
        else:
            q += " ORDER BY question_index"
        q += " LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            d["options"] = json.loads(d["options"])
            d["images"] = json.loads(d.get("images") or "[]")
            d["alt_images"] = json.loads(d.get("alt_images") or "[]")
            result.append(d)
        return result

    def has_enem_year_cached(self, year: int) -> bool:
        """Verifica se um ano já tem questões em cache."""
        return self.get_cached_enem_year_count(year) > 0

    # ── Progresso do Quiz ENEM Real ──────────────────────────
    def save_enem_quiz_progress(
        self, year: int, discipline: str, total: int,
        correct: int, score: float, user_id: int = None
    ):
        """Salva resultado de um quiz de questões reais do ENEM."""
        conn = self._conn()
        conn.execute(
            """INSERT INTO enem_quiz_progress
               (user_id, year, discipline, total_questions, correct_answers, score)
               VALUES (?,?,?,?,?,?)""",
            (user_id, year, discipline, total, correct, score),
        )
        conn.commit()
        conn.close()

    def get_enem_quiz_history(self, user_id: int = None, limit: int = 50) -> list[dict]:
        """Retorna histórico de quizzes ENEM reais do usuário."""
        conn = self._conn()
        rows = conn.execute(
            """SELECT * FROM enem_quiz_progress
               WHERE user_id IS ?
               ORDER BY completed_at DESC LIMIT ?""",
            (user_id, limit),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_enem_quiz_stats_by_year(self, user_id: int = None) -> list[dict]:
        """Retorna estatísticas agrupadas por ano."""
        conn = self._conn()
        rows = conn.execute(
            """SELECT year, discipline,
                      COUNT(*) as attempts,
                      AVG(score) as avg_score,
                      MAX(score) as best_score,
                      SUM(total_questions) as total_q,
                      SUM(correct_answers) as total_correct
               FROM enem_quiz_progress
               WHERE user_id IS ?
               GROUP BY year, discipline
               ORDER BY year DESC""",
            (user_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
