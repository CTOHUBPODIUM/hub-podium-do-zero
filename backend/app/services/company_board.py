COMPANY_NAME = "HUB-PODIUM"
PRODUCT_CODE = "HUB-PODIUM-ATHLETE-INTELLIGENCE"
PRODUCT_NAME = "Plataforma HUB-PODIUM de Analise Inteligente de Atleta"
BOARD_DECISION_ID = "BOARD_MEETING_004"
OPERATING_MANDATE_ID = "BOARD_MEETING_005"
CEO_DELIVERY_REPORT_ID = "BOARD_MEETING_009"


EXECUTIVE_BOARD = {
    "CEO": {
        "role": "CEO",
        "executive_name": None,
        "title": "Chief Executive Officer",
        "seat": "Presidencia executiva",
        "authority_level": 100,
        "responsibilities": [
            "Direcao final da empresa e do produto",
            "Aprovacao institucional da plataforma e do app",
            "Priorizacao estrategica e decisao final de go-to-market",
        ],
        "permissions": [
            "company.final_approval",
            "product.publish",
            "product.pricing.override",
            "operations.priority_override",
            "partnerships.final_approval",
        ],
    },
    "CFO": {
        "role": "CFO",
        "executive_name": None,
        "title": "Chief Financial Officer",
        "seat": "Financas e receita",
        "authority_level": 90,
        "responsibilities": [
            "Modelo financeiro, precificacao e margem",
            "Controle de pagamentos, repasses e custos",
            "Aprovacao de investimentos e fornecedores financeiros",
        ],
        "permissions": [
            "finance.pricing.approve",
            "finance.payments.manage",
            "finance.costs.approve",
            "finance.revenue_reports.view",
            "product.monetization.approve",
        ],
    },
    "CCO": {
        "role": "CCO",
        "executive_name": None,
        "title": "Chief Commercial Officer",
        "seat": "Comercial e clientes",
        "authority_level": 88,
        "responsibilities": [
            "Oferta comercial e funil de vendas",
            "Parcerias com escolas, clubes e categorias de base",
            "Politica de relacionamento e sucesso do cliente",
        ],
        "permissions": [
            "commercial.offers.approve",
            "commercial.partnerships.manage",
            "commercial.customer_success.manage",
            "commercial.sales_pipeline.view",
            "product.offer_positioning.approve",
        ],
    },
    "CTO": {
        "role": "CTO",
        "executive_name": "Rafael Duarte",
        "title": "Chief Technology Officer",
        "seat": "Tecnologia, dados e seguranca",
        "authority_level": 92,
        "responsibilities": [
            "Arquitetura tecnica da plataforma e do app",
            "Seguranca, dados, infraestrutura e releases",
            "Integracoes com IA, pagamentos, storage e banco",
        ],
        "permissions": [
            "technology.architecture.approve",
            "technology.release.approve",
            "technology.security.manage",
            "technology.data.manage",
            "integrations.production.manage",
        ],
    },
    "CMO": {
        "role": "CMO",
        "executive_name": None,
        "title": "Chief Marketing Officer",
        "seat": "Marca, comunicacao e crescimento",
        "authority_level": 84,
        "responsibilities": [
            "Marca HUB-PODIUM e posicionamento do produto",
            "Campanhas, conteudo, canais e aquisicao",
            "Aprovacao de mensagens publicas e materiais comerciais",
        ],
        "permissions": [
            "marketing.brand.approve",
            "marketing.campaigns.manage",
            "marketing.public_copy.approve",
            "marketing.growth_channels.manage",
            "product.launch_communication.approve",
        ],
    },
}


