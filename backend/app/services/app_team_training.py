APP_TEAM_TRAINING_ID = "HUB_PODIUM_APP_TEAM_TRAINING_001"

APP_TEAM_AGENT_TRAINING = [
    {
        "agent_code": "agent_app_product_experience",
        "person_name": "Camila Rocha",
        "title": "Lider de Produto e Experiencia Mobile",
        "mission": "Transformar a jornada HUB-PODIUM em uma experiencia emocional, clara e confiavel para atletas, pais e responsaveis.",
        "tools_to_master": ["Figma futuro", "Expo Router", "Firebase Remote Config futuro", "analytics de funil"],
        "market_inputs": ["OneFootball", "FotMob", "Tonsser", "FIFA+"],
        "deliverables_30_days": [
            "Mapa de jornada Sub-8 a Sub-12 com apelo emocional",
            "Mapa de jornada Sub-13 a Sub-20 com leitura evolutiva",
            "Fluxo de onboarding, consentimento, foto, video, resultado e compartilhamento",
            "Padrao de microcopy para pais, atletas e responsaveis",
        ],
    },
    {
        "agent_code": "agent_mobile_engineering",
        "person_name": "Mateus Albuquerque",
        "title": "Lider de Engenharia Mobile",
        "mission": "Construir o app com base tecnica escalavel, performatica e pronta para iOS, Android e futuras experiencias web.",
        "tools_to_master": ["Expo", "React Native", "TypeScript futuro", "Expo Router futuro", "TanStack Query futuro", "Zustand futuro", "EAS CLI"],
        "market_inputs": ["Expo", "React Native", "Hudl", "Veo", "Trace"],
        "deliverables_30_days": [
            "Plano de migracao gradual para TypeScript",
            "Arquitetura de modulos para cadastro, camera, upload, analise e entregaveis",
            "Checklist de performance para upload de video e foto",
            "Configuracao de builds reais com EAS",
        ],
    },
    {
        "agent_code": "agent_mobile_quality_release",
        "person_name": "Renata Iwata",
        "title": "Lider de Qualidade e Release Mobile",
        "mission": "Garantir que a beta funcione com estabilidade em aparelhos reais, redes instaveis e jornadas completas.",
        "tools_to_master": ["EAS Build", "Expo Doctor", "Sentry futuro", "Maestro/Detox futuro", "TestFlight futuro", "Google Play Internal Testing futuro"],
        "market_inputs": ["SofaScore", "FotMob", "Hudl", "Veo"],
        "deliverables_30_days": [
            "Matriz de testes iPhone, Android, tablet e rede movel",
            "Checklist de camera, galeria, upload, PDF, card e WhatsApp",
            "Plano de monitoramento de crash/performance",
            "Roteiro de beta fechada para pais e responsaveis",
        ],
    },
    {
        "agent_code": "agent_app_support_delivery",
        "person_name": "Joao Pedro Salles",
        "title": "Lider de Suporte e Entrega do App",
        "mission": "Fazer o resultado chegar com clareza, seguranca e valor percebido para familias, atletas e clubes.",
        "tools_to_master": ["WhatsApp", "expo-sharing", "RevenueCat futuro", "Firebase Analytics futuro", "CRM futuro"],
        "market_inputs": ["Trace", "Tonsser", "Hudl", "OneFootball"],
        "deliverables_30_days": [
            "Fluxo de entrega do PDF e card para responsavel",
            "Padrao de mensagens de erro e recuperacao",
            "Roteiro de suporte para upload lento ou falha de backend",
            "Plano de recompra e evolucao mensal do atleta",
        ],
    },
]

