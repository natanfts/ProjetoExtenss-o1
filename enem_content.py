"""
enem_content.py — Banco de conteúdo expandido para o ENEM.

Contém questões, flashcards e queries de vídeo cobrindo TODAS as competências
e habilidades da Matriz de Referência do ENEM nas 5 áreas:
  1. Linguagens, Códigos e suas Tecnologias
  2. Matemática e suas Tecnologias
  3. Ciências da Natureza e suas Tecnologias
  4. Ciências Humanas e suas Tecnologias
  5. Redação
"""

import json

# ══════════════════════════════════════════════════════════════
# ── QUESTÕES EXPANDIDAS ──────────────────────────────────────
# ══════════════════════════════════════════════════════════════
# Formato: (category, subject, topic, question, options_json, correct, explanation, difficulty)

EXPANDED_QUESTIONS = [
    # ╔════════════════════════════════════════════════════════╗
    # ║  1. LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS           ║
    # ╚════════════════════════════════════════════════════════╝

    # ── Funções da Linguagem ─────────────────────────────────
    ("enem", "Linguagens", "Funções da Linguagem",
     "A função da linguagem centrada no emissor, que expressa sentimentos e emoções, é a função:",
     json.dumps(["Referencial", "Emotiva", "Conativa", "Fática"]),
     "Emotiva",
     "A função emotiva (ou expressiva) está centrada no emissor e expressa sentimentos, opiniões e emoções. Usa 1ª pessoa e interjeições.",
     "fácil"),

    ("enem", "Linguagens", "Funções da Linguagem",
     "Qual função da linguagem predomina em textos jornalísticos informativos?",
     json.dumps(["Poética", "Emotiva", "Referencial", "Metalinguística"]),
     "Referencial",
     "A função referencial (ou denotativa) é centrada no referente/contexto. Predomina em textos informativos, científicos e jornalísticos.",
     "fácil"),

    ("enem", "Linguagens", "Funções da Linguagem",
     "'Vote em mim! Compre agora!' — Qual função da linguagem predomina?",
     json.dumps(["Fática", "Metalinguística", "Conativa", "Poética"]),
     "Conativa",
     "A função conativa (ou apelativa) é centrada no receptor. Usa verbos no imperativo e vocativos para persuadir.",
     "fácil"),

    ("enem", "Linguagens", "Funções da Linguagem",
     "Um dicionário é um exemplo de texto com predominância da função:",
     json.dumps(["Referencial", "Metalinguística", "Fática", "Poética"]),
     "Metalinguística",
     "A função metalinguística usa a linguagem para falar da própria linguagem. Dicionários, gramáticas e poemas sobre poesia são exemplos.",
     "médio"),

    # ── Gêneros Textuais ────────────────────────────────────
    ("enem", "Linguagens", "Gêneros Textuais",
     "Qual gênero textual tem como objetivo principal convencer o leitor sobre um ponto de vista?",
     json.dumps(["Narração", "Descrição",
                "Dissertação-argumentativa", "Injunção"]),
     "Dissertação-argumentativa",
     "A dissertação-argumentativa tem como objetivo defender uma tese usando argumentos para convencer o leitor.",
     "fácil"),

    ("enem", "Linguagens", "Gêneros Textuais",
     "Um manual de instruções é um exemplo de texto:",
     json.dumps(["Narrativo", "Descritivo", "Injuntivo", "Argumentativo"]),
     "Injuntivo",
     "Textos injuntivos (ou instrucionais) orientam o leitor a realizar uma ação, como manuais, receitas e bulas.",
     "fácil"),

    ("enem", "Linguagens", "Gêneros Textuais",
     "O editorial de jornal é um gênero textual que pertence ao tipo:",
     json.dumps(["Narrativo", "Descritivo", "Argumentativo", "Expositivo"]),
     "Argumentativo",
     "O editorial apresenta a opinião do jornal sobre um assunto atual, usando argumentação para defender um ponto de vista.",
     "médio"),

    # ── Variação Linguística ─────────────────────────────────
    ("enem", "Linguagens", "Variação Linguística",
     "A variação linguística relacionada à região geográfica do falante é chamada de:",
     json.dumps(["Variação histórica", "Variação diatópica",
                "Variação diastrática", "Variação diafásica"]),
     "Variação diatópica",
     "Variação diatópica (ou regional) é a diferença linguística entre regiões, como sotaques e expressões regionais.",
     "médio"),

    ("enem", "Linguagens", "Variação Linguística",
     "A diferença entre a fala de um médico e a de um pedreiro sobre o mesmo assunto exemplifica a variação:",
     json.dumps(["Diatópica", "Diacrônica", "Diastrática", "Diafásica"]),
     "Diastrática",
     "Variação diastrática (ou social) ocorre entre diferentes grupos sociais, relacionada a classe social, escolaridade e profissão.",
     "médio"),

    ("enem", "Linguagens", "Variação Linguística",
     "Quando uma pessoa usa linguagem formal no trabalho e informal com amigos, trata-se de variação:",
     json.dumps(["Diastrática", "Diatópica", "Diafásica", "Diacrônica"]),
     "Diafásica",
     "Variação diafásica (ou situacional/de registro) ocorre conforme a situação comunicativa — formal ou informal.",
     "médio"),

    # ── Figuras de Linguagem ─────────────────────────────────
    ("enem", "Linguagens", "Figuras de Linguagem",
     "'Aquele homem é um touro!' — Qual figura de linguagem?",
     json.dumps(["Comparação", "Metáfora", "Metonímia", "Hipérbole"]),
     "Metáfora",
     "Metáfora é a comparação implícita (sem 'como' ou 'tal qual'). Atribui-se uma característica de um ser a outro.",
     "fácil"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "'Li Machado de Assis nas férias.' — Qual figura de linguagem?",
     json.dumps(["Metáfora", "Metonímia", "Catacrese", "Antítese"]),
     "Metonímia",
     "Metonímia substitui um termo por outro com relação de contiguidade. Aqui, o autor substitui a obra.",
     "médio"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "'Eu já te disse um milhão de vezes!' — Qual figura de linguagem?",
     json.dumps(["Eufemismo", "Ironia", "Hipérbole", "Litotes"]),
     "Hipérbole",
     "Hipérbole é o exagero intencional para dar ênfase a uma ideia.",
     "fácil"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "'Ele passou desta para melhor.' — Qual figura de linguagem?",
     json.dumps(["Hipérbole", "Eufemismo", "Ironia", "Pleonasmo"]),
     "Eufemismo",
     "Eufemismo suaviza uma expressão desagradável. 'Passou desta para melhor' substitui 'morreu'.",
     "fácil"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "'A vida é curta, a arte é longa.' — Qual figura?",
     json.dumps(["Metáfora", "Paradoxo", "Antítese", "Sinestesia"]),
     "Antítese",
     "Antítese é a oposição de ideias ou palavras contrárias (curta × longa) na mesma construção.",
     "médio"),

    # ── Movimentos Literários ────────────────────────────────
    ("enem", "Linguagens", "Literatura - Movimentos",
     "O Barroco brasileiro teve como principal representante:",
     json.dumps(["Castro Alves", "Padre Antônio Vieira",
                "Álvares de Azevedo", "Gonçalves Dias"]),
     "Padre Antônio Vieira",
     "Padre Antônio Vieira é o principal nome do Barroco brasileiro, com seus famosos Sermões.",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "O Romantismo no Brasil foi inaugurado com a publicação de:",
     json.dumps(["Memórias Póstumas de Brás Cubas",
                "Suspiros Poéticos e Saudades", "Os Sertões", "A Moreninha"]),
     "Suspiros Poéticos e Saudades",
     "Suspiros Poéticos e Saudades (1836), de Gonçalves de Magalhães, é considerado o marco inicial do Romantismo brasileiro.",
     "difícil"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "Qual geração romântica brasileira ficou conhecida como 'mal do século'?",
     json.dumps(["1ª geração", "2ª geração", "3ª geração", "4ª geração"]),
     "2ª geração",
     "A 2ª geração romântica (Ultrarromantismo) se caracteriza pelo pessimismo, egocentrismo e obsessão pela morte. Álvares de Azevedo é seu maior representante.",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "Castro Alves, o 'poeta dos escravos', pertence a qual geração romântica?",
     json.dumps(["1ª geração", "2ª geração", "3ª geração", "Parnasianismo"]),
     "3ª geração",
     "A 3ª geração romântica (Condoreira) tem caráter social e abolicionista. Castro Alves é seu principal representante.",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "O Naturalismo se diferencia do Realismo principalmente por:",
     json.dumps(["Valorizar o subjetivismo", "Usar linguagem rebuscada",
                 "Analisar o ser humano sob visão determinista/científica", "Idealizar os personagens"]),
     "Analisar o ser humano sob visão determinista/científica",
     "O Naturalismo radicaliza o Realismo, usando determinismo biológico, social e ambiental. Aluísio Azevedo é o principal nome no Brasil.",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "O Parnasianismo se caracteriza pela busca de:",
     json.dumps(["Subjetividade", "Engajamento social",
                "Perfeição formal", "Liberdade de expressão"]),
     "Perfeição formal",
     "O Parnasianismo valoriza a 'arte pela arte', com perfeição formal, rimas ricas e vocabulário culto. Olavo Bilac é seu maior representante.",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "A obra 'Grande Sertão: Veredas' é de autoria de:",
     json.dumps(["Graciliano Ramos", "Guimarães Rosa",
                "Jorge Amado", "Érico Veríssimo"]),
     "Guimarães Rosa",
     "Grande Sertão: Veredas (1956) é a obra-prima de Guimarães Rosa, marco da 3ª geração modernista (Geração de 45).",
     "fácil"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "'Vidas Secas' de Graciliano Ramos pertence a qual fase do modernismo?",
     json.dumps(["1ª geração", "2ª geração", "3ª geração", "Pré-Modernismo"]),
     "2ª geração",
     "Vidas Secas (1938) pertence à 2ª geração modernista (1930-45), focada na prosa regionalista e social.",
     "médio"),

    # ── Intertextualidade ────────────────────────────────────
    ("enem", "Linguagens", "Intertextualidade",
     "Quando um texto faz referência direta a outro, citando-o literalmente, temos:",
     json.dumps(["Paródia", "Paráfrase", "Citação", "Alusão"]),
     "Citação",
     "Citação é a referência direta e literal a outro texto, geralmente entre aspas ou com indicação da fonte.",
     "fácil"),

    ("enem", "Linguagens", "Intertextualidade",
     "A paródia se diferencia da paráfrase porque a paródia:",
     json.dumps(["Copia o texto original", "Subverte/critica o texto original",
                 "Apenas resume o original", "Traduz o texto para outra língua"]),
     "Subverte/critica o texto original",
     "A paródia recria o texto original com intenção crítica, humorística ou irônica, subvertendo seu sentido.",
     "médio"),

    # ── Artes ─────────────────────────────────────────────
    ("enem", "Linguagens", "Artes",
     "O movimento artístico que buscou representar as impressões visuais através de luz e cor foi o:",
     json.dumps(["Cubismo", "Impressionismo",
                "Expressionismo", "Surrealismo"]),
     "Impressionismo",
     "O Impressionismo (séc. XIX) buscava captar impressões visuais com ênfase na luz e cor. Monet e Renoir são seus maiores nomes.",
     "médio"),

    ("enem", "Linguagens", "Artes",
     "Anita Malfatti e Di Cavalcanti são artistas ligados a qual movimento?",
     json.dumps(["Barroco", "Neoclassicismo",
                "Modernismo brasileiro", "Pop Art"]),
     "Modernismo brasileiro",
     "Anita Malfatti e Di Cavalcanti foram protagonistas do Modernismo brasileiro e da Semana de Arte Moderna de 1922.",
     "fácil"),

    ("enem", "Linguagens", "Artes",
     "A obra 'Abaporu' de Tarsila do Amaral representa qual movimento artístico?",
     json.dumps(["Cubismo", "Surrealismo", "Antropofagia", "Expressionismo"]),
     "Antropofagia",
     "Abaporu (1928) inspirou o Manifesto Antropófago de Oswald de Andrade, propondo 'devorar' a cultura europeia e criar arte brasileira.",
     "médio"),

    # ── Comunicação e Tecnologia ─────────────────────────────
    ("enem", "Linguagens", "Comunicação e Tecnologia",
     "O fenômeno das fake news está diretamente relacionado à falta de:",
     json.dumps(["Tecnologia", "Letramento midiático",
                "Censura", "Redes sociais"]),
     "Letramento midiático",
     "Letramento midiático é a capacidade de avaliar criticamente informações nos meios de comunicação, essencial contra fake news.",
     "médio"),

    # ╔════════════════════════════════════════════════════════╗
    # ║  2. MATEMÁTICA E SUAS TECNOLOGIAS                    ║
    # ╚════════════════════════════════════════════════════════╝

    # ── Razão e Proporção / Regra de Três ────────────────────
    ("enem", "Matemática", "Razão e Proporção",
     "Se 5 operários fazem uma obra em 12 dias, em quantos dias 10 operários farão a mesma obra?",
     json.dumps(["24 dias", "6 dias", "10 dias", "8 dias"]),
     "6 dias",
     "Grandezas inversamente proporcionais: 5×12 = 10×x → x = 60/10 = 6 dias.",
     "fácil"),

    ("enem", "Matemática", "Razão e Proporção",
     "Um mapa está na escala 1:50.000. A distância real entre duas cidades que no mapa estão a 3 cm é:",
     json.dumps(["150 m", "1.500 m", "15.000 m", "150.000 m"]),
     "1.500 m",
     "3 cm × 50.000 = 150.000 cm = 1.500 m = 1,5 km.",
     "médio"),

    ("enem", "Matemática", "Regra de Três",
     "Se 3 kg de carne custam R$ 75,00, quanto custam 5 kg?",
     json.dumps(["R$ 100,00", "R$ 125,00", "R$ 150,00", "R$ 115,00"]),
     "R$ 125,00",
     "Regra de três direta: 3/75 = 5/x → x = (75×5)/3 = R$ 125,00.",
     "fácil"),

    # ── Equações ─────────────────────────────────────────────
    ("enem", "Matemática", "Equações",
     "As raízes da equação x² - 5x + 6 = 0 são:",
     json.dumps(["1 e 6", "2 e 3", "-2 e -3", "1 e 5"]),
     "2 e 3",
     "x² - 5x + 6 = 0. Δ = 25-24 = 1. x = (5±1)/2 → x₁=3, x₂=2.",
     "fácil"),

    ("enem", "Matemática", "Equações",
     "Qual o valor de x na equação 3x + 7 = 22?",
     json.dumps(["3", "5", "7", "4"]),
     "5",
     "3x + 7 = 22 → 3x = 15 → x = 5.",
     "fácil"),

    ("enem", "Matemática", "Equações",
     "O discriminante (Δ) da equação 2x² + 4x + 2 = 0 vale:",
     json.dumps(["0", "4", "8", "-4"]),
     "0",
     "Δ = b² - 4ac = 16 - 16 = 0. Quando Δ = 0, a equação tem duas raízes reais iguais.",
     "médio"),

    # ── Sistemas de Equações ─────────────────────────────────
    ("enem", "Matemática", "Sistemas de Equações",
     "No sistema { x + y = 10 ; x - y = 4 }, o valor de x é:",
     json.dumps(["3", "5", "7", "8"]),
     "7",
     "Somando as equações: 2x = 14 → x = 7 (e y = 3).",
     "fácil"),

    # ── Análise Combinatória ─────────────────────────────────
    ("enem", "Matemática", "Análise Combinatória",
     "De quantas maneiras 5 pessoas podem se sentar em 5 cadeiras?",
     json.dumps(["25", "120", "60", "24"]),
     "120",
     "Permutação simples: P(5) = 5! = 5×4×3×2×1 = 120.",
     "fácil"),

    ("enem", "Matemática", "Análise Combinatória",
     "Uma combinação de 6 elementos tomados 2 a 2, C(6,2), vale:",
     json.dumps(["12", "15", "30", "36"]),
     "15",
     "C(6,2) = 6!/(2!×4!) = (6×5)/2 = 15.",
     "médio"),

    ("enem", "Matemática", "Análise Combinatória",
     "Quantos anagramas tem a palavra AMOR?",
     json.dumps(["12", "24", "16", "8"]),
     "24",
     "AMOR tem 4 letras distintas: P(4) = 4! = 24 anagramas.",
     "fácil"),

    # ── Progressões ──────────────────────────────────────────
    ("enem", "Matemática", "Progressões",
     "Na PA (2, 5, 8, 11, ...), qual é o 10° termo?",
     json.dumps(["27", "29", "30", "32"]),
     "29",
     "aₙ = a₁ + (n-1)r = 2 + 9×3 = 2 + 27 = 29.",
     "fácil"),

    ("enem", "Matemática", "Progressões",
     "Na PG (3, 6, 12, 24, ...), qual é a razão?",
     json.dumps(["2", "3", "4", "6"]),
     "2",
     "Razão da PG: q = a₂/a₁ = 6/3 = 2.",
     "fácil"),

    # ── Trigonometria ────────────────────────────────────────
    ("enem", "Matemática", "Trigonometria",
     "O seno de 30° vale:",
     json.dumps(["1/2", "√2/2", "√3/2", "1"]),
     "1/2",
     "sen 30° = 1/2. É um dos valores notáveis da trigonometria.",
     "fácil"),

    ("enem", "Matemática", "Trigonometria",
     "Em um triângulo retângulo, o seno de um ângulo é igual a:",
     json.dumps(["Cateto adjacente / hipotenusa", "Cateto oposto / hipotenusa",
                 "Cateto oposto / cateto adjacente", "Hipotenusa / cateto oposto"]),
     "Cateto oposto / hipotenusa",
     "sen α = cateto oposto / hipotenusa. É a razão trigonométrica fundamental.",
     "fácil"),

    ("enem", "Matemática", "Trigonometria",
     "A identidade fundamental da trigonometria afirma que:",
     json.dumps(["sen²x + cos²x = 1", "sen²x - cos²x = 1",
                "senx × cosx = 1", "senx + cosx = 1"]),
     "sen²x + cos²x = 1",
     "A identidade trigonométrica fundamental é sen²x + cos²x = 1, válida para qualquer ângulo x.",
     "médio"),

    # ── Geometria Espacial ───────────────────────────────────
    ("enem", "Matemática", "Geometria Espacial",
     "O volume de um cilindro de raio 5 cm e altura 10 cm é:",
     json.dumps(["250π cm³", "500π cm³", "100π cm³", "200π cm³"]),
     "250π cm³",
     "V = π × r² × h = π × 25 × 10 = 250π cm³.",
     "médio"),

    ("enem", "Matemática", "Geometria Espacial",
     "O volume de uma pirâmide é dado pela fórmula:",
     json.dumps(["V = A_base × h", "V = (A_base × h)/3",
                "V = (A_base × h)/2", "V = π × r² × h"]),
     "V = (A_base × h)/3",
     "O volume da pirâmide é 1/3 do produto da área da base pela altura.",
     "médio"),

    ("enem", "Matemática", "Geometria Espacial",
     "Um cone tem raio da base 3 cm e altura 4 cm. Sua geratriz mede:",
     json.dumps(["5 cm", "7 cm", "6 cm", "4,5 cm"]),
     "5 cm",
     "Pelo Teorema de Pitágoras: g² = r² + h² = 9 + 16 = 25 → g = 5 cm.",
     "médio"),

    # ── Geometria Analítica ──────────────────────────────────
    ("enem", "Matemática", "Geometria Analítica",
     "A distância entre os pontos A(1, 2) e B(4, 6) é:",
     json.dumps(["5", "7", "3", "4"]),
     "5",
     "d = √[(4-1)² + (6-2)²] = √[9+16] = √25 = 5.",
     "médio"),

    ("enem", "Matemática", "Geometria Analítica",
     "A equação y = 2x + 3 representa uma reta com coeficiente angular:",
     json.dumps(["3", "2", "5", "1"]),
     "2",
     "Na equação y = mx + n, m é o coeficiente angular (inclinação). Aqui, m = 2.",
     "fácil"),

    # ── Logaritmos ───────────────────────────────────────────
    ("enem", "Matemática", "Logaritmos",
     "O valor de log₂(8) é:",
     json.dumps(["2", "3", "4", "8"]),
     "3",
     "log₂(8) = x → 2ˣ = 8 → 2³ = 8 → x = 3.",
     "fácil"),

    ("enem", "Matemática", "Logaritmos",
     "Se log(a) = 2 e log(b) = 3, então log(a×b) vale:",
     json.dumps(["5", "6", "1", "23"]),
     "5",
     "Propriedade: log(a×b) = log(a) + log(b) = 2 + 3 = 5.",
     "médio"),

    # ── Matemática Financeira ────────────────────────────────
    ("enem", "Matemática", "Matemática Financeira",
     "Um capital de R$ 1.000 aplicado a juros simples de 5% ao mês durante 4 meses renderá:",
     json.dumps(["R$ 200", "R$ 150", "R$ 250", "R$ 100"]),
     "R$ 200",
     "Juros simples: J = C × i × t = 1000 × 0,05 × 4 = R$ 200.",
     "fácil"),

    ("enem", "Matemática", "Matemática Financeira",
     "A diferença entre juros simples e compostos é que nos compostos:",
     json.dumps(["Os juros são menores", "Não há rendimento",
                "Os juros incidem sobre juros", "A taxa é fixa"]),
     "Os juros incidem sobre juros",
     "Nos juros compostos, os juros de cada período incidem sobre o montante acumulado (juros sobre juros).",
     "fácil"),

    # ── Grandezas e Medidas / Gráficos ──────────────────────
    ("enem", "Matemática", "Grandezas e Medidas",
     "1 m³ equivale a quantos litros?",
     json.dumps(["10 litros", "100 litros", "1.000 litros", "10.000 litros"]),
     "1.000 litros",
     "1 m³ = 1.000 litros (1 dm³ = 1 litro).",
     "fácil"),

    ("enem", "Matemática", "Leitura de Gráficos",
     "Em um gráfico de setores (pizza), um setor de 90° representa qual fração do total?",
     json.dumps(["1/2", "1/3", "1/4", "1/6"]),
     "1/4",
     "O círculo total tem 360°. 90°/360° = 1/4 = 25% do total.",
     "fácil"),

    # ╔════════════════════════════════════════════════════════╗
    # ║  3. CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS          ║
    # ╚════════════════════════════════════════════════════════╝

    # ── Física – Óptica ──────────────────────────────────────
    ("enem", "Ciências da Natureza", "Física - Óptica",
     "A decomposição da luz branca em cores ao passar por um prisma chama-se:",
     json.dumps(["Reflexão", "Refração", "Dispersão", "Difração"]),
     "Dispersão",
     "A dispersão da luz branca em suas cores componentes (espectro visível) ocorre porque cada cor tem um índice de refração diferente.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Física - Óptica",
     "A miragem observada em estradas quentes é causada por:",
     json.dumps(["Reflexão da luz", "Refração da luz em camadas de ar",
                "Difração da luz", "Absorção da luz"]),
     "Refração da luz em camadas de ar",
     "A miragem ocorre pela refração da luz ao passar por camadas de ar com diferentes temperaturas e densidades.",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Óptica",
     "Espelhos côncavos são utilizados em:",
     json.dumps(["Retrovisores de carro", "Faróis de carro",
                "Espelhos de lojas", "Lentes de contato"]),
     "Faróis de carro",
     "Espelhos côncavos convergem a luz, por isso são usados em faróis, holofotes e telescópios refletores.",
     "médio"),

    # ── Física – Ondulatória ─────────────────────────────────
    ("enem", "Ciências da Natureza", "Física - Ondulatória",
     "A velocidade de uma onda é dada pela fórmula:",
     json.dumps(["v = λ × f", "v = λ / f", "v = f / λ", "v = λ + f"]),
     "v = λ × f",
     "Velocidade da onda = comprimento de onda (λ) × frequência (f).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Física - Ondulatória",
     "O efeito Doppler explica por que:",
     json.dumps(["O som some com a distância", "A sirene de uma ambulância muda de tom ao se aproximar/afastar",
                 "O eco ocorre", "O som não se propaga no vácuo"]),
     "A sirene de uma ambulância muda de tom ao se aproximar/afastar",
     "O efeito Doppler é a mudança de frequência percebida quando há movimento relativo entre fonte e observador.",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Ondulatória",
     "O som NÃO se propaga no:",
     json.dumps(["Ar", "Água", "Ferro", "Vácuo"]),
     "Vácuo",
     "O som é uma onda mecânica e precisa de um meio material para se propagar. Não se propaga no vácuo.",
     "fácil"),

    # ── Física – Eletricidade ────────────────────────────────
    ("enem", "Ciências da Natureza", "Física - Eletricidade",
     "A unidade de medida da potência elétrica é:",
     json.dumps(["Ampère", "Volt", "Watt", "Ohm"]),
     "Watt",
     "Potência elétrica (P) é medida em Watts (W). P = V × I.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Física - Eletricidade",
     "Um chuveiro elétrico de 5.500 W ligado durante 15 minutos consome:",
     json.dumps(["1,375 kWh", "5,5 kWh", "0,825 kWh", "82,5 kWh"]),
     "1,375 kWh",
     "E = P × t = 5500W × 0,25h = 1375 Wh = 1,375 kWh.",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Eletricidade",
     "Em um circuito em série, a corrente elétrica é:",
     json.dumps(["Diferente em cada resistor",
                "Igual em todos os pontos", "Zero", "Infinita"]),
     "Igual em todos os pontos",
     "Em circuitos em série, a corrente é a mesma em todos os componentes, pois há apenas um caminho para ela.",
     "fácil"),

    # ── Física – Energia e Trabalho ──────────────────────────
    ("enem", "Ciências da Natureza", "Física - Energia",
     "A energia potencial gravitacional de um corpo é calculada por:",
     json.dumps(["Ep = m×v²/2", "Ep = m×g×h", "Ep = F×d", "Ep = k×x²/2"]),
     "Ep = m×g×h",
     "Energia potencial gravitacional: Ep = massa × gravidade × altura.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Física - Energia",
     "O Teorema da Conservação de Energia Mecânica afirma que:",
     json.dumps(["A energia sempre diminui", "Energia cinética = Energia potencial",
                 "Em sistemas conservativos, E_mecânica = constante", "A energia pode ser criada"]),
     "Em sistemas conservativos, E_mecânica = constante",
     "Em sistemas onde só atuam forças conservativas, a soma Ec + Ep permanece constante.",
     "médio"),

    # ── Física – Hidrostática ────────────────────────────────
    ("enem", "Ciências da Natureza", "Física - Hidrostática",
     "O Princípio de Arquimedes afirma que um corpo imerso em um fluido recebe:",
     json.dumps(["Uma força para baixo", "Um empuxo igual ao peso do fluido deslocado",
                 "Uma força magnética", "Uma pressão uniforme"]),
     "Um empuxo igual ao peso do fluido deslocado",
     "Princípio de Arquimedes: E = ρ_fluido × V_deslocado × g. O empuxo é igual ao peso do fluido deslocado.",
     "médio"),

    # ── Química – Ligações Químicas ──────────────────────────
    ("enem", "Ciências da Natureza", "Química - Ligações Químicas",
     "A ligação entre sódio (Na) e cloro (Cl) no NaCl é do tipo:",
     json.dumps(["Covalente", "Iônica", "Metálica", "Van der Waals"]),
     "Iônica",
     "Ligação iônica ocorre entre metal e não-metal, por transferência de elétrons. Na (metal) doa 1 elétron para Cl (não-metal).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Ligações Químicas",
     "A água (H₂O) possui ligação do tipo:",
     json.dumps(["Iônica", "Covalente polar", "Covalente apolar", "Metálica"]),
     "Covalente polar",
     "H₂O possui ligação covalente polar: os átomos compartilham elétrons, mas o oxigênio é mais eletronegativo.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Ligações Químicas",
     "As ligações de hidrogênio entre moléculas de água explicam:",
     json.dumps(["Sua baixa temperatura de ebulição", "Sua alta temperatura de ebulição",
                 "Sua cor azul", "Seu baixo calor específico"]),
     "Sua alta temperatura de ebulição",
     "Ligações de hidrogênio são intermoleculares fortes, elevando a temperatura de ebulição da água para 100°C.",
     "médio"),

    # ── Química – Soluções ───────────────────────────────────
    ("enem", "Ciências da Natureza", "Química - Soluções",
     "Uma solução com concentração de 10 g/L significa que em 1 litro há:",
     json.dumps(["10 mL de soluto", "10 g de soluto",
                "10 mol de soluto", "10% de soluto"]),
     "10 g de soluto",
     "Concentração comum (C) = massa do soluto / volume da solução. C = 10 g/L → 10 g em 1 L.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Soluções",
     "Ao adicionar sal em água e agitar até dissolver, o sal é o:",
     json.dumps(["Solvente", "Soluto", "Solução", "Mistura heterogênea"]),
     "Soluto",
     "Soluto é a substância dissolvida (sal). Solvente é o que dissolve (água). Juntos formam a solução.",
     "fácil"),

    # ── Química – Eletroquímica ──────────────────────────────
    ("enem", "Ciências da Natureza", "Química - Eletroquímica",
     "Em uma pilha eletroquímica, o ânodo é o eletrodo onde ocorre:",
     json.dumps(["Redução", "Oxidação", "Neutralização", "Sublimação"]),
     "Oxidação",
     "No ânodo ocorre oxidação (perda de elétrons). No cátodo ocorre redução (ganho de elétrons). Macete: ÂNODO = OXIDAÇÃO.",
     "médio"),

    ("enem", "Ciências da Natureza", "Química - Eletroquímica",
     "A corrosão do ferro (ferrugem) é um processo de:",
     json.dumps(["Redução do ferro", "Oxidação do ferro",
                "Neutralização", "Decomposição"]),
     "Oxidação do ferro",
     "A ferrugem (Fe₂O₃) é formada pela oxidação do ferro na presença de oxigênio e umidade.",
     "fácil"),

    # ── Química – Orgânica ───────────────────────────────────
    ("enem", "Ciências da Natureza", "Química - Orgânica",
     "O metano (CH₄) é o hidrocarboneto mais simples da classe dos:",
     json.dumps(["Alcenos", "Alcinos", "Alcanos", "Cicloalcanos"]),
     "Alcanos",
     "Alcanos são hidrocarbonetos de cadeia aberta com apenas ligações simples. Fórmula geral: CₙH₂ₙ₊₂.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Orgânica",
     "O etanol (C₂H₅OH) pertence à função orgânica dos:",
     json.dumps(["Ácidos carboxílicos", "Ésteres", "Aldeídos", "Álcoois"]),
     "Álcoois",
     "Álcoois possuem o grupo funcional -OH (hidroxila) ligado a carbono saturado.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Orgânica",
     "A isomeria que ocorre entre etanol e éter dimetílico é chamada de:",
     json.dumps(["Isomeria de cadeia", "Isomeria de função",
                "Isomeria de posição", "Isomeria geométrica"]),
     "Isomeria de função",
     "Isomeria de função: mesma fórmula molecular, mas funções orgânicas diferentes (álcool × éter).",
     "difícil"),

    # ── Química – Termoquímica ───────────────────────────────
    ("enem", "Ciências da Natureza", "Química - Termoquímica",
     "Uma reação exotérmica é aquela que:",
     json.dumps(["Absorve calor", "Libera calor",
                "Não troca calor", "Absorve luz"]),
     "Libera calor",
     "Reações exotérmicas liberam calor para o ambiente (ΔH < 0). Exemplo: combustão.",
     "fácil"),

    # ── Química – Cinética Química ───────────────────────────
    ("enem", "Ciências da Natureza", "Química - Cinética",
     "Qual fator NÃO aumenta a velocidade de uma reação química?",
     json.dumps(["Aumento de temperatura", "Uso de catalisador",
                "Diminuição da concentração", "Aumento da superfície de contato"]),
     "Diminuição da concentração",
     "A diminuição da concentração dos reagentes reduz a velocidade. Os outros fatores (temperatura, catalisador, superfície de contato) aumentam.",
     "médio"),

    # ── Química – Equilíbrio Químico ─────────────────────────
    ("enem", "Ciências da Natureza", "Química - Equilíbrio",
     "Segundo o Princípio de Le Chatelier, ao aumentar a temperatura de uma reação exotérmica em equilíbrio:",
     json.dumps(["O equilíbrio desloca para os produtos", "O equilíbrio desloca para os reagentes",
                 "Não há alteração", "A reação para"]),
     "O equilíbrio desloca para os reagentes",
     "Le Chatelier: ao aquecer uma reação exotérmica, o equilíbrio se desloca no sentido endotérmico (reagentes).",
     "difícil"),

    # ── Química – Ambiental ──────────────────────────────────
    ("enem", "Ciências da Natureza", "Química - Ambiental",
     "O efeito estufa é intensificado principalmente pela emissão de:",
     json.dumps(["Oxigênio (O₂)", "Nitrogênio (N₂)",
                "Gás carbônico (CO₂)", "Hélio (He)"]),
     "Gás carbônico (CO₂)",
     "O CO₂ é o principal gás estufa emitido por atividades humanas (queima de combustíveis fósseis).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Química - Ambiental",
     "A chuva ácida é causada principalmente pela presença de quais gases na atmosfera?",
     json.dumps(["CO₂ e O₂", "SO₂ e NOₓ", "N₂ e O₂", "CH₄ e H₂"]),
     "SO₂ e NOₓ",
     "Chuva ácida: SO₂ e NOₓ reagem com vapor d'água formando H₂SO₄ e HNO₃. pH < 5,6.",
     "médio"),

    # ── Biologia – Evolução ──────────────────────────────────
    ("enem", "Ciências da Natureza", "Biologia - Evolução",
     "A teoria da seleção natural foi proposta por:",
     json.dumps(["Lamarck", "Mendel", "Darwin", "Pasteur"]),
     "Darwin",
     "Charles Darwin propôs a teoria da seleção natural em 'A Origem das Espécies' (1859).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Biologia - Evolução",
     "Segundo Lamarck, as girafas teriam pescoços longos devido a:",
     json.dumps(["Mutação genética", "Seleção natural",
                "Uso e desuso / herança de caracteres adquiridos", "Especiação"]),
     "Uso e desuso / herança de caracteres adquiridos",
     "Lamarck propôs a Lei do Uso e Desuso e a herança de caracteres adquiridos (teoria hoje refutada).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Biologia - Evolução",
     "Estruturas homólogas indicam:",
     json.dumps(["Mesma função", "Ancestral comum",
                "Convergência evolutiva", "Mutação recente"]),
     "Ancestral comum",
     "Estruturas homólogas têm mesma origem embrionária mas podem ter funções diferentes, indicando ancestral comum.",
     "médio"),

    # ── Biologia – Fisiologia Humana ─────────────────────────
    ("enem", "Ciências da Natureza", "Biologia - Fisiologia",
     "A troca gasosa nos pulmões ocorre nos:",
     json.dumps(["Brônquios", "Bronquíolos", "Alvéolos", "Traqueia"]),
     "Alvéolos",
     "Nos alvéolos pulmonares ocorre a hematose: troca de CO₂ (sangue → alvéolo) por O₂ (alvéolo → sangue).",
     "fácil"),

    ("enem", "Ciências da Natureza", "Biologia - Fisiologia",
     "A insulina é produzida pelo pâncreas e tem como função principal:",
     json.dumps(["Aumentar a glicemia", "Reduzir a glicemia",
                "Digerir proteínas", "Produzir bile"]),
     "Reduzir a glicemia",
     "A insulina reduz a glicemia ao facilitar a entrada de glicose nas células. Sua deficiência causa diabetes.",
     "fácil"),

    ("enem", "Ciências da Natureza", "Biologia - Fisiologia",
     "O órgão responsável pela filtração do sangue e produção de urina é:",
     json.dumps(["Fígado", "Baço", "Rim", "Pâncreas"]),
     "Rim",
     "Os rins filtram o sangue, eliminando resíduos metabólicos na forma de urina. A unidade funcional é o néfron.",
     "fácil"),

    # ── Biologia – Biotecnologia ─────────────────────────────
    ("enem", "Ciências da Natureza", "Biologia - Biotecnologia",
     "A técnica de produzir organismos geneticamente modificados (OGMs) utiliza:",
     json.dumps(["Seleção natural",
                "Engenharia genética / DNA recombinante", "Especiação", "Mitose"]),
     "Engenharia genética / DNA recombinante",
     "Organismos transgênicos são produzidos pela inserção de genes de outras espécies via DNA recombinante.",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Biotecnologia",
     "A PCR (Reação em Cadeia da Polimerase) é usada para:",
     json.dumps(["Produzir proteínas", "Amplificar fragmentos de DNA",
                "Clonar organismos", "Produzir vacinas"]),
     "Amplificar fragmentos de DNA",
     "A PCR multiplica rapidamente segmentos específicos de DNA. É essencial em testes genéticos, forense e diagnósticos.",
     "difícil"),

    # ── Biologia – Ecologia (expandido) ──────────────────────
    ("enem", "Ciências da Natureza", "Biologia - Ecologia",
     "A relação ecológica em que uma espécie se beneficia sem prejudicar a outra é chamada de:",
     json.dumps(["Parasitismo", "Comensalismo", "Predação", "Competição"]),
     "Comensalismo",
     "No comensalismo, uma espécie se beneficia (comensal) sem causar prejuízo ou benefício à outra (hospedeiro).",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Ecologia",
     "A sucessão ecológica que ocorre em um terreno nunca antes colonizado é chamada de:",
     json.dumps(["Secundária", "Primária", "Terciária", "Regressiva"]),
     "Primária",
     "Sucessão primária: colonização de ambientes sem vida anterior (rochas nuas, lava solidificada).",
     "médio"),

    # ╔════════════════════════════════════════════════════════╗
    # ║  4. CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS              ║
    # ╚════════════════════════════════════════════════════════╝

    # ── História – Antiguidade ───────────────────────────────
    ("enem", "Ciências Humanas", "História - Antiguidade",
     "A democracia ateniense se diferenciava da democracia moderna porque:",
     json.dumps(["Era representativa", "Era direta e excluía mulheres, escravos e estrangeiros",
                 "Incluía todos os habitantes", "Era uma monarquia"]),
     "Era direta e excluía mulheres, escravos e estrangeiros",
     "Em Atenas, a democracia era direta (cidadãos votavam nas leis), mas excluía mulheres, escravos e metecos.",
     "médio"),

    ("enem", "Ciências Humanas", "História - Antiguidade",
     "O Império Romano do Ocidente caiu em:",
     json.dumps(["1453", "476", "27 a.C.", "395"]),
     "476",
     "A queda do Império Romano do Ocidente em 476 d.C. marca o fim da Idade Antiga e início da Idade Média.",
     "fácil"),

    # ── História – Idade Média ───────────────────────────────
    ("enem", "Ciências Humanas", "História - Idade Média",
     "O sistema econômico predominante na Europa medieval era o:",
     json.dumps(["Capitalismo", "Mercantilismo", "Feudalismo", "Socialismo"]),
     "Feudalismo",
     "O feudalismo baseava-se na posse de terras (feudos), relação de suserania/vassalagem e economia agrária de subsistência.",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Idade Média",
     "As Cruzadas foram expedições militares promovidas pela Igreja com o objetivo principal de:",
     json.dumps(["Descobrir a América", "Reconquistar a Terra Santa",
                "Colonizar a África", "Combater os vikings"]),
     "Reconquistar a Terra Santa",
     "As Cruzadas (séculos XI-XIII) visavam retomar Jerusalém e a Terra Santa do controle muçulmano.",
     "fácil"),

    # ── História – Renascimento e Reforma ────────────────────
    ("enem", "Ciências Humanas", "História - Renascimento",
     "O Renascimento cultural teve como característica principal:",
     json.dumps(["Teocentrismo", "Antropocentrismo e valorização da razão",
                 "Misticismo", "Rejeição da arte"]),
     "Antropocentrismo e valorização da razão",
     "O Renascimento (séc. XIV-XVI) colocou o ser humano no centro (antropocentrismo), valorizando a razão, a ciência e a arte clássica.",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Reforma Protestante",
     "Martinho Lutero iniciou a Reforma Protestante em 1517 com:",
     json.dumps(["A criação do anglicanismo", "As 95 teses contra a venda de indulgências",
                 "A tradução da Bíblia para o inglês", "A fundação da Igreja Calvinista"]),
     "As 95 teses contra a venda de indulgências",
     "Lutero fixou as 95 teses na porta da Igreja de Wittenberg (1517), criticando a venda de indulgências pela Igreja Católica.",
     "fácil"),

    # ── História – Era Vargas ────────────────────────────────
    ("enem", "Ciências Humanas", "História - Era Vargas",
     "O período do Estado Novo de Getúlio Vargas durou de:",
     json.dumps(["1930 a 1935", "1937 a 1945", "1945 a 1950", "1930 a 1945"]),
     "1937 a 1945",
     "O Estado Novo (1937-1945) foi um regime ditatorial de Vargas, com constituição autoritária, censura e centralização do poder.",
     "médio"),

    ("enem", "Ciências Humanas", "História - Era Vargas",
     "A CLT (Consolidação das Leis do Trabalho) foi criada durante o governo de:",
     json.dumps(["Juscelino Kubitschek", "Getúlio Vargas",
                "João Goulart", "Eurico Gaspar Dutra"]),
     "Getúlio Vargas",
     "A CLT foi criada em 1943 por Vargas, consolidando direitos trabalhistas como salário mínimo, férias e jornada de trabalho.",
     "fácil"),

    # ── História – Ditadura Militar ──────────────────────────
    ("enem", "Ciências Humanas", "História - Ditadura Militar",
     "O golpe militar no Brasil aconteceu em:",
     json.dumps(["1960", "1964", "1968", "1970"]),
     "1964",
     "O golpe de 31 de março de 1964 depôs o presidente João Goulart, instaurando a ditadura militar (1964-1985).",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Ditadura Militar",
     "O AI-5, considerado o ato mais repressivo da ditadura, foi decretado em:",
     json.dumps(["1964", "1966", "1968", "1972"]),
     "1968",
     "O AI-5 (dez/1968) fechou o Congresso, suspendeu habeas corpus, permitiu cassações e inaugurou os 'anos de chumbo'.",
     "médio"),

    ("enem", "Ciências Humanas", "História - Ditadura Militar",
     "O processo de redemocratização do Brasil culminou com:",
     json.dumps(["A eleição direta de Tancredo Neves", "As Diretas Já e a eleição indireta de Tancredo",
                 "Um novo golpe militar", "A Constituição de 1967"]),
     "As Diretas Já e a eleição indireta de Tancredo",
     "As Diretas Já (1983-84) foram derrotadas, mas Tancredo Neves foi eleito indiretamente em 1985, encerrando a ditadura.",
     "médio"),

    # ── História – Guerras Mundiais ──────────────────────────
    ("enem", "Ciências Humanas", "História - Guerras Mundiais",
     "A Primeira Guerra Mundial (1914-1918) foi desencadeada pelo:",
     json.dumps(["Ataque a Pearl Harbor", "Assassinato do Arquiduque Francisco Ferdinando",
                 "Invasão da Polônia", "Revolução Russa"]),
     "Assassinato do Arquiduque Francisco Ferdinando",
     "O estopim foi o assassinato de Francisco Ferdinando da Áustria em Sarajevo (1914), num contexto de tensões imperialistas.",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Guerras Mundiais",
     "O Holocausto, durante a Segunda Guerra Mundial, foi o genocídio de:",
     json.dumps(["Cerca de 600 mil pessoas", "Cerca de 6 milhões de judeus",
                 "Apenas soldados", "Cerca de 60 mil pessoas"]),
     "Cerca de 6 milhões de judeus",
     "O Holocausto foi o extermínio sistemático de ~6 milhões de judeus pelos nazistas, além de outras minorias.",
     "fácil"),

    # ── História – Guerra Fria ───────────────────────────────
    ("enem", "Ciências Humanas", "História - Guerra Fria",
     "A Guerra Fria foi o conflito ideológico entre:",
     json.dumps(["Inglaterra e França", "EUA (capitalismo) e URSS (socialismo)",
                 "China e Japão", "Alemanha e Itália"]),
     "EUA (capitalismo) e URSS (socialismo)",
     "A Guerra Fria (1947-1991) foi a disputa entre EUA e URSS por hegemonia mundial, sem confronto militar direto entre eles.",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Guerra Fria",
     "A queda do Muro de Berlim, símbolo do fim da Guerra Fria, ocorreu em:",
     json.dumps(["1985", "1989", "1991", "1993"]),
     "1989",
     "O Muro de Berlim caiu em 9 de novembro de 1989, simbolizando o fim da divisão entre leste e oeste.",
     "fácil"),

    # ── História – Brasil Império ────────────────────────────
    ("enem", "Ciências Humanas", "História - Brasil Império",
     "A Lei Áurea, que aboliu a escravidão no Brasil, foi assinada em:",
     json.dumps(["1822", "1850", "1871", "1888"]),
     "1888",
     "A Lei Áurea foi assinada pela Princesa Isabel em 13 de maio de 1888, libertando todos os escravizados.",
     "fácil"),

    ("enem", "Ciências Humanas", "História - Brasil Império",
     "O Primeiro Reinado (1822-1831) foi governado por:",
     json.dumps(["Dom Pedro II", "Dom Pedro I",
                "Marechal Deodoro", "José Bonifácio"]),
     "Dom Pedro I",
     "Dom Pedro I governou o Brasil no Primeiro Reinado, desde a Independência (1822) até sua abdicação (1831).",
     "fácil"),

    # ── Geografia – Clima ────────────────────────────────────
    ("enem", "Ciências Humanas", "Geografia - Clima",
     "O clima predominante na região Norte do Brasil é:",
     json.dumps(["Semiárido", "Tropical", "Equatorial", "Subtropical"]),
     "Equatorial",
     "O clima equatorial tem temperaturas altas e chuvas abundantes o ano todo. Predomina na Amazônia.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Clima",
     "O fenômeno El Niño provoca no Brasil:",
     json.dumps(["Mais chuvas no Sul e secas no Norte/Nordeste", "Secas no Sul e chuvas no Nordeste",
                 "Neve em todo o país", "Nenhuma alteração climática"]),
     "Mais chuvas no Sul e secas no Norte/Nordeste",
     "O El Niño aquece as águas do Pacífico, causando mais chuvas no Sul e secas no Norte/Nordeste do Brasil.",
     "médio"),

    # ── Geografia – Hidrografia ──────────────────────────────
    ("enem", "Ciências Humanas", "Geografia - Hidrografia",
     "Qual é o rio mais extenso do Brasil e do mundo?",
     json.dumps(["Rio São Francisco", "Rio Paraná",
                "Rio Amazonas", "Rio Nilo"]),
     "Rio Amazonas",
     "O Rio Amazonas é o mais extenso (~6.992 km) e o de maior vazão do mundo.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Hidrografia",
     "A transposição do Rio São Francisco tem como objetivo:",
     json.dumps(["Gerar energia elétrica", "Levar água ao Semiárido nordestino",
                 "Irrigar o Sul do país", "Construir hidrovias"]),
     "Levar água ao Semiárido nordestino",
     "A transposição do São Francisco visa distribuir água para regiões secas do Nordeste, beneficiando milhões de pessoas.",
     "fácil"),

    # ── Geografia – Geopolítica ──────────────────────────────
    ("enem", "Ciências Humanas", "Geografia - Geopolítica",
     "O BRICS é formado por:",
     json.dumps(["Brasil, Rússia, Índia, China e África do Sul", "Brasil, Romênia, Itália, Canadá e Suécia",
                 "Bolívia, Rússia, Irlanda, Chile e Suíça", "Brasil, Rússia, Indonésia, Colômbia e Singapura"]),
     "Brasil, Rússia, Índia, China e África do Sul",
     "O BRICS é um grupo de economias emergentes: Brasil, Rússia, Índia, China e África do Sul (e mais recentes membros).",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Geopolítica",
     "A ONU (Organização das Nações Unidas) foi criada em:",
     json.dumps(["1919", "1939", "1945", "1948"]),
     "1945",
     "A ONU foi fundada em 24 de outubro de 1945, após a 2ª Guerra Mundial, para manter a paz e a segurança internacionais.",
     "fácil"),

    # ── Geografia – Meio Ambiente ────────────────────────────
    ("enem", "Ciências Humanas", "Geografia - Meio Ambiente",
     "O desmatamento da Amazônia contribui para:",
     json.dumps(["Redução do efeito estufa", "Aumento da biodiversidade",
                 "Aquecimento global e perda de biodiversidade", "Diminuição das chuvas no Norte apenas"]),
     "Aquecimento global e perda de biodiversidade",
     "O desmatamento libera CO₂, reduz a absorção de carbono, destrói habitats e altera o ciclo hidrológico.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Meio Ambiente",
     "O Protocolo de Kyoto (1997) estabeleceu metas para:",
     json.dumps(["Reduzir o desmatamento", "Reduzir emissões de gases do efeito estufa",
                 "Proteger a camada de ozônio", "Preservar os oceanos"]),
     "Reduzir emissões de gases do efeito estufa",
     "O Protocolo de Kyoto estabeleceu metas de redução de emissões de gases do efeito estufa para países industrializados.",
     "médio"),

    # ── Geografia – Energia ──────────────────────────────────
    ("enem", "Ciências Humanas", "Geografia - Energia",
     "A principal fonte de energia elétrica no Brasil é:",
     json.dumps(["Termoelétrica", "Eólica", "Hidrelétrica", "Nuclear"]),
     "Hidrelétrica",
     "Cerca de 65% da matriz elétrica brasileira é de origem hidrelétrica, graças ao grande potencial hídrico do país.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Energia",
     "A energia eólica utiliza como recurso natural:",
     json.dumps(["A água", "O sol", "O vento", "O calor da Terra"]),
     "O vento",
     "Energia eólica converte a energia cinética dos ventos em eletricidade através de aerogeradores.",
     "fácil"),

    # ── Geografia – Agropecuária e Industrialização ──────────
    ("enem", "Ciências Humanas", "Geografia - Agropecuária",
     "O agronegócio brasileiro se destaca mundialmente na exportação de:",
     json.dumps(["Trigo e centeio", "Soja, carne bovina e café",
                 "Arroz e milho apenas", "Produtos industrializados"]),
     "Soja, carne bovina e café",
     "O Brasil é um dos maiores exportadores mundiais de soja, carne bovina, café, suco de laranja e açúcar.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Industrialização",
     "A concentração industrial brasileira historicamente se deu na região:",
     json.dumps(["Norte", "Nordeste", "Sudeste", "Centro-Oeste"]),
     "Sudeste",
     "O Sudeste, especialmente São Paulo, concentra a maior parte do parque industrial brasileiro desde o início da industrialização.",
     "fácil"),

    # ── Geografia – Migração e Desigualdade ──────────────────
    ("enem", "Ciências Humanas", "Geografia - Migração",
     "O êxodo rural é a migração do:",
     json.dumps(["Centro para a periferia", "Campo para a cidade",
                 "Cidade para o campo", "País para o exterior"]),
     "Campo para a cidade",
     "Êxodo rural é a migração em massa do campo para as cidades, intensificada no Brasil a partir de 1950.",
     "fácil"),

    ("enem", "Ciências Humanas", "Geografia - Desigualdade Social",
     "O Índice de Gini mede:",
     json.dumps(["O PIB do país", "A desigualdade de renda",
                "O IDH", "A taxa de desemprego"]),
     "A desigualdade de renda",
     "O coeficiente de Gini varia de 0 (igualdade perfeita) a 1 (desigualdade máxima). O Brasil tem um dos maiores do mundo.",
     "médio"),

    # ── Filosofia (expandido) ────────────────────────────────
    ("enem", "Ciências Humanas", "Filosofia - Moderna",
     "'Penso, logo existo' é a frase célebre de:",
     json.dumps(["Kant", "Descartes", "Hegel", "Locke"]),
     "Descartes",
     "René Descartes (1596-1650) fundou o racionalismo moderno. O 'Cogito ergo sum' é a base de sua filosofia.",
     "fácil"),

    ("enem", "Ciências Humanas", "Filosofia - Moderna",
     "Kant afirmava que o conhecimento depende de:",
     json.dumps(["Apenas da experiência", "Apenas da razão",
                 "Da união entre experiência e razão", "Da fé"]),
     "Da união entre experiência e razão",
     "Kant propôs que o conhecimento nasce da experiência (empirismo) organizada pelas categorias da razão (racionalismo).",
     "médio"),

    ("enem", "Ciências Humanas", "Filosofia - Contemporânea",
     "O existencialismo de Sartre afirma que:",
     json.dumps(["A essência precede a existência", "A existência precede a essência",
                 "Deus determina nosso destino", "O ser humano não é livre"]),
     "A existência precede a essência",
     "Para Sartre, primeiro existimos, depois nos definimos. O ser humano é condenado a ser livre.",
     "médio"),

    ("enem", "Ciências Humanas", "Filosofia - Contemporânea",
     "A Escola de Frankfurt é conhecida por desenvolver a:",
     json.dumps(["Filosofia analítica", "Teoria Crítica",
                "Fenomenologia", "Filosofia da linguagem"]),
     "Teoria Crítica",
     "A Escola de Frankfurt (Adorno, Horkheimer, Marcuse, Habermas) desenvolveu a Teoria Crítica da sociedade capitalista.",
     "difícil"),

    ("enem", "Ciências Humanas", "Filosofia - Ética",
     "A ética aristotélica é baseada na busca do(a):",
     json.dumps(["Prazer imediato", "Dever moral",
                "Virtude e felicidade (eudaimonia)", "Utilidade"]),
     "Virtude e felicidade (eudaimonia)",
     "Para Aristóteles, a ética visa a eudaimonia (felicidade/bem-estar) através do exercício das virtudes.",
     "médio"),

    # ── Sociologia (expandido) ────────────────────────────────
    ("enem", "Ciências Humanas", "Sociologia - Trabalho",
     "A mais-valia, conceito de Karl Marx, refere-se a:",
     json.dumps(["Lucro legítimo do empresário", "Diferença entre o valor produzido pelo trabalhador e o salário recebido",
                 "Imposto sobre a produção", "Custo das matérias-primas"]),
     "Diferença entre o valor produzido pelo trabalhador e o salário recebido",
     "A mais-valia é a exploração do trabalho: o trabalhador produz mais valor do que recebe em salário.",
     "médio"),

    ("enem", "Ciências Humanas", "Sociologia - Cultura",
     "O etnocentrismo é a atitude de:",
     json.dumps(["Valorizar todas as culturas igualmente", "Julgar outras culturas a partir da sua própria",
                 "Rejeitar a própria cultura", "Estudar as culturas primitivas"]),
     "Julgar outras culturas a partir da sua própria",
     "Etnocentrismo é considerar sua cultura como superior e julgar as demais a partir dos próprios valores.",
     "fácil"),

    ("enem", "Ciências Humanas", "Sociologia - Movimentos Sociais",
     "Os movimentos sociais são caracterizados por:",
     json.dumps(["Ações individuais isoladas", "Ações coletivas organizadas por mudanças sociais",
                 "Decisões governamentais", "Ações empresariais"]),
     "Ações coletivas organizadas por mudanças sociais",
     "Movimentos sociais são ações coletivas de grupos que buscam mudanças sociais, políticas ou culturais.",
     "fácil"),

    ("enem", "Ciências Humanas", "Sociologia - Estratificação",
     "Max Weber diferenciou a estratificação social em três dimensões:",
     json.dumps(["Raça, gênero e idade", "Classe, status e partido",
                 "Rico, médio e pobre", "Urbano, rural e suburbano"]),
     "Classe, status e partido",
     "Weber analisou a estratificação por: classe (econômica), status (prestígio social) e partido (poder político).",
     "difícil"),

    ("enem", "Ciências Humanas", "Sociologia - Cidadania",
     "Cidadania envolve três dimensões de direitos, segundo T.H. Marshall:",
     json.dumps(["Econômicos, culturais e ambientais", "Civis, políticos e sociais",
                 "Individuais, coletivos e difusos", "Públicos, privados e mistos"]),
     "Civis, políticos e sociais",
     "Marshall: direitos civis (séc. XVIII), políticos (séc. XIX) e sociais (séc. XX) formam a cidadania plena.",
     "difícil"),

    # ╔════════════════════════════════════════════════════════╗
    # ║  5. REDAÇÃO                                           ║
    # ╚════════════════════════════════════════════════════════╝

    ("enem", "Redação", "Proposta de Intervenção",
     "A proposta de intervenção na redação do ENEM deve conter:",
     json.dumps(["Apenas a solução", "Agente, ação, modo/meio, detalhamento e finalidade",
                 "Opinião pessoal", "Citação de um autor"]),
     "Agente, ação, modo/meio, detalhamento e finalidade",
     "Uma proposta completa: QUEM (agente), FAZ O QUÊ (ação), COMO (modo), detalhamento e PARA QUÊ (finalidade).",
     "médio"),

    ("enem", "Redação", "Proposta de Intervenção",
     "Na proposta de intervenção, o agente pode ser:",
     json.dumps(["Apenas o governo", "O governo, ONGs, escolas, mídia, empresas, família, sociedade",
                 "Apenas a escola", "Apenas o cidadão"]),
     "O governo, ONGs, escolas, mídia, empresas, família, sociedade",
     "Diversos agentes podem ser propostos: Governo (federal, estadual, municipal), ONGs, escolas, mídia, família, etc.",
     "fácil"),

    ("enem", "Redação", "Repertório Sociocultural",
     "O repertório sociocultural na redação serve para:",
     json.dumps(["Decorar o texto", "Fundamentar os argumentos com referências culturais/científicas",
                 "Aumentar o número de linhas", "Mostrar vocabulário rebuscado"]),
     "Fundamentar os argumentos com referências culturais/científicas",
     "Repertório sociocultural (filósofos, dados, leis, obras) dá credibilidade e profundidade à argumentação.",
     "fácil"),

    ("enem", "Redação", "Repertório Sociocultural",
     "Qual NÃO é um exemplo válido de repertório sociocultural?",
     json.dumps(["Citação de filósofo", "Dados do IBGE",
                "Opinião pessoal sem embasamento", "Referência à Constituição"]),
     "Opinião pessoal sem embasamento",
     "Repertório sociocultural são referências legitimadas: dados estatísticos, obras, filósofos, leis, eventos históricos.",
     "fácil"),

    ("enem", "Redação", "Conectivos",
     "Qual conectivo indica uma relação de causa?",
     json.dumps(["Porém", "Pois / Porque / Visto que", "Entretanto", "Embora"]),
     "Pois / Porque / Visto que",
     "Conectivos causais: pois, porque, já que, visto que, uma vez que, dado que.",
     "fácil"),

    ("enem", "Redação", "Conectivos",
     "Os conectivos 'porém', 'todavia', 'entretanto' e 'contudo' expressam ideia de:",
     json.dumps(["Adição", "Oposição / Adversidade",
                "Conclusão", "Explicação"]),
     "Oposição / Adversidade",
     "São conjunções adversativas: introduzem ideias contrárias ao que foi dito antes.",
     "fácil"),

    ("enem", "Redação", "Conectivos",
     "'Portanto', 'logo', 'assim' e 'dessa forma' são conectivos de:",
     json.dumps(["Causa", "Condição", "Conclusão", "Tempo"]),
     "Conclusão",
     "Conectivos conclusivos introduzem a consequência ou conclusão do que foi argumentado.",
     "fácil"),

    ("enem", "Redação", "Argumentação",
     "Um argumento de autoridade consiste em:",
     json.dumps(["Usar dados estatísticos", "Citar especialistas ou pensadores reconhecidos",
                 "Comparar situações", "Narrar uma história"]),
     "Citar especialistas ou pensadores reconhecidos",
     "Argumento de autoridade: usar falas/ideias de especialistas, filósofos ou instituições para fortalecer a tese.",
     "fácil"),

    ("enem", "Redação", "Argumentação",
     "O argumento por exemplificação utiliza:",
     json.dumps(["Citações de filósofos", "Casos concretos e exemplos para ilustrar a tese",
                 "Dados estatísticos", "Comparações com outros países"]),
     "Casos concretos e exemplos para ilustrar a tese",
     "Exemplificação: usar casos reais, fatos históricos ou situações concretas para comprovar a tese.",
     "fácil"),

    ("enem", "Redação", "Temas Frequentes",
     "Qual destes temas já foi cobrado na redação do ENEM?",
     json.dumps(["Violência no trânsito", "Persistência da violência contra a mulher",
                 "Exploração espacial", "Inteligência artificial"]),
     "Persistência da violência contra a mulher",
     "A redação do ENEM 2015 abordou 'A persistência da violência contra a mulher na sociedade brasileira'.",
     "fácil"),

    ("enem", "Redação", "Temas Frequentes",
     "O tema da redação do ENEM 2018 foi:",
     json.dumps(["Caminhos para combater o racismo", "Manipulação do comportamento do usuário pelo controle de dados na internet",
                 "Evasão escolar", "Mobilidade urbana"]),
     "Manipulação do comportamento do usuário pelo controle de dados na internet",
     "ENEM 2018: 'Manipulação do comportamento do usuário pelo controle de dados na internet' — tema sobre privacidade digital.",
     "médio"),

    ("enem", "Redação", "Temas Frequentes",
     "O tema da redação do ENEM 2022 foi:",
     json.dumps(["Desafios para a valorização de comunidades e povos tradicionais",
                 "Democratização do acesso ao cinema", "Invisibilidade e registro civil",
                 "Estigma associado às doenças mentais"]),
     "Desafios para a valorização de comunidades e povos tradicionais",
     "ENEM 2022: 'Desafios para a valorização de comunidades e povos tradicionais no Brasil'.",
     "médio"),
]