AREA_EXECUTION_MANDATES = {
    "CEO": {
        "area": "Presidencia executiva",
        "mission": "Transformar a HUB-PODIUM em empresa operacional, com direcao estrategica, governanca e decisao final.",
        "autonomy": [
            "Definir prioridades corporativas e metas trimestrais",
            "Aprovar entrada de novos produtos, mercados e parcerias estrategicas",
            "Resolver conflitos entre areas quando houver impacto cruzado",
        ],
        "execution_authorities": [
            "company.strategy.define",
            "company.okrs.approve",
            "company.board_consensus.call",
            "company.cross_area_conflict.resolve",
            "company.external_representation.authorize",
        ],
        "requires_board_consensus": [
            "Mudanca estrutural de produto ou modelo de negocio",
            "Compromissos financeiros acima do limite aprovado pelo CFO",
            "Parcerias que alterem marca, dados, receita ou controle operacional",
        ],
        "accountability": "Prestar contas ao board sobre estrategia, prioridades, riscos e resultados gerais.",
    },
    "CFO": {
        "area": "Financas, receita e compliance financeiro",
        "mission": "Garantir que a empresa opere com preco, caixa, custos, impostos, repasses e contratos sustentaveis.",
        "autonomy": [
            "Definir controles financeiros e rotina de caixa",
            "Aprovar custos operacionais dentro do orcamento",
            "Gerir pagamentos, recebimentos, margem e relatorios financeiros",
        ],
        "execution_authorities": [
            "finance.cashflow.manage",
            "finance.budget.allocate",
            "finance.vendor_cost.approve",
            "finance.payment_provider.operate",
            "finance.tax_and_compliance.coordinate",
        ],
        "requires_board_consensus": [
            "Alteracao de preco principal do produto",
            "Contratos financeiros recorrentes de alto impacto",
            "Qualquer decisao que reduza margem abaixo da meta aprovada",
        ],
        "accountability": "Prestar contas ao board sobre caixa, margem, precificacao, custos e riscos financeiros.",
    },
    "CCO": {
        "area": "Comercial, parcerias e sucesso do cliente",
        "mission": "Gerar receita, validar canais comerciais e criar relacionamento real com clientes e parceiros.",
        "autonomy": [
            "Executar vendas, prospeccao e relacionamento com clientes",
            "Negociar parcerias comerciais dentro da politica aprovada",
            "Organizar funil, atendimento, pos-venda e indicadores comerciais",
        ],
        "execution_authorities": [
            "commercial.sales.execute",
            "commercial.pipeline.manage",
            "commercial.partner_terms.negotiate",
            "commercial.customer_success.operate",
            "commercial.feedback.collect",
        ],
        "requires_board_consensus": [
            "Parcerias exclusivas",
            "Promessas comerciais que alterem produto, preco, tecnologia ou marca",
            "Contratos fora do padrao aprovado por CEO e CFO",
        ],
        "accountability": "Prestar contas ao board sobre receita, conversao, clientes, churn, parcerias e feedback de mercado.",
    },
    "CTO": {
        "area": "Tecnologia, produto, dados e seguranca",
        "mission": "Construir, operar e proteger plataforma, app, backend, banco, integracoes e infraestrutura.",
        "autonomy": [
            "Definir arquitetura tecnica e padroes de desenvolvimento",
            "Executar releases, manutencoes e integracoes aprovadas",
            "Estabelecer controles de seguranca, dados, backup e disponibilidade",
        ],
        "execution_authorities": [
            "technology.product_build.execute",
            "technology.infrastructure.operate",
            "technology.release.deploy",
            "technology.security_controls.enforce",
            "technology.data_governance.operate",
        ],
        "requires_board_consensus": [
            "Uso de dados sensiveis fora do escopo do produto",
            "Mudancas que afetem experiencia comercial, preco, marca ou compliance",
            "Contratacao de infraestrutura com custo relevante recorrente",
        ],
        "accountability": "Prestar contas ao board sobre roadmap tecnico, seguranca, estabilidade, dados e riscos de produto.",
    },
    "CMO": {
        "area": "Marca, marketing e crescimento",
        "mission": "Construir percepcao de marca, demanda qualificada e comunicacao consistente da HUB-PODIUM.",
        "autonomy": [
            "Executar campanhas, conteudo e canais de aquisicao",
            "Padronizar identidade, mensagens publicas e materiais comerciais",
            "Testar posicionamento e medir crescimento por canal",
        ],
        "execution_authorities": [
            "marketing.brand_system.manage",
            "marketing.campaign.execute",
            "marketing.public_copy.publish",
            "marketing.growth_experiment.run",
            "marketing.launch_plan.operate",
        ],
        "requires_board_consensus": [
            "Promessas publicas que mudem o escopo real do produto",
            "Campanhas com investimento acima do orcamento aprovado",
            "Mudancas de posicionamento central da marca HUB-PODIUM",
        ],
        "accountability": "Prestar contas ao board sobre marca, canais, CAC, conteudo, campanhas e aprendizagem de mercado.",
    },
}


