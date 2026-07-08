from __future__ import annotations

import re
from pathlib import Path

from motor.settings import Settings, get_settings

INSTRUCOES_PATH = "sistema/instrucoes_projeto.md"
COMO_ATUALIZAR_PATH = "sistema/como_atualizar_arquivos.md"

SESSION_COMMAND_CATEGORIES: list[dict] = [
    {
        "id": "summary",
        "title": "Resumo e encerramento",
        "commands": [
            {
                "id": "resumo_sessao",
                "label": "Resumo da Sessão",
                "text": "[Resumo da Sessão]",
                "matchers": ["resumo da sessão"],
            },
            {
                "id": "criar_resumo",
                "label": "Criar resumo da sessão atual",
                "text": "[Criar resumo da sessão atual]",
                "matchers": ["criar resumo da sessão atual"],
            },
            {
                "id": "finalizar_sessao",
                "label": "Finalizar sessão e gerar resumo",
                "text": "[Finalizar sessão e gerar resumo]",
                "matchers": ["finalizar sessão e gerar resumo"],
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
                "matchers": ["passou 1 dia", "1 dia in-game", "pulso do mundo"],
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
                "matchers": ["vários dias", "varios dias", "saltos temporais"],
            },
            {
                "id": "dormir_noite",
                "label": "Dormir a noite toda",
                "text": (
                    "Ryan dorme a noite toda. "
                    "[Passagem de tempo — 1 dia in-game; rodar Pulso do Mundo ao narrar o despertar.]"
                ),
                "matchers": ["dormiu a noite", "dormir a noite"],
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
                "matchers": ["resumo rápido", "preview", "resumo do que precisa ser atualizado"],
            },
            {
                "id": "registrar_downtime",
                "label": "Registrar downtime do Ryan",
                "text": "Atualize o downtime_ryan.md com as atividades que Ryan realizou neste período.",
                "matchers": ["foco em downtime", "downtime_ryan"],
            },
            {
                "id": "atualizacao_completa",
                "label": "Proposta de atualização completa",
                "text": (
                    "Faça uma análise completa desta sessão e proponha atualizações para Board, "
                    "Consequências, Relacionamentos e Downtime. "
                    "Só aplique depois que eu confirmar."
                ),
                "matchers": ["atualização completa", "atualizacao completa"],
            },
        ],
    },
]

_UPDATE_PURPOSE_HINTS = {
    "preview_atualizacoes": ("resumo",),
    "registrar_downtime": ("downtime",),
    "atualizacao_completa": ("completa", "segur"),
}


def _read_repo_text(settings: Settings, rel_path: str) -> str:
    path = settings.repo_root / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _strip_md(value: str) -> str:
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    return cleaned.strip()


