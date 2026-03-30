# 🍅 PomodoroStudy — Estude com Foco!

> Aplicativo desktop de estudos com timer Pomodoro, quizzes do ENEM, flashcards com repetição espaçada, shorts educativos do YouTube e gamificação — tudo com temas de anime!

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Sobre o Projeto

O **PomodoroStudy** é um aplicativo de estudos completo desenvolvido em Python com interface gráfica moderna usando CustomTkinter. Foi criado como projeto de extensão universitária com foco em ajudar estudantes a se prepararem para o **ENEM** e **concursos** de forma produtiva e engajante.

O app combina técnicas comprovadas de estudo (Pomodoro, repetição espaçada, quizzes) com elementos de gamificação e temas visuais de animes populares para tornar a experiência de estudo mais motivadora.

---

## ✨ Funcionalidades

### 🏠 Dashboard
- Visão geral do progresso (XP, nível, streak)
- Metas diárias de estudo configuráveis
- Resumo de conquistas e estatísticas

### 🍅 Timer Pomodoro
- Ciclos de foco + pausa configuráveis
- Notificação sonora ao final de cada ciclo
- Registro automático de sessões de estudo
- Ganho de XP por sessão completada

### 📋 Gerenciamento de Tarefas
- Criar, editar e excluir tarefas de estudo
- Marcar tarefas como concluídas
- Organização por prioridade

### 📚 Quizzes ENEM
- **171 questões** cobrindo todas as 5 áreas do ENEM:
  - 🔤 Linguagens, Códigos e suas Tecnologias
  - 📐 Matemática e suas Tecnologias
  - 🔬 Ciências da Natureza e suas Tecnologias
  - 🏛️ Ciências Humanas e suas Tecnologias
  - ✏️ Redação
- Integração com API do ENEM e Open Trivia DB
- Feedback imediato com explicações

### 🃏 Flashcards com Repetição Espaçada
- **62 flashcards** organizados por área do ENEM
- Algoritmo SM-2 para revisão espaçada inteligente
- Classificação: Fácil / Bom / Difícil / Esqueci
- Agendamento automático de revisões

### 📱 Shorts Educativos
- Feed estilo TikTok com vídeos curtos do YouTube
- **Feed infinito** com paginação automática em tempo real
- Filtro por área ENEM (5 áreas)
- Thumbnails reais carregadas do YouTube
- Navegação vertical (botões ⬆️⬇️ ou scroll do mouse)
- Abre vídeos diretamente no navegador
- 60+ tópicos de busca otimizados

### 📊 Histórico
- Registro completo de sessões de estudo
- Estatísticas de tempo estudado
- Acompanhamento de progresso

### ⚙️ Configurações
- Personalização do timer Pomodoro
- Troca de temas visuais
- Configurações de conta

### 🎮 Gamificação
- **Sistema de XP e Níveis** — ganhe experiência estudando
- **23 Conquistas** desbloqueáveis
- **Streak diário** — mantenha sua sequência de estudos
- **Metas diárias** configuráveis

### 🔑 Sistema de Login
- Cadastro e autenticação local
- Perfis individuais com progresso salvo
- Modo convidado disponível

---

## 🎨 Temas

10 temas visuais inspirados em animes e séries populares:

| Tema | Emoji | Descrição |
|------|-------|-----------|
| **Naruto** | 🍥 | Ninja mais imprevisível da Vila da Folha! |
| **Dragon Ball** | 🟠 | Poder de mais de 8000! Estude como um Saiyajin! |
| **Demon Slayer** | 🔥 | Respire e estude como um Caçador de Demônios! |
| **Attack on Titan** | ⚔️ | Dedique seu coração aos estudos! |
| **My Hero Academia** | 💪 | Plus Ultra! Vá além dos seus limites! |
| **One Piece** | 🏴‍☠️ | O Rei dos Estudantes será você! |
| **Death Note** | 📓 | Escreva seu nome no caderno do sucesso! |
| **Jujutsu Kaisen** | 👁️ | Domínio de estudo expandido! |
| **Stranger Things** | 💡 | O Mundo Invertido dos estudos! |
| **Breaking Bad** | 🧪 | Ciência pura nos estudos! |

---

## 🏗️ Estrutura do Projeto

```
PomodoroStudy/
├── main.py                 # Ponto de entrada da aplicação
├── database.py             # Gerenciamento do banco SQLite (14+ tabelas)
├── api_service.py          # Integrações externas (ENEM API, YouTube)
├── content_updater.py      # Atualização automática de conteúdo em background
├── enem_content.py         # Banco expandido de questões e flashcards ENEM
├── themes.py               # 10 temas visuais com paletas de cores
├── requirements.txt        # Dependências do projeto
├── pomodoro_study.db       # Banco de dados SQLite (gerado automaticamente)
└── views/
    ├── app.py              # Shell principal (sidebar + navegação)
    ├── dashboard_view.py   # Dashboard com estatísticas e metas
    ├── pomodoro_view.py    # Timer Pomodoro
    ├── tasks_view.py       # Gerenciamento de tarefas
    ├── study_view.py       # Quizzes e vídeos educativos
    ├── flashcards_view.py  # Flashcards com repetição espaçada (SM-2)
    ├── shorts_view.py      # Feed de shorts educativos (estilo TikTok)
    ├── history_view.py     # Histórico de sessões
    ├── settings_view.py    # Configurações do app
    └── login_view.py       # Login e cadastro
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/natanfts/ProjetoExtenss-o1.git
cd ProjetoExtenss-o1

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
python main.py
```

---

## 📦 Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| `customtkinter` | ≥ 5.2.0 | Interface gráfica moderna |
| `Pillow` | ≥ 10.0.0 | Processamento de imagens (thumbnails) |
| `requests` | ≥ 2.31.0 | Requisições HTTP (APIs) |
| `CTkMessagebox` | ≥ 2.5 | Caixas de diálogo customizadas |
| `youtube-search-python` | ≥ 1.6.6 | Busca de vídeos no YouTube |
| `httpx` | < 0.28 | Cliente HTTP (compatibilidade) |

---

## 📊 Conteúdo ENEM

O app cobre **todas as 5 áreas** do ENEM com conteúdo abrangente:

| Área | Questões | Flashcards | Queries de Vídeo |
|------|----------|------------|-------------------|
| Linguagens | 35+ | 12+ | 20+ |
| Matemática | 40+ | 14+ | 25+ |
| Ciências da Natureza | 45+ | 18+ | 30+ |
| Ciências Humanas | 35+ | 12+ | 20+ |
| Redação | 16+ | 6+ | 10+ |
| **Total** | **171** | **62** | **105** |

---

## 🔄 Versionamento

| Versão | Descrição |
|--------|-----------|
| **v1.0** | App Pomodoro de Estudos com Quiz ENEM Real |
| **v2.0** | Gamificação, Dashboard, Flashcards e Metas Diárias |
| **v2.1** | Expansão de conteúdo ENEM + Shorts educativos com feed infinito |

---

## 🛠️ Tecnologias

- **Python 3.11** — Linguagem principal
- **CustomTkinter** — Framework GUI moderno (baseado em Tkinter)
- **SQLite** — Banco de dados local embutido
- **youtube-search-python** — Busca de vídeos sem API key
- **Pillow** — Manipulação de imagens
- **Algoritmo SM-2** — Repetição espaçada nos flashcards

---

## 👤 Autor

**Natan** — [@natanfts](https://github.com/natanfts)

---

## 📄 Licença

Este projeto é de código aberto e foi desenvolvido como projeto de extensão universitária.
