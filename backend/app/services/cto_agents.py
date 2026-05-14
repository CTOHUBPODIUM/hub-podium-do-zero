CTO_AGENT_SYSTEM_ID = "CTO_AGENT_SYSTEM_BETA_001"
CTO_EXECUTIVE_NAME = "Rafael Duarte"

CTO_DEVELOPMENT_AGENTS = [
    {
        "code": "agent_product_architecture",
        "name": "Agente de Produto e Arquitetura",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Traduzir prioridade do CEO em escopo tecnico, arquitetura e criterios de aceite.",
        "responsibilities": [
            "Organizar roadmap beta do app",
            "Definir contratos entre app, backend, PDF, card e HUB-ELITE",
            "Validar se cada entrega atende o produto real",
        ],
        "tools": ["README", "docs", "schema.sql", "Flask API", "Expo app"],
    },
    {
        "code": "agent_mobile_development",
        "name": "Agente de Desenvolvimento Mobile",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Construir a experiencia beta do app para pais, responsaveis e atletas Sub-8 a Sub-20.",
        "responsibilities": [
            "Implementar cadastro do atleta",
            "Capturar foto e video por camera nativa",
            "Selecionar foto/video da galeria quando necessario",
            "Cadastrar WhatsApp do responsavel e clube do coracao",
            "Enviar dados para backend",
            "Receber analise HUB-ELITE",
            "Salvar e compartilhar PDF/card",
        ],
        "tools": ["Expo", "React Native", "expo-image-picker", "expo-file-system", "expo-sharing"],
    },
    {
        "code": "agent_backend_programming",
        "name": "Agente de Programacao Backend",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Criar APIs beta para analise automatica, pacote de entrega e governanca tecnica.",
        "responsibilities": [
            "Receber upload de foto e video",
            "Executar reconhecimento facial beta entre foto e frames do video",
            "Executar algoritmo HUB-ELITE com comparativo de perfil respeitando familia da posicao",
            "Gerar relatorio PDF com foto e atleta de referencia",
            "Gerar card estilo FIFA com blocos e foto",
            "Expor endpoints de agentes e ferramentas",
        ],
        "tools": ["Python", "Flask", "OpenCV", "NumPy", "Pillow", "ReportLab"],
    },
    {
        "code": "agent_implementation_release",
        "name": "Agente de Implementacao e Release",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Empacotar a beta, validar fluxo completo e preparar entrega para testes reais.",
        "responsibilities": [
            "Validar rotas da API",
            "Validar fluxo app-backend",
            "Registrar pendencias tecnicas",
            "Preparar checklist de beta",
        ],
        "tools": ["git", "npm", "python", "pip", "Expo CLI"],
    },
    {
        "code": "agent_tool_interconnection",
        "name": "Agente de Interconexao de Ferramentas",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Conectar todas as ferramentas utilizaveis para que a beta opere como produto real.",
        "responsibilities": [
            "Conectar app ao backend",
            "Conectar app as cameras de celulares e tablets",
            "Planejar conexao web com webcam em computadores",
            "Conectar backend ao HUB-ELITE",
            "Conectar backend ao reconhecimento facial beta",
            "Conectar backend aos geradores PDF/card",
            "Preparar futuras conexoes com Supabase, storage e pagamentos",
        ],
        "tools": ["Expo", "ImagePicker camera", "Flask", "OpenCV", "Supabase futuro", "Mercado Pago futuro", "Vercel futuro", "Render futuro"],
    },
]

