from __future__ import annotations

SESSION_COMMAND_CATEGORIES: list[dict] = [
    {
        "id": "summary",
        "title": "Resumo e encerramento",
        "commands": [
            {
                "id": "resumo_sessao",
                "label": "Resumo da Sessão",
                "text": "[Resumo da Sessão]",
                "description": (
                    "Gera resumo estruturado da sessão atual e propõe salvar em "
                    "logs/sessao_resumo_XXX.md (sem gravar sem sua confirmação)."
                ),
                "source": "sistema/diretrizes_ia.md",
            },
            {
                "id": "criar_resumo",
                "label": "Criar resumo da sessão atual",
                "text": "[Criar resumo da sessão atual]",
                "description": "Alias do resumo — mesmo efeito que [Resumo da Sessão].",
                "source": "sistema/instrucoes_projeto.md",
            },
            {
                "id": "finalizar_sessao",
                "label": "Finalizar sessão e gerar resumo",
                "text": "[Finalizar sessão e gerar resumo]",
                "description": (
                    "Encerra a sessão narrativa e gera o resumo para arquivo, "
                    "incluindo a seção Arquivos Atualizados Nesta Sessão."
                ),
                "source": "sistema/diretrizes_ia.md",
            },
        ],
    },
    {
        "id": "time",
        "title": "Passagem de tempo",
        "commands": [
            {
                "id": "pulso_1_dia",
                "label": "Passar 1 dia (Pulso do Mundo)",
                "text": (
                    "[Passagem de tempo — passou 1 dia in-game. "
                    "Rodar o Pulso do Mundo conforme pulso_procedimento.md "
                    "e narrar o que Ryan percebe ao retomar a cena.]"
                ),
                "description": (
                    "Obrigatório quando passa 1 dia in-game ou Ryan dorme a noite: "
                    "1 rolagem d100 por linha em pulso_geral.md."
                ),
                "source": "sistema/pulso_procedimento.md",
            },
            {
                "id": "pulso_varios_dias",
                "label": "Passar vários dias",
                "text": (
                    "[Passagem de tempo — passaram vários dias in-game. "
                    "Rodar 1 ciclo de Pulso do Mundo por dia narrado, "
                    "resumir off-screen e só então retomar a cena. "
                    "Pergunte quantos dias se ainda não estiver claro.]"
                ),
                "description": "Para viagem, downtime longo ou saltos temporais maiores.",
                "source": "sistema/pulso_procedimento.md",
            },
            {
                "id": "dormir_noite",
                "label": "Dormir a noite toda",
                "text": (
                    "Ryan dorme a noite toda. "
                    "[Passagem de tempo — 1 dia in-game; rodar Pulso do Mundo ao narrar o despertar.]"
                ),
                "description": "Equivalente a passar 1 dia quando Ryan encerra o dia dormindo.",
                "source": "sistema/pulso_procedimento.md",
            },
        ],
    },
    {
        "id": "updates",
        "title": "Atualização de arquivos",
        "commands": [
            {
                "id": "preview_atualizacoes",
                "label": "Preview de atualizações pós-sessão",
                "text": (
                    "[Faça um resumo do que precisa ser atualizado nos arquivos após essa sessão, "
                    "liste também em quais arquivos ocorrerão essas atualizações. "
                    "Me mostre o resumo antes de qualquer alteração.]"
                ),
                "description": "Lista mudanças propostas em board, consequências, relacionamentos etc.",
                "source": "sistema/como_atualizar_arquivos.md",
            },
            {
                "id": "registrar_downtime",
                "label": "Registrar downtime do Ryan",
                "text": "Atualize o downtime_ryan.md com as atividades que Ryan realizou neste período.",
                "description": "Registra projetos, oficina e atividades de downtime.",
                "source": "sistema/como_atualizar_arquivos.md",
            },
            {
                "id": "atualizacao_completa",
                "label": "Proposta de atualização completa",
                "text": (
                    "Faça uma análise completa desta sessão e proponha atualizações para Board, "
                    "Consequências, Relacionamentos e Downtime. "
                    "Só aplique depois que eu confirmar."
                ),
                "description": "Análise ampla com aprovação explícita antes de alterar arquivos.",
                "source": "sistema/como_atualizar_arquivos.md",
            },
        ],
    },
]


def build_session_commands() -> dict:
    quick_ids = ("resumo_sessao", "pulso_1_dia", "finalizar_sessao")
    quick: list[dict] = []
    for category in SESSION_COMMAND_CATEGORIES:
        for command in category["commands"]:
            if command["id"] in quick_ids:
                quick.append({**command, "category": category["title"]})

    return {
        "categories": SESSION_COMMAND_CATEGORIES,
        "quick": quick,
        "sources": [
            "sistema/instrucoes_projeto.md",
            "sistema/diretrizes_ia.md",
            "sistema/pulso_procedimento.md",
            "sistema/como_atualizar_arquivos.md",
        ],
    }