APP_MARKET_REFERENCES = [
    {
        "name": "FotMob",
        "category": "live_scores_stats_news",
        "signal": "App essencial de futebol com live scores, alertas, estatisticas detalhadas, xG, mapas de chute, video, audio e ratings.",
        "practices_to_adopt": [
            "Personalizacao por clube, atleta e competicao",
            "Entrega rapida de informacao importante",
            "Uso de estatisticas em blocos simples e legiveis",
            "Widgets e notificacoes como extensao da experiencia",
        ],
        "sources": ["https://www.fotmob.com/en/download", "https://apps.apple.com/us/app/fotmob-soccer-live-scores/id488575683"],
    },
    {
        "name": "SofaScore",
        "category": "advanced_match_stats",
        "signal": "Experiencia rica em estatisticas, ratings, atributos, momentum, shot map, heatmap e comparacao de jogadores.",
        "practices_to_adopt": [
            "Visualizar atributos em categorias claras",
            "Evitar telas vazias com dados acionaveis",
            "Transformar estatisticas complexas em leitura rapida",
            "Criar confianca visual em metricas e rankings",
        ],
        "sources": ["https://www.sofascore.com/", "https://apps.apple.com/us/app/sofascore-live-score-app/id1176147574"],
    },
    {
        "name": "OneFootball",
        "category": "fan_engagement_news_streaming",
        "signal": "App de futebol com noticias, placares, estatisticas, video, personalizacao, quizzes e experimentacao de produto com Firebase.",
        "practices_to_adopt": [
            "Testar funcionalidades antes de liberar para todos",
            "Personalizar conteudo sem perder descoberta editorial",
            "Medir engajamento diario por sessao e conteudo consumido",
            "Usar Remote Config e analytics para evoluir o produto",
        ],
        "sources": ["https://onefootballsupport.zendesk.com/hc/en-us/articles/4412970161937-What-does-the-OneFootball-app-offer", "https://firebase.google.com/use-cases/onefootball?hl=es-419"],
    },
    {
        "name": "FIFA+",
        "category": "official_content_global_football",
        "signal": "Destino digital oficial com arquivo historico, jogos ao vivo, noticias, dados globais e conteudo de futebol.",
        "practices_to_adopt": [
            "Combinar arquivo, contexto e conteudo em uma unica experiencia",
            "Criar linguagem global e acessivel",
            "Valorizar conteudo oficial e confiavel",
            "Usar match centre e dados como camada de profundidade",
        ],
        "sources": ["https://www.plus.fifa.com/", "https://www.fifa.com/en/articles/about-fifa-original-content-live-scores-world-cup-archive-breaking-news"],
    },
    {
        "name": "Hudl",
        "category": "video_analysis_coaching",
        "signal": "Plataforma de captura, analise, comentarios, playlists, highlights e compartilhamento para times e atletas.",
        "practices_to_adopt": [
            "Video como centro da evolucao do atleta",
            "Comentarios, highlights e desenhos como ferramentas de aprendizado",
            "Relatorios automatizados ligados ao video",
            "Compartilhamento seguro com equipe e familia",
        ],
        "sources": ["https://www.hudl.com/sports/soccer", "https://www.hudl.com/products/hudl"],
    },
    {
        "name": "Veo",
        "category": "ai_camera_player_development",
        "signal": "Camera e plataforma com follow-cam, eventos automaticos, analytics, Player Spotlight, heatmap, shot map e progresso.",
        "practices_to_adopt": [
            "Reduzir trabalho manual de analise de video",
            "Gerar momentos individuais do atleta",
            "Transformar video em progresso recorrente",
            "Usar metricas visuais para facilitar conversa com treinador e familia",
        ],
        "sources": ["https://www.veo.com/en-us/sport/soccer", "https://www.veo.com/en-us/partnership/soccer-profile"],
    },
    {
        "name": "Tonsser",
        "category": "youth_player_profile",
        "signal": "App de futebol jovem com perfil de jogador, highlights, estatisticas, rating e progresso de performance.",
        "practices_to_adopt": [
            "Dar protagonismo ao atleta jovem",
            "Construir historico evolutivo e identidade esportiva",
            "Misturar sonho, comunidade, prova social e desempenho",
            "Criar linguagem aspiracional sem prometer carreira profissional",
        ],
        "sources": ["https://tonsser.com/", "https://play.google.com/store/apps/details?id=com.tonsser.tonsser"],
    },
    {
        "name": "Trace",
        "category": "youth_soccer_video_highlights",
        "signal": "Sistema de video para futebol de base com PlayerFocus, highlights automaticos e entrega direta aos jogadores/familias.",
        "practices_to_adopt": [
            "Automatizar entrega de highlights por atleta",
            "Priorizar facilidade para pais e clubes",
            "Entregar resultado direto no canal do usuario",
            "Reduzir friccao de gravacao e compartilhamento",
        ],
        "sources": ["https://site.traceup.com/how-it-works/", "https://apps.apple.com/us/app/trace-teams/id1351001083"],
    },
]