CTO_DEPARTMENT_TEAMS = [
    {
        "code": "time_app",
        "name": "Time App",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Construir e evoluir o aplicativo HUB-PODIUM para atletas Sub-8 a Sub-20, pais e responsaveis.",
        "autonomy": [
            "Definir fluxo mobile dentro da prioridade aprovada pelo CEO e board",
            "Executar telas, camera, uploads, compartilhamento e experiencia por categoria",
            "Aprovar ajustes de usabilidade que nao alterem preco, marca oficial ou politica de dados",
        ],
        "interfaces": ["Time Plataforma", "Time Algoritmo", "CMO", "CCO"],
        "agents": [
            {
                "code": "agent_app_product_experience",
                "person_name": "Camila Rocha",
                "name": "Agente de Produto e Experiencia Mobile",
                "function": "Desenhar a jornada do atleta, responsavel e avaliador dentro do app.",
                "responsibilities": [
                    "Separar experiencia emocional para Sub-8 a Sub-12",
                    "Separar experiencia evolutiva para Sub-13 a Sub-20",
                    "Definir cadastro, consentimento, foto obrigatoria e dados do responsavel",
                    "Garantir clareza no resultado, PDF, card e WhatsApp",
                ],
                "training_focus": "Benchmark de FotMob, OneFootball, FIFA+, Tonsser e Trace para jornada, linguagem, engajamento e entrega familiar.",
                "tools": ["Expo", "React Native", "Expo Router futuro", "Firebase Remote Config futuro", "docs", "feedback beta"],
            },
            {
                "code": "agent_mobile_engineering",
                "person_name": "Mateus Albuquerque",
                "name": "Agente de Engenharia Mobile",
                "function": "Implementar telas, estado, camera, galeria, upload e consumo das APIs.",
                "responsibilities": [
                    "Manter o app funcionando em iOS e Android",
                    "Integrar camera de foto e video em celulares e tablets",
                    "Enviar foto, video e formulario para o backend",
                    "Receber pacote de analise, PDF e card",
                ],
                "training_focus": "Arquitetura Expo/React Native, EAS, TypeScript futuro, cache de API, upload resiliente e performance mobile.",
                "tools": ["Expo", "React Native", "EAS CLI", "npm", "expo-image-picker", "expo-file-system", "expo-sharing"],
            },
            {
                "code": "agent_mobile_quality_release",
                "person_name": "Renata Iwata",
                "name": "Agente de Qualidade e Release Mobile",
                "function": "Validar estabilidade, compatibilidade e entrega da beta do aplicativo.",
                "responsibilities": [
                    "Testar Expo Go, builds e fluxo completo app-backend",
                    "Registrar falhas por aparelho, versao e rede",
                    "Validar cadastro, camera, envio, relatorio e card",
                    "Preparar checklist de release mobile",
                ],
                "training_focus": "Matriz de testes em aparelhos reais, Expo Doctor, EAS Build, Sentry futuro, TestFlight e Play Internal Testing.",
                "tools": ["Expo CLI", "EAS Build", "Expo Doctor", "npm", "git", "iPhone", "Android"],
            },
            {
                "code": "agent_app_support_delivery",
                "person_name": "Joao Pedro Salles",
                "name": "Agente de Suporte e Entrega do App",
                "function": "Cuidar da entrega do resultado para pais, responsaveis e clientes.",
                "responsibilities": [
                    "Validar compartilhamento por WhatsApp",
                    "Garantir acesso ao PDF e card no aparelho",
                    "Organizar mensagens de erro e orientacao ao usuario",
                    "Coletar feedback da beta para priorizacao",
                ],
                "training_focus": "Entrega familiar inspirada em Trace, Hudl e Tonsser: highlights, resultado claro, suporte e recorrencia.",
                "tools": ["WhatsApp", "expo-sharing", "Firebase Analytics futuro", "RevenueCat futuro", "docs", "suporte beta"],
            },
        ],
    },
    {
        "code": "time_plataforma",
        "name": "Time Plataforma",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Sustentar backend, banco, APIs, seguranca, integracoes e operacao tecnica do produto.",
        "autonomy": [
            "Definir contratos de API e padroes tecnicos aprovados pelo CTO",
            "Executar infraestrutura, logs, banco, storage e integracoes do MVP",
            "Bloquear releases que violem seguranca, privacidade ou estabilidade",
        ],
        "interfaces": ["Time App", "Time Algoritmo", "CFO", "CCO"],
        "agents": [
            {
                "code": "agent_backend_api",
                "name": "Agente de API Backend",
                "function": "Construir e manter endpoints Flask para analise, governanca e entregaveis.",
                "responsibilities": [
                    "Manter rotas de saude, analise, PDF, card e governanca",
                    "Validar payloads de cadastro, foto e video",
                    "Integrar backend com HUB-ELITE e reconhecimento facial",
                    "Documentar contratos para app e plataforma",
                ],
                "tools": ["Python", "Flask", "pytest futuro", "Postman futuro"],
            },
            {
                "code": "agent_infrastructure_devops",
                "name": "Agente de Infraestrutura e DevOps",
                "function": "Preparar ambientes locais, beta e producao para operar como empresa real.",
                "responsibilities": [
                    "Configurar backend em Render ou ambiente equivalente",
                    "Configurar landing e plataforma web em Vercel",
                    "Controlar variaveis de ambiente, logs e health checks",
                    "Organizar processo de deploy e rollback",
                ],
                "tools": ["git", "Render", "Vercel", "Cloudflare Tunnel", "logs"],
            },
            {
                "code": "agent_data_security",
                "name": "Agente de Dados e Seguranca",
                "function": "Proteger dados de atletas, responsaveis, fotos, videos, PDFs e cards.",
                "responsibilities": [
                    "Modelar banco Supabase/PostgreSQL",
                    "Definir politicas de LGPD, consentimento e retencao",
                    "Proteger upload, armazenamento e acesso aos arquivos",
                    "Registrar auditoria tecnica das analises",
                ],
                "tools": ["PostgreSQL", "Supabase futuro", "schema.sql", "LGPD"],
            },
            {
                "code": "agent_integrations",
                "name": "Agente de Integracoes",
                "function": "Conectar HUB-PODIUM a servicos externos usados pelo produto.",
                "responsibilities": [
                    "Planejar Mercado Pago para monetizacao",
                    "Planejar WhatsApp para compartilhamento e relacionamento",
                    "Integrar storage externo para videos e entregaveis",
                    "Preparar APIs de clubes, escolas e parceiros",
                ],
                "tools": ["Mercado Pago futuro", "WhatsApp", "Supabase Storage futuro", "APIs externas"],
            },
        ],
    },
    {
        "code": "time_algoritmo",
        "name": "Time Algoritmo",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Evoluir o HUB-ELITE para analise automatica, reconhecimento facial e comparativo esportivo confiavel.",
        "autonomy": [
            "Definir metricas tecnicas de performance por categoria e posicao",
            "Ajustar regras de similaridade sem ferir coerencia esportiva aprovada pelo CTO",
            "Reprovar comparativos incoerentes entre posicoes incompativeis",
        ],
        "interfaces": ["Time App", "Time Plataforma", "CEO", "CTO"],
        "agents": [
            {
                "code": "agent_hub_elite_scoring",
                "person_name": "Helena Martins",
                "name": "Agente de Scoring HUB-ELITE",
                "function": "Definir pontuacao, atributos e leitura de performance por categoria.",
                "responsibilities": [
                    "Calibrar metricas Sub-8 a Sub-20",
                    "Separar atributos tecnicos, fisicos, taticos e mentais",
                    "Gerar notas usadas no relatorio e card",
                    "Evoluir benchmarks por idade e posicao",
                ],
                "training_focus": "Python cientifico, NumPy, scikit-learn, metricas esportivas e benchmarks por categoria.",
                "tools": ["Python", "NumPy", "scikit-learn", "HUB-ELITE", "MLflow futuro", "base de referencias"],
            },
            {
                "code": "agent_computer_vision",
                "person_name": "Bruno Kato",
                "name": "Agente de Visao Computacional",
                "function": "Analisar imagens e videos para detectar rosto, frames uteis e sinais de movimento.",
                "responsibilities": [
                    "Comparar foto do cadastro com frames do video",
                    "Melhorar reconhecimento facial beta",
                    "Preparar rastreamento multi-atleta",
                    "Avaliar qualidade minima de imagem e video",
                ],
                "training_focus": "OpenCV, MediaPipe, YOLO, extracao de frames, pose estimation e qualidade de video.",
                "tools": ["OpenCV", "MediaPipe futuro", "Ultralytics YOLO futuro", "Python", "frames de video", "embeddings faciais futuros"],
            },
            {
                "code": "agent_profile_matching",
                "person_name": "Lara Nascimento",
                "name": "Agente de Perfil e Similaridade",
                "function": "Comparar o atleta com referencias reais ou arquetipos compativeis.",
                "responsibilities": [
                    "Evitar similaridade incoerente entre atacante e goleiro",
                    "Criar familias de posicao antes do comparativo",
                    "Gerar frase de perfil para o relatorio",
                    "Selecionar atleta de referencia por estilo, posicao e categoria",
                ],
                "training_focus": "Metric learning, similaridade vetorial, familias de posicao e explicabilidade do resultado.",
                "tools": ["HUB-ELITE", "Python", "scikit-learn", "tabelas de perfil", "validacao esportiva"],
            },
            {
                "code": "agent_model_validation",
                "person_name": "Diego Torres",
                "name": "Arquiteto Global do Algoritmo HUB-ELITE",
                "function": "Desenhar a arquitetura global do HUB-ELITE, sua governanca tecnica e o mapa evolutivo Golden Ball.",
                "responsibilities": [
                    "Definir o blueprint masculino e feminino do algoritmo",
                    "Separar avaliacao atual, potencial evolutivo e estagio competitivo",
                    "Validar resultados por categoria e posicao",
                    "Criar criterios de confianca baixa, media e alta",
                    "Sinalizar quando precisa de revisao humana",
                    "Documentar limites do algoritmo no relatorio",
                ],
                "training_focus": "Arquitetura de algoritmo, scouting, alto rendimento, testes, auditoria, reproducibilidade, versao de dataset, confianca e governanca do modelo.",
                "tools": ["pytest futuro", "MLflow futuro", "DVC futuro", "amostras beta", "metricas", "relatorios", "blueprint HUB-ELITE"],
            },
        ],
    },
    {
        "code": "time_novos_produtos_digitais",
        "name": "Time Novos Produtos Digitais",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "mission": "Transformar aprendizados do app em novos produtos digitais para atletas, pais, clubes e parceiros.",
        "autonomy": [
            "Propor novos produtos sem desviar a prioridade do app beta",
            "Criar prototipos e provas de conceito aprovadas pelo CTO",
            "Levar modelos comerciais ao CCO, CFO e CEO antes de producao",
        ],
        "interfaces": ["CEO", "CCO", "CMO", "CFO", "Time Plataforma"],
        "agents": [
            {
                "code": "agent_product_discovery",
                "name": "Agente de Descoberta de Produto",
                "function": "Mapear oportunidades digitais a partir de atletas, pais, escolas e clubes.",
                "responsibilities": [
                    "Entrevistar usuarios da beta",
                    "Identificar dores de pais, responsaveis, treinadores e clubes",
                    "Priorizar ideias por impacto, custo e alinhamento estrategico",
                    "Transformar oportunidades em briefings de produto",
                ],
                "tools": ["pesquisa", "docs", "metricas beta", "CRM futuro"],
            },
            {
                "code": "agent_digital_product_design",
                "name": "Agente de Design de Produtos Digitais",
                "function": "Criar prototipos de novas experiencias digitais HUB-PODIUM.",
                "responsibilities": [
                    "Prototipar painel de pais e responsaveis",
                    "Prototipar painel de treinadores e clubes",
                    "Prototipar historico evolutivo do atleta",
                    "Validar linguagem visual com CMO",
                ],
                "tools": ["Figma futuro", "React futuro", "landing-page", "design system"],
            },
            {
                "code": "agent_growth_experiments",
                "name": "Agente de Experimentos de Crescimento",
                "function": "Testar canais, ofertas e jornadas digitais para aquisicao de usuarios.",
                "responsibilities": [
                    "Criar testes de landing pages e funis",
                    "Acompanhar conversao de interessados para analises pagas",
                    "Gerar hipoteses de campanhas com CMO",
                    "Medir tracao por categoria, cidade e parceiro",
                ],
                "tools": ["landing-page", "analytics futuro", "campanhas", "CRM futuro"],
            },
            {
                "code": "agent_business_models",
                "name": "Agente de Modelos Digitais e Parcerias",
                "function": "Estruturar produtos digitais monetizaveis com clubes, escolas e academias.",
                "responsibilities": [
                    "Criar pacote para escolas de futebol",
                    "Criar pacote para clubes e avaliadores",
                    "Planejar marketplace de servicos esportivos",
                    "Levar impacto financeiro para CFO e estrategia comercial para CCO",
                ],
                "tools": ["docs", "precificacao futura", "parcerias", "Mercado Pago futuro"],
            },
        ],
    },
]

