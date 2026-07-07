from __future__ import annotations

import re

from motor.llm.types import ContextManifest, QualityCheck, QualityReport

_PROTagonist_CONTROL_RE = re.compile(
    r"\b(voce|você)\s+(decide|ataca|corre|dispara|mata|entra|sai)\b",
    re.IGNORECASE,
)
_NAME_RE = re.compile(r"\b([A-Z][a-záàâãéêíóôõúç]{2,})(?:\s+[A-Z][a-záàâãéêíóôõúç]{2,})?\b")
_LOCATION_CONFLICTS = (
    ("night city", "badlands"),
    ("night city", "acampamento"),
    ("corporate plaza", "deserto"),
)


class ResponseQualityGate:
    def validate(
        self,
        reply: str,
        manifest: ContextManifest,
        channel: str,
    ) -> QualityReport:
        checks: list[QualityCheck] = []
        known_tokens = self._known_tokens(manifest)

        checks.append(self._check_minimum_length(reply, channel))
        checks.append(self._check_protagonist_control(reply))
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
                tokens.add(stem.split(" - ", 1)[1].strip())
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
        match = _PROTagonist_CONTROL_RE.search(reply)
        passed = match is None
        return QualityCheck(
            name="protagonist_control",
            passed=passed,
            detail="Narrador controlou acao do protagonista" if not passed else "Sem controle do protagonista",
        )

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