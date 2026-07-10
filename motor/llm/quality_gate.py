from __future__ import annotations

import re
import unicodedata

from motor.llm.types import ContextManifest, QualityCheck, QualityReport

_PROTAGONIST_CONTROL_RE = re.compile(
    r"\b(voce|você)\s+("
    r"decide|ataca|corre|dispara|mata|entra|sai|continua|aproxima|pergunta|nota|"
    r"vê|ve|olha|começa|comeca|reconhece|levanta|volta|retorna|investiga|procura|"
    r"vai|sabe|diz|responde|observa|escuta|sente|tenta|chama|grita|sussurra|cumprimenta"
    r")\b",
    re.IGNORECASE,
)
_NAME_RE = re.compile(r"\b([A-Z][a-záàâãéêíóôõúç]{2,})(?:\s+[A-Z][a-záàâãéêíóôõúç]{2,})?\b")
_BOARD_NAME_RE = re.compile(r"\*\*([^*]+)\*\*")
_LOCATION_CONFLICTS = (
    ("night city", "badlands"),
    ("night city", "acampamento"),
    ("corporate plaza", "deserto"),
)
_META_QUESTION_RE = re.compile(
    r"(?:"
    r"o que (?:voce|você) (?:faz|fara|fará|faz em seguida|deseja fazer)|"
    r"agora,?\s*o que (?:voce|você)|"
    r"qual (?:e|é) a sua (?:prioridade|proxima acao)|"
    r"o que acontece em seguida"
    r")",
    re.IGNORECASE,
)
_STOP_WORDS = frozenset(
    {
        "a",
        "ao",
        "aos",
        "as",
        "com",
        "da",
        "de",
        "do",
        "dos",
        "e",
        "em",
        "eu",
        "ja",
        "mais",
        "na",
        "no",
        "nos",
        "o",
        "os",
        "para",
        "por",
        "que",
        "se",
        "sobre",
        "um",
        "uma",
        "voce",
        "você",
        "the",
    }
)


def _normalize_text(text: str) -> str:
    lowered = unicodedata.normalize("NFKD", text.lower())
    stripped = "".join(ch for ch in lowered if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9\s]", " ", stripped)


def _content_words(text: str) -> set[str]:
    return {
        word
        for word in _normalize_text(text).split()
        if len(word) >= 3 and word not in _STOP_WORDS
    }


def _word_overlap_ratio(left: str, right: str) -> float:
    left_words = _content_words(left)
    right_words = _content_words(right)
    if not left_words or not right_words:
        return 0.0
    shared = left_words & right_words
    return len(shared) / min(len(left_words), len(right_words))


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


