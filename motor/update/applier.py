from __future__ import annotations

import re
from pathlib import Path

from motor.settings import Settings, get_settings
from motor.update.models import ApplyReport, UpdateProposal
from motor.update.paths import normalize_target_path, resolve_target_file

_SECTION_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$", re.MULTILINE)


class UpdateApplier:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def apply(self, proposals: list[UpdateProposal]) -> ApplyReport:
        files_changed: set[str] = set()
        errors: list[str] = []
        applied = 0

        for proposal in proposals:
            try:
                rel = self._apply_one(proposal)
                if rel:
                    files_changed.add(rel)
                    applied += 1
            except Exception as exc:  # pragma: no cover - surfaced in report
                errors.append(f"{proposal.id}: {exc}")

        sync_report = {"sqlite": 0, "faiss_chunks_added": 0}
        if files_changed:
            try:
                from motor.index.faiss_index import FaissIndex
                from motor.markdown.sync_engine import SyncEngine

                engine = SyncEngine(self.settings)
                for rel in sorted(files_changed):
                    path = self.settings.campanha_root / rel
                    if path.exists():
                        report = engine.sync_file(path, rel_path=rel)
                        sync_report["sqlite"] += report.documents_synced
                sync_report["faiss_chunks_added"] = FaissIndex(self.settings).rebuild()
            except Exception as exc:  # pragma: no cover
                errors.append(f"sync: {exc}")

        return ApplyReport(
            applied=applied,
            files_changed=sorted(files_changed),
            sync_report=sync_report,
            errors=errors,
        )

    def _apply_one(self, proposal: UpdateProposal) -> str | None:
        target = resolve_target_file(proposal.target_path, self.settings.campanha_root)
        if target is None:
            raise FileNotFoundError(proposal.target_path)

        content = target.read_text(encoding="utf-8")
        rel = normalize_target_path(proposal.target_path)

        if proposal.change_type == "append":
            addition = str(proposal.payload.get("text") or proposal.payload.get("content") or "").strip()
            if not addition:
                raise ValueError("payload.text obrigatorio para append")
            updated = content.rstrip() + "\n\n" + addition + "\n"
        elif proposal.change_type == "replace":
            updated = self._replace_section(content, proposal.target_section, proposal.payload)
        elif proposal.change_type == "insert_row":
            updated = self._insert_row(content, proposal.target_section, proposal.payload)
        elif proposal.change_type == "upsert_field":
            updated = self._upsert_field(content, proposal.target_section, proposal.payload)
        else:
            raise ValueError(f"change_type nao suportado: {proposal.change_type}")

        target.write_text(updated, encoding="utf-8")
        return rel

    def _replace_section(self, content: str, section: str | None, payload: dict) -> str:
        if not section:
            raise ValueError("target_section obrigatorio para replace")
        replacement = str(payload.get("text") or payload.get("content") or "").strip()
        if not replacement:
            raise ValueError("payload.text obrigatorio para replace")

        pattern = re.compile(
            rf"(^##+\s+{re.escape(section)}\s*$)([\s\S]*?)(?=^##+\s|\Z)",
            re.MULTILINE | re.IGNORECASE,
        )
        match = pattern.search(content)
        if not match:
            raise ValueError(f"Secao nao encontrada: {section}")
        heading = match.group(1)
        return pattern.sub(f"{heading}\n\n{replacement}\n", content, count=1)

    def _insert_row(self, content: str, section: str | None, payload: dict) -> str:
        personagem = str(payload.get("personagem") or payload.get("name") or "Desconhecido").strip()
        nivel = str(payload.get("nivel") or payload.get("level") or "-").strip()
        justificativa = str(payload.get("justificativa") or payload.get("reason") or "").strip()
        row = f"| **{personagem}** | {nivel} | {justificativa} |"

        section_pattern = None
        if section:
            section_pattern = re.compile(
                rf"(^##+\s+{re.escape(section)}\s*$)([\s\S]*?)(?=^##+\s|\Z)",
                re.MULTILINE | re.IGNORECASE,
            )
        else:
            section_pattern = re.compile(
                r"(^##+\s+.*Heat.*$)([\s\S]*?)(?=^##+\s|\Z)",
                re.MULTILINE | re.IGNORECASE,
            )

        match = section_pattern.search(content)
        if not match:
            raise ValueError("Secao de tabela nao encontrada")

        block = match.group(0)
        lines = block.splitlines()
        last_table_idx = -1
        for idx, line in enumerate(lines):
            if line.strip().startswith("|"):
                last_table_idx = idx

        if last_table_idx < 0:
            raise ValueError("Tabela nao encontrada na secao")

        insert_at = last_table_idx + 1
        new_lines = lines[:insert_at] + [row, ""] + lines[insert_at:]
        new_block = "\n".join(new_lines)
        if not new_block.endswith("\n"):
            new_block += "\n"
        return content.replace(block, new_block, 1)

    def _upsert_field(self, content: str, section: str | None, payload: dict) -> str:
        attribute = str(payload.get("attribute") or payload.get("field") or "").strip()
        value = str(payload.get("value") or "").strip()
        target_name = str(payload.get("target") or payload.get("personagem") or "").strip()
        if not attribute or not value:
            raise ValueError("payload.attribute e payload.value obrigatorios")

        note = (
            f"\n> Atualizacao assistida ({attribute}"
            f"{f' / {target_name}' if target_name else ''}): {value}"
        )
        if section:
            pattern = re.compile(
                rf"(^##+\s+{re.escape(section)}\s*$)",
                re.MULTILINE | re.IGNORECASE,
            )
            match = pattern.search(content)
            if match:
                insert_at = match.end()
                return content[:insert_at] + note + content[insert_at:]
        return content.rstrip() + note + "\n"