# ══════════════════════════════════════════════════════════════
# ── FLASHCARDS EXPANDIDOS ────────────────────────────────────
# ══════════════════════════════════════════════════════════════
# Formato: (category, subject, topic, front, back, difficulty)

EXPANDED_FLASHCARDS = [
    # ── Linguagens ──────────────────────────────────────────
    ("enem", "Linguagens", "Funções da Linguagem",
     "Quais são as 6 funções da linguagem?",
     "1. Emotiva (emissor)\n2. Conativa (receptor)\n3. Referencial (contexto)\n4. Metalinguística (código)\n5. Fática (canal)\n6. Poética (mensagem)",
     "médio"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "O que é Metonímia?",
     "Substituição de um termo por outro com relação de contiguidade.\nEx: 'Li Machado de Assis' (autor pela obra)\n'Bebeu dois copos' (continente pelo conteúdo)",
     "médio"),

    ("enem", "Linguagens", "Figuras de Linguagem",
     "Antítese × Paradoxo — Qual a diferença?",
     "Antítese: oposição de ideias (amor/ódio)\nParadoxo (oxímoro): ideias contraditórias coexistindo\nEx paradoxo: 'Estou cego e vejo'",
     "difícil"),

    ("enem", "Linguagens", "Variação Linguística",
     "4 tipos de variação linguística",
     "1. Diatópica (regional): sotaques\n2. Diastrática (social): escolaridade\n3. Diafásica (situacional): formal/informal\n4. Diacrônica (histórica): evolução da língua",
     "médio"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "Linha do tempo das escolas literárias brasileiras",
     "Quinhentismo → Barroco → Arcadismo → Romantismo → Realismo/Naturalismo → Parnasianismo → Simbolismo → Pré-Modernismo → Modernismo (1ª, 2ª, 3ª geração) → Contemporânea",
     "difícil"),

    ("enem", "Linguagens", "Literatura - Movimentos",
     "Características do Romantismo brasileiro",
     "• Subjetivismo e sentimentalismo\n• Nacionalismo e indianismo (1ª geração)\n• Mal do século — pessimismo (2ª geração)\n• Poesia social e abolicionista (3ª geração)",
     "médio"),

    ("enem", "Linguagens", "Gêneros Textuais",
     "Tipos textuais vs Gêneros textuais",
     "Tipos: narração, descrição, dissertação, injunção, exposição (estrutura)\nGêneros: crônica, editorial, receita, romance, notícia (função social)\nGêneros usam um ou mais tipos textuais",
     "médio"),

    ("enem", "Linguagens", "Interpretação de Texto",
     "Diferença entre texto e discurso",
     "Texto: materialidade linguística (escrita/oral)\nDiscurso: texto + contexto + intenção + ideologia\nTodo texto carrega um discurso",
     "difícil"),

    # ── Matemática ──────────────────────────────────────────
    ("enem", "Matemática", "Trigonometria",
     "Tabela de valores notáveis (sen, cos, tg)",
     "      30°    45°    60°\nsen: 1/2   √2/2   √3/2\ncos: √3/2  √2/2   1/2\ntg:  √3/3   1     √3",
     "médio"),

    ("enem", "Matemática", "Análise Combinatória",
     "Permutação × Arranjo × Combinação",
     "Permutação: todos os elementos, ordem importa (P=n!)\nArranjo: parte dos elementos, ordem importa (A=n!/(n-p)!)\nCombinação: parte dos elementos, ordem NÃO importa (C=n!/p!(n-p)!)",
     "difícil"),

    ("enem", "Matemática", "Progressões",
     "Soma dos termos de uma PA",
     "Sₙ = (a₁ + aₙ) × n / 2\nonde:\na₁ = primeiro termo\naₙ = último termo\nn = número de termos",
     "médio"),

    ("enem", "Matemática", "Logaritmos",
     "Propriedades dos logaritmos",
     "1. log(a×b) = log a + log b\n2. log(a/b) = log a - log b\n3. log(aⁿ) = n × log a\n4. log_a(a) = 1\n5. log_a(1) = 0",
     "médio"),

    ("enem", "Matemática", "Geometria Espacial",
     "Fórmulas de volume (sólidos)",
     "Cubo: a³\nParalelepípedo: a×b×c\nCilindro: πr²h\nCone: πr²h/3\nEsfera: 4πr³/3\nPirâmide: Ab×h/3\nPrisma: Ab×h",
     "médio"),

    ("enem", "Matemática", "Geometria Analítica",
     "Equação geral da reta e distância entre pontos",
     "Reta: y = mx + n (m = coef. angular)\nDistância: d = √[(x₂-x₁)² + (y₂-y₁)²]\nPonto médio: M = ((x₁+x₂)/2, (y₁+y₂)/2)",
     "médio"),

    ("enem", "Matemática", "Matemática Financeira",
     "Juros Simples × Juros Compostos",
     "Simples: M = C(1 + i×t) — cresce linearmente\nCompostos: M = C(1 + i)ᵗ — cresce exponencialmente\nC = capital, i = taxa, t = tempo",
     "médio"),

    ("enem", "Matemática", "Estatística",
     "Média, Moda e Mediana",
     "Média: soma dos valores / n\nModa: valor mais frequente\nMediana: valor central (dados ordenados)\nSe n par: média dos dois centrais",
     "fácil"),

    # ── Ciências da Natureza ────────────────────────────────
    ("enem", "Ciências da Natureza", "Física - Óptica",
     "Leis da reflexão",
     "1ª Lei: raio incidente, refletido e normal são coplanares\n2ª Lei: ângulo de incidência = ângulo de reflexão\nEspelho plano: imagem virtual, direita, mesmo tamanho",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Ondulatória",
     "Ondas: tipos e classificação",
     "Mecânicas: precisam de meio (som, ondas do mar)\nEletromagnéticas: não precisam (luz, rádio)\nTransversais: vibração ⊥ propagação\nLongitudinais: vibração // propagação",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Eletricidade",
     "Fórmulas de eletricidade",
     "Lei de Ohm: V = R × I\nPotência: P = V × I\nEnergia: E = P × t\nResistores em série: Req = R₁+R₂+...\nParalelo: 1/Req = 1/R₁+1/R₂+...",
     "médio"),

    ("enem", "Ciências da Natureza", "Física - Energia",
     "Tipos de energia e conversões",
     "Cinética: Ec = mv²/2\nPotencial grav.: Ep = mgh\nElástica: Ee = kx²/2\nMecânica: Em = Ec + Ep\nConservação: Em₁ = Em₂ (sist. conservativo)",
     "médio"),

    ("enem", "Ciências da Natureza", "Química - Ligações Químicas",
     "Iônica × Covalente × Metálica",
     "Iônica: metal + não-metal (transferência e⁻)\nCovalente: não-metal + não-metal (compartilhamento e⁻)\nMetálica: metal + metal (elétrons livres / mar de elétrons)",
     "médio"),

    ("enem", "Ciências da Natureza", "Química - Orgânica",
     "Funções orgânicas principais",
     "Álcool: R-OH\nAldeído: R-CHO\nCetona: R-CO-R\nÁcido carboxílico: R-COOH\nÉster: R-COO-R\nÉter: R-O-R\nAmina: R-NH₂\nAmida: R-CO-NH₂",
     "difícil"),

    ("enem", "Ciências da Natureza", "Química - Ambiental",
     "Problemas ambientais e suas causas",
     "Efeito estufa: CO₂, CH₄ (queima fósseis)\nChuva ácida: SO₂, NOₓ (indústrias/carros)\nBuraco na camada de ozônio: CFCs\nEutrofização: excesso nutrientes na água",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Evolução",
     "Darwin × Lamarck",
     "Darwin: seleção natural, variabilidade genética\n- Mais aptos sobrevivem e se reproduzem\nLamarck: uso/desuso + herança adquirida\n- Características adquiridas passam aos filhos (refutado)",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Fisiologia",
     "Sistemas do corpo humano",
     "Digestório: boca→esôfago→estômago→intestinos\nRespiratório: nariz→laringe→traqueia→brônquios→alvéolos\nCirculatório: coração→artérias→veias→capilares\nExcretor: rins→ureteres→bexiga→uretra",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Genética",
     "Leis de Mendel",
     "1ª Lei (Segregação): cada caráter é determinado por 2 fatores (alelos) que se separam na formação dos gametas\n2ª Lei (Segregação Independente): genes em cromossomos diferentes segregam independentemente",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Ecologia",
     "Cadeia alimentar e níveis tróficos",
     "Produtores (autótrofos): plantas, algas\n1° consumidor (herbívoro)\n2° consumidor (carnívoro)\n3° consumidor (topo)\nDecompositores: fungos, bactérias\nRegra dos 10%: ~10% da energia passa ao próximo nível",
     "médio"),

    ("enem", "Ciências da Natureza", "Biologia - Biotecnologia",
     "Transgênicos, clonagem e células-tronco",
     "Transgênico: organismo com gene de outra espécie (DNA recombinante)\nClonagem: cópia genética idêntica\nCélulas-tronco: células indiferenciadas que podem se tornar qualquer tipo celular",
     "difícil"),

    # ── Ciências Humanas ────────────────────────────────────
    ("enem", "Ciências Humanas", "História - Ditadura Militar",
     "Atos Institucionais da ditadura",
     "AI-1 (1964): cassações e eleições indiretas\nAI-2 (1965): bipartidarismo (ARENA/MDB)\nAI-5 (1968): o mais severo — fechou Congresso, cassou direitos, censurou imprensa, suspendeu habeas corpus",
     "difícil"),

    ("enem", "Ciências Humanas", "História - Era Vargas",
     "Governos de Getúlio Vargas",
     "1930-34: Governo Provisório\n1934-37: Governo Constitucional\n1937-45: Estado Novo (ditatorial)\n1951-54: Governo democrático\n1954: suicídio (carta-testamento)",
     "médio"),

    ("enem", "Ciências Humanas", "Geografia - Clima",
     "Climas do Brasil",
     "Equatorial: N (quente/úmido o ano todo)\nTropical: maior parte (quente, verão chuvoso)\nSemiárido: NE interior (quente, pouca chuva)\nSubtropical: S (4 estações, geadas)\nTropical de Altitude: SE serras",
     "médio"),

    ("enem", "Ciências Humanas", "Geografia - Brasil",
     "6 Biomas brasileiros (características)",
     "Amazônia: maior, floresta densa, biodiversa\nCerrado: savana, solo ácido, 2ª maior\nMata Atlântica: litoral, muito devastada\nCaatinga: semiárido, plantas xerófitas\nPampa: campos sulinos\nPantanal: maior planície alagável",
     "médio"),

    ("enem", "Ciências Humanas", "Filosofia - Moderna",
     "Racionalismo × Empirismo",
     "Racionalismo (Descartes): conhecimento pela razão, ideias inatas\nEmpirismo (Locke, Hume): conhecimento pela experiência, mente = 'tábula rasa'\nKant: síntese — razão organiza dados da experiência",
     "difícil"),

    ("enem", "Ciências Humanas", "Sociologia - Trabalho",
     "Pensadores clássicos da Sociologia",
     "Durkheim: fato social, solidariedade, anomia\nMarx: luta de classes, mais-valia, materialismo histórico\nWeber: ação social, burocracia, tipos de dominação (legal, tradicional, carismática)",
     "difícil"),

    # ── Redação ─────────────────────────────────────────────
    ("enem", "Redação", "Estrutura",
     "Estrutura da redação dissertativa-argumentativa",
     "§1 INTRODUÇÃO: contextualização + tese\n§2 DESENVOLVIMENTO 1: argumento 1 + repertório\n§3 DESENVOLVIMENTO 2: argumento 2 + repertório\n§4 CONCLUSÃO: retomada + proposta de intervenção (agente, ação, modo, detalhamento, finalidade)",
     "médio"),

    ("enem", "Redação", "Competências",
     "5 competências detalhadas da redação ENEM",
     "C1: Domínio da norma culta (200pts)\nC2: Compreender o tema + gênero dissertativo (200pts)\nC3: Selecionar/organizar argumentos (200pts)\nC4: Coesão textual — conectivos (200pts)\nC5: Proposta de intervenção completa (200pts)\nTotal: 1000 pontos",
     "médio"),

    ("enem", "Redação", "Proposta de Intervenção",
     "Elementos da proposta de intervenção perfeita",
     "5 elementos obrigatórios:\n1. AGENTE (quem?): governo, escola, mídia...\n2. AÇÃO (o quê?): criar, promover, fiscalizar...\n3. MODO/MEIO (como?): por meio de, através de...\n4. DETALHAMENTO: especificar a ação\n5. FINALIDADE (para quê?): a fim de, para que...",
     "médio"),

    ("enem", "Redação", "Conectivos",
     "Conectivos essenciais por tipo",
     "Adição: além disso, ademais, outrossim\nOposição: porém, todavia, entretanto, contudo\nCausa: pois, porque, visto que, uma vez que\nConsequência: logo, portanto, dessa forma\nConcessão: embora, conquanto, ainda que\nComparação: assim como, tal qual",
     "médio"),

    ("enem", "Redação", "Temas Frequentes",
     "Temas recentes da redação ENEM",
     "2023: Desafios para o enfrentamento da invisibilidade do trabalho de cuidado\n2022: Comunidades e povos tradicionais\n2021: Invisibilidade e registro civil\n2020: Estigma às doenças mentais\n2019: Democratização do cinema\n2018: Controle de dados na internet",
     "difícil"),
]