def _parse_table_rows(section_text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in section_text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cols = [_strip_md(col) for col in line.strip("|").split("|")]
        if len(cols) < 2:
            continue
        if cols[0].lower() in {"comando", "finalidade", "o que aconteceu na sessão"}:
            continue
        rows.append((cols[0], cols[1]))
    return rows


def _section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def _subsection_text(section_text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^\*\*{re.escape(heading)}\*\*\s*\n(.*?)(?=^\*\*|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(section_text)
    return match.group(1) if match else ""


def _bullet_lines(block: str) -> list[str]:
    lines: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(_strip_md(line[2:].strip()))
    return lines


def _normalize_lookup(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _parse_player_commands_table(instrucoes_text: str) -> dict[str, str]:
    section = _section_text(instrucoes_text, "Comandos do jogador")
    mapping: dict[str, str] = {}
    for comando, acao in _parse_table_rows(section):
        for part in re.split(r"\s*/\s*", comando):
            key = _normalize_lookup(part)
            if key:
                mapping[key] = acao
    return mapping


def _parse_update_templates(como_atualizar_text: str) -> list[tuple[str, str]]:
    section = _section_text(como_atualizar_text, "Comandos Recomendados")
    rows: list[tuple[str, str]] = []
    for finalidade, comando in _parse_table_rows(section):
        rows.append((finalidade, comando))
    return rows


def _parse_event_files(como_atualizar_text: str) -> dict[str, str]:
    section = _section_text(como_atualizar_text, "Arquivos a Atualizar por Tipo de Evento")
    mapping: dict[str, str] = {}
    for evento, arquivos in _parse_table_rows(section):
        key = _normalize_lookup(evento)
        if key:
            mapping[key] = arquivos
    return mapping


def _summary_behavior(instrucoes_text: str) -> str:
    section = _section_text(instrucoes_text, "Comandos do jogador")
    bullets = _bullet_lines(_subsection_text(section, "Resumos de sessão"))
    if bullets:
        return " ".join(bullets)
    return (
        "Incluir seção Arquivos Atualizados Nesta Sessão. "
        "Nunca salvar/commitar/push sem confirmação explícita do jogador."
    )


def _time_behavior(como_atualizar_text: str, instrucoes_text: str) -> str:
    events = _parse_event_files(como_atualizar_text)
    for key, value in events.items():
        if "passou1dia" in key or "dormiuanoite" in key:
            return value
    refresh = _section_text(instrucoes_text, "Refresh de estado")
    for line in refresh.splitlines():
        if "passar 1 dia" in line.lower():
            return _strip_md(line)
    return "Rodar pulso_procedimento.md e atualizar pulso_do_mundo/ conforme impacto."


def _match_player_description(command: dict, player_table: dict[str, str]) -> str:
    for matcher in command.get("matchers", []):
        key = _normalize_lookup(matcher)
        if key in player_table:
            return player_table[key]
    label_key = _normalize_lookup(command["label"])
    if label_key in player_table:
        return player_table[label_key]
    return ""


def _find_update_template(
    command_id: str,
    templates: list[tuple[str, str]],
) -> tuple[str, str]:
    hints = _UPDATE_PURPOSE_HINTS.get(command_id, ())
    for finalidade, comando in templates:
        lowered = finalidade.lower()
        if hints and all(hint in lowered for hint in hints):
            return finalidade, _strip_md(comando)
    return "", ""


def _match_update_description(command: dict, templates: list[tuple[str, str]]) -> tuple[str, str]:
    finalidade, comando = _find_update_template(command["id"], templates)
    description = finalidade or command["label"]
    behavior = comando or (
        "Sempre mostre mudanças propostas antes de aplicar. "
        "Seja específico sobre qual arquivo atualizar."
    )
    return description, behavior


def _enrich_command(
    command: dict,
    *,
    category_id: str,
    player_table: dict[str, str],
    update_templates: list[tuple[str, str]],
    summary_behavior: str,
    time_behavior: str,
    instrucoes_path: str,
    como_atualizar_path: str,
) -> dict:
    enriched = {
        "id": command["id"],
        "label": command["label"],
        "text": command["text"],
        "source": instrucoes_path if category_id == "summary" else como_atualizar_path,
    }

    if category_id == "summary":
        description = _match_player_description(command, player_table)
        enriched["description"] = description or "Gera resumo estruturado da sessão atual."
        enriched["behavior"] = summary_behavior
        enriched["source"] = instrucoes_path
    elif category_id == "time":
        enriched["description"] = "Passagem de tempo in-game com Pulso do Mundo obrigatório."
        enriched["behavior"] = time_behavior
        enriched["source"] = como_atualizar_path
    else:
        description, behavior = _match_update_description(command, update_templates)
        enriched["description"] = description
        enriched["behavior"] = behavior
        enriched["source"] = como_atualizar_path

    return enriched


def build_session_commands(settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    instrucoes_text = _read_repo_text(cfg, INSTRUCOES_PATH)
    como_atualizar_text = _read_repo_text(cfg, COMO_ATUALIZAR_PATH)

    player_table = _parse_player_commands_table(instrucoes_text)
    update_templates = _parse_update_templates(como_atualizar_text)
    summary_behavior = _summary_behavior(instrucoes_text)
    time_behavior = _time_behavior(como_atualizar_text, instrucoes_text)

    categories: list[dict] = []
    for category in SESSION_COMMAND_CATEGORIES:
        commands = [
            _enrich_command(
                command,
                category_id=category["id"],
                player_table=player_table,
                update_templates=update_templates,
                summary_behavior=summary_behavior,
                time_behavior=time_behavior,
                instrucoes_path=INSTRUCOES_PATH,
                como_atualizar_path=COMO_ATUALIZAR_PATH,
            )
            for command in category["commands"]
        ]
        categories.append(
            {
                "id": category["id"],
                "title": category["title"],
                "commands": commands,
            }
        )

    quick_ids = ("resumo_sessao", "pulso_1_dia", "finalizar_sessao")
    quick: list[dict] = []
    for category in categories:
        for command in category["commands"]:
            if command["id"] in quick_ids:
                quick.append({**command, "category": category["title"]})

    return {
        "categories": categories,
        "quick": quick,
        "sources": [INSTRUCOES_PATH, COMO_ATUALIZAR_PATH],
    }