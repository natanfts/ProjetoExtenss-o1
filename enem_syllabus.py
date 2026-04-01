"""
enem_syllabus.py — Conteúdo teórico baseado nos editais oficiais do ENEM.

Estrutura: Área → Matéria → Tópico → Resumo teórico + conceitos-chave + fórmulas.
Baseado na Matriz de Referência do ENEM (INEP/MEC) e editais oficiais.
Cada tópico inclui:
  - title: Nome do tópico
  - summary: Resumo teórico completo
  - key_concepts: Lista de conceitos-chave
  - formulas: Fórmulas importantes (quando aplicável)
  - tips: Dicas para o ENEM
  - related_topics: Tópicos relacionados para estudo cruzado
  - difficulty: fácil | médio | difícil
  - wiki_query: Termo para busca complementar na Wikipedia
"""

import unicodedata
ENEM_SYLLABUS = {
    # ╔════════════════════════════════════════════════════════════╗
    # ║  1. LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS               ║
    # ╚════════════════════════════════════════════════════════════╝
    "Linguagens": {
        "emoji": "📝",
        "description": "Linguagens, Códigos e suas Tecnologias — Língua Portuguesa, Literatura, Artes, Educação Física e Língua Estrangeira.",
        "topics": [
            {
                "title": "Funções da Linguagem",
                "summary": (
                    "As funções da linguagem foram definidas pelo linguista Roman Jakobson e estão relacionadas "
                    "aos elementos da comunicação. São seis funções:\n\n"
                    "• Função Referencial (Denotativa): Centrada no referente/contexto. Linguagem objetiva, informativa. "
                    "Presente em textos jornalísticos, científicos e didáticos.\n\n"
                    "• Função Emotiva (Expressiva): Centrada no emissor. Expressa sentimentos, emoções e opiniões pessoais. "
                    "Usa 1ª pessoa, interjeições e pontuação expressiva.\n\n"
                    "• Função Conativa (Apelativa): Centrada no receptor. Busca persuadir ou influenciar. "
                    "Usa imperativos, vocativos e 2ª pessoa. Comum em publicidade.\n\n"
                    "• Função Fática: Centrada no canal de comunicação. Serve para verificar, estabelecer ou "
                    "encerrar a comunicação. Ex: 'Alô?', 'Entendeu?'\n\n"
                    "• Função Metalinguística: Centrada no código. A linguagem fala de si mesma. "
                    "Ex: dicionários, gramáticas, poemas sobre poesia.\n\n"
                    "• Função Poética: Centrada na mensagem. Valoriza a forma, o ritmo, a sonoridade. "
                    "Presente em poemas, slogans e textos literários."
                ),
                "key_concepts": [
                    "Emissor, receptor, canal, código, referente, mensagem",
                    "Jakobson e os elementos da comunicação",
                    "Função predominante vs. funções secundárias",
                    "Identificação em textos do ENEM",
                ],
                "formulas": [],
                "tips": [
                    "No ENEM, identifique a função PREDOMINANTE — um texto pode ter várias funções",
                    "Publicidade = Conativa; Notícia = Referencial; Poema = Poética",
                    "Fática aparece em conversas informais e cumprimentos",
                ],
                "related_topics": ["Gêneros Textuais", "Interpretação de Texto"],
                "difficulty": "fácil",
                "wiki_query": "Funções da linguagem Jakobson",
            },
            {
                "title": "Gêneros Textuais",
                "summary": (
                    "Gêneros textuais são formas relativamente estáveis de enunciados, definidos por seu conteúdo "
                    "temático, estilo e construção composicional (Bakhtin).\n\n"
                    "Tipos textuais (estrutura):\n"
                    "• Narração: conta uma história com personagens, tempo, espaço e enredo\n"
                    "• Descrição: caracteriza seres, objetos, ambientes\n"
                    "• Dissertação-argumentativa: defende uma tese com argumentos\n"
                    "• Exposição: apresenta informações sem necessariamente argumentar\n"
                    "• Injunção: orienta ações (receitas, manuais, leis)\n\n"
                    "Gêneros textuais (exemplos concretos):\n"
                    "• Carta, e-mail, crônica, conto, romance, editorial, artigo de opinião, "
                    "resenha, notícia, reportagem, entrevista, propaganda, receita, bula, "
                    "charge, tirinha, HQ, blog, podcast, meme."
                ),
                "key_concepts": [
                    "Diferença entre tipo textual e gênero textual",
                    "Bakhtin e os gêneros do discurso",
                    "Gêneros digitais: meme, tweet, blog, podcast",
                    "Multimodalidade: texto + imagem",
                ],
                "formulas": [],
                "tips": [
                    "O ENEM adora questões sobre gêneros digitais e multimodais",
                    "Saiba identificar o gênero pela finalidade comunicativa",
                    "Charge e tirinha: humor + crítica social",
                ],
                "related_topics": ["Funções da Linguagem", "Interpretação de Texto", "Redação"],
                "difficulty": "fácil",
                "wiki_query": "Gêneros textuais",
            },
            {
                "title": "Variação Linguística",
                "summary": (
                    "A língua não é homogênea — varia de acordo com fatores sociais, regionais, "
                    "históricos e situacionais.\n\n"
                    "Tipos de variação:\n"
                    "• Diatópica (geográfica): diferenças regionais. Ex: 'mandioca' vs 'aipim' vs 'macaxeira'\n"
                    "• Diastrática (social): relacionada a classe social, escolaridade, profissão\n"
                    "• Diafásica (situacional): registro formal vs informal, adequado ao contexto\n"
                    "• Diacrônica (histórica): mudanças ao longo do tempo. Ex: 'pharmacia' → 'farmácia'\n\n"
                    "Conceitos importantes:\n"
                    "• Norma culta/padrão: variedade de prestígio, usada em contextos formais\n"
                    "• Preconceito linguístico: toda forma de discriminação baseada na variante do falante\n"
                    "• Adequação linguística: usar a variedade adequada ao contexto"
                ),
                "key_concepts": [
                    "Variação diatópica, diastrática, diafásica, diacrônica",
                    "Preconceito linguístico",
                    "Norma culta vs. norma popular",
                    "Adequação linguística ao contexto",
                ],
                "formulas": [],
                "tips": [
                    "O ENEM valoriza o respeito à diversidade linguística",
                    "Nenhuma variante é 'errada' — existe adequação ao contexto",
                    "Questões frequentes sobre preconceito linguístico",
                ],
                "related_topics": ["Funções da Linguagem", "Interpretação de Texto"],
                "difficulty": "fácil",
                "wiki_query": "Variação linguística",
            },
            {
                "title": "Interpretação de Texto",
                "summary": (
                    "A interpretação textual é a competência mais cobrada no ENEM. Envolve compreender "
                    "o sentido global do texto, identificar a intenção do autor, reconhecer informações "
                    "explícitas e implícitas, e relacionar textos entre si (intertextualidade).\n\n"
                    "Estratégias de leitura:\n"
                    "• Identificar o tema central e a tese (se houver)\n"
                    "• Distinguir fato de opinião\n"
                    "• Reconhecer argumentos e contra-argumentos\n"
                    "• Identificar pressupostos e subentendidos\n"
                    "• Analisar elementos coesivos e conectivos\n"
                    "• Considerar o contexto de produção\n\n"
                    "Intertextualidade:\n"
                    "• Citação: referência direta a outro texto\n"
                    "• Paráfrase: reescrita com outras palavras\n"
                    "• Paródia: imitação com tom cômico/crítico\n"
                    "• Alusão: referência indireta"
                ),
                "key_concepts": [
                    "Tema vs. tese vs. título",
                    "Informação explícita vs. implícita",
                    "Intertextualidade: citação, paráfrase, paródia, alusão",
                    "Coerência e coesão textual",
                ],
                "formulas": [],
                "tips": [
                    "Leia o texto INTEIRO antes de responder",
                    "A resposta está no texto, não na sua opinião pessoal",
                    "Cuidado com alternativas que 'parecem certas' mas extrapolam o texto",
                ],
                "related_topics": ["Gêneros Textuais", "Funções da Linguagem"],
                "difficulty": "médio",
                "wiki_query": "Interpretação de texto",
            },
            {
                "title": "Figuras de Linguagem",
                "summary": (
                    "Figuras de linguagem são recursos expressivos que enriquecem a comunicação, "
                    "criando efeitos de sentido.\n\n"
                    "Figuras de palavras (semânticas):\n"
                    "• Metáfora: comparação implícita. 'A vida é um rio.'\n"
                    "• Metonímia: substituição por relação de proximidade. 'Leu Machado' (obra pelo autor)\n"
                    "• Catacrese: metáfora cristalizada. 'Pé da mesa', 'asa do avião'\n"
                    "• Sinestesia: mistura de sentidos. 'Voz doce', 'cor quente'\n\n"
                    "Figuras de pensamento:\n"
                    "• Antítese: oposição de ideias. 'Amor e ódio'\n"
                    "• Paradoxo: contradição aparente. 'Estou cego de tanto ver'\n"
                    "• Ironia: dizer o contrário do que se pensa\n"
                    "• Hipérbole: exagero intencional. 'Morri de rir'\n"
                    "• Eufemismo: suavização. 'Ele passou desta para melhor'\n\n"
                    "Figuras de sintaxe:\n"
                    "• Elipse: omissão de termo subentendido\n"
                    "• Pleonasmo: redundância expressiva. 'Vi com meus próprios olhos'\n"
                    "• Anáfora: repetição no início de versos/frases"
                ),
                "key_concepts": [
                    "Metáfora vs. comparação vs. metonímia",
                    "Ironia, hipérbole, eufemismo",
                    "Antítese vs. paradoxo",
                    "Figuras de som: aliteração, assonância, onomatopeia",
                ],
                "formulas": [],
                "tips": [
                    "Metáfora é a figura mais cobrada no ENEM",
                    "Identifique o efeito de sentido da figura, não apenas o nome",
                    "Questões costumam pedir a função da figura no contexto",
                ],
                "related_topics": ["Interpretação de Texto", "Literatura"],
                "difficulty": "médio",
                "wiki_query": "Figuras de linguagem",
            },
            {
                "title": "Literatura Brasileira",
                "summary": (
                    "Movimentos literários brasileiros cobrados no ENEM:\n\n"
                    "• Quinhentismo (1500-1601): Literatura de Informação (Carta de Caminha) e Jesuítica (Anchieta)\n"
                    "• Barroco (1601-1768): Dualidade, conflito entre fé e razão. Gregório de Matos, Pe. Vieira\n"
                    "• Arcadismo (1768-1836): Valorização da natureza, vida simples. Tomás Antônio Gonzaga\n"
                    "• Romantismo (1836-1881): 3 gerações — indianista, ultrarromântica, social. Castro Alves, José de Alencar\n"
                    "• Realismo/Naturalismo (1881-1893): Crítica social, análise psicológica. Machado de Assis\n"
                    "• Parnasianismo: Arte pela arte, forma perfeita. Olavo Bilac\n"
                    "• Simbolismo (1893-1902): Subjetividade, musicalidade. Cruz e Sousa\n"
                    "• Pré-Modernismo (1902-1922): Transição. Euclides da Cunha, Lima Barreto, Monteiro Lobato\n"
                    "• Modernismo — 1ª fase (1922-1930): Ruptura, Semana de 22. Oswald e Mário de Andrade\n"
                    "• Modernismo — 2ª fase (1930-1945): Romance de 30, poesia intimista. Graciliano Ramos, Drummond\n"
                    "• Modernismo — 3ª fase (1945-): Guimarães Rosa, Clarice Lispector, Concretismo"
                ),
                "key_concepts": [
                    "Periodização literária e contexto histórico",
                    "Características de cada escola literária",
                    "Autores e obras representativos",
                    "Relação entre literatura e contexto social",
                ],
                "formulas": [],
                "tips": [
                    "O ENEM cobra mais interpretação de texto literário do que memorização de escolas",
                    "Modernismo (especialmente 2ª fase) é o mais cobrado",
                    "Machado de Assis é o autor mais recorrente no ENEM",
                ],
                "related_topics": ["Interpretação de Texto", "Figuras de Linguagem"],
                "difficulty": "médio",
                "wiki_query": "Literatura brasileira movimentos literários",
            },
            {
                "title": "Redação ENEM",
                "summary": (
                    "A redação do ENEM é uma dissertação-argumentativa sobre um tema de ordem social, "
                    "científica, cultural ou política. Vale 1000 pontos e é avaliada por 5 competências:\n\n"
                    "Competência 1: Demonstrar domínio da modalidade escrita formal da língua portuguesa.\n"
                    "Competência 2: Compreender a proposta de redação e aplicar conceitos para "
                    "desenvolver o tema dentro da estrutura dissertativo-argumentativa.\n"
                    "Competência 3: Selecionar, organizar e interpretar informações, fatos, opiniões e "
                    "argumentos em defesa de um ponto de vista.\n"
                    "Competência 4: Demonstrar conhecimento dos mecanismos linguísticos necessários para "
                    "a construção da argumentação (coesão).\n"
                    "Competência 5: Elaborar proposta de intervenção para o problema abordado, respeitando "
                    "os direitos humanos.\n\n"
                    "Estrutura: Introdução (contextualização + tese) → 2 parágrafos de desenvolvimento "
                    "(argumento + repertório) → Conclusão (proposta de intervenção detalhada)."
                ),
                "key_concepts": [
                    "5 competências avaliadas (200 pontos cada)",
                    "Proposta de intervenção: agente, ação, modo, efeito, detalhamento",
                    "Repertório sociocultural legitimado",
                    "Conectivos e operadores argumentativos",
                ],
                "formulas": [],
                "tips": [
                    "A proposta de intervenção DEVE respeitar os direitos humanos",
                    "Use repertório diversificado: dados, filósofos, obras literárias",
                    "Pratique semanalmente e peça correções",
                    "Nunca fuja do tema proposto nos textos motivadores",
                ],
                "related_topics": ["Gêneros Textuais", "Interpretação de Texto"],
                "difficulty": "difícil",
                "wiki_query": "Redação ENEM competências",
            },
        ],
    },

    # ╔════════════════════════════════════════════════════════════╗
    # ║  2. MATEMÁTICA E SUAS TECNOLOGIAS                        ║
    # ╚════════════════════════════════════════════════════════════╝
    "Matemática": {
        "emoji": "🔢",
        "description": "Matemática e suas Tecnologias — Aritmética, Álgebra, Geometria, Estatística e Probabilidade.",
        "topics": [
            {
                "title": "Razão, Proporção e Regra de Três",
                "summary": (
                    "Razão é a relação entre duas grandezas (a/b). Proporção é a igualdade "
                    "entre duas razões (a/b = c/d).\n\n"
                    "Regra de Três Simples:\n"
                    "Relaciona duas grandezas diretamente ou inversamente proporcionais.\n"
                    "Se A↑ e B↑ → diretamente proporcionais (multiplica em cruz)\n"
                    "Se A↑ e B↓ → inversamente proporcionais (multiplica em linha)\n\n"
                    "Regra de Três Composta:\n"
                    "Envolve três ou mais grandezas. Analise cada grandeza em relação à incógnita "
                    "e monte a proporção multiplicando as razões.\n\n"
                    "Porcentagem:\n"
                    "x% de N = (x/100) × N\n"
                    "Aumento de x%: N × (1 + x/100)\n"
                    "Desconto de x%: N × (1 - x/100)\n"
                    "Aumentos/descontos sucessivos: multiplique os fatores"
                ),
                "key_concepts": [
                    "Grandezas diretamente e inversamente proporcionais",
                    "Regra de três simples e composta",
                    "Porcentagem, aumento e desconto",
                    "Escala: E = d(desenho) / d(real)",
                ],
                "formulas": [
                    "a/b = c/d → a·d = b·c",
                    "Aumento: V_final = V_inicial × (1 + i)",
                    "Desconto: V_final = V_inicial × (1 - i)",
                    "Sucessivos: V_final = V_inicial × (1±i₁) × (1±i₂)",
                ],
                "tips": [
                    "Tema MAIS cobrado em Matemática no ENEM",
                    "Sempre identifique se as grandezas são diretas ou inversas",
                    "Porcentagem de porcentagem: multiplique os fatores",
                ],
                "related_topics": ["Matemática Financeira", "Estatística Básica"],
                "difficulty": "fácil",
                "wiki_query": "Regra de três proporção",
            },
            {
                "title": "Matemática Financeira",
                "summary": (
                    "Juros simples e compostos são fundamentais para o ENEM.\n\n"
                    "Juros Simples:\n"
                    "O juro é calculado sempre sobre o capital inicial.\n"
                    "J = C × i × t\n"
                    "M = C + J = C × (1 + i × t)\n\n"
                    "Juros Compostos:\n"
                    "O juro é calculado sobre o montante do período anterior (juros sobre juros).\n"
                    "M = C × (1 + i)^t\n\n"
                    "Onde: C = capital, i = taxa (em decimal), t = tempo, M = montante, J = juros.\n\n"
                    "Lucro e Prejuízo:\n"
                    "Lucro = Preço de venda - Preço de custo\n"
                    "Lucro% = (Lucro / Custo) × 100"
                ),
                "key_concepts": [
                    "Diferença entre juros simples e compostos",
                    "Capital, montante, taxa e tempo",
                    "Lucro, prejuízo e preço de custo",
                    "Parcelamento e financiamento",
                ],
                "formulas": [
                    "J = C · i · t (simples)",
                    "M = C · (1 + i)^t (compostos)",
                    "M = C + J",
                    "Taxa real = ((1+i_nominal)/(1+inflação)) - 1",
                ],
                "tips": [
                    "No ENEM, juros compostos são mais cobrados que simples",
                    "Converta sempre a taxa e o tempo para a mesma unidade",
                    "Questões contextualizadas: financiamento, empréstimo, investimento",
                ],
                "related_topics": ["Razão, Proporção e Regra de Três", "Função Exponencial"],
                "difficulty": "médio",
                "wiki_query": "Juros compostos matemática financeira",
            },
            {
                "title": "Estatística Básica",
                "summary": (
                    "Estatística no ENEM envolve leitura e interpretação de dados.\n\n"
                    "Medidas de Tendência Central:\n"
                    "• Média aritmética: soma de todos os valores dividida pela quantidade\n"
                    "  x̄ = (x₁ + x₂ + ... + xₙ) / n\n"
                    "• Média ponderada: cada valor tem um peso\n"
                    "  x̄ₚ = (x₁·p₁ + x₂·p₂ + ...) / (p₁ + p₂ + ...)\n"
                    "• Mediana: valor central quando os dados estão ordenados\n"
                    "• Moda: valor que mais se repete\n\n"
                    "Medidas de Dispersão:\n"
                    "• Amplitude: maior valor - menor valor\n"
                    "• Variância: média dos quadrados dos desvios\n"
                    "• Desvio padrão: raiz quadrada da variância\n\n"
                    "Gráficos: barras, setores (pizza), histograma, linha, boxplot"
                ),
                "key_concepts": [
                    "Média, mediana e moda",
                    "Variância e desvio padrão",
                    "Leitura de tabelas e gráficos",
                    "Frequência absoluta e relativa",
                ],
                "formulas": [
                    "Média: x̄ = Σxᵢ / n",
                    "Variância: σ² = Σ(xᵢ - x̄)² / n",
                    "Desvio padrão: σ = √(σ²)",
                    "Freq. relativa: fᵢ / Σfᵢ",
                ],
                "tips": [
                    "Saiba ler gráficos! Isso cai MUITO no ENEM",
                    "Mediana ≠ média — cuidado com dados assimétricos",
                    "Questões de estatística costumam ser contextualizadas com dados reais",
                ],
                "related_topics": ["Probabilidade", "Razão, Proporção e Regra de Três"],
                "difficulty": "médio",
                "wiki_query": "Estatística descritiva média mediana",
            },
            {
                "title": "Probabilidade",
                "summary": (
                    "Probabilidade mede a chance de um evento ocorrer.\n\n"
                    "Probabilidade simples:\n"
                    "P(A) = número de casos favoráveis / número de casos possíveis\n\n"
                    "Espaço amostral: conjunto de todos os resultados possíveis.\n"
                    "Evento: subconjunto do espaço amostral.\n\n"
                    "Regras:\n"
                    "• 0 ≤ P(A) ≤ 1\n"
                    "• P(A) + P(Ā) = 1 (complementar)\n"
                    "• P(A ∪ B) = P(A) + P(B) - P(A ∩ B) (união)\n"
                    "• P(A ∩ B) = P(A) × P(B) se independentes\n\n"
                    "Probabilidade condicional:\n"
                    "P(A|B) = P(A ∩ B) / P(B)"
                ),
                "key_concepts": [
                    "Espaço amostral e evento",
                    "Eventos independentes e dependentes",
                    "Probabilidade complementar",
                    "Probabilidade condicional",
                ],
                "formulas": [
                    "P(A) = n(A) / n(S)",
                    "P(Ā) = 1 - P(A)",
                    "P(A ∪ B) = P(A) + P(B) - P(A ∩ B)",
                    "P(A|B) = P(A ∩ B) / P(B)",
                ],
                "tips": [
                    "Monte sempre o espaço amostral antes de calcular",
                    "Dados, moedas e cartas são contextos clássicos",
                    "No ENEM, as questões são muito contextualizadas — interprete bem o enunciado",
                ],
                "related_topics": ["Estatística Básica", "Análise Combinatória"],
                "difficulty": "médio",
                "wiki_query": "Probabilidade estatística",
            },
            {
                "title": "Geometria Plana",
                "summary": (
                    "Estudo das figuras bidimensionais e suas propriedades.\n\n"
                    "Triângulos:\n"
                    "• Área = (base × altura) / 2\n"
                    "• Soma dos ângulos internos = 180°\n"
                    "• Teorema de Pitágoras (retângulo): a² = b² + c²\n"
                    "• Semelhança: lados proporcionais, ângulos iguais\n\n"
                    "Quadriláteros:\n"
                    "• Quadrado: A = l², P = 4l\n"
                    "• Retângulo: A = b × h, P = 2(b + h)\n"
                    "• Paralelogramo: A = b × h\n"
                    "• Trapézio: A = (B + b) × h / 2\n"
                    "• Losango: A = (D × d) / 2\n\n"
                    "Círculo:\n"
                    "• Comprimento: C = 2πr\n"
                    "• Área: A = πr²\n"
                    "• Setor circular: A = (θ/360) × πr²"
                ),
                "key_concepts": [
                    "Teorema de Pitágoras",
                    "Semelhança de triângulos",
                    "Áreas de figuras planas",
                    "Relações métricas no triângulo retângulo",
                ],
                "formulas": [
                    "A_triângulo = b·h/2",
                    "A_círculo = π·r²",
                    "C = 2·π·r",
                    "a² = b² + c² (Pitágoras)",
                    "A_trapézio = (B+b)·h/2",
                ],
                "tips": [
                    "Pitágoras é o teorema mais cobrado no ENEM",
                    "Saiba calcular áreas compostas (soma/subtração de áreas)",
                    "Questões com plantas baixas e terrenos são comuns",
                ],
                "related_topics": ["Geometria Espacial", "Trigonometria"],
                "difficulty": "médio",
                "wiki_query": "Geometria plana áreas",
            },
            {
                "title": "Geometria Espacial",
                "summary": (
                    "Estudo dos sólidos geométricos tridimensionais.\n\n"
                    "Prismas:\n"
                    "• Volume = Área da base × altura\n"
                    "• Cubo: V = a³, A_total = 6a²\n"
                    "• Paralelepípedo: V = a × b × c\n\n"
                    "Pirâmides:\n"
                    "• Volume = (Área da base × altura) / 3\n\n"
                    "Cilindro:\n"
                    "• Volume = π × r² × h\n"
                    "• Área lateral = 2π × r × h\n"
                    "• Área total = 2πr(r + h)\n\n"
                    "Cone:\n"
                    "• Volume = (π × r² × h) / 3\n"
                    "• Área lateral = π × r × g (g = geratriz)\n\n"
                    "Esfera:\n"
                    "• Volume = (4/3) × π × r³\n"
                    "• Área = 4 × π × r²"
                ),
                "key_concepts": [
                    "Volume e área de prismas, cilindros, cones, esferas",
                    "Relação entre sólidos e planificação",
                    "Tronco de cone e pirâmide",
                    "Capacidade: 1L = 1dm³ = 1000cm³",
                ],
                "formulas": [
                    "V_prisma = A_base · h",
                    "V_pirâmide = A_base · h / 3",
                    "V_cilindro = π·r²·h",
                    "V_cone = π·r²·h / 3",
                    "V_esfera = 4π·r³ / 3",
                ],
                "tips": [
                    "Conversão de unidades é essencial: 1m³ = 1000L",
                    "Questões sobre caixas d'água, tanques e embalagens são frequentes",
                    "Saiba planificar sólidos (desdobrar em 2D)",
                ],
                "related_topics": ["Geometria Plana", "Razão, Proporção e Regra de Três"],
                "difficulty": "médio",
                "wiki_query": "Geometria espacial volume",
            },
            {
                "title": "Funções",
                "summary": (
                    "Função é uma relação entre dois conjuntos onde cada elemento do domínio "
                    "tem exatamente uma imagem no contradomínio.\n\n"
                    "Função Afim (1º grau): f(x) = ax + b\n"
                    "• Gráfico: reta\n"
                    "• a > 0: crescente | a < 0: decrescente\n"
                    "• Raiz (zero): x = -b/a\n\n"
                    "Função Quadrática (2º grau): f(x) = ax² + bx + c\n"
                    "• Gráfico: parábola\n"
                    "• a > 0: concavidade para cima | a < 0: para baixo\n"
                    "• Raízes: x = (-b ± √Δ) / 2a, onde Δ = b² - 4ac\n"
                    "• Vértice: xᵥ = -b/2a, yᵥ = -Δ/4a\n\n"
                    "Função Exponencial: f(x) = aˣ (a > 0, a ≠ 1)\n"
                    "Função Logarítmica: f(x) = log_a(x)"
                ),
                "key_concepts": [
                    "Domínio, contradomínio e imagem",
                    "Função afim, quadrática, exponencial, logarítmica",
                    "Gráficos e suas características",
                    "Máximo e mínimo da função quadrática",
                ],
                "formulas": [
                    "f(x) = ax + b (afim)",
                    "f(x) = ax² + bx + c (quadrática)",
                    "Δ = b² - 4ac",
                    "x = (-b ± √Δ) / 2a",
                    "xᵥ = -b/2a",
                ],
                "tips": [
                    "Saiba interpretar gráficos de funções — tema muito frequente",
                    "Problemas de máximo/mínimo usam função quadrática",
                    "Crescimento populacional e radioatividade usam exponencial",
                ],
                "related_topics": ["Matemática Financeira", "Geometria Analítica"],
                "difficulty": "médio",
                "wiki_query": "Funções matemáticas primeiro segundo grau",
            },
        ],
    },

    # ╔════════════════════════════════════════════════════════════╗
    # ║  3. CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS              ║
    # ╚════════════════════════════════════════════════════════════╝
    "Ciências da Natureza": {
        "emoji": "🔬",
        "description": "Ciências da Natureza e suas Tecnologias — Física, Química e Biologia.",
        "topics": [
            {
                "title": "Ecologia e Meio Ambiente",
                "summary": (
                    "Ecologia estuda as relações entre os seres vivos e o ambiente.\n\n"
                    "Níveis de organização: organismo → população → comunidade → ecossistema → biosfera\n\n"
                    "Relações ecológicas:\n"
                    "• Harmônicas: mutualismo, protocooperação, comensalismo\n"
                    "• Desarmônicas: parasitismo, predação, competição\n\n"
                    "Ciclos biogeoquímicos: água, carbono, nitrogênio, oxigênio\n\n"
                    "Problemas ambientais:\n"
                    "• Efeito estufa e aquecimento global (CO₂, CH₄)\n"
                    "• Desmatamento e perda de biodiversidade\n"
                    "• Poluição (ar, água, solo)\n"
                    "• Chuva ácida (SO₂, NOₓ)\n"
                    "• Destruição da camada de ozônio (CFCs)\n"
                    "• Eutrofização de rios e lagos\n\n"
                    "Biomas brasileiros: Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa, Pantanal"
                ),
                "key_concepts": [
                    "Cadeias e teias alimentares",
                    "Pirâmides ecológicas (energia, biomassa, números)",
                    "Ciclos biogeoquímicos",
                    "Biomas brasileiros e suas características",
                    "Desenvolvimento sustentável",
                ],
                "formulas": [],
                "tips": [
                    "Tema MAIS cobrado em Biologia no ENEM",
                    "Questões sempre relacionam ecologia com problemas ambientais atuais",
                    "Saiba os biomas brasileiros e seus problemas específicos",
                ],
                "related_topics": ["Evolução", "Energia e Recursos Naturais"],
                "difficulty": "médio",
                "wiki_query": "Ecologia meio ambiente biomas brasileiros",
            },
            {
                "title": "Energia e suas Transformações",
                "summary": (
                    "Energia é a capacidade de realizar trabalho ou provocar transformações.\n\n"
                    "Tipos de energia:\n"
                    "• Cinética: Ec = mv²/2\n"
                    "• Potencial gravitacional: Ep = mgh\n"
                    "• Potencial elástica: Ee = kx²/2\n"
                    "• Térmica, elétrica, química, nuclear, luminosa, sonora\n\n"
                    "Princípio da conservação de energia:\n"
                    "Energia não se cria nem se destrói, apenas se transforma.\n"
                    "Energia mecânica: Em = Ec + Ep (constante sem atrito)\n\n"
                    "Trabalho: W = F × d × cos(θ)\n"
                    "Potência: P = W/t = F × v\n\n"
                    "Fontes de energia:\n"
                    "• Renováveis: solar, eólica, hidráulica, biomassa\n"
                    "• Não renováveis: petróleo, carvão, gás natural, nuclear"
                ),
                "key_concepts": [
                    "Conservação de energia",
                    "Trabalho, potência e rendimento",
                    "Fontes renováveis vs não renováveis",
                    "Matriz energética brasileira",
                ],
                "formulas": [
                    "Ec = m·v²/2",
                    "Ep = m·g·h",
                    "W = F·d·cos(θ)",
                    "P = W/t",
                    "Rendimento = η = P_útil/P_total × 100%",
                ],
                "tips": [
                    "Conservação de energia é muito cobrado em Física no ENEM",
                    "Questões sobre matriz energética brasileira são frequentes",
                    "Saiba converter unidades: 1kWh = 3,6 × 10⁶ J",
                ],
                "related_topics": ["Ecologia e Meio Ambiente", "Termoquímica"],
                "difficulty": "médio",
                "wiki_query": "Energia mecânica conservação fontes renováveis",
            },
            {
                "title": "Termoquímica",
                "summary": (
                    "Estudo das trocas de calor nas reações químicas.\n\n"
                    "Reação exotérmica: libera calor (ΔH < 0)\n"
                    "Reação endotérmica: absorve calor (ΔH > 0)\n\n"
                    "Entalpia (H): energia armazenada nas ligações químicas.\n"
                    "ΔH = H_produtos - H_reagentes\n\n"
                    "Lei de Hess:\n"
                    "A variação de entalpia de uma reação depende apenas dos estados "
                    "inicial e final, não do caminho percorrido. Permite calcular ΔH "
                    "combinando reações intermediárias.\n\n"
                    "Energia de ligação:\n"
                    "ΔH = Σ(energia de ligação dos reagentes) - Σ(energia de ligação dos produtos)\n\n"
                    "Calorimetria:\n"
                    "Q = m × c × ΔT (calor sensível)\n"
                    "Q = m × L (calor latente)"
                ),
                "key_concepts": [
                    "Reações exotérmicas e endotérmicas",
                    "Lei de Hess",
                    "Entalpia de formação e combustão",
                    "Energia de ligação",
                    "Calorimetria",
                ],
                "formulas": [
                    "ΔH = H_prod - H_reag",
                    "Q = m·c·ΔT",
                    "Q = m·L",
                    "Lei de Hess: ΔH = ΔH₁ + ΔH₂ + ...",
                ],
                "tips": [
                    "Lei de Hess: manipule as equações (inverta, multiplique) para encontrar ΔH",
                    "Combustão é sempre exotérmica",
                    "Questões misturam Química com Física (calorimetria)",
                ],
                "related_topics": ["Energia e suas Transformações", "Estequiometria"],
                "difficulty": "médio",
                "wiki_query": "Termoquímica entalpia Lei de Hess",
            },
            {
                "title": "Estequiometria",
                "summary": (
                    "Estequiometria é o cálculo das quantidades de reagentes e produtos "
                    "em uma reação química.\n\n"
                    "Conceitos fundamentais:\n"
                    "• Mol: 6,022 × 10²³ partículas (Número de Avogadro)\n"
                    "• Massa molar (M): massa de 1 mol em gramas\n"
                    "• Volume molar (CNTP): 22,4 L/mol\n\n"
                    "Passos:\n"
                    "1. Escreva e balanceie a equação química\n"
                    "2. Identifique as grandezas envolvidas\n"
                    "3. Monte a proporção usando os coeficientes estequiométricos\n"
                    "4. Resolva a regra de três\n\n"
                    "Reagente limitante: reagente que se esgota primeiro e limita a produção.\n"
                    "Rendimento: quantidade real / quantidade teórica × 100%\n"
                    "Pureza: massa pura / massa total × 100%"
                ),
                "key_concepts": [
                    "Mol, massa molar, volume molar",
                    "Balanceamento de equações",
                    "Reagente limitante e em excesso",
                    "Rendimento e pureza",
                ],
                "formulas": [
                    "n = m / M (mols)",
                    "n = V / 22,4 (CNTP)",
                    "N = n × 6,022×10²³",
                    "Rendimento = (real/teórico) × 100%",
                ],
                "tips": [
                    "Sempre balanceie a equação ANTES de calcular",
                    "Identifique se há reagente limitante",
                    "Atenção às unidades: g, mol, L, moléculas",
                ],
                "related_topics": ["Termoquímica", "Soluções"],
                "difficulty": "médio",
                "wiki_query": "Estequiometria cálculo mol",
            },
            {
                "title": "Genética e Evolução",
                "summary": (
                    "Genética estuda a hereditariedade e a variação dos seres vivos.\n\n"
                    "Conceitos básicos:\n"
                    "• Gene: segmento de DNA que codifica uma proteína\n"
                    "• Alelo: versões diferentes de um gene (dominante/recessivo)\n"
                    "• Genótipo: composição genética (AA, Aa, aa)\n"
                    "• Fenótipo: característica expressa (genótipo + ambiente)\n"
                    "• Homozigoto: AA ou aa | Heterozigoto: Aa\n\n"
                    "Leis de Mendel:\n"
                    "• 1ª Lei (Segregação): cada indivíduo tem 2 alelos que se separam na formação dos gametas\n"
                    "• 2ª Lei (Segregação Independente): genes em cromossomos diferentes segregam independentemente\n\n"
                    "Evolução:\n"
                    "• Darwin: Seleção Natural — os mais aptos sobrevivem e se reproduzem\n"
                    "• Lamarck: uso e desuso + herança de caracteres adquiridos (superada)\n"
                    "• Neodarwinismo: seleção natural + genética (mutação + recombinação)"
                ),
                "key_concepts": [
                    "Leis de Mendel e cruzamentos",
                    "Dominância, codominância, herança ligada ao sexo",
                    "Seleção natural e adaptação",
                    "Especiação e isolamento reprodutivo",
                ],
                "formulas": [
                    "Proporção mendeliana: 3:1 (F2 monoíbrido)",
                    "Proporção diíbrida: 9:3:3:1",
                    "Hardy-Weinberg: p² + 2pq + q² = 1",
                ],
                "tips": [
                    "Saiba montar e interpretar heredogramas",
                    "Questões de evolução geralmente envolvem interpretação de texto",
                    "Diferencie Lamarck de Darwin — isso cai muito!",
                ],
                "related_topics": ["Ecologia e Meio Ambiente", "Biologia Celular"],
                "difficulty": "médio",
                "wiki_query": "Genética mendeliana evolução Darwin",
            },
            {
                "title": "Eletricidade",
                "summary": (
                    "Estudo das cargas elétricas, corrente, resistência e circuitos.\n\n"
                    "Corrente elétrica: fluxo ordenado de cargas\n"
                    "i = Q/t (Ampères)\n\n"
                    "Lei de Ohm: U = R × i\n"
                    "U = tensão (Volts), R = resistência (Ohms), i = corrente (Ampères)\n\n"
                    "Potência elétrica: P = U × i = R × i² = U²/R\n"
                    "Energia: E = P × t\n\n"
                    "Circuitos:\n"
                    "• Série: mesma corrente, resistência total = R₁ + R₂ + ...\n"
                    "• Paralelo: mesma tensão, 1/R_total = 1/R₁ + 1/R₂ + ...\n\n"
                    "Consumo residencial:\n"
                    "E (kWh) = P(kW) × t(h)\n"
                    "Custo = E(kWh) × tarifa (R$/kWh)"
                ),
                "key_concepts": [
                    "Lei de Ohm e resistência elétrica",
                    "Potência e consumo de energia",
                    "Circuitos em série e paralelo",
                    "Efeito Joule",
                ],
                "formulas": [
                    "U = R·i (Lei de Ohm)",
                    "P = U·i",
                    "E = P·t",
                    "Série: R_t = R₁ + R₂",
                    "Paralelo: 1/R_t = 1/R₁ + 1/R₂",
                ],
                "tips": [
                    "Questões sobre consumo de energia elétrica residencial são muito comuns",
                    "Saiba calcular o custo mensal de um aparelho: P × h × dias × tarifa",
                    "kWh é unidade de ENERGIA, não de potência",
                ],
                "related_topics": ["Energia e suas Transformações"],
                "difficulty": "médio",
                "wiki_query": "Eletricidade Lei de Ohm circuitos",
            },
        ],
    },

    # ╔════════════════════════════════════════════════════════════╗
    # ║  4. CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS                  ║
    # ╚════════════════════════════════════════════════════════════╝
    "Ciências Humanas": {
        "emoji": "🌍",
        "description": "Ciências Humanas e suas Tecnologias — História, Geografia, Filosofia e Sociologia.",
        "topics": [
            {
                "title": "Brasil Colônia e Império",
                "summary": (
                    "Brasil Colônia (1500-1822):\n"
                    "• Período Pré-Colonial (1500-1530): exploração do pau-brasil, escambo com indígenas\n"
                    "• Capitanias Hereditárias (1534): divisão do território em lotes\n"
                    "• Governo-Geral (1549): centralização administrativa. Tomé de Sousa, 1º governador\n"
                    "• Ciclo do Açúcar (séc. XVI-XVII): plantation, engenhos, trabalho escravo\n"
                    "• Invasões Holandesas (1630-1654): Nassau em Pernambuco\n"
                    "• Ciclo do Ouro (séc. XVIII): Minas Gerais, Derrama, Inconfidência Mineira (1789)\n\n"
                    "Brasil Império (1822-1889):\n"
                    "• Independência (1822): D. Pedro I, grito do Ipiranga\n"
                    "• Primeiro Reinado (1822-1831): Constituição de 1824, poder moderador\n"
                    "• Período Regencial (1831-1840): revoltas (Cabanagem, Farroupilha, Sabinada, Balaiada)\n"
                    "• Segundo Reinado (1840-1889): D. Pedro II, café, abolição (Lei Áurea 1888)"
                ),
                "key_concepts": [
                    "Colonização e exploração mercantilista",
                    "Escravidão e resistência (quilombos)",
                    "Movimentos de independência",
                    "Poder moderador e centralização",
                ],
                "formulas": [],
                "tips": [
                    "O ENEM não cobra datas, mas CONTEXTOS e CONSEQUÊNCIAS",
                    "Escravidão e resistência negra é tema muito frequente",
                    "Relacione o período colonial com questões de desigualdade atuais",
                ],
                "related_topics": ["Brasil República", "Cidadania e Direitos Humanos"],
                "difficulty": "médio",
                "wiki_query": "Brasil Colônia história",
            },
            {
                "title": "Brasil República",
                "summary": (
                    "República Velha (1889-1930):\n"
                    "• Política do café com leite (SP e MG alternando no poder)\n"
                    "• Coronelismo, voto de cabresto, curral eleitoral\n"
                    "• Movimentos: Canudos (1896), Cangaço, Tenentismo\n\n"
                    "Era Vargas (1930-1945):\n"
                    "• Governo Provisório (1930-34), Constitucional (1934-37), Estado Novo (1937-45)\n"
                    "• CLT, voto feminino, trabalhismo, populismo, censura no Estado Novo\n\n"
                    "República Populista (1945-1964):\n"
                    "• Vargas volta eleito (1950-54), JK e '50 anos em 5', Brasília\n"
                    "• João Goulart e as Reformas de Base\n\n"
                    "Ditadura Militar (1964-1985):\n"
                    "• AI-5, censura, tortura, 'milagre econômico'\n"
                    "• Abertura lenta e gradual, Diretas Já (1984)\n\n"
                    "Nova República (1985-):\n"
                    "• Constituição de 1988 (Constituição Cidadã)\n"
                    "• Redemocratização, impeachments, Plano Real"
                ),
                "key_concepts": [
                    "Coronelismo e república oligárquica",
                    "Populismo e trabalhismo (Vargas)",
                    "Ditadura militar e resistência",
                    "Constituição de 1988 e redemocratização",
                ],
                "formulas": [],
                "tips": [
                    "Ditadura Militar é o tema mais cobrado de História do Brasil no ENEM",
                    "Relacione os períodos com garantia/supressão de direitos",
                    "Compare diferentes momentos autoritários da história brasileira",
                ],
                "related_topics": ["Brasil Colônia e Império", "Cidadania e Direitos Humanos"],
                "difficulty": "médio",
                "wiki_query": "Brasil República história ditadura militar",
            },
            {
                "title": "Cidadania e Direitos Humanos",
                "summary": (
                    "Cidadania é o exercício de direitos e deveres civis, políticos e sociais.\n\n"
                    "Gerações de Direitos:\n"
                    "• 1ª geração: Direitos civis e políticos (liberdade) — séc. XVIII\n"
                    "• 2ª geração: Direitos sociais, econômicos, culturais (igualdade) — séc. XIX-XX\n"
                    "• 3ª geração: Direitos difusos e coletivos (fraternidade) — meio ambiente, paz\n\n"
                    "Constituição de 1988:\n"
                    "• Art. 5º: direitos e garantias fundamentais\n"
                    "• Art. 6º: direitos sociais (educação, saúde, trabalho, moradia)\n"
                    "• Sufrágio universal, voto direto e secreto\n\n"
                    "Movimentos sociais:\n"
                    "• Movimento negro, feminista, LGBTQIA+, indígena, MST\n"
                    "• Luta por reconhecimento e redistribuição\n\n"
                    "Declaração Universal dos Direitos Humanos (ONU, 1948):\n"
                    "• Todo ser humano nasce livre e igual em dignidade e direitos"
                ),
                "key_concepts": [
                    "Gerações de direitos (liberdade, igualdade, fraternidade)",
                    "Constituição de 1988 e direitos fundamentais",
                    "Movimentos sociais e luta por direitos",
                    "Democracia e participação política",
                ],
                "formulas": [],
                "tips": [
                    "Tema transversal no ENEM — aparece em todas as áreas",
                    "Questões relacionam direitos humanos com situações atuais",
                    "A redação SEMPRE envolve direitos humanos na proposta de intervenção",
                ],
                "related_topics": ["Brasil República", "Filosofia Política"],
                "difficulty": "fácil",
                "wiki_query": "Cidadania direitos humanos Constituição 1988",
            },
            {
                "title": "Globalização e Geopolítica",
                "summary": (
                    "Globalização é o processo de integração econômica, cultural e política mundial.\n\n"
                    "Aspectos da globalização:\n"
                    "• Econômica: multinacionais, livre comércio, blocos econômicos\n"
                    "• Cultural: homogeneização vs. valorização do local\n"
                    "• Tecnológica: internet, redes sociais, revolução digital\n\n"
                    "Blocos econômicos: UE, Mercosul, BRICS, NAFTA/USMCA\n\n"
                    "Organizações internacionais: ONU, OMC, FMI, Banco Mundial\n\n"
                    "Geopolítica atual:\n"
                    "• Ordem multipolar\n"
                    "• Conflitos: questão palestina, tensões EUA-China\n"
                    "• Crise migratória e refugiados\n"
                    "• Terrorismo e extremismo\n"
                    "• Mudanças climáticas e acordos ambientais (Paris, COP)"
                ),
                "key_concepts": [
                    "Globalização e seus efeitos positivos/negativos",
                    "Blocos econômicos e organizações internacionais",
                    "Nova ordem mundial multipolar",
                    "Conflitos contemporâneos e migrações",
                ],
                "formulas": [],
                "tips": [
                    "Geopolítica exige que você esteja atualizado!",
                    "Questões relacionam globalização com desigualdade social",
                    "Entenda o papel do Brasil nos blocos econômicos",
                ],
                "related_topics": ["Cidadania e Direitos Humanos", "Urbanização"],
                "difficulty": "médio",
                "wiki_query": "Globalização geopolítica blocos econômicos",
            },
            {
                "title": "Filosofia e Sociologia",
                "summary": (
                    "Filosofia no ENEM:\n"
                    "• Sócrates: método socrático, maiêutica, 'Só sei que nada sei'\n"
                    "• Platão: mundo das ideias, alegoria da caverna\n"
                    "• Aristóteles: lógica, ética, política, metafísica\n"
                    "• Maquiavel: 'O Príncipe', separação entre ética e política\n"
                    "• Contratualistas: Hobbes (Estado forte), Locke (liberalismo), Rousseau (vontade geral)\n"
                    "• Kant: imperativo categórico, razão e moral\n"
                    "• Marx: materialismo histórico, luta de classes, mais-valia\n"
                    "• Nietzsche: crítica à moral, super-homem\n\n"
                    "Sociologia no ENEM:\n"
                    "• Durkheim: fato social, solidariedade mecânica/orgânica, anomia\n"
                    "• Weber: ação social, tipos de dominação, ética protestante\n"
                    "• Marx: classes sociais, infraestrutura/superestrutura\n"
                    "• Bourdieu: capital cultural e social, reprodução\n"
                    "• Indústria cultural (Escola de Frankfurt): Adorno e Horkheimer"
                ),
                "key_concepts": [
                    "Filósofos clássicos e seus conceitos centrais",
                    "Contratualismo: Hobbes, Locke, Rousseau",
                    "Pais da Sociologia: Durkheim, Weber, Marx",
                    "Indústria cultural e sociedade de consumo",
                ],
                "formulas": [],
                "tips": [
                    "O ENEM não cobra decorar autores, mas INTERPRETAR suas ideias",
                    "Questões usam trechos de filósofos para interpretação",
                    "Marx e os contratualistas são os mais cobrados",
                ],
                "related_topics": ["Cidadania e Direitos Humanos", "Globalização e Geopolítica"],
                "difficulty": "médio",
                "wiki_query": "Filosofia sociologia ENEM contratualismo",
            },
            {
                "title": "Urbanização e Problemas Urbanos",
                "summary": (
                    "Urbanização é o processo de crescimento das cidades e migração campo-cidade.\n\n"
                    "Urbanização brasileira:\n"
                    "• Tardia e acelerada (a partir de 1950)\n"
                    "• Êxodo rural impulsionado pela industrialização\n"
                    "• Macrocefalia urbana: crescimento desordenado de metrópoles\n"
                    "• Hoje: mais de 85% da população é urbana\n\n"
                    "Problemas urbanos:\n"
                    "• Favelização e déficit habitacional\n"
                    "• Mobilidade urbana e trânsito\n"
                    "• Violência e segregação socioespacial\n"
                    "• Poluição e ilhas de calor\n"
                    "• Enchentes e deslizamentos\n"
                    "• Gentrificação\n\n"
                    "Conceitos:\n"
                    "• Conurbação: cidades que se unem fisicamente\n"
                    "• Metrópole e região metropolitana\n"
                    "• Megalópole: conjunto de metrópoles"
                ),
                "key_concepts": [
                    "Êxodo rural e urbanização acelerada",
                    "Macrocefalia urbana e segregação",
                    "Problemas urbanos contemporâneos",
                    "Conurbação, metrópole, megalópole",
                ],
                "formulas": [],
                "tips": [
                    "Urbanização brasileira é tema frequente no ENEM",
                    "Relacione problemas urbanos com desigualdade social",
                    "Questões podem usar mapas, imagens de satélite e gráficos",
                ],
                "related_topics": ["Globalização e Geopolítica", "Cidadania e Direitos Humanos"],
                "difficulty": "fácil",
                "wiki_query": "Urbanização brasileira problemas urbanos",
            },
        ],
    },
}

