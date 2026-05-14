HUB_ELITE_DATASET_ID = "HUB_ELITE_REAL_ATHLETE_DATASET_1994_2026"

from services.hub_elite_population import get_seed_population_summary

CANONICAL_POSITIONS = [
    {
        "code": "goleiro",
        "name": "Goleiro",
        "family": "goleiro",
        "target_athletes": 100,
        "aliases": ["GK", "Goalkeeper", "Goleiro"],
    },
    {
        "code": "lateral_direito",
        "name": "Lateral direito",
        "family": "lateral",
        "target_athletes": 100,
        "aliases": ["RB", "Right-Back", "Right Back", "Lateral direito", "Ala direito"],
    },
    {
        "code": "lateral_esquerdo",
        "name": "Lateral esquerdo",
        "family": "lateral",
        "target_athletes": 100,
        "aliases": ["LB", "Left-Back", "Left Back", "Lateral esquerdo", "Ala esquerdo"],
    },
    {
        "code": "zagueiro",
        "name": "Zagueiro",
        "family": "zagueiro",
        "target_athletes": 100,
        "aliases": ["CB", "Centre-Back", "Center Back", "Defender", "Zagueiro"],
    },
    {
        "code": "volante",
        "name": "Volante",
        "family": "volante",
        "target_athletes": 100,
        "aliases": ["DM", "Defensive Midfield", "Holding Midfielder", "Volante"],
    },
    {
        "code": "meia_central",
        "name": "Meia central",
        "family": "meia",
        "target_athletes": 100,
        "aliases": ["CM", "Central Midfield", "Box-to-box", "Meia central"],
    },
    {
        "code": "meia_ofensivo",
        "name": "Meia ofensivo",
        "family": "meia",
        "target_athletes": 100,
        "aliases": ["AM", "Attacking Midfield", "Playmaker", "Meia ofensivo"],
    },
    {
        "code": "ponta_direita",
        "name": "Ponta direita",
        "family": "ponta",
        "target_athletes": 100,
        "aliases": ["RW", "Right Winger", "Ponta direita"],
    },
    {
        "code": "ponta_esquerda",
        "name": "Ponta esquerda",
        "family": "ponta",
        "target_athletes": 100,
        "aliases": ["LW", "Left Winger", "Ponta esquerda"],
    },
    {
        "code": "segundo_atacante",
        "name": "Segundo atacante",
        "family": "atacante",
        "target_athletes": 100,
        "aliases": ["SS", "Second Striker", "Inside Forward", "Segundo atacante"],
    },
    {
        "code": "centroavante",
        "name": "Centroavante",
        "family": "atacante",
        "target_athletes": 100,
        "aliases": ["CF", "Centre-Forward", "Center Forward", "Striker", "Centroavante"],
    },
]

DATA_SOURCE_REGISTRY = [
    {
        "tier": 1,
        "name": "FIFA Professional Football Landscape",
        "type": "official_global_database",
        "access": "public_or_registered",
        "use": "Mapear jogadores, clubes, transferencias e competicoes de primeira divisao em associacoes FIFA.",
        "url": "https://inside.fifa.com/en/legal/news/fifa-launches-first-ever-digital-platform-dedicated-to-professional-football",
    },
    {
        "tier": 1,
        "name": "FIFA+ Archive e FIFA World Cup records",
        "type": "official_competition_archive",
        "access": "public",
        "use": "Validar Copa do Mundo, desempenho em selecoes, jogos grandes e contexto historico.",
        "url": "https://www.fifa.com/en/archive",
    },
    {
        "tier": 1,
        "name": "UEFA Champions League all-time stats",
        "type": "official_competition_statistics",
        "access": "public",
        "use": "Validar presencas, gols, assistencias e impacto continental na Europa.",
        "url": "https://www.uefa.com/uefachampionsleague/history/rankings/players/matches_played/",
    },
    {
        "tier": 1,
        "name": "CONMEBOL Libertadores estatisticas",
        "type": "official_competition_statistics",
        "access": "public",
        "use": "Validar impacto continental na America do Sul.",
        "url": "https://www.conmebol.com/pt-br/conmebol-libertadores-estatisticas/",
    },
    {
        "tier": 2,
        "name": "Transfermarkt",
        "type": "public_market_and_player_database",
        "access": "public_or_registered",
        "use": "Normalizar posicao, carreira, valor de mercado historico, clubes, ligas e nacionalidades.",
        "url": "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop",
    },
    {
        "tier": 2,
        "name": "FBref",
        "type": "public_player_stats_and_scouting_reports",
        "access": "public_or_registered",
        "use": "Cruzar estatisticas por temporada, quando disponiveis publicamente e dentro dos termos.",
        "url": "https://fbref.com/",
    },
    {
        "tier": 2,
        "name": "worldfootball.net",
        "type": "historical_competition_database",
        "access": "public",
        "use": "Completar historico de competicoes, jogos, elencos e estatisticas basicas.",
        "url": "https://www.worldfootball.net/",
    },
    {
        "tier": 3,
        "name": "Wyscout, StatsBomb, Opta/Stats Perform, InStat, SkillCorner, CIES, BeSoccer Pro",
        "type": "specialist_or_commercial_scouting_sources",
        "access": "registered_or_commercial",
        "use": "Aprofundar dados de eventos, scouting, tracking, xG, passes, duelos, pressao e dados fisicos.",
        "url": "commercial_or_registered_access",
    },
    {
        "tier": 4,
        "name": "Premiacoes, rankings e revistas especializadas",
        "type": "expert_consensus_sources",
        "access": "public_or_registered",
        "use": "Agregar consenso historico de Ballon d'Or, FIFA The Best, FIFPro XI, UEFA awards e revistas de scouting.",
        "url": "multiple_public_sources",
    },
]