class ResponseQualityGate:
    def validate(
        self,
        reply: str,
        manifest: ContextManifest,
        channel: str,
        *,
        player_message: str = "",
        previous_narrator: str = "",
    ) -> QualityReport:
        checks: list[QualityCheck] = []
        known_tokens = self._known_tokens(manifest)

        checks.append(self._check_minimum_length(reply, channel))
        checks.append(self._check_protagonist_control(reply))
        checks.append(self._check_meta_questions(reply, channel))
        checks.append(self._check_duplicate_prefix(reply, channel))
        checks.append(self._check_player_echo(reply, player_message, channel))
        checks.append(self._check_narrator_repeat(reply, previous_narrator, channel))
        checks.append(self._check_invented_npc(reply, known_tokens))
        checks.append(self._check_board_consistency(reply, manifest))

        passed = all(check.passed for check in checks)
        return QualityReport(passed=passed, checks=checks)

    def _known_tokens(self, manifest: ContextManifest) -> set[str]:
        tokens: set[str] = set()
        for entity_id in manifest.entity_ids:
            tokens.add(entity_id.lower())
            for part in entity_id.split("_"):
                if len(part) >= 3:
                    tokens.add(part.lower())
        for path in manifest.source_paths:
            stem = path.split("/")[-1].replace(".md", "").lower()
            tokens.add(stem)
            if " - " in stem:
                slug = stem.split(" - ", 1)[1].strip()
                tokens.add(slug)
                for part in slug.replace("_recruit", "").split("_"):
                    if len(part) >= 3:
                        tokens.add(part)
            if "/npc/" in path.replace("\\", "/"):
                npc_slug = stem.replace("_recruit", "")
                tokens.add(npc_slug)
                for part in npc_slug.split("_"):
                    if len(part) >= 3:
                        tokens.add(part)
        for match in _BOARD_NAME_RE.finditer(manifest.board_excerpt):
            label = match.group(1).strip()
            for part in re.split(r"[\s\"']+", label):
                cleaned = part.strip(".,;:")
                if len(cleaned) >= 3:
                    tokens.add(cleaned.lower())
        allow = {
            "ryan",
            "wireghost",
            "voss",
            "valk",
            "lena",
            "kane",
            "night",
            "city",
            "badlands",
            "pack",
            "the",
            "mule",
            "cyberpunk",
            "rede",
            "fixer",
            "nomad",
            "techie",
            "doc",
            "crew",
            "elias",
            "tomas",
            "mara",
            "reyes",
            "gringo",
            "sasha",
            "lira",
            "lina",
        }
        tokens.update(allow)
        return tokens

    def _check_minimum_length(self, reply: str, channel: str) -> QualityCheck:
        if channel == "narrador":
            return QualityCheck(name="minimum_length", passed=True, detail="Canal narrador isento")
        passed = len(reply.strip()) >= 50
        return QualityCheck(
            name="minimum_length",
            passed=passed,
            detail="Resposta curta demais" if not passed else "Comprimento adequado",
        )

    def _check_protagonist_control(self, reply: str) -> QualityCheck:
        match = _PROTAGONIST_CONTROL_RE.search(reply)
        passed = match is None
        return QualityCheck(
            name="protagonist_control",
            passed=passed,
            detail="Narrador controlou acao do protagonista" if not passed else "Sem controle do protagonista",
        )

    def _check_meta_questions(self, reply: str, channel: str) -> QualityCheck:
        if channel != "narracao":
            return QualityCheck(name="meta_questions", passed=True, detail="Canal isento")
        passed = _META_QUESTION_RE.search(reply) is None
        return QualityCheck(
            name="meta_questions",
            passed=passed,
            detail="Pergunta meta ao jogador (o que voce faz)" if not passed else "Sem pergunta meta",
        )

    def _check_duplicate_prefix(self, reply: str, channel: str) -> QualityCheck:
        if channel != "narracao":
            return QualityCheck(name="duplicate_prefix", passed=True, detail="Canal isento")
        count = len(re.findall(r"\bNARRADOR\s*:", reply, flags=re.IGNORECASE))
        passed = count <= 1
        return QualityCheck(
            name="duplicate_prefix",
            passed=passed,
            detail="Prefixo NARRADOR duplicado" if not passed else "Prefixo limpo",
        )

    def _check_player_echo(self, reply: str, player_message: str, channel: str) -> QualityCheck:
        if channel != "narracao" or not player_message.strip():
            return QualityCheck(name="player_echo", passed=True, detail="Sem mensagem do jogador")
        opening = " ".join(_sentences(reply)[:2])
        overlap = _word_overlap_ratio(player_message, opening or reply[:240])
        passed = overlap < 0.42
        return QualityCheck(
            name="player_echo",
            passed=passed,
            detail=f"Eco da acao do jogador (overlap {overlap:.0%})" if not passed else "Sem eco do jogador",
        )

    def _check_narrator_repeat(self, reply: str, previous_narrator: str, channel: str) -> QualityCheck:
        if channel != "narracao" or not previous_narrator.strip():
            return QualityCheck(name="narrator_repeat", passed=True, detail="Sem resposta anterior")
        prev_norm = _normalize_text(previous_narrator)
        repeated: list[str] = []
        for sentence in _sentences(reply):
            norm = _normalize_text(sentence)
            if len(norm) < 24:
                continue
            if norm in prev_norm or norm[:50] in prev_norm:
                repeated.append(sentence[:60])
                continue
            for prev_sentence in _sentences(previous_narrator):
                if _word_overlap_ratio(sentence, prev_sentence) >= 0.68:
                    repeated.append(sentence[:60])
                    break
        passed = len(repeated) == 0
        detail = "Repetiu trechos da resposta anterior"
        if repeated:
            detail = f"{detail}: {repeated[0]}..."
        return QualityCheck(name="narrator_repeat", passed=passed, detail=detail)

    def _check_invented_npc(self, reply: str, known_tokens: set[str]) -> QualityCheck:
        unknown: list[str] = []
        for match in _NAME_RE.finditer(reply):
            full = match.group(0)
            parts = [part.lower() for part in full.split()]
            if all(part in known_tokens for part in parts):
                continue
            compact = "".join(parts)
            if compact in known_tokens:
                continue
            if full not in unknown:
                unknown.append(full)

        passed = len(unknown) == 0
        detail = f"NPCs desconhecidos: {', '.join(unknown)}" if unknown else "NPCs consistentes com manifest"
        return QualityCheck(name="known_entities", passed=passed, detail=detail)

    def _check_board_consistency(self, reply: str, manifest: ContextManifest) -> QualityCheck:
        board = manifest.board_excerpt.lower()
        reply_lower = reply.lower()
        if not board:
            return QualityCheck(name="board_consistency", passed=True, detail="Sem board no manifest")

        for reply_term, board_term in _LOCATION_CONFLICTS:
            if reply_term in reply_lower and board_term in board:
                return QualityCheck(
                    name="board_consistency",
                    passed=False,
                    detail=f"Local '{reply_term}' contradiz board ({board_term})",
                )
        return QualityCheck(name="board_consistency", passed=True, detail="Consistente com board")