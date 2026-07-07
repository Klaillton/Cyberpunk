from __future__ import annotations

from motor.update.parser import UpdateParser

SAMPLE = """A cena termina com o pack em alerta.

---UPDATE_PROPOSALS---
```json
[
  {
    "target_path": "campanha/estado/heat.md",
    "target_section": "Heat por Personagem",
    "change_type": "insert_row",
    "payload": {
      "personagem": "Ryan",
      "nivel": "Alta",
      "justificativa": "Operacao exposta a crew"
    },
    "rationale": "Operacao expôs a crew",
    "confidence": 0.85
  }
]
```
"""


def test_update_parser_extracts_proposals_block() -> None:
    parser = UpdateParser()
    narrative, proposals = parser.parse(SAMPLE)

    assert "alerta" in narrative
    assert "UPDATE_PROPOSALS" not in narrative
    assert len(proposals) == 1
    assert proposals[0].target_path.endswith("heat.md")
    assert proposals[0].change_type == "insert_row"
    assert proposals[0].confidence == 0.85