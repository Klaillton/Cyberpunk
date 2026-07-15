from __future__ import annotations

import re

_DELEGATION_VERB_RE = re.compile(
    r"\b("
    r"planej\w*|"
    r"organiz\w*(?:\s+(?:a|o|para|isso|a\s+cac\w*))?|"
    r"monta\s+o\s+plano|faz\s+o\s+plano|define\s+a\s+rota|estrutur\w*"
    r")\b",
    re.IGNORECASE,
)
_DELEGATION_TARGET_RE = re.compile(
    r"\b(valk|lena|elias|reyes|mara|tomas|tio\s*gringo|gringo|rusty|jax)\b",
    re.IGNORECASE,
)
_PASSIVE_OBSERVATION_RE = re.compile(
    r"(?:"
    r"\*[^*]*(?:observ|esper|silenc)[^*]*\*|"
    r"\b(?:observ\w*|espero|aguardo)\b.*\b(?:silenc|quieto|parado)|"
    r"\[ag[eê]ncia\s*npc\]|"
    r"deix(?:em|a)\s+(?:eles|elas|os|as)\s+decid"
    r")",
    re.IGNORECASE,
)
_EXPLICIT_AGENCY_RE = re.compile(
    r"\b(?:agencia\s*npc|npcs?\s+(?:falam|decid|resolvem)|entre\s+si)\b",
    re.IGNORECASE,
)
_PLANNING_PING_PONG_RE = re.compile(
    r"(?:"
    r"como\s+(?:voce|você)\s+(?:prefere|quer)\s+planej|"
    r"qual\s+rota\s+(?:voce|você)\s+prefere|"
    r"detalhe\s+o\s+planejamento|"
    r"(?:voce|você)\s+prefere\s+(?:a|b|c|op[cç][aã]o)|"
    r"como\s+(?:voce|você)\s+quer\s+(?:planej|organiz)|"
    r"o\s+que\s+(?:voce|você)\s+prefere\s+(?:fazer|escolher)"
    r")",
    re.IGNORECASE,
)
_PLAN_DELIVERY_RE = re.compile(
    r"\b("
    r"\d{1,2}h\d{0,2}|"
    r"rota|hor[aá]rio|equipamento|per[ií]metro|"
    r"amanh[aã]|sa[ií]da|volta|mule|c[aâ]nion|overwatch|r[aá]dio"
    r")\b",
    re.IGNORECASE,
)

_NPC_PULSO_PATHS: dict[str, list[str]] = {
    "valk": [
        "fichas/nomad - lena_valk_kane.md",
        "pulso_do_mundo/crew/valk.md",
    ],
    "lena": [
        "fichas/nomad - lena_valk_kane.md",
        "pulso_do_mundo/crew/valk.md",
    ],
    "elias": [
        "fichas/npc/elias_recruit.md",
        "pulso_do_mundo/pack_badlands/recrutas.md",
    ],
    "reyes": [
        "fichas/npc/reyes.md",
        "pulso_do_mundo/pack_badlands/reyes.md",
    ],
    "mara": [
        "fichas/npc/mara_recruit.md",
        "pulso_do_mundo/pack_badlands/recrutas.md",
    ],
    "tomas": [
        "fichas/npc/tomas_recruit.md",
        "pulso_do_mundo/pack_badlands/recrutas.md",
    ],
    "gringo": [
        "fichas/npc/tio_gringo.md",
        "pulso_do_mundo/pack_badlands/tio_gringo.md",
    ],
    "rusty": ["board/board_campanha.md"],
    "jax": ["pulso_do_mundo/crew/jax.md"],
}


def delegation_target_npc(message: str) -> str | None:
    match = _DELEGATION_TARGET_RE.search(message)
    if not match:
        return None
    name = match.group(1).lower().replace(" ", "")
    if name in {"tiogringo", "tio"}:
        return "gringo"
    return name


def is_delegation_turn(message: str) -> bool:
    text = message.strip()
    if not text:
        return False
    if not _DELEGATION_VERB_RE.search(text):
        return False
    return _DELEGATION_TARGET_RE.search(text) is not None


def is_passive_observation_turn(message: str) -> bool:
    return bool(_PASSIVE_OBSERVATION_RE.search(message.strip()))


def is_npc_agency_turn(message: str) -> bool:
    text = message.strip()
    if not text:
        return False
    return (
        is_delegation_turn(text)
        or is_passive_observation_turn(text)
        or bool(_EXPLICIT_AGENCY_RE.search(text))
    )


def agency_context_paths(message: str) -> list[str]:
    paths = ["sistema/npc_agencia_cena.md"]
    target = delegation_target_npc(message)
    if target and target in _NPC_PULSO_PATHS:
        paths.extend(_NPC_PULSO_PATHS[target])
    elif is_passive_observation_turn(message):
        if re.search(r"\belias\b", message, re.IGNORECASE):
            paths.extend(_NPC_PULSO_PATHS["elias"])
        if re.search(r"\b(?:tio\s*gringo|gringo)\b", message, re.IGNORECASE):
            paths.extend(_NPC_PULSO_PATHS["gringo"])
        if re.search(r"\bvalk\b", message, re.IGNORECASE):
            paths.extend(_NPC_PULSO_PATHS["valk"])
    elif re.search(r"\bvalk\b", message, re.IGNORECASE):
        paths.extend(_NPC_PULSO_PATHS["valk"])
    return list(dict.fromkeys(paths))


def count_delegation_turns_in_history(history: list[dict] | None) -> int:
    if not history:
        return 0
    count = 0
    for entry in history:
        if str(entry.get("role", "")).lower() != "user":
            continue
        if is_delegation_turn(str(entry.get("content", ""))):
            count += 1
    return count


def build_agency_prompt_block(message: str, history: list[dict] | None) -> str:
    if not is_npc_agency_turn(message):
        return ""

    lines = [
        "## Agencia NPC (obrigatorio neste turno)",
        "- NPCs podem falar entre si com tags [NPC-M:] / [NPC-F:] em linhas separadas.",
        "- Nao invente NPCs fora do contexto/board/fichas.",
        "- Nao controle Ryan; termine com gancho para ele reagir (sem 'o que voce faz').",
    ]

    if is_delegation_turn(message):
        target = delegation_target_npc(message) or "NPC nomeado"
        prior = count_delegation_turns_in_history(history)
        lines.extend(
            [
                f"- DELEGACAO: Ryan pediu a {target} planejar/organizar — o NPC ENTREGA plano concreto.",
                "- Plano deve incluir: horario, rota ou area, equipamento, quem fica onde (quando couber).",
                "- PROIBIDO devolver planejamento ao jogador ('qual rota prefere', A/B/C, 'como voce quer planejar').",
            ]
        )
        if prior >= 1:
            lines.append(
                f"- ANTI-LOOP: delegacao ja pedida {prior + 1}x nesta sessao — ENTREGUE o plano agora, sem repetir menu."
            )
    elif is_passive_observation_turn(message):
        lines.extend(
            [
                "- Jogador observa em silencio: permita 1-2 trocas curtas NPC↔NPC visiveis para Ryan.",
                "- Narre so o que Ryan percebe; nao monologo interno.",
            ]
        )

    return "\n".join(lines)


def reply_passes_delegation_check(reply: str, player_message: str) -> bool:
    if not is_delegation_turn(player_message):
        return True
    if _PLANNING_PING_PONG_RE.search(reply):
        return False
    return _PLAN_DELIVERY_RE.search(reply) is not None