ALGORITHM_TEAM_TRAINING_PROGRAM = {
    "program": "HUB-ELITE Algorithm Excellence Program",
    "owner": "CTO",
    "owner_name": CTO_EXECUTIVE_NAME,
    "team": "Time Algoritmo",
    "status": "training_cycle_started",
    "started_at": "2026-05-01",
    "current_cycle": "Sprint 0 - Fundacao de elite HUB-ELITE",
    "authority": {
        "level": "full_cto_operational_authority",
        "granted_by": "CEO",
        "scope": [
            "Instalar e validar ferramentas tecnicas necessarias ao algoritmo",
            "Pesquisar fontes publicas e cadastradas permitidas",
            "Criar baselines, testes e criterios de confianca",
            "Evoluir reconhecimento facial, visao computacional e similaridade esportiva",
        ],
        "guardrails": [
            "Nao copiar dados proprietarios pagos sem licenca ou aprovacao do board",
            "Nao publicar comparativo sem posicao, categoria, fonte e nivel de confianca",
            "Nao transformar similaridade esportiva em promessa de carreira profissional",
        ],
    },
    "goal": "Elevar o Time Algoritmo ao padrao de mercado em IA aplicada, visao computacional, validacao e produto esportivo.",
    "global_architect": {
        "person_name": "Diego Torres",
        "title": "Arquiteto Global do Algoritmo HUB-ELITE",
        "status": "appointed",
        "appointed_at": "2026-05-07",
        "formal_plan": "docs/ALGORITHM_GLOBAL_ARCHITECT_FORMATION_PLAN.md",
        "golden_ball_map": "docs/HUB_ELITE_GOLDEN_BALL_MAP.md",
        "executive_roadmap": "docs/ALGORITHM_GLOBAL_ARCHITECT_EXECUTIVE_ROADMAP_2026_05_07.md",
        "kpi_scoreboard": "docs/HUB_ELITE_ALGORITHM_KPI_SCOREBOARD_2026_05_07.md",
        "mission": "Transformar o HUB-ELITE em um mapa completo de desenvolvimento esportivo para futebol masculino e feminino, com rigor tecnico, governanca e comparativos coerentes.",
    },
    "kpis": {
        "scoreboard_document": "docs/HUB_ELITE_ALGORITHM_KPI_SCOREBOARD_2026_05_07.md",
        "executive_frequency": "weekly",
        "owners": {
            "consolidation": "Diego Torres",
            "technical_validation": "Rafael Duarte",
            "strategic_readout": "Eduardo Valença",
        },
        "priority_metrics": [
            "coerencia_posicional",
            "coerencia_trilha_competitiva",
            "taxa_comparativo_incoerente_critico",
            "taxa_analise_liberada_com_confianca_adequada",
            "taxa_video_utilizavel",
            "confiabilidade_foto_video_do_atleta",
            "cobertura_base_masculina",
            "cobertura_base_feminina",
            "aderencia_ao_mapa_golden_ball",
        ],
    },
    "facial_recognition_target": {
        "status": "program_started",
        "goal": "Atingir 90 por cento de confianca operacional medida em validacao controlada para verificacao foto-video do atleta.",
        "important_note": "A meta so sera considerada atingida com benchmark rotulado e auditoria de validacao, nao apenas por threshold interno de codigo.",
        "current_method": "opencv_haar_histogram_beta",
    },
    "kickoff_order": {
        "issued_by": CTO_EXECUTIVE_NAME,
        "issued_at": "2026-05-01",
        "status": "in_execution",
        "operational_command": "Iniciar treinamento imediato com foco em transformar o HUB-ELITE em motor confiavel de analise automatica, perfil esportivo e comparacao com atletas reais.",
        "first_48_hours": [
            "Rodar checagem tecnica do ambiente de algoritmo",
            "Validar regras anti-comparativo incoerente no analisador atual",
            "Criar backlog de features para top 100 atletas por posicao",
            "Definir criterios minimos de confianca para liberar resultado ao app beta",
        ],
        "training_artifact": "docs/ALGORITHM_TRAINING_KICKOFF_2026_05_01.md",
        "validation_script": "tools/algorithm_training_check.py",
    },
    "market_references": [
        {
            "name": "Andrej Karpathy",
            "signal": "Implementacoes minimalistas e didaticas de modelos complexos.",
            "practices_to_adopt": [
                "Dominar fundamentos antes de adicionar complexidade",
                "Criar prototipos pequenos, legiveis e reproduziveis",
                "Usar PyTorch para experimentacao e C/CUDA apenas quando performance justificar",
            ],
            "tools": ["Python", "PyTorch", "C/CUDA", "GitHub"],
            "sources": ["https://github.com/karpathy/nanoGPT", "https://github.com/karpathy/llm.c"],
        },
        {
            "name": "Francois Chollet",
            "signal": "Criacao do Keras e foco em APIs simples para deep learning produtivo.",
            "practices_to_adopt": [
                "Projetar APIs de algoritmo simples para produto",
                "Separar backend tecnico de experiencia do usuario",
                "Manter portabilidade entre JAX, TensorFlow e PyTorch quando fizer sentido",
            ],
            "tools": ["Keras 3", "TensorFlow", "JAX", "PyTorch"],
            "sources": ["https://keras.io/getting_started/about/"],
        },
        {
            "name": "Jeremy Howard e fast.ai",
            "signal": "Aprendizado pratico, foco em entregas reais e PyTorch por tras da biblioteca fastai.",
            "practices_to_adopt": [
                "Treinar por projetos reais, nao apenas teoria",
                "Comecar com baselines simples e evoluir por experimentos",
                "Documentar cada decisao de modelo em linguagem de produto",
            ],
            "tools": ["Python", "PyTorch", "fastai", "Kaggle"],
            "sources": ["https://course19.fast.ai/"],
        },
        {
            "name": "Google DeepMind / Demis Hassabis",
            "signal": "Pesquisa de fronteira com benchmarks rigorosos, como AlphaFold.",
            "practices_to_adopt": [
                "Tratar validacao como parte central do algoritmo",
                "Separar treino, avaliacao, inferencia e auditoria",
                "Manter protocolo claro de confianca antes de publicar resultado",
            ],
            "tools": ["JAX", "TensorFlow", "XLA", "benchmarks cientificos"],
            "sources": ["https://www.nature.com/articles/s41586-021-03819-2"],
        },
    ],
    "toolchain": [
        {
            "layer": "Base cientifica",
            "tools": ["Python 3.12", "NumPy", "pandas", "scikit-learn", "OpenCV", "pytest"],
            "status": "install_now",
            "purpose": "Pontuacao, similaridade, validacao estatistica, analise de imagem e video.",
        },
        {
            "layer": "Visao computacional esportiva",
            "tools": ["OpenCV", "MediaPipe Pose Landmarker", "Ultralytics YOLO pose/tracking"],
            "status": "technical_spike",
            "purpose": "Rosto, pose, deteccao, rastreamento e qualidade de movimento.",
        },
        {
            "layer": "Deep learning",
            "tools": ["PyTorch", "Keras 3", "JAX", "Hugging Face Transformers"],
            "status": "planned_after_dataset",
            "purpose": "Fine-tuning, embeddings, classificadores e modelos multimodais.",
        },
        {
            "layer": "MLOps e qualidade",
            "tools": ["MLflow", "Weights & Biases", "DVC", "pytest"],
            "status": "planned_after_first_dataset",
            "purpose": "Rastrear experimentos, datasets, metricas, versoes e regressao de modelo.",
        },
    ],
    "agent_training": [
        {
            "agent_code": "agent_hub_elite_scoring",
            "person_name": "Helena Martins",
            "title": "Lider de Scoring HUB-ELITE",
            "training_mission": "Transformar atributos esportivos em notas comparaveis por categoria e posicao.",
            "tools_to_master": ["Python", "NumPy", "pandas", "scikit-learn", "pytest", "MLflow futuro"],
            "sprint_0_assignment": "Criar matriz inicial de features por posicao e validar normalizacao por categoria Sub-8 a Sub-20.",
            "deliverables_30_days": [
                "Matriz de atributos por categoria Sub-8 a Sub-20",
                "Regra de normalizacao por idade e posicao",
                "Baseline de scoring com testes",
            ],
        },
        {
            "agent_code": "agent_computer_vision",
            "person_name": "Bruno Kato",
            "title": "Lider de Visao Computacional",
            "training_mission": "Evoluir reconhecimento facial beta para leitura de video com qualidade esportiva.",
            "tools_to_master": ["OpenCV", "MediaPipe Pose Landmarker", "Ultralytics YOLO pose/tracking", "PyTorch futuro"],
            "sprint_0_assignment": "Definir protocolo de qualidade de foto/video e spike de pose estimation em frames de futebol.",
            "deliverables_30_days": [
                "Checklist de qualidade minima de foto e video",
                "Pipeline de frames uteis para analise",
                "Plano de pose estimation para futebol",
            ],
        },
        {
            "agent_code": "agent_profile_matching",
            "person_name": "Lara Nascimento",
            "title": "Lider de Perfil e Similaridade",
            "training_mission": "Criar comparativos esportivos coerentes, explicaveis e compativeis com posicao.",
            "tools_to_master": ["Python", "scikit-learn", "metric learning", "HUB-ELITE"],
            "sprint_0_assignment": "Blindar o comparativo por familia posicional e desenhar ranking top 100 sem misturar funcoes incompativeis.",
            "deliverables_30_days": [
                "Mapa de familias de posicao",
                "Regra anti-comparativo incoerente",
                "Frases de similaridade para relatorio dos pais",
            ],
        },
        {
            "agent_code": "agent_model_validation",
            "person_name": "Diego Torres",
            "title": "Arquiteto Global do Algoritmo HUB-ELITE",
            "training_mission": "Transformar o algoritmo em um motor esportivo de alcance global, com scouting, IA, validacao e mapa evolutivo Golden Ball.",
            "tools_to_master": ["pytest", "MLflow", "DVC", "metricas de confianca", "auditoria de fontes", "scouting moderno", "arquitetura HUB-ELITE"],
            "sprint_0_assignment": "Criar o blueprint do HUB-ELITE, os gates de confianca para analise, dataset, reconhecimento facial e a primeira versao do mapa Golden Ball.",
            "deliverables_30_days": [
                "Blueprint masculino e feminino do HUB-ELITE",
                "Criterios de confianca baixa, media e alta",
                "Checklist de revisao humana",
                "Suite inicial de testes do algoritmo",
                "Mapa Golden Ball com estagios de progressao do atleta",
            ],
        },
    ],
    "training_tracks": [
        {
            "period": "Semana 1",
            "module": "Fundamentos e baseline",
            "outcome": "Todo agente consegue ler, testar e explicar o HUB-ELITE atual.",
        },
        {
            "period": "Semanas 2-3",
            "module": "Visao computacional aplicada ao futebol",
            "outcome": "Pipeline de foto, frames, rosto, pose e qualidade de video definido.",
        },
        {
            "period": "Semanas 4-5",
            "module": "Similaridade, perfis e familias de posicao",
            "outcome": "Comparativos deixam de misturar perfis esportivos incompativeis.",
        },
        {
            "period": "Semanas 6-7",
            "module": "Validacao, metricas e confianca",
            "outcome": "Cada resultado passa por criterio de confianca e risco antes de entrar no PDF.",
        },
        {
            "period": "Semana 8",
            "module": "Entrega de produto",
            "outcome": "Relatorio e card explicam o resultado com clareza para pais, atletas e clubes.",
        },
    ],
    "non_negotiable_rules": [
        "Atacante nunca deve ser comparado como goleiro sem justificativa tecnica explicita.",
        "Todo comparativo precisa respeitar categoria, posicao, estilo e confianca minima.",
        "Reconhecimento facial deve informar limite tecnico quando a imagem ou video forem ruins.",
        "Nenhuma decisao sensivel sobre atleta deve ocultar criterio, limite ou necessidade de revisao humana.",
    ],
}