BOARD_CONSENSUS = {
    "decision_id": OPERATING_MANDATE_ID,
    "proposed_by": "CEO",
    "status": "approved_by_consensus",
    "decision": "Definir atribuicoes por area e conceder autonomia executiva para operacao real da HUB-PODIUM.",
    "consensus_rule": "Cada diretoria executa com autonomia dentro do proprio escopo. Impactos cruzados, compromissos acima de limite, mudancas de produto, marca, preco, dados ou parcerias estrategicas exigem consenso do board.",
    "votes": [
        {"role": "CEO", "vote": "approved", "scope": "Direcao geral e decisao final"},
        {"role": "CFO", "vote": "approved", "scope": "Viabilidade financeira e controle de custos"},
        {"role": "CCO", "vote": "approved", "scope": "Execucao comercial e relacionamento com clientes"},
        {"role": "CTO", "vote": "approved", "scope": "Execucao tecnica, dados e seguranca"},
        {"role": "CMO", "vote": "approved", "scope": "Marca, comunicacao e crescimento"},
    ],
}


PRODUCT_AUTHORIZATIONS = [
    {
        "role": "CEO",
        "scope": "company_product",
        "status": "approved",
        "decision": "Autoriza a plataforma e o app como produto oficial da HUB-PODIUM.",
    },
    {
        "role": "CFO",
        "scope": "monetization",
        "status": "approved",
        "decision": "Autoriza preco inicial, receita, pagamentos e controle financeiro do produto.",
    },
    {
        "role": "CCO",
        "scope": "commercial",
        "status": "approved",
        "decision": "Autoriza oferta comercial, parcerias e relacao com clientes.",
    },
    {
        "role": "CTO",
        "scope": "technology",
        "status": "approved",
        "decision": "Autoriza arquitetura, seguranca, integracoes e publicacao tecnica.",
    },
    {
        "role": "CMO",
        "scope": "brand",
        "status": "approved",
        "decision": "Autoriza marca, posicionamento e comunicacao do produto HUB-PODIUM.",
    },
]