SCORING_MODEL = {
    "model": "HUB-ELITE Top 100 Position Score",
    "status": "definition_ready",
    "weights": [
        {
            "dimension": "performance_oficial",
            "weight": 35,
            "description": "Gols, assistencias, minutos, clean sheets, duelos, passes, titulos e impacto em competicoes oficiais.",
        },
        {
            "dimension": "excelencia_posicional",
            "weight": 25,
            "description": "Comparacao apenas contra atletas da mesma posicao canonica e familia tecnica.",
        },
        {
            "dimension": "pico_competitivo",
            "weight": 15,
            "description": "Melhores temporadas e torneios entre 1994 e a data atual.",
        },
        {
            "dimension": "longevidade",
            "weight": 10,
            "description": "Consistencia em anos, clubes, selecoes e competicoes de alto nivel.",
        },
        {
            "dimension": "impacto_internacional_continental",
            "weight": 10,
            "description": "Copa do Mundo, Euro, Copa America, Champions League, Libertadores, AFCON, Asian Cup e equivalentes.",
        },
        {
            "dimension": "consenso_scout_premiacoes",
            "weight": 5,
            "description": "Premiacoes, rankings de especialistas, scout reports e reconhecimento publico auditavel.",
        },
    ],
}

PIPELINE_PHASES = [
    {
        "phase": "01_source_registry",
        "owner": "Diego Torres",
        "output": "Registro de fontes, acesso, termos, pais, confederacao e confianca.",
    },
    {
        "phase": "02_candidate_discovery",
        "owner": "Helena Martins",
        "output": "Lista inicial de pelo menos 200 candidatos por posicao antes do corte top 100.",
    },
    {
        "phase": "03_identity_normalization",
        "owner": "Lara Nascimento",
        "output": "ID unico por atleta, nome principal, aliases, nacionalidade, periodo ativo e posicoes.",
    },
    {
        "phase": "04_feature_extraction",
        "owner": "Helena Martins",
        "output": "Metricas oficiais e derivadas por temporada, competicao, clube, selecao e posicao.",
    },
    {
        "phase": "05_role_aware_ranking",
        "owner": "Lara Nascimento",
        "output": "Ranking top 100 por posicao canonica, sem comparar funcoes incompativeis.",
    },
    {
        "phase": "06_video_and_cv_alignment",
        "owner": "Bruno Kato",
        "output": "Mapa entre perfil historico, atributos visuais, pose, movimento e analise de video do app.",
    },
    {
        "phase": "07_validation_and_release_gate",
        "owner": "Diego Torres",
        "output": "Aprovacao por confianca, fonte, completude e risco antes de entrar no HUB-ELITE.",
    },
]

TEAM_ASSIGNMENTS = [
    {
        "person_name": "Helena Martins",
        "agent": "Scoring HUB-ELITE",
        "mandate": "Criar a pontuacao top 100 por posicao com pesos, normalizacao por era e nivel competitivo.",
    },
    {
        "person_name": "Bruno Kato",
        "agent": "Visao Computacional",
        "mandate": "Conectar atributos historicos do atleta real aos sinais visuais que o app mede nos videos.",
    },
    {
        "person_name": "Lara Nascimento",
        "agent": "Perfil e Similaridade",
        "mandate": "Definir taxonomia posicional, familias de estilo e comparativos coerentes com posicao.",
    },
    {
        "person_name": "Diego Torres",
        "agent": "Validacao do Modelo",
        "mandate": "Auditar fonte, permissao, confianca, vies, completude e necessidade de revisao humana.",
    },
]