APP_TOOLCHAIN = [
    {
        "layer": "Mobile base",
        "tools": ["Expo 54", "React Native 0.81", "EAS CLI", "npm", "git"],
        "status": "install_now",
        "purpose": "Rodar, construir, publicar e manter a beta em aparelhos reais.",
    },
    {
        "layer": "Arquitetura de app",
        "tools": ["TypeScript futuro", "Expo Router futuro", "TanStack Query futuro", "Zustand futuro"],
        "status": "planned_refactor",
        "purpose": "Escalar telas, estado, API, cache, upload e entregaveis sem virar um arquivo unico.",
    },
    {
        "layer": "Camera, video e entregaveis",
        "tools": ["expo-image-picker", "expo-file-system", "expo-sharing", "WhatsApp deep link"],
        "status": "active",
        "purpose": "Capturar foto/video, enviar para backend, salvar PDF/card e compartilhar resultado.",
    },
    {
        "layer": "Qualidade e observabilidade",
        "tools": ["Expo Doctor", "Sentry futuro", "Maestro/Detox futuro", "TestFlight futuro", "Play Internal Testing futuro"],
        "status": "planned_beta_hardening",
        "purpose": "Monitorar crash, performance, regressao e compatibilidade em aparelhos reais.",
    },
    {
        "layer": "Produto e crescimento",
        "tools": ["Firebase Analytics futuro", "Firebase Remote Config futuro", "RevenueCat futuro", "CRM futuro"],
        "status": "planned_after_beta",
        "purpose": "Medir onboarding, testar telas, monetizar e acompanhar familias/atletas.",
    },
]

APP_TRAINING_TRACKS = [
    {
        "period": "Semana 1",
        "module": "Benchmark e linguagem do app",
        "outcome": "Time entende FotMob, SofaScore, OneFootball, FIFA+, Hudl, Veo, Tonsser e Trace como referencias de produto.",
    },
    {
        "period": "Semanas 2-3",
        "module": "Jornada Sub-8 a Sub-20",
        "outcome": "Fluxos separados para emocao familiar, evolucao tecnica, video, PDF, card e WhatsApp.",
    },
    {
        "period": "Semanas 4-5",
        "module": "Arquitetura mobile real",
        "outcome": "Plano para modularizar o app, preparar EAS, reduzir falhas de upload e padronizar componentes.",
    },
    {
        "period": "Semanas 6-7",
        "module": "Qualidade, release e observabilidade",
        "outcome": "Beta testavel em aparelho real com checklist de camera, rede, backend, PDF, card e compartilhamento.",
    },
    {
        "period": "Semana 8",
        "module": "Crescimento e retencao",
        "outcome": "Plano de notificacoes, historico evolutivo, recompra, feedback e experimentos controlados.",
    },
]

APP_NON_NEGOTIABLE_RULES = [
    "O app deve entregar o produto real na primeira tela util, sem depender de explicacao longa.",
    "Sub-8 a Sub-12 recebe linguagem emocional, familiar e segura; Sub-13 a Sub-20 recebe linguagem evolutiva e tecnica.",
    "Foto, video, consentimento, WhatsApp e responsavel devem ser tratados como fluxo sensivel.",
    "Nenhum resultado deve prometer carreira profissional ou equivalencia literal com atleta real.",
    "Falha de rede, backend ou upload precisa ter recuperacao clara para o responsavel.",
]


def get_app_team_training_program():
    return {
        "training_id": APP_TEAM_TRAINING_ID,
        "program": "HUB-PODIUM App Excellence Program",
        "owner": "CTO",
        "owner_name": "Rafael Duarte",
        "team": "Time App",
        "status": "active",
        "goal": "Transformar o Time App em referencia de produto mobile para futebol de base, video, performance, relatorio e compartilhamento familiar.",
        "agents": APP_TEAM_AGENT_TRAINING,
        "market_references": APP_MARKET_REFERENCES,
        "toolchain": APP_TOOLCHAIN,
        "training_tracks": APP_TRAINING_TRACKS,
        "non_negotiable_rules": APP_NON_NEGOTIABLE_RULES,
    }