CEO_DEPARTMENT_DELIVERY_REPORT = {
    "report_id": CEO_DELIVERY_REPORT_ID,
    "requested_by": "CEO",
    "status": "issued",
    "issued_at": "2026-04-30",
    "planning_window": {
        "start": "2026-05-01",
        "end": "2026-06-15",
    },
    "executive_summary": (
        "O CEO solicita cronograma integrado para que cada departamento opere com entregas, "
        "responsaveis, criterios de aceite e prestacao de contas semanais."
    ),
    "departments": [
        {
            "role": "CEO",
            "department": "Presidencia executiva",
            "owner": "CEO",
            "mission": "Alinhar estrategia, prioridades, governanca e decisao final da HUB-PODIUM.",
            "milestones": [
                {
                    "date": "2026-05-03",
                    "delivery": "Validar escopo executivo da beta e aprovar prioridades do produto.",
                    "acceptance": "Board alinhado sobre beta mobile, reconhecimento facial e entregaveis PDF/card.",
                },
                {
                    "date": "2026-05-10",
                    "delivery": "Aprovar plano de operacao real e rotina semanal de status por departamento.",
                    "acceptance": "Ritual de reporte ativo com riscos, bloqueios e proximas entregas.",
                },
                {
                    "date": "2026-05-31",
                    "delivery": "Decidir readiness para pilotos com usuarios reais.",
                    "acceptance": "Checklist juridico, financeiro, comercial, tecnico e marketing revisado.",
                },
            ],
            "dependencies": ["CTO", "CFO", "CCO", "CMO"],
        },
        {
            "role": "CTO",
            "department": "Tecnologia, produto, dados e seguranca",
            "owner": "Rafael Duarte",
            "owner_role": "CTO",
            "mission": "Entregar app beta, backend, reconhecimento facial, algoritmo HUB-ELITE, PDF, card e infraestrutura.",
            "milestones": [
                {
                    "date": "2026-05-07",
                    "delivery": "Concluir beta funcional com camera, foto, video, reconhecimento facial e comparativo HUB-ELITE.",
                    "acceptance": "Fluxo iPhone/Expo abre, envia foto/video e retorna analise com status facial.",
                },
                {
                    "date": "2026-05-14",
                    "delivery": "Preparar backend em ambiente externo e storage seguro para videos, fotos, PDFs e cards.",
                    "acceptance": "Ambiente acessivel fora da maquina local com variaveis, logs e health check.",
                },
                {
                    "date": "2026-05-28",
                    "delivery": "Implementar base Supabase, autenticacao inicial e trilha de auditoria LGPD.",
                    "acceptance": "Dados sensiveis armazenados com controle minimo de acesso e rastreabilidade.",
                },
                {
                    "date": "2026-06-15",
                    "delivery": "Entregar release candidata a piloto real.",
                    "acceptance": "Checklist tecnico aprovado e fluxo testado ponta a ponta com usuario piloto.",
                },
            ],
            "dependencies": ["CEO", "CFO"],
        },
        {
            "role": "CFO",
            "department": "Financas, receita e compliance financeiro",
            "owner": "CFO",
            "mission": "Definir preco, custos, pagamentos, margem e controles financeiros para operacao real.",
            "milestones": [
                {
                    "date": "2026-05-07",
                    "delivery": "Validar preco inicial, margem, custo de infraestrutura e custo por analise.",
                    "acceptance": "Modelo de unit economics aprovado para a oferta inicial.",
                },
                {
                    "date": "2026-05-21",
                    "delivery": "Preparar integracao Mercado Pago e processo de conciliacao.",
                    "acceptance": "Fluxo de pagamento, recibo e status financeiro documentados.",
                },
                {
                    "date": "2026-06-05",
                    "delivery": "Definir politica de reembolso, comprovantes e controle mensal.",
                    "acceptance": "Regras financeiras prontas para pilotos pagos.",
                },
            ],
            "dependencies": ["CEO", "CTO", "CCO"],
        },
        {
            "role": "CCO",
            "department": "Comercial, parcerias e sucesso do cliente",
            "owner": "CCO",
            "mission": "Validar mercado, canais, oferta, atendimento e pilotos com clientes reais.",
            "milestones": [
                {
                    "date": "2026-05-08",
                    "delivery": "Definir oferta comercial beta para pais, escolinhas, clubes e categorias de base.",
                    "acceptance": "Proposta comercial aprovada com promessa alinhada ao produto real.",
                },
                {
                    "date": "2026-05-22",
                    "delivery": "Listar e priorizar 20 leads/parceiros para piloto.",
                    "acceptance": "Pipeline com contato, segmento, status e proximo passo.",
                },
                {
                    "date": "2026-06-12",
                    "delivery": "Executar primeiros pilotos assistidos e coletar feedback.",
                    "acceptance": "Feedback estruturado enviado ao CEO, CTO e CMO.",
                },
            ],
            "dependencies": ["CEO", "CTO", "CMO"],
        },
        {
            "role": "CMO",
            "department": "Marca, marketing e crescimento",
            "owner": "CMO",
            "mission": "Construir mensagem, identidade, conteudo, funil e materiais de lancamento da HUB-PODIUM.",
            "milestones": [
                {
                    "date": "2026-05-08",
                    "delivery": "Definir narrativa de marca para Sub-8 a Sub-12 e Sub-13 a Sub-20.",
                    "acceptance": "Mensagens separadas por publico, sem prometer mais que o produto entrega.",
                },
                {
                    "date": "2026-05-24",
                    "delivery": "Criar kit comercial: landing, pitch, imagens, textos e perguntas frequentes.",
                    "acceptance": "Material aprovado por CEO, CCO e CTO.",
                },
                {
                    "date": "2026-06-10",
                    "delivery": "Preparar campanha de pilotos e coleta de depoimentos.",
                    "acceptance": "Plano de canais, calendario e metricas de crescimento definidos.",
                },
            ],
            "dependencies": ["CEO", "CCO", "CTO"],
        },
        {
            "role": "LEGAL",
            "department": "Departamento Juridico HUB-PODIUM",
            "owner": "CEO",
            "mission": "Proteger contratos digitais, LGPD, direito de imagem, marcas, patentes, software, direitos autorais e segredos de negocio.",
            "milestones": [
                {
                    "date": "2026-05-06",
                    "delivery": "Criar minutas beta de termos de uso, privacidade, compra e consentimento de imagem.",
                    "acceptance": "Documentos prontos para revisao do CEO, CTO, CCO, CMO e CFO.",
                },
                {
                    "date": "2026-05-10",
                    "delivery": "Criar inventario inicial de propriedade intelectual e dados pessoais.",
                    "acceptance": "HUB-PODIUM, HUB-ELITE, app, backend, algoritmo, cards e relatorios classificados por protecao.",
                },
                {
                    "date": "2026-05-24",
                    "delivery": "Preparar plano INPI para marcas, software, design e estrategia de segredo de negocio.",
                    "acceptance": "Plano de marcas, registro de software, busca de anterioridade e patenteabilidade documentado.",
                },
                {
                    "date": "2026-05-31",
                    "delivery": "Emitir gate juridico para piloto pago.",
                    "acceptance": "Campanha, checkout, imagem, dados, contratos e PI revisados antes de escalar vendas.",
                },
            ],
            "dependencies": ["CEO", "CTO", "CFO", "CCO", "CMO"],
        },
    ],
    "reporting_rules": [
        "Cada departamento deve enviar status semanal toda sexta-feira ate 18h.",
        "Status deve conter: entregue, em andamento, bloqueios, riscos e decisao necessaria.",
        "Bloqueios entre areas devem ser escalados ao CEO em ate 24 horas.",
        "Mudancas de prazo que afetem piloto real exigem ciencia do board.",
    ],
}