FACIAL_RECOGNITION_90_PLAN = {
    "program": "HUB-PODIUM Face Recognition 90 Plan",
    "owner": "CTO",
    "owner_name": CTO_EXECUTIVE_NAME,
    "status": "sprint_1_in_execution",
    "issued_at": "2026-05-02",
    "current_sprint": "Sprint 1 - Baseline audit and quality gate foundation",
    "target": {
        "metric_name": "photo_to_video_identity_verification",
        "goal_percent": 90,
        "rule": "A meta vale apenas quando o modelo atingir pelo menos 90 por cento na validacao rotulada definida pelo Time Algoritmo.",
        "quality_scope": [
            "um atleta principal por video",
            "foto frontal ou semi-frontal com rosto detectavel",
            "video com iluminacao aceitavel",
            "rosto detectado em frames uteis",
        ],
    },
    "current_state": {
        "method": "opencv_haar_histogram_beta",
        "maturity": "baseline_beta",
        "can_support": [
            "triagem inicial",
            "alerta de baixa confianca",
            "comparacao simples entre foto e frames",
        ],
        "cannot_claim_yet": [
            "90 por cento real em producao",
            "robustez forte contra angulo, oclusao, baixa luz e multiatleta",
            "benchmark estatistico confiavel sem base rotulada",
        ],
        "main_gaps": [
            "detector facial antigo e sensivel a variacao de pose",
            "assinatura por histograma e fraca para identidade real",
            "poucos frames amostrados",
            "ausencia de dataset rotulado de validacao HUB-PODIUM",
            "ausencia de gate forte de qualidade antes da verificacao",
        ],
    },
    "team_command": {
        "cto_message": "Rafael determina que o Time Algoritmo trate 90 por cento de reconhecimento facial como meta tecnica de release e nao como marketing. O time deve medir, validar, bloquear quando a confianca real nao estiver comprovada e subir de nivel por etapas.",
        "board_rule": "Nenhum material comercial deve prometer 90 por cento antes do benchmark oficial aprovado por Diego Torres e pelo CTO.",
    },
    "kickoff_order": {
        "issued_by": CTO_EXECUTIVE_NAME,
        "issued_at": "2026-05-02",
        "status": "in_execution",
        "artifact": "docs/FACIAL_RECOGNITION_90_KICKOFF_2026_05_02.md",
        "first_72_hours": [
            "Bruno Kato mede o baseline atual e propõe recorte facial mais robusto",
            "Diego Torres define benchmark rotulado inicial e matriz de avaliacao",
            "Helena Martins fecha score minimo de qualidade para foto e video",
            "Lara Nascimento define textos e gates de alta, media e baixa confianca no relatorio",
        ],
        "checkpoint": {
            "date": "2026-05-06",
            "expected_outputs": [
                "baseline facial medido",
                "criterios de qualidade definidos",
                "threshold beta revisado",
                "backlog de embeddings e multi-frame priorizado",
            ],
        },
    },
    "workstreams": [
        {
            "owner": "Bruno Kato",
            "front": "deteccao e embeddings faciais",
            "mission": "Substituir o baseline por pipeline moderno com detector mais robusto, extracao de embeddings e agregacao multi-frame.",
            "deliverables": [
                "avaliacao de MediaPipe Face Detector ou Face Landmarker para recorte mais estavel",
                "spike com embeddings faciais por modelo especializado",
                "pooling multi-frame com melhor frame score e score medio robusto",
            ],
        },
        {
            "owner": "Diego Torres",
            "front": "validacao e benchmark",
            "mission": "Criar protocolo de medicao e aprovar ou reprovar a meta de 90 por cento.",
            "deliverables": [
                "dataset rotulado HUB-PODIUM com pares positivos e negativos",
                "matriz de metricas com precision, recall, false accept rate e false reject rate",
                "threshold oficial para aprovado, revisao humana e bloqueio",
            ],
        },
        {
            "owner": "Helena Martins",
            "front": "qualidade de entrada",
            "mission": "Definir criterios minimos de foto e video para que o reconhecimento tenha chance real de atingir 90 por cento.",
            "deliverables": [
                "score de qualidade da foto do cadastro",
                "score de qualidade do video enviado",
                "regras de bloqueio para video escuro, distante ou sem face util",
            ],
        },
        {
            "owner": "Lara Nascimento",
            "front": "integracao com o relatorio",
            "mission": "Traduzir a confianca facial em experiencia compreensivel e segura para pais e responsaveis.",
            "deliverables": [
                "texto claro para alta, media e baixa confianca",
                "regra para esconder comparativo automatico quando a identidade estiver insegura",
                "explicacao de revisao humana quando necessario",
            ],
        },
    ],
    "execution_roadmap": [
        {
            "phase": "sprint_1_baseline_audit",
            "window": "2026-05-02 a 2026-05-06",
            "goal": "Medir o baseline atual e registrar o ponto de partida real.",
            "exit_criteria": [
                "benchmark inicial rodado",
                "limites do metodo atual documentados",
                "thresholds beta revisados",
            ],
        },
        {
            "phase": "sprint_2_quality_gate",
            "window": "2026-05-06 a 2026-05-12",
            "goal": "Bloquear entradas ruins e selecionar frames uteis antes da comparacao facial.",
            "exit_criteria": [
                "score de qualidade da foto implementado",
                "score de qualidade do video implementado",
                "selecionador de frames uteis implementado",
            ],
        },
        {
            "phase": "sprint_3_embedding_pipeline",
            "window": "2026-05-12 a 2026-05-22",
            "goal": "Trocar assinatura fraca por embeddings faciais e score agregado por multiplos frames.",
            "exit_criteria": [
                "pipeline de embeddings validado",
                "comparacao multi-frame implementada",
                "nova curva de threshold medida",
            ],
        },
        {
            "phase": "sprint_4_release_gate_90",
            "window": "2026-05-22 a 2026-06-05",
            "goal": "Aprovar ou reprovar a meta de 90 por cento em validacao rotulada.",
            "exit_criteria": [
                "precision minima de 90 por cento no benchmark aprovado",
                "regras de revisao humana ativas abaixo do threshold",
                "documentacao de risco e limites pronta para board e comercial",
            ],
        },
    ],
    "acceptance_gates": {
        "approve_automatic": [
            "detector encontra face util na foto",
            "video apresenta quantidade minima de frames validos",
            "score de qualidade de entrada acima do minimo",
            "modelo aprovado no benchmark oficial do sprint 4",
        ],
        "force_human_review": [
            "oclusao facial relevante",
            "video com mais de um atleta dominante",
            "baixa iluminacao",
            "confianca abaixo do threshold oficial",
        ],
        "block_result": [
            "sem face detectada na foto",
            "sem face util no video",
            "qualidade de entrada abaixo do minimo",
            "conflito de identidade nao resolvido",
        ],
    },
}

