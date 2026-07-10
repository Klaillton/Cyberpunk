#!/usr/bin/env python3
"""
Motor de narracao para campanha solo: integridade de estado + contexto inteligente + chat.

Exemplos:
  python scripts/narracao_engine.py check
  python scripts/narracao_engine.py chat --message "Quais eventos estao pendentes?"
  python scripts/narracao_engine.py repl

Provider:
  - grok (padrao): usa GROK_BIN para responder
  - none: apenas gera prompt consolidado para uso manual
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from motor.markdown.campaign_paths import is_template_path
from motor.player_message import format_player_message_for_prompt, parse_player_message
from motor.npc import list_campaign_sheets
from motor.session_command_handler import (
    format_history_block,
    is_finalize_summary_command,
    latest_session_log_path,
    next_session_log_rel,
    session_summary_context_paths,
)
SYSTEM_DIR = REPO_ROOT / "sistema"
CHAT_DIR = REPO_ROOT / ".chat-engine"
SESSIONS_DIR = CHAT_DIR / "sessions"

GROK_BIN = Path(os.environ.get("GROK_BIN", r"C:\Users\Dante\.grok\bin\grok.exe"))

# Arquivos minimos para operar com integridade de estado.
MANDATORY_FILES = [
    "sistema/registro_arquivos.md",
    "sistema/instrucoes_projeto.md",
    "sistema/diretrizes_ia.md",
    "sistema/diretrizes_narrador.md",
    "sistema/dashboard_contexto.md",
    "board/board_campanha.md",
    "consequencias/consequencias_persistentes.md",
    "reputacao.md",
    "heat.md",
    "event_queue.md",
    "economia.md",
    "relacionamentos/mapa_relacional_geral.md",
]

CORE_CONTEXT = [
    "sistema/registro_arquivos.md",
    "sistema/instrucoes_projeto.md",
    "sistema/dashboard_contexto.md",
    "board/board_campanha.md",
]

OLLAMA_SKIP_CONTEXT = frozenset(
    {
        "sistema/registro_arquivos.md",
        "sistema/instrucoes_projeto.md",
        "sistema/diretrizes_ia.md",
        "sistema/diretrizes_narrador.md",
    }
)

OLLAMA_FILE_PRIORITY = (
    "board/board_campanha.md",
    "heat.md",
    "reputacao.md",
    "economia.md",
    "event_queue.md",
    "consequencias/consequencias_persistentes.md",
    "relacionamentos/",
    "facoes/",
    "sistema/dashboard_contexto.md",
)

SISTEMA_OLLAMA_KEEP = frozenset(
    {
        "sistema/registro_arquivos.md",
        "sistema/instrucoes_projeto.md",
        "sistema/como_atualizar_arquivos.md",
        "sistema/dashboard_contexto.md",
        "sistema/diretrizes_ia.md",
    }
)

OLLAMA_SISTEMA_PRIORITY = (
    "fichas/",
    "sistema/registro_arquivos.md",
    "sistema/dashboard_contexto.md",
    "sistema/instrucoes_projeto.md",
    "board/board_campanha.md",
    "logs/sessao_resumo_",
    "event_queue.md",
    "relacionamentos/",
)

OLLAMA_MESTRE_PRIORITY = (
    "fichas/npc/",
    "pulso_do_mundo/pack_badlands/",
    "board/board_campanha.md",
    "relacionamentos/mapa_relacional_geral.md",
    "relacionamentos/ryan_relacionamentos.md",
    "relacionamentos/crew_relacionamentos.md",
    "relacionamentos/crew_polycule_ryan_valk_alex_reina.md",
    "relacionamentos/",
)

MESTRE_BASE_CONTEXT = [
    "relacionamentos/mapa_relacional_geral.md",
    "board/board_campanha.md",
]

SISTEMA_BASE_CONTEXT = [
    "sistema/registro_arquivos.md",
    "relacionamentos/mapa_relacional_geral.md",
    "sistema/instrucoes_projeto.md",
]

_TECH_QUESTION_RE = re.compile(
    r"\b(llm|api|interface|provider|ollama|funcionando|sistema|arquivo|comando|github|servidor|frontend|bug|erro)\b",
    re.IGNORECASE,
)

_FICHA_PATH_RE = re.compile(
    r"\b(ficha|fichas/|\.md\b|caminho|arquivo|registro)\b",
    re.IGNORECASE,
)

_FICHA_LIST_RE = re.compile(
    r"\b(quais|liste|lista|quantas?|tem alguma|dispon[ií]veis?|carregad)\b.*\b(fichas?)\b"
    r"|\b(fichas?)\b.*\b(quais|liste|lista|quantas?|pasta|dispon[ií]veis?|carregad)\b",
    re.IGNORECASE,
)

_FICHA_LOOKUP_RE = re.compile(
    r"\b(ficha|fichas/|caminho.*ficha|qual.*ficha|ficha.*(?:da|do|de))\b",
    re.IGNORECASE,
)

_ROLE_FICHA_RE = re.compile(
    r"\b(netrunner|nomad|techie|medtech|fixer|solo|vehicle)\b",
    re.IGNORECASE,
)

_CAMPAIGN_BRIEF_RE = re.compile(
    r"\b(resumo.*campanha|brief|resumo\s+at[eé]\s+aqui|como funciona.*resumo)\b",
    re.IGNORECASE,
)

_UPDATE_PREVIEW_RE = re.compile(
    r"\b(resumo.*atualiz|atualiz.*arquiv|arquivos.*sess|o que precisa ser atualizado)\b",
    re.IGNORECASE,
)

_INFO_QUESTION_RE = re.compile(
    r"\b(quem|qual|quais|quantos?|liste|lista|faz parte|membros?|crew|equipe|npcs?)\b",
    re.IGNORECASE,
)

_TIMELINE_QUESTION_RE = re.compile(
    r"\b(futur[oa]s?|night city|voltar|quando|plano|canon|cronolog|deveria|ainda n[aã]o)\b",
    re.IGNORECASE,
)

_PACK_RECRUIT_RE = re.compile(
    r"\b(tomas|mara|elias|recrutas?|pack\s+badlands|badlands)\b",
    re.IGNORECASE,
)

_TRAITOR_SUSPICION_RE = re.compile(
    r"\b(trai(?:d(?:or|a))?|trai[cç][aã]o|nervos[oa]|desconfia|suspeit|inquiet|monitorament)\b",
    re.IGNORECASE,
)

_POLYCULE_QUESTION_RE = re.compile(
    r"\b(polycule|harem|reina|alex|jax|kaz|doc|night\s*city|crew\s+futur)\b",
    re.IGNORECASE,
)

_CREW_MEMBERSHIP_RE = re.compile(
    r"\b(quem|qual|quais|membros?|faz\s+parte)\b.*\b(crew|equipe)\b|\b(crew|equipe)\b.*\b(quem|qual|quais|membros?|faz\s+parte)\b",
    re.IGNORECASE,
)


def normalize_channel(channel: str | None) -> str:
    value = (channel or "narracao").strip().lower()
    if value in {"narrador", "mestre", "gm", "off-game", "offgame"}:
        return "mestre"
    if value in {"sistema", "system", "tech", "dev", "suporte"}:
        return "sistema"
    if value in {"narracao", "gestor"}:
        return value
    return "narracao"

DEFAULT_OLLAMA_MAX_PROMPT_CHARS = 12_000
DEFAULT_OLLAMA_MAX_CONTEXT_FILES = 10

INTENT_RULES: list[tuple[re.Pattern[str], list[str]]] = [
    (
        re.compile(r"\b(heat|exposicao|perseguicao|rastreamento)\b", re.IGNORECASE),
        ["heat.md", "event_queue.md", "consequencias/consequencias_persistentes.md"],
    ),
    (
        re.compile(r"\b(reputacao|faccao|fac[c|c]ao|faccoes)\b", re.IGNORECASE),
        ["reputacao.md", "relacionamentos/faccao_relacionamentos.md", "facoes/faccoes_geral.md"],
    ),
    (
        re.compile(r"\b(economia|grana|eddies|recursos|oficina|projeto)\b", re.IGNORECASE),
        ["economia.md", "logs/downtime_ryan.md"],
    ),
    (
        re.compile(
            r"\b(npc|reyes|valk|alex|reina|kaz|doc|jax|ryan|tomas|mara|elias)\b",
            re.IGNORECASE,
        ),
        [
            "relacionamentos/mapa_relacional_geral.md",
            "relacionamentos/ryan_relacionamentos.md",
            "relacionamentos/crew_relacionamentos.md",
        ],
    ),
    (
        _PACK_RECRUIT_RE,
        [
            "pulso_do_mundo/pack_badlands/recrutas.md",
            "fichas/npc/tomas_recruit.md",
        ],
    ),
    (
        re.compile(r"\b(pulso|off-screen|offscreen|dia in-game|dia ingame|downtime)\b", re.IGNORECASE),
        ["sistema/pulso_procedimento.md", "pulso_do_mundo/README.md"],
    ),
    (
        _TIMELINE_QUESTION_RE,
        [
            "relacionamentos/crew_polycule_ryan_valk_alex_reina.md",
            "relacionamentos/crew_relacionamentos.md",
        ],
    ),
]


@dataclass
class ChatTurn:
    timestamp: str
    role: str
    message: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


SUMMARY_CONTEXT_TEMPLATES = frozenset({"logs/sessao_resumo_template.md"})


def resolve_paths(rel_paths: list[str], *, allow_summary_templates: bool = False) -> list[Path]:
    out: list[Path] = []
    for rel in rel_paths:
        if is_template_path(rel) and not (
            allow_summary_templates and rel.replace("\\", "/") in SUMMARY_CONTEXT_TEMPLATES
        ):
            continue
        p = REPO_ROOT / rel
        if p.exists() and p.is_file():
            out.append(p)
    return out


def check_integrity() -> list[str]:
    missing: list[str] = []
    for rel in MANDATORY_FILES:
        if not (REPO_ROOT / rel).exists():
            missing.append(rel)
    return missing


def _priority_tuple(rel: str, priority_prefixes: tuple[str, ...]) -> tuple[int, int, str]:
    for index, prefix in enumerate(priority_prefixes):
        if rel == prefix or rel.startswith(prefix):
            return (0, index, rel)
    if rel.startswith("sistema/"):
        return (2, 0, rel)
    return (1, 0, rel)


def prioritize_paths_for_ollama(paths: list[Path], channel: str | None = None) -> list[Path]:
    if channel == "mestre":
        priority = OLLAMA_MESTRE_PRIORITY
    elif channel == "sistema":
        priority = OLLAMA_SISTEMA_PRIORITY
    else:
        priority = OLLAMA_FILE_PRIORITY
    return sorted(
        paths,
        key=lambda path: _priority_tuple(path.relative_to(REPO_ROOT).as_posix(), priority),
    )


def select_context_files(
    user_message: str,
    max_files: int = 10,
    *,
    provider: str | None = None,
    channel: str | None = None,
    session_intent: str | None = None,
) -> list[Path]:
    effective_max = max_files
    if provider == "ollama" and max_files == 10:
        if session_intent == "summary":
            effective_max = 6
        elif channel == "sistema":
            effective_max = 6
        elif channel == "mestre":
            effective_max = 5
        else:
            effective_max = DEFAULT_OLLAMA_MAX_CONTEXT_FILES

    if session_intent == "summary":
        selected = set(session_summary_context_paths())
        paths = resolve_paths(sorted(selected), allow_summary_templates=True)
        if provider == "ollama":
            paths = prioritize_paths_for_ollama(paths, channel="gestor")
        return paths[:effective_max]

    if channel == "sistema":
        selected = set(SISTEMA_BASE_CONTEXT)
        if _CAMPAIGN_BRIEF_RE.search(user_message):
            selected.update(
                [
                    "sistema/dashboard_contexto.md",
                    "board/board_campanha.md",
                    "sistema/instrucoes_projeto.md",
                    "sistema/diretrizes_ia.md",
                    "event_queue.md",
                ]
            )
            latest_log = latest_session_log_path()
            if latest_log is not None:
                selected.add(latest_log.relative_to(REPO_ROOT).as_posix())
        if (
            _FICHA_LIST_RE.search(user_message)
            or _FICHA_LOOKUP_RE.search(user_message)
            or _ROLE_FICHA_RE.search(user_message)
            or re.search(r"\balex\b", user_message, re.IGNORECASE)
        ):
            selected.add("sistema/instrucoes_projeto.md")
            if re.search(r"netrunner|\balex\b", user_message, re.IGNORECASE):
                selected.add("fichas/netrunner - alex_specter_kane.md")
            if re.search(r"nomad|valk|lena", user_message, re.IGNORECASE):
                selected.add("fichas/nomad - lena_valk_kane.md")
            if re.search(r"techie|ryan", user_message, re.IGNORECASE):
                selected.add("fichas/techie - ryan_wireghost_voss.md")
        if _UPDATE_PREVIEW_RE.search(user_message):
            selected.update(
                [
                    "board/board_campanha.md",
                    "sistema/dashboard_contexto.md",
                    "consequencias/consequencias_persistentes.md",
                    "relacionamentos/ryan_relacionamentos.md",
                    "heat.md",
                    "event_queue.md",
                ]
            )
        elif _TECH_QUESTION_RE.search(user_message):
            selected.update(["sistema/arquitetura_narracao_solo.md", "README.md"])
    elif channel == "mestre":
        selected = set(MESTRE_BASE_CONTEXT)
        if _PACK_RECRUIT_RE.search(user_message) or _TRAITOR_SUSPICION_RE.search(user_message):
            selected.update(
                [
                    "fichas/npc/tomas_recruit.md",
                    "pulso_do_mundo/pack_badlands/recrutas.md",
                ]
            )
            if re.search(r"\bmara\b", user_message, re.IGNORECASE):
                selected.add("fichas/npc/mara_recruit.md")
            if re.search(r"\belias\b", user_message, re.IGNORECASE):
                selected.add("fichas/npc/elias_recruit.md")
        if _CREW_MEMBERSHIP_RE.search(user_message) or _POLYCULE_QUESTION_RE.search(
            user_message
        ):
            selected.update(
                [
                    "relacionamentos/crew_relacionamentos.md",
                    "relacionamentos/crew_polycule_ryan_valk_alex_reina.md",
                ]
            )
        elif _INFO_QUESTION_RE.search(user_message):
            selected.update(["relacionamentos/ryan_relacionamentos.md"])
        if _TIMELINE_QUESTION_RE.search(user_message):
            selected.update(
                [
                    "relacionamentos/crew_polycule_ryan_valk_alex_reina.md",
                    "relacionamentos/crew_relacionamentos.md",
                ]
            )
        for pattern, files in INTENT_RULES:
            if pattern.search(user_message):
                selected.update(files)
    else:
        selected = set(CORE_CONTEXT)
        for pattern, files in INTENT_RULES:
            if pattern.search(user_message):
                selected.update(files)
        selected.update(["reputacao.md", "heat.md", "event_queue.md", "economia.md"])

    paths = resolve_paths(sorted(selected))
    if provider == "ollama":
        paths = [
            path
            for path in paths
            if path.relative_to(REPO_ROOT).as_posix() not in OLLAMA_SKIP_CONTEXT
            or (
                channel == "sistema"
                and path.relative_to(REPO_ROOT).as_posix() in SISTEMA_OLLAMA_KEEP
            )
        ]
        paths = prioritize_paths_for_ollama(paths, channel=channel)

    return paths[:effective_max]


def compact_content(path: Path, max_chars: int = 4000) -> str:
    text = read_text(path)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...conteudo truncado para caber no contexto...]\n"


def compact_board_npcs(path: Path, max_chars: int = 1800) -> str:
    text = read_text(path)
    marker = "## NPCs Importantes"
    start = text.find(marker)
    if start < 0:
        return compact_content(path, max_chars=max_chars)
    excerpt = text[start : start + max_chars]
    if len(text) > start + max_chars:
        excerpt += "\n\n[...board truncado...]\n"
    return excerpt


def _sistema_needs_ficha_index(user_message: str) -> bool:
    return bool(
        _FICHA_LIST_RE.search(user_message)
        or _FICHA_LOOKUP_RE.search(user_message)
        or _ROLE_FICHA_RE.search(user_message)
        or re.search(r"\balex\b", user_message, re.IGNORECASE)
    )


def _build_fichas_index_block() -> str:
    sheets = list_campaign_sheets()
    if not sheets:
        return ""
    lines = [
        "### Indice de fichas (gerado do disco — fonte autoritativa para paths)",
        "",
    ]
    for item in sheets:
        lines.append(f"- `{item['rel']}` — papel: {item['role']}")
    return "\n".join(lines)


def _ollama_mode_hint(mode: str) -> str:
    if mode == "mestre":
        return "Modo MESTRE: meta, fora da cronologia."
    if mode == "narrador":
        return "Nao controle acoes do protagonista."
    return (
        "Modo GESTOR: responda com consistencia de estado. "
        "Nao altere arquivos nem proponha updates automaticos."
    )


def _ollama_channel_hint(channel: str) -> str:
    if channel == "mestre":
        return (
            "Canal MESTRE off-game: responda como GM de mesa, sem narrar cena."
        )
    if channel == "sistema":
        return (
            "Canal SISTEMA: responda sobre LLM, API, arquivos e comandos. Sem narrar cena."
        )
    if channel == "gestor":
        return (
            "Canal GESTOR: responda objetivamente sobre estado e consistencia. "
            "Sem narrar cena."
        )
    return (
        "Canal NARRACAO PRINCIPAL: 1-2 paragrafos curtos com a CONSEQUENCIA imediata da ultima acao. "
        "CONTINUIDADE OBRIGATORIA: mantenha local, postura e NPCs presentes do historico; "
        "nao teleporte Ryan (ex: de parede do acampamento para dentro da tenda) sem ele se mover. "
        "Nao reabra narrando de novo o que o jogador acabou de fazer. "
        "Se o jogador JA executou a acao, narre o que acontece em seguida — nao ofereca menu de opcoes. "
        "Falas entre aspas do jogador JA foram ditas — reaja com NPCs/ambiente, sem repetir a frase. "
        "ANTI-REPETICAO: nao copie frases da sua resposta anterior; traga fato NOVO (reacao de NPC, detalhe sensorial, interrupcao). "
        "Maximo 2 paragrafos curtos (3-5 frases). Termine com consequencia ou reacao de NPC — NAO pergunte 'o que voce faz'. "
        "PROIBIDO: A/B/C, listas numeradas, 'Voce pode', 'Qual e sua prioridade', ecoar/reformular a acao do jogador, prefixo 'NARRADOR:'."
    )


def _last_narrator_text(history: list[dict] | None) -> str:
    if not history:
        return ""
    for entry in reversed(history):
        if str(entry.get("role", "")).lower() != "assistant":
            continue
        content = str(entry.get("content", "")).strip()
        if content:
            return content
    return ""


def _last_player_text(history: list[dict] | None) -> str:
    if not history:
        return ""
    for entry in reversed(history):
        if str(entry.get("role", "")).lower() != "user":
            continue
        content = str(entry.get("content", "")).strip()
        if content:
            return re.sub(r"^\[[^\]]+\]\s*VOCE:\s*", "", content, flags=re.IGNORECASE).strip()
    return ""


def _dedupe_sentences_against_previous(text: str, previous: str) -> str:
    if not previous.strip():
        return text
    prev = re.sub(r"\s+", " ", previous.lower())
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    kept: list[str] = []
    for sentence in sentences:
        part = sentence.strip()
        if not part:
            continue
        norm = re.sub(r"\s+", " ", part.lower())
        if len(norm) >= 24 and (norm in prev or norm[:50] in prev):
            continue
        kept.append(part)
    return " ".join(kept).strip() if kept else text.strip()


def _sanitize_narracao_reply(
    text: str,
    *,
    previous: str = "",
    player_message: str = "",
) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^(?:NARRADOR\s*:\s*)+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r"(?:Aqui está uma pergunta|Aqui esta uma pergunta)\s*:?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = _dedupe_sentences_against_previous(cleaned, previous)
    if player_message.strip():
        cleaned = _dedupe_sentences_against_previous(cleaned, player_message)
    cleaned = re.sub(r"^\s*[A-D]\)\s+.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\d+\s*[-.)]\s+.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(
        r"(?:Você pode|Voce pode|Você tem as seguintes opções|Voce tem as seguintes opcoes):.*$",
        "",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"(?:Qual é a sua prioridade|Qual e a sua prioridade|O que você fará|O que voce fara)\??.*$",
        "",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"(?:O que (?:você|voce) faz em seguida|Agora,?\s*o que (?:você|voce) faz)\??.*$",
        "",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"Escolha uma op[cç][aã]o.*$",
        "",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _sanitize_summary_reply(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"(?<!\n)(#{1,3} )", r"\n\n\1", cleaned)
    cleaned = re.sub(r"^\n+", "", cleaned)
    cleaned = re.sub(r"^\s*\d+\s*[-.)]\s+.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"O que você (?:faz|deseja fazer)\??.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"O que voce (?:faz|deseja fazer)\??.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"Você pode:.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"Voce pode:.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"Escolha uma op[cç][aã]o.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def sanitize_ollama_reply(
    text: str,
    channel: str = "narracao",
    *,
    session_intent: str | None = None,
    history: list[dict] | None = None,
) -> str:
    if session_intent == "summary":
        return _sanitize_summary_reply(text)
    cleaned = text.strip()
    if channel == "narracao":
        cleaned = _sanitize_narracao_reply(
            cleaned,
            previous=_last_narrator_text(history),
            player_message=_last_player_text(history),
        )
    cleaned = re.sub(
        r"\([^)]*(?:respondid[ao]|anteriormente|remova|relevante|jogador|turno|instruc)[^)]*\)",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"(?:Aqui está a cena atual:|Aqui esta a cena atual:)\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"Os arquivos utilizados foram[^\n]*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    if channel in {"mestre", "sistema"}:
        cleaned = re.sub(r"\*\*Tom de mesa de RPG\*\*\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\*\*Pergunta do jogador\*\*\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\*\*Resposta\*\*\s*", "", cleaned, flags=re.IGNORECASE)
    if channel == "sistema":
        cleaned = re.sub(
            r"^(?:Vamos l[aá]|Ol[aá])[!,.]?\s*(?:Como assistente do canal SISTEMA,?)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(
            r"(?:Alguns comandos recomendados incluem|Lembre-se de sempre mencionar).*$",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
    if channel == "mestre":
        cleaned = re.sub(
            r"\*\*[^*]+\?\*\*\s*",
            "",
            cleaned,
            count=1,
        )
        cleaned = re.sub(
            r"(?:Você quer|Voce quer|Quais das informações).*?$",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
        cleaned = re.sub(r"^\s*[A-D]\)\s+.*$", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*\d+\.\s+.*$", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*\*\s+.*\?\s*$", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(
            r"Escolha uma op[cç][aã]o.*$",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
        cleaned = re.sub(
            r"Qual [eé] a escolha\??.*$",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
        cleaned = re.sub(
            r"(?:Quem é|Quem e) [A-Z][^.?!]*\?\s*",
            "",
            cleaned,
            count=2,
        )
        cleaned = re.sub(
            r"##\s*(?:Pergunta do jogador|Resposta):?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"\*\*downtime\*\*", "downtime", cleaned, flags=re.IGNORECASE)
        lines = [line for line in cleaned.splitlines() if line.strip()]
        if lines and lines[0].strip().endswith("?") and len(lines[0]) < 120:
            lines = lines[1:]
        scene_markers = (
            "a luz do sol",
            "a manhã",
            "a manha",
            "o sol começa",
            "ryan observa",
            "você está em",
            "voce esta em",
        )
        if lines and any(lines[0].lower().startswith(marker) for marker in scene_markers):
            lines = [line for line in lines if not any(line.lower().startswith(m) for m in scene_markers)]
        cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"  +", " ", cleaned)
    return cleaned.strip()


def _ollama_file_budget(
    rel: str,
    context_budget: int,
    remaining_files: int,
    *,
    channel: str = "narracao",
) -> int:
    if remaining_files <= 0:
        return 0
    if channel == "mestre" and rel.startswith("relacionamentos/"):
        return min(int(context_budget * 0.5), 3200)
    if rel == "board/board_campanha.md":
        if channel == "mestre":
            return min(1800, context_budget // max(remaining_files, 1))
        return min(int(context_budget * 0.45), 2800)
    if rel == "heat.md":
        return min(int(context_budget * 0.25), 1400)
    if remaining_files == 1:
        return context_budget
    return min(max(context_budget // remaining_files, 400), 1200)


def _build_ollama_context_blocks(
    context_paths: list[Path],
    context_budget: int,
    *,
    channel: str = "narracao",
) -> list[str]:
    blocks: list[str] = []
    used = 0
    ordered = prioritize_paths_for_ollama(context_paths, channel=channel)

    for index, path in enumerate(ordered):
        remaining_files = len(ordered) - index
        remaining_budget = context_budget - used
        if remaining_budget < 200:
            break

        rel = path.relative_to(REPO_ROOT).as_posix()
        file_cap = min(
            _ollama_file_budget(rel, context_budget, remaining_files, channel=channel),
            remaining_budget,
        )
        if file_cap < 200:
            continue

        if channel == "mestre" and rel == "board/board_campanha.md":
            content = compact_board_npcs(path, max_chars=file_cap)
        else:
            content = compact_content(path, max_chars=file_cap)
        block = f"### {rel}\n\n{content}"
        blocks.append(block)
        used += len(block)

    return blocks


def _build_session_summary_prompt(
    user_message: str,
    context_paths: list[Path],
    *,
    max_prompt_chars: int,
    history: list[dict] | None = None,
) -> str:
    target_log = next_session_log_rel()
    finalize = is_finalize_summary_command(user_message)
    opener = "✅ Sessão Finalizada" if finalize else "Resumo da sessão"
    history_block = format_history_block(history)

    header_parts = [
        "Voce recebeu um COMANDO DE RESUMO DE SESSAO. Isso NAO e acao in-game.",
        "PROIBIDO: narrar cenas, descrever ambiente, menus numerados, perguntar o que Ryan faz.",
        "O historico do chat abaixo e a fonte principal dos eventos desta sessao.",
        "",
        "## Tarefa",
        f"Gere um resumo estruturado da sessao atual e proponha salvar em `{target_log}`.",
        "Use o template em logs/sessao_resumo_template.md e o tom do ultimo resumo em logs/ (se houver no contexto).",
        "Inclua a secao **Arquivos Atualizados Nesta Sessão** com paths concretos.",
        "Em **Decisões Importantes**: APENAS acoes que o jogador declarou explicitamente (linhas VOCE no historico).",
        "Se uma decisao nao foi tomada no historico, coloque em Pendências — nao invente.",
        "Use quebras de linha entre secoes (linha em branco antes de cada ##).",
        "Nunca diga que salvou o arquivo; apenas pergunte se o jogador confirma o salvamento.",
        "",
        "## Formato obrigatorio da resposta",
        f"1. Primeira linha: `{opener}`",
        "2. Titulo: `Resumo da Sessão — [tema curto] ([data])`",
        "3. Secoes com bullets: Eventos Principais; Mudanças de Estado (Relacionamentos, Reputação/Heat/Economia, Consequências);",
        "   Decisões Importantes do Jogador; Pendências / Ganchos; Arquivos que Precisam de Atualização (lista com paths).",
        f"4. Ultima linha: pergunta se deseja salvar como `{target_log}`.",
        "",
        "## Comando do jogador",
        user_message,
        "",
        "## Historico da conversa",
        history_block,
        "",
        "## Contexto de arquivos",
    ]
    header = "\n".join(header_parts)
    safety_margin = 64
    context_budget = max(max_prompt_chars - len(header) - safety_margin, 1200)
    context_blocks = _build_ollama_context_blocks(
        context_paths,
        context_budget,
        channel="gestor",
    )
    prompt = header
    if context_blocks:
        prompt = f"{header}\n\n" + "\n\n".join(context_blocks)
    if len(prompt) > max_prompt_chars:
        suffix = "\n\n[...prompt truncado...]\n"
        keep = max(max_prompt_chars - len(suffix), 0)
        prompt = prompt[:keep] + suffix
    return prompt


def _build_ollama_prompt(
    user_message: str,
    context_paths: list[Path],
    mode: str,
    *,
    max_prompt_chars: int,
    channel: str = "narracao",
    session_intent: str | None = None,
    history: list[dict] | None = None,
) -> str:
    if session_intent == "summary":
        return _build_session_summary_prompt(
            user_message,
            context_paths,
            max_prompt_chars=max_prompt_chars,
            history=history,
        )
    if channel == "sistema":
        history_block = format_history_block(history, max_chars=2000) if history else ""
        fichas_index = _build_fichas_index_block() if _sistema_needs_ficha_index(user_message) else ""
        header_parts = [
            "Voce e o assistente do canal SISTEMA (meta-tecnico).",
            "Responda APENAS o que o jogador pediu. Nao recite manuais nem listas genericas de boas praticas.",
            "",
            "## Regras",
            "- Portugues direto, 2-8 linhas. Bullets curtos so quando listar arquivos ou passos concretos.",
            "- Para fichas: use SOMENTE paths do Indice de fichas ou de sistema/registro_arquivos.md. Nao invente nem troque papeis (ex: Lena Valk = nomad, Alex = netrunner).",
            "- Arquivos em relacionamentos/ NAO sao fichas — sao mapas de relacao. Fichas mecanicas ficam em fichas/.",
            "- Se perguntarem caminho de ficha: path exato + arquivo de relacionamentos correspondente quando existir.",
            "- Se pedirem resumo de atualizacoes: liste arquivos ESPECIFICOS e O QUE revisar em cada um com base no contexto; nao repita templates de como_atualizar.",
            "- Perguntas sobre LLM/API: resposta curta e objetiva (sim/nao + detalhe tecnico).",
            "- Historia/cenas/canon de jogo: indique canal Mestre ou Narracao em 1 linha.",
            "- PROIBIDO: 'Vamos la', 'Ola', 'Como assistente', menus A/B/C, narrar cenas.",
            "",
            "## Exemplo (resumo da campanha / brief)",
            "Pergunta: Como funciona o resumo da campanha? Quais arquivos consulta?",
            "Resposta: O painel Resumo Ate Aqui vem de GET /api/brief (motor/brief_service.py). Fontes tipicas:",
            "- sistema/dashboard_contexto.md — situacao com o Pack",
            "- board/board_campanha.md — missao, pistas, NPCs",
            "- logs/sessao_resumo_XXX.md — ultima sessao salva",
            "Objetivos de curto prazo tambem usam event_queue.md e heat.md.",
            "",
            "## Exemplo (listar fichas)",
            "Pergunta: quais fichas voce tem na pasta fichas?",
            "Resposta: Liste do Indice de fichas abaixo, agrupando crew (fichas/*.md), npc/ e notas_narrador/.",
            "",
            "## Exemplo (netrunner)",
            "Pergunta: qual a ficha da netrunner?",
            "Resposta: fichas/netrunner - alex_specter_kane.md (Alex Specter Kane). Relacionamentos: relacionamentos/alex_specter_kane_relacionamentos.md. Lena Valk e nomad: fichas/nomad - lena_valk_kane.md.",
            "",
            "## Exemplo (caminho de ficha)",
            "Pergunta: a ficha da Lena Valk e fichas/nomad - lena_valk_kane.md?",
            "Resposta: Correto. Ficha principal: fichas/nomad - lena_valk_kane.md. Relacionamentos: relacionamentos/lena_valk_kane_relacionamentos.md.",
            "",
            "## Exemplo (preview de atualizacao)",
            "Pergunta: [resumo do que atualizar apos a sessao]",
            "Resposta:",
            "- board/board_campanha.md — revisar missao/local apos integracao dos recrutas.",
            "- relacionamentos/ryan_relacionamentos.md — registrar interacoes com Mara, Elias, Tomas.",
            "- sistema/dashboard_contexto.md — alinhar resumo rapido com o board.",
            "Nenhuma alteracao aplicada; aguardo sua confirmacao.",
            "",
            "## Pergunta do jogador",
            user_message,
        ]
        if history_block:
            header_parts.extend(
                [
                    "",
                    "## Historico do canal Sistema",
                    history_block,
                ]
            )
        if fichas_index:
            header_parts.extend(["", fichas_index])
        header_parts.extend(["", "## Contexto"])
    elif channel == "mestre":
        history_block = format_history_block(history, max_chars=2500) if history else ""
        header_parts = [
            "Voce e o MESTRE off-game (meta). O jogador conversa FORA da cronologia oficial.",
            "Papel: tirar duvidas de canon, separar estado atual de planos futuros, sugerir ajustes em arquivos.",
            "Voce NAO narra cenas. NAO interpreta acoes do Ryan. NAO descreve clima, ambiente ou escolhas in-game.",
            "Se a pergunta for sobre LLM, API ou funcionamento da interface, diga para usar o canal Sistema.",
            "",
            "## Formato obrigatorio",
            "- Tom de mesa de RPG (2-8 linhas). Listas em bullet quando listar pessoas.",
            "- Responda PRIMEIRO a pergunta literal do jogador (ex: 'ja virou traidor?' -> nao confirmado / gancho aberto).",
            "- Use rotulos curtos SOMENTE para duvidas de canon: Canon atual: / Plano futuro: / Sugestao de registro:",
            "- PROIBIDO: narrar cena, downtime jogavel, menus, opcoes numeradas, perguntas de volta.",
            "- PROIBIDO: desviar para polycule/harem ou romance futuro (Reina, Alex) se a pergunta for sobre NPCs do Pack em Badlands.",
            "- PROIBIDO: tratar Alex, Reina, Kaz, Doc e Jax como recrutas do Pack em Badlands (sao crew futura em Night City).",
            "",
            "## Exemplo (suspeita / traidor)",
            "Pergunta: Tomas parece nervoso — o NPC ja se tornou traidor?",
            "Resposta:",
            "Canon atual: nao. Tomas e recruta do Pack sob monitoramento; nervosismo/inquietacao registrados, sem prova de traição.",
            "Ryan desconfia mas o Vesper nao achou transmissao ativa; gancho aberto (infiltrado, trauma ou falso positivo).",
            "Sugestao de registro: manter tensao sem confirmar vilao ate jogada do jogador; atualizar ficha se houver incidente.",
            "",
            "## Exemplo (timeline)",
            "Pergunta: Reina, Alex, Jax e Kaz ja estao na crew agora?",
            "Resposta:",
            "Canon atual: no Pack em Badlands, em campo estao Ryan e Valk; recrutas do Pack sao Mara, Elias e Tomas.",
            "Plano futuro: Alex, Reina, Kaz, Doc e Jax entram na crew quando Ryan voltar a Night City.",
            "",
            "## Exemplo (consulta NPC)",
            "Pergunta: Quem sao Reina, Alex, Jax e Kaz?",
            "Resposta:",
            "- Reina \"Bearclaw\": solo, futura crew; confidente emocional; Ryan nao lembra do passado com ela.",
            "- Alex \"Specter\" Kane: netrunner, futura crew; rivalidade velada com Ryan.",
            "- Jax \"Razor\" Kane: solo, futura crew; respeito profissional, pouca interacao.",
            "- Kaz \"The Broker\": fixer, futura crew; trouxe jobs e monta a equipe em NC.",
            "",
            "## Pergunta do jogador",
            user_message,
        ]
        if history_block:
            header_parts.extend(
                [
                    "",
                    "## Historico do canal Mestre (contexto off-game)",
                    history_block,
                ]
            )
        header_parts.extend(["", "## Contexto"])
    else:
        history_block = format_history_block(history, max_chars=3500) if history else ""
        player_block = format_player_message_for_prompt(parse_player_message(user_message))
        header_parts = [
            "Voce e o narrador de uma campanha Cyberpunk RED solo.",
            "",
            "## Regras",
            "- Use apenas fatos presentes no contexto e no historico abaixo. Nao invente NPCs, locais ou consequencias.",
            "- O HISTORICO DA CONVERSA define a cena ATUAL (local, quem esta presente, o que ja aconteceu).",
            "- Convencao do jogador: prosa = acao; _ ou [Fala] ou \"aspas\" = fala; *asteriscos* = beat/gesto.",
            "- Acoes e falas listadas abaixo JA ocorreram. Narre somente consequencias NOVAS.",
            "- PROIBIDO controlar o protagonista: nao escreva 'Voce continua/se aproxima/pergunta/nota/entra/vai/olha/cumprimenta'.",
            "- PROIBIDO ecoar a entrada do jogador ('Voce sai da tenda...' quando ele ja disse isso). Reaja com mundo/NPCs.",
            "- Descreva ambiente, NPCs e consequencias sensoriais; deixe a proxima acao para o jogador.",
            "- PROIBIDO perguntar 'O que voce faz em seguida?' ou 'Agora, o que voce faz?'.",
            "- Quando um NPC falar, use [NPC-M: Nome] ou [NPC-F: Nome] seguido da fala (ex: [NPC-M: Tio Gringo] \"Ola, Ryan.\").",
            "- Acao fisica de NPC (sem fala) pode usar [NPC-M: Nome] descricao curta da acao.",
            "- Nao repita paragrafos da sua ultima resposta no historico (ex: nao re-descrever Elias na destilaria se ja foi dito).",
            "- Nao cite caminhos de arquivos, JSON, blocos UPDATE_PROPOSALS nem meta-comentarios sobre o prompt.",
            "- Nao descreva alteracoes em arquivos da campanha; apenas narre ou responda.",
            "- Responda somente com o texto final para o jogador, sem rascunhos nem auto-correcoes.",
            f"- {_ollama_channel_hint(channel)}",
            f"- {_ollama_mode_hint(mode)}",
        ]
        if history_block:
            header_parts.extend(
                [
                    "",
                    "## Historico da conversa (cena atual — manter continuidade)",
                    history_block,
                    "",
                    "## Ultima resposta do Narrador (NAO repetir — avance a cena)",
                    _last_narrator_text(history) or "(primeira resposta da cena)",
                ]
            )
        header_parts.extend(
            [
                "",
                "## Entrada do jogador AGORA (parseada)",
                player_block,
                "",
                "## Contexto de arquivos (estado canonico)",
            ]
        )
    header = "\n".join(header_parts)
    safety_margin = 64
    context_budget = max(max_prompt_chars - len(header) - safety_margin, 1200)
    context_blocks = _build_ollama_context_blocks(context_paths, context_budget, channel=channel)

    prompt = header
    if context_blocks:
        prompt = f"{header}\n\n" + "\n\n".join(context_blocks)

    if len(prompt) > max_prompt_chars:
        suffix = "\n\n[...prompt truncado para caber no limite do Ollama...]\n"
        keep = max(max_prompt_chars - len(suffix), 0)
        prompt = prompt[:keep] + suffix

    return prompt


def build_prompt(
    user_message: str,
    context_paths: list[Path],
    mode: str,
    *,
    provider: str | None = None,
    max_prompt_chars: int | None = None,
    channel: str = "narracao",
    session_intent: str | None = None,
    history: list[dict] | None = None,
) -> str:
    if provider == "ollama":
        return _build_ollama_prompt(
            user_message,
            context_paths,
            mode,
            max_prompt_chars=max_prompt_chars or DEFAULT_OLLAMA_MAX_PROMPT_CHARS,
            channel=channel,
            session_intent=session_intent,
            history=history,
        )

    if channel == "mestre" or mode == "mestre":
        mode_hint = (
            "Modo MESTRE off-game: responda como GM de mesa. "
            "Separe canon atual de planos futuros. Nao narre cenas."
        )
    elif mode == "narrador":
        mode_hint = (
            "Modo NARRADOR: foque em proposta de cena e perguntas ao jogador sem controlar o protagonista."
        )
    else:
        mode_hint = (
            "Modo GESTOR: foque em consistencia de estado, arquivos a atualizar e rastreabilidade."
        )

    context_blocks: list[str] = []
    for p in context_paths:
        rel = p.relative_to(REPO_ROOT).as_posix()
        context_blocks.append(f"### Arquivo: {rel}\n\n{compact_content(p)}")

    return "\n\n".join(
        [
            "# Sistema de Narracao Solo - Prompt Orquestrado",
            "",
            "## Regras obrigatorias",
            "- Se nao estiver registrado nos arquivos, nao trate como fato canonico.",
            "- Cite quais arquivos sustentam cada decisao importante.",
            "- Se detectar lacuna de estado, proponha pergunta objetiva antes de assumir qualquer detalhe.",
            "",
            f"## Perfil de operacao\n{mode_hint}",
            "",
            f"## Pergunta do usuario\n{user_message}",
            "",
            "## Contexto carregado",
            *context_blocks,
        ]
    )


def run_grok(prompt: str) -> str:
    if not GROK_BIN.exists():
        raise FileNotFoundError(f"grok nao encontrado: {GROK_BIN}")

    proc = subprocess.run(
        [
            str(GROK_BIN),
            "-p",
            prompt,
            "--cwd",
            str(REPO_ROOT),
            "--output-format",
            "plain",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "erro desconhecido")[-2000:]
        raise RuntimeError(f"grok falhou: {err}")
    return proc.stdout.strip()


def append_session_log(session_file: Path, turn: ChatTurn) -> None:
    with session_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(turn.__dict__, ensure_ascii=False) + "\n")


def get_session_file(session_name: str | None = None) -> Path:
    if session_name:
        return SESSIONS_DIR / f"{session_name}.jsonl"
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return SESSIONS_DIR / f"session-{ts}.jsonl"


def cmd_check() -> int:
    missing = check_integrity()
    if missing:
        print("Integridade: FALHA")
        for rel in missing:
            print(f"- Ausente: {rel}")
        return 2
    print("Integridade: OK")
    return 0


def cmd_chat(message: str, provider: str, mode: str, print_prompt: bool) -> int:
    missing = check_integrity()
    if missing:
        print("Nao foi possivel responder: faltam arquivos obrigatorios.")
        for rel in missing:
            print(f"- {rel}")
        return 2

    ensure_dirs()
    session_file = get_session_file()

    context_paths = select_context_files(message)
    prompt = build_prompt(message, context_paths, mode)

    if print_prompt or provider == "none":
        print("===== PROMPT ORQUESTRADO =====")
        print(prompt)
        print("===== FIM PROMPT =====")

    append_session_log(session_file, ChatTurn(utc_now(), "user", message))

    if provider == "none":
        answer = (
            "Provider desativado (none). Use o prompt acima em qualquer LLM e registre a resposta."
        )
    else:
        answer = run_grok(prompt)

    append_session_log(session_file, ChatTurn(utc_now(), "assistant", answer))

    print(answer)
    print(f"\n[session-log] {session_file.relative_to(REPO_ROOT).as_posix()}")
    return 0


def cmd_repl(provider: str, mode: str, print_prompt: bool) -> int:
    missing = check_integrity()
    if missing:
        print("Nao foi possivel iniciar REPL: faltam arquivos obrigatorios.")
        for rel in missing:
            print(f"- {rel}")
        return 2

    ensure_dirs()
    session_file = get_session_file()
    print("REPL iniciado. Digite 'sair' para encerrar.")

    while True:
        try:
            message = input("\nvoce> ").strip()
        except KeyboardInterrupt:
            print("\nEncerrado.")
            return 130

        if not message:
            continue
        if message.lower() in {"sair", "exit", "quit"}:
            print("Encerrando REPL.")
            return 0

        append_session_log(session_file, ChatTurn(utc_now(), "user", message))
        context_paths = select_context_files(message)
        prompt = build_prompt(message, context_paths, mode)

        if print_prompt:
            print("\n===== PROMPT ORQUESTRADO =====")
            print(prompt)
            print("===== FIM PROMPT =====")

        if provider == "none":
            answer = "Provider none: resposta automatica desativada para este turno."
        else:
            try:
                answer = run_grok(prompt)
            except Exception as exc:  # pragma: no cover - depende de ambiente externo
                answer = f"ERRO ao consultar provider: {exc}"

        append_session_log(session_file, ChatTurn(utc_now(), "assistant", answer))
        print(f"\nengine> {answer}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Motor de narracao solo com contexto inteligente")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Valida integridade minima de arquivos")

    chat = sub.add_parser("chat", help="Executa um turno unico")
    chat.add_argument("--message", required=True, help="Mensagem do usuario")
    chat.add_argument("--provider", choices=["grok", "none"], default="grok")
    chat.add_argument("--mode", choices=["gestor", "narrador"], default="gestor")
    chat.add_argument("--print-prompt", action="store_true")

    repl = sub.add_parser("repl", help="Chat interativo")
    repl.add_argument("--provider", choices=["grok", "none"], default="grok")
    repl.add_argument("--mode", choices=["gestor", "narrador"], default="gestor")
    repl.add_argument("--print-prompt", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.cmd == "check":
        return cmd_check()
    if args.cmd == "chat":
        return cmd_chat(args.message, args.provider, args.mode, args.print_prompt)
    if args.cmd == "repl":
        return cmd_repl(args.provider, args.mode, args.print_prompt)

    print(f"Comando invalido: {args.cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