def get_company_board():
    return {
        "company": COMPANY_NAME,
        "board": list(EXECUTIVE_BOARD.values()),
    }


def get_product_authorization():
    return {
        "company": COMPANY_NAME,
        "product_code": PRODUCT_CODE,
        "product_name": PRODUCT_NAME,
        "platform": "web_platform",
        "app": "mobile_app",
        "status": "authorized",
        "decision_id": BOARD_DECISION_ID,
        "authorizations": PRODUCT_AUTHORIZATIONS,
    }


def get_operating_mandate():
    return {
        "company": COMPANY_NAME,
        "product_code": PRODUCT_CODE,
        "mandate": BOARD_CONSENSUS,
        "areas": list(AREA_EXECUTION_MANDATES.values()),
    }


def get_department_delivery_report():
    return {
        "company": COMPANY_NAME,
        "product_code": PRODUCT_CODE,
        "product_name": PRODUCT_NAME,
        "report": CEO_DEPARTMENT_DELIVERY_REPORT,
    }


def get_area_authority(role):
    normalized_role = (role or "").upper()
    member = EXECUTIVE_BOARD.get(normalized_role)
    mandate = AREA_EXECUTION_MANDATES.get(normalized_role)

    if not member or not mandate:
        return {
            "found": False,
            "reason": "Role not found in HUB-PODIUM operating mandate.",
        }

    return {
        "found": True,
        "company": COMPANY_NAME,
        "role": normalized_role,
        "executive_name": member.get("executive_name"),
        "title": member["title"],
        "authority_level": member["authority_level"],
        "mandate": mandate,
    }


def check_execution_authority(role, authority_code):
    normalized_role = (role or "").upper()
    requested_authority = (authority_code or "").strip()
    mandate = AREA_EXECUTION_MANDATES.get(normalized_role)

    if not mandate:
        return {
            "authorized": False,
            "reason": "Role not found in HUB-PODIUM operating mandate.",
        }

    is_allowed = requested_authority in mandate["execution_authorities"]

    return {
        "authorized": is_allowed,
        "company": COMPANY_NAME,
        "role": normalized_role,
        "authority_code": requested_authority,
        "area": mandate["area"],
        "reason": "Execution authority granted." if is_allowed else "Execution authority not granted for this area.",
    }


def check_permission(role, permission):
    normalized_role = (role or "").upper()
    requested_permission = (permission or "").strip()
    member = EXECUTIVE_BOARD.get(normalized_role)

    if not member:
        return {
            "authorized": False,
            "reason": "Role not found in HUB-PODIUM executive board.",
        }

    is_allowed = requested_permission in member["permissions"]

    return {
        "authorized": is_allowed,
        "company": COMPANY_NAME,
        "role": normalized_role,
        "permission": requested_permission,
        "authority_level": member["authority_level"],
        "reason": "Permission granted." if is_allowed else "Permission not granted for this role.",
    }
