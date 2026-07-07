from __future__ import annotations

import json
import re

from motor.update.models import UpdateProposal

_MARKER = "---UPDATE_PROPOSALS---"
_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", re.IGNORECASE)
_ARRAY_RE = re.compile(r"(\[[\s\S]*\])")


class UpdateParser:
    def split_narrative(self, narrative: str) -> tuple[str, str | None]:
        if _MARKER not in narrative:
            return narrative.strip(), None
        narrative_part, proposals_part = narrative.split(_MARKER, 1)
        return narrative_part.strip(), proposals_part.strip()

    def parse(self, narrative: str) -> tuple[str, list[UpdateProposal]]:
        clean_narrative, block = self.split_narrative(narrative)
        if not block:
            return clean_narrative, []

        raw_json = self._extract_json(block)
        if not raw_json:
            return clean_narrative, []

        try:
            items = json.loads(raw_json)
        except json.JSONDecodeError:
            return clean_narrative, []

        if not isinstance(items, list):
            return clean_narrative, []

        proposals: list[UpdateProposal] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if "target_path" not in item or "change_type" not in item:
                continue
            proposals.append(UpdateProposal.from_dict(item))
        return clean_narrative, proposals

    def _extract_json(self, block: str) -> str | None:
        fenced = _JSON_BLOCK_RE.search(block)
        if fenced:
            return fenced.group(1).strip()
        array = _ARRAY_RE.search(block)
        if array:
            return array.group(1).strip()
        return None