# ── Índice rápido para busca ─────────────────────────────────


def get_all_topics() -> list[dict]:
    """Retorna lista plana de todos os tópicos com sua área."""
    topics = []
    for area, data in ENEM_SYLLABUS.items():
        for topic in data["topics"]:
            topics.append({
                "area": area,
                "area_emoji": data["emoji"],
                "area_description": data["description"],
                **topic,
            })
    return topics


def get_topics_by_area(area: str) -> list[dict]:
    """Retorna tópicos de uma área específica."""
    data = ENEM_SYLLABUS.get(area, {})
    return data.get("topics", [])


def get_topic(area: str, title: str) -> dict | None:
    """Retorna um tópico específico."""
    for topic in get_topics_by_area(area):
        if topic["title"] == title:
            return topic
    return None


def _normalize(text: str) -> str:
    """Remove acentos e converte para minúsculo para busca flexível."""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def search_topics(query: str) -> list[tuple[str, dict]]:
    """Busca tópicos pelo nome ou conteúdo.
    Retorna lista de tuplas (area_key, topic_dict) ordenadas por relevância.
    Ignora acentos (ex: 'funcao' encontra 'Funções').
    """
    q = _normalize(query)
    scored = []
    for area_key, area_data in ENEM_SYLLABUS.items():
        for topic in area_data["topics"]:
            score = 0
            if q in _normalize(topic["title"]):
                score += 3
            if q in _normalize(topic["summary"]):
                score += 1
            for concept in topic["key_concepts"]:
                if q in _normalize(concept):
                    score += 2
            if topic.get("tips"):
                for tip in topic["tips"]:
                    if q in _normalize(tip):
                        score += 1
            if topic.get("formulas"):
                for f in topic["formulas"]:
                    if q in _normalize(f):
                        score += 1
            if score > 0:
                scored.append((score, area_key, topic))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(area_key, topic) for _, area_key, topic in scored]