TOOL_INTERCONNECTIONS = [
    {
        "from": "Expo mobile app",
        "to": "Flask backend",
        "status": "beta_connected",
        "purpose": "Enviar cadastro, foto obrigatoria, categoria, posicao e video para analise.",
    },
    {
        "from": "Camera do aparelho",
        "to": "Expo mobile app",
        "status": "beta_connected",
        "purpose": "Capturar foto facial e video do atleta em celulares e tablets.",
    },
    {
        "from": "Flask backend",
        "to": "HUB-ELITE",
        "status": "beta_connected",
        "purpose": "Executar comparativo automatico por categoria, posicao e perfil de atleta real.",
    },
    {
        "from": "Flask backend",
        "to": "OpenCV facial recognition beta",
        "status": "beta_connected",
        "purpose": "Comparar rosto da foto com rostos detectados em frames do video.",
    },
    {
        "from": "Flask backend",
        "to": "ReportLab PDF",
        "status": "beta_connected",
        "purpose": "Gerar relatorio PDF para pais e responsaveis com foto e comparativo.",
    },
    {
        "from": "Flask backend",
        "to": "Pillow card generator",
        "status": "beta_connected",
        "purpose": "Gerar card estilo FIFA do atleta com foto e atributos em blocos.",
    },
    {
        "from": "App beta",
        "to": "Arquivo local e compartilhamento",
        "status": "beta_connected",
        "purpose": "Salvar e compartilhar PDF/card no dispositivo.",
    },
]