# ══════════════════════════════════════════════════════════════
# ── SEARCH QUERIES EXPANDIDAS (para YouTube) ─────────────────
# ══════════════════════════════════════════════════════════════
# Formato: {(category, subject, topic): "query de busca"}

EXPANDED_SEARCH_QUERIES = {
    # ── Linguagens (novos) ────────────────────────────────
    ("enem", "Linguagens", "Funções da Linguagem"):
        "funções da linguagem ENEM aula completa",
    ("enem", "Linguagens", "Gêneros Textuais"):
        "gêneros textuais ENEM aula completa",
    ("enem", "Linguagens", "Variação Linguística"):
        "variação linguística ENEM aula",
    ("enem", "Linguagens", "Figuras de Linguagem"):
        "figuras de linguagem ENEM aula completa",
    ("enem", "Linguagens", "Intertextualidade"):
        "intertextualidade ENEM aula",
    ("enem", "Linguagens", "Literatura - Movimentos"):
        "escolas literárias brasileiras resumo ENEM aula",
    ("enem", "Linguagens", "Artes"):
        "artes ENEM aula pintura música",
    ("enem", "Linguagens", "Comunicação e Tecnologia"):
        "linguagens tecnologia comunicação ENEM aula",

    # ── Matemática (novos) ────────────────────────────────
    ("enem", "Matemática", "Razão e Proporção"):
        "razão proporção regra de três ENEM aula",
    ("enem", "Matemática", "Regra de Três"):
        "regra de três simples composta ENEM aula",
    ("enem", "Matemática", "Equações"):
        "equação primeiro segundo grau ENEM aula",
    ("enem", "Matemática", "Sistemas de Equações"):
        "sistemas de equações ENEM aula completa",
    ("enem", "Matemática", "Análise Combinatória"):
        "análise combinatória permutação arranjo combinação ENEM aula",
    ("enem", "Matemática", "Progressões"):
        "progressão aritmética geométrica PA PG ENEM aula",
    ("enem", "Matemática", "Trigonometria"):
        "trigonometria ENEM seno cosseno tangente aula",
    ("enem", "Matemática", "Geometria Espacial"):
        "geometria espacial volume cilindro cone esfera ENEM aula",
    ("enem", "Matemática", "Geometria Analítica"):
        "geometria analítica reta ponto ENEM aula",
    ("enem", "Matemática", "Logaritmos"):
        "logaritmo propriedades ENEM aula",
    ("enem", "Matemática", "Matemática Financeira"):
        "matemática financeira juros simples compostos ENEM aula",
    ("enem", "Matemática", "Grandezas e Medidas"):
        "grandezas medidas conversão unidades ENEM aula",
    ("enem", "Matemática", "Leitura de Gráficos"):
        "leitura interpretação gráficos tabelas ENEM aula",

    # ── Ciências da Natureza (novos) ──────────────────────
    ("enem", "Ciências da Natureza", "Física - Óptica"):
        "óptica geométrica reflexão refração ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Ondulatória"):
        "ondulatória ondas ENEM aula completa",
    ("enem", "Ciências da Natureza", "Física - Eletricidade"):
        "eletricidade circuitos elétricos ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Energia"):
        "energia trabalho potência conservação ENEM aula",
    ("enem", "Ciências da Natureza", "Física - Hidrostática"):
        "hidrostática pressão empuxo ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Ligações Químicas"):
        "ligações químicas iônica covalente metálica ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Soluções"):
        "soluções concentração diluição ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Eletroquímica"):
        "eletroquímica pilhas eletrólise ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Orgânica"):
        "química orgânica funções orgânicas ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Termoquímica"):
        "termoquímica entalpia ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Cinética"):
        "cinética química velocidade reação ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Equilíbrio"):
        "equilíbrio químico Le Chatelier ENEM aula",
    ("enem", "Ciências da Natureza", "Química - Ambiental"):
        "química ambiental efeito estufa chuva ácida ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Evolução"):
        "evolução Darwin seleção natural ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Fisiologia"):
        "fisiologia humana sistemas corpo humano ENEM aula",
    ("enem", "Ciências da Natureza", "Biologia - Biotecnologia"):
        "biotecnologia transgênicos DNA recombinante ENEM aula",

    # ── Ciências Humanas (novos) ──────────────────────────
    ("enem", "Ciências Humanas", "História - Antiguidade"):
        "história antiga Grécia Roma ENEM aula",
    ("enem", "Ciências Humanas", "História - Idade Média"):
        "Idade Média feudalismo cruzadas ENEM aula",
    ("enem", "Ciências Humanas", "História - Renascimento"):
        "Renascimento cultural artístico ENEM aula",
    ("enem", "Ciências Humanas", "História - Reforma Protestante"):
        "Reforma Protestante Lutero Calvino ENEM aula",
    ("enem", "Ciências Humanas", "História - Era Vargas"):
        "Era Vargas Estado Novo ENEM aula",
    ("enem", "Ciências Humanas", "História - Ditadura Militar"):
        "ditadura militar Brasil ENEM aula",
    ("enem", "Ciências Humanas", "História - Guerras Mundiais"):
        "Primeira Segunda Guerra Mundial ENEM aula",
    ("enem", "Ciências Humanas", "História - Guerra Fria"):
        "Guerra Fria bipolarização ENEM aula",
    ("enem", "Ciências Humanas", "História - Brasil Império"):
        "Brasil Império independência abolição ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Clima"):
        "climas do Brasil tipos climáticos ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Hidrografia"):
        "hidrografia brasileira rios bacias ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Geopolítica"):
        "geopolítica relações internacionais ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Meio Ambiente"):
        "meio ambiente sustentabilidade ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Energia"):
        "matriz energética Brasil fontes energia ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Agropecuária"):
        "agropecuária brasileira agronegócio ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Industrialização"):
        "industrialização brasileira ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Migração"):
        "migração êxodo rural urbanização ENEM aula",
    ("enem", "Ciências Humanas", "Geografia - Desigualdade Social"):
        "desigualdade social Brasil IDH Gini ENEM aula",
    ("enem", "Ciências Humanas", "Filosofia - Moderna"):
        "filosofia moderna Descartes Kant ENEM aula",
    ("enem", "Ciências Humanas", "Filosofia - Contemporânea"):
        "filosofia contemporânea Sartre existencialismo ENEM aula",
    ("enem", "Ciências Humanas", "Filosofia - Ética"):
        "ética moral filosofia ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia - Trabalho"):
        "sociologia do trabalho Marx mais-valia ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia - Cultura"):
        "cultura indústria cultural sociologia ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia - Movimentos Sociais"):
        "movimentos sociais cidadania ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia - Estratificação"):
        "estratificação social classes ENEM aula",
    ("enem", "Ciências Humanas", "Sociologia - Cidadania"):
        "cidadania direitos sociais ENEM aula",

    # ── Redação (novos) ──────────────────────────────────
    ("enem", "Redação", "Proposta de Intervenção"):
        "proposta intervenção redação ENEM nota 1000 aula",
    ("enem", "Redação", "Repertório Sociocultural"):
        "repertório sociocultural redação ENEM aula",
    ("enem", "Redação", "Conectivos"):
        "conectivos redação ENEM coesão aula",
    ("enem", "Redação", "Argumentação"):
        "argumentação tipos de argumento redação ENEM aula",
    ("enem", "Redação", "Temas Frequentes"):
        "temas redação ENEM mais cobrados aula",
}