DATA_GOVERNANCE = {
    "public_first": True,
    "registered_access_authorized": True,
    "registration_policy": [
        "Usar cadastros gratuitos ou profissionais somente quando os termos permitirem pesquisa e uso interno.",
        "Nao copiar dados proprietarios pagos para a base sem contrato, licenca ou aprovacao do board.",
        "Armazenar URL, data de acesso, fonte, tipo de permissao e confianca para cada informacao sensivel do ranking.",
        "Separar fato publico, metrica derivada HUB-ELITE e opiniao de scouting.",
    ],
    "quality_gates": [
        "Minimo de duas fontes independentes para entrada no top 100.",
        "Fonte oficial pesa mais que ranking editorial.",
        "Dados de uma era devem ser normalizados para evitar vantagem de calendario, midia ou volume de competicoes.",
        "Atleta so pode entrar em uma posicao principal e ate duas posicoes secundarias com justificativa.",
    ],
}

COMPETITION_TRACKS = [
    {
        "code": "masculino",
        "name": "Futebol masculino",
        "target_per_position": 100,
        "positions": len(CANONICAL_POSITIONS),
        "target_total_athletes": sum(position["target_athletes"] for position in CANONICAL_POSITIONS),
        "status": "seed_population_started",
        "comparison_rule": "Comparar atletas masculinos com referencias masculinas da mesma posicao canonica e familia tecnica.",
    },
    {
        "code": "feminino",
        "name": "Futebol feminino",
        "target_per_position": 100,
        "positions": len(CANONICAL_POSITIONS),
        "target_total_athletes": sum(position["target_athletes"] for position in CANONICAL_POSITIONS),
        "status": "parameterization_started",
        "comparison_rule": "Comparar atletas femininas com referencias femininas da mesma posicao canonica e familia tecnica.",
    },
]

WOMENS_POPULATION_ROADMAP = [
    {
        "phase": "sprint_01_parameterization",
        "window": "2026-05-02 a 2026-05-06",
        "owner": "Lara Nascimento",
        "goal": "Fechar taxonomia feminina por posicao, aliases, familias tecnicas e criterios de comparacao.",
        "target_output": "11 posicoes femininas parametrizadas com regra de matching pronta para runtime.",
    },
    {
        "phase": "sprint_02_candidate_discovery",
        "window": "2026-05-05 a 2026-05-12",
        "owner": "Helena Martins",
        "goal": "Levantar pelo menos 200 candidatas por posicao canonica para corte top 100.",
        "target_output": "2.200 candidatas iniciais mapeadas para o feminino.",
    },
    {
        "phase": "sprint_03_identity_and_sources",
        "window": "2026-05-08 a 2026-05-16",
        "owner": "Diego Torres",
        "goal": "Auditar identidade, periodo ativo, fonte primaria, fonte secundaria e confianca minima.",
        "target_output": "Cada atleta feminina com duas fontes e trilha de permissao registrada.",
    },
    {
        "phase": "sprint_04_seed_runtime",
        "window": "2026-05-12 a 2026-05-20",
        "owner": "Bruno Kato",
        "goal": "Publicar seed feminino beta e conectar a comparacao do app por trilha competitiva.",
        "target_output": "Seed feminino com pelo menos 5 atletas por posicao pronta para beta comparativo.",
    },
    {
        "phase": "sprint_05_ranked_top_100",
        "window": "2026-05-20 a 2026-06-10",
        "owner": "Helena Martins e Diego Torres",
        "goal": "Fechar top 100 feminino por posicao com scoring auditado e release gate.",
        "target_output": "1.100 atletas femininas validadas para producao HUB-ELITE.",
    },
]


def get_real_athlete_dataset_plan():
    target_per_track = sum(position["target_athletes"] for position in CANONICAL_POSITIONS)
    target_total = target_per_track * len(COMPETITION_TRACKS)
    return {
        "dataset_id": HUB_ELITE_DATASET_ID,
        "name": "Base Global de Atletas Reais HUB-ELITE",
        "status": "dual_track_population_started",
        "period": {
            "from": "1994-01-01",
            "to": "2026-05-02",
            "rule": "Atualizar continuamente ate a data corrente de producao.",
        },
        "scope": {
            "target_per_position": 100,
            "positions": len(CANONICAL_POSITIONS),
            "target_total_per_track": target_per_track,
            "target_total_athletes": target_total,
            "competition_tracks": len(COMPETITION_TRACKS),
            "coverage": "Europa, Americas, Africa, Asia, Oriente Medio e competicoes oficiais de federacoes nacionais e continentais.",
        },
        "competition_tracks": COMPETITION_TRACKS,
        "canonical_positions": CANONICAL_POSITIONS,
        "sources": DATA_SOURCE_REGISTRY,
        "scoring_model": SCORING_MODEL,
        "population": get_seed_population_summary(),
        "pipeline": PIPELINE_PHASES,
        "womens_population_roadmap": WOMENS_POPULATION_ROADMAP,
        "team_assignments": TEAM_ASSIGNMENTS,
        "governance": DATA_GOVERNANCE,
    }