BETA_RELEASE_SCOPE = {
    "release": "HUB-PODIUM App Beta 0.1",
    "status": "implementation_ready",
    "owner": "CTO",
    "owner_name": CTO_EXECUTIVE_NAME,
    "priority": "app_first",
    "must_have": [
        "Cadastro do atleta",
        "Foto obrigatoria do atleta",
        "Captura de foto pela camera",
        "Categoria Sub-8 a Sub-20",
        "Captura ou upload de video",
        "Reconhecimento facial beta entre foto e video",
        "Analise automatica HUB-ELITE beta",
        "Comparativo com atletas reais/arquetipos compativeis com a posicao",
        "WhatsApp do responsavel para compartilhamento",
        "Clube do coracao no card",
        "Relatorio PDF com comparativo",
        "Card estilo FIFA com foto",
        "Compartilhamento de entregaveis",
    ],
    "known_limits": [
        "A beta executa reconhecimento facial inicial por OpenCV; embeddings faciais avancados e rastreamento multi-atleta entram na proxima fase.",
        "Conexao com cameras de computadores exige interface web/PWA ou app desktop na proxima fase.",
        "Banco Supabase, autenticacao, pagamento e storage externo seguem como integracoes de producao posteriores.",
    ],
}


def get_cto_agents():
    return {
        "system_id": CTO_AGENT_SYSTEM_ID,
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "agents": CTO_DEVELOPMENT_AGENTS,
    }


def get_cto_department_structure():
    return {
        "system_id": CTO_AGENT_SYSTEM_ID,
        "department": "Departamento de Tecnologia HUB-PODIUM",
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "operating_model": "Quatro times com autonomia tecnica dentro do consenso do board e prioridade do app beta.",
        "teams": CTO_DEPARTMENT_TEAMS,
    }


def get_algorithm_team_training_program():
    return {
        "system_id": CTO_AGENT_SYSTEM_ID,
        **ALGORITHM_TEAM_TRAINING_PROGRAM,
    }


def get_tool_interconnections():
    return {
        "system_id": CTO_AGENT_SYSTEM_ID,
        "owner": "CTO",
        "owner_name": CTO_EXECUTIVE_NAME,
        "interconnections": TOOL_INTERCONNECTIONS,
    }


def get_beta_release_scope():
    return BETA_RELEASE_SCOPE


def get_facial_recognition_90_plan():
    return {
        "system_id": CTO_AGENT_SYSTEM_ID,
        **FACIAL_RECOGNITION_90_PLAN,
    }
