#!/usr/bin/env python3
"""
Servidor local para front-end de narracao solo + API de chat.

Uso:
  python scripts/narracao_api.py

Abre:
  http://127.0.0.1:8787/

Endpoints:
  POST /api/narracao  -> canal principal
  POST /api/narrador  -> canal privado (off-record)
"""

from __future__ import annotations

import json
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import narracao_engine as engine

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = REPO_ROOT / "frontend"
HOST = os.environ.get("NARRACAO_API_HOST", "127.0.0.1")
PORT = int(os.environ.get("NARRACAO_API_PORT", "8787"))
PROVIDER = os.environ.get("NARRACAO_PROVIDER", "none").strip().lower()
CHARACTER_ID = "ryan_wireghost_voss"
CHARACTER_SHEET = REPO_ROOT / "fichas" / "techie - ryan_wireghost_voss.md"
CHARACTER_IMAGE = REPO_ROOT / "imagens" / "techie - ryan_wireghost_voss.jpg"
CHARACTER_REL = REPO_ROOT / "relacionamentos" / "ryan_relacionamentos.md"
JOURNAL_DIR = REPO_ROOT / "logs" / "journal"
IMAGES_DIR = REPO_ROOT / "imagens"
GENERIC_MALE_IMAGE = IMAGES_DIR / "NPC_generic_male.png"
GENERIC_FEMALE_IMAGE = IMAGES_DIR / "NPC_generic_female.png"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
JOURNAL_API_PREFIX = "/api/journal/"
PROVIDER_OPTIONS = {
    "1": ("none", "Desativado / fallback local"),
    "2": ("grok", "Grok / provider externo"),
    "3": ("chatgpt", "ChatGPT (teste / sem integração real)"),
    "4": ("gemini", "Gemini (teste / sem integração real)"),
    "5": ("copilot", "Copilot (teste / sem integração real)"),
}
REAL_PROVIDERS = {"grok"}


def clean_error_text(value: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", value)


def format_provider_failure(provider: str, error: Exception) -> str:
    message = clean_error_text(str(error)).strip()
    lowered = message.lower()

    if provider == "grok" and ("402" in lowered or "payment required" in lowered or "balance exhausted" in lowered):
        return "Grok indisponivel no momento. O saldo/credito do provider foi esgotado. Escolha outro provider ou tente mais tarde."

    if provider in {"chatgpt", "gemini", "copilot"}:
        return f"Provider de teste '{provider}' indisponivel para integracao real neste momento."

    return "Nao foi possivel consultar o provider no momento. Tente novamente mais tarde."


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    handler.end_headers()
    handler.wfile.write(raw)


def choose_provider(default_provider: str) -> str:
    if not sys.stdin.isatty():
        return default_provider

    current = default_provider if default_provider in {"none", "grok", "chatgpt", "gemini", "copilot"} else "none"
    print("\nSelecione o provider de narracao:")
    for key, (value, description) in PROVIDER_OPTIONS.items():
        marker = "[padrão]" if value == current else ""
        print(f"  {key}. {value} - {description} {marker}".rstrip())

    selected = input(f"Escolha [1-5] (Enter = {current}): ").strip()
    if not selected:
        return current

    provider = PROVIDER_OPTIONS.get(selected)
    if provider is None:
        print(f"Provider invalido: {selected}. Usando {current}.")
        return current

    return provider[0]


def provider_display_name(provider: str) -> str:
    labels = {
        "none": "Desativado / fallback local",
        "grok": "Grok / provider externo",
        "chatgpt": "ChatGPT (teste / sem integração real)",
        "gemini": "Gemini (teste / sem integração real)",
        "copilot": "Copilot (teste / sem integração real)",
    }
    return labels.get(provider, provider)


def safe_read_json(handler: SimpleHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def parse_sections(markdown_text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def parse_markdown_heading(line: str) -> tuple[int, str] | None:
    heading_match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
    if not heading_match:
        return None
    return len(heading_match.group(1)), heading_match.group(2).strip()


def append_markdown_section(
    stack: list[dict[str, object]], sections: list[dict[str, object]], level: int, title: str
) -> None:
    node: dict[str, object] = {
        "title": title,
        "level": level,
        "content": [],
        "children": [],
    }
    while stack and int(stack[-1]["level"]) >= level:
        stack.pop()
    if stack:
        stack[-1]["children"].append(node)
    else:
        sections.append(node)
    stack.append(node)


def parse_markdown_tree(markdown_text: str) -> dict[str, object]:
    title = ""
    intro_lines: list[str] = []
    sections: list[dict[str, object]] = []
    stack: list[dict[str, object]] = []

    for line in markdown_text.splitlines():
        title_match = re.match(r"^#\s+(.+?)\s*$", line)
        if title_match and not title:
            title = title_match.group(1).strip()
            continue

        heading_info = parse_markdown_heading(line)
        if heading_info:
            append_markdown_section(stack, sections, heading_info[0], heading_info[1])
            continue

        target = stack[-1]["content"] if stack else intro_lines
        target.append(line)

    return {"title": title, "introLines": intro_lines, "sections": sections}


def render_section_tree(nodes: list[dict[str, object]]) -> list[dict[str, object]]:
    rendered: list[dict[str, object]] = []
    for node in nodes:
        rendered.append(
            {
                "title": str(node.get("title", "")).strip(),
                "level": int(node.get("level", 2)),
                "content": "\n".join(str(line) for line in node.get("content", [])).strip(),
                "children": render_section_tree(list(node.get("children", []))),
            }
        )
    return rendered


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def find_sheet_by_name(name: str) -> Path | None:
    normalized = normalize_name(name)
    fichas_dir = REPO_ROOT / "fichas"
    if not fichas_dir.exists():
        return None

    matches: list[Path] = []
    for path in fichas_dir.rglob("*.md"):
        stem = normalize_name(path.stem)
        if not stem:
            continue
        if normalized in stem or stem in normalized:
            matches.append(path)

    if not matches:
        return None
    # Preferir ficha mais específica (nome de arquivo mais próximo do nome buscado).
    return min(matches, key=lambda p: abs(len(normalize_name(p.stem)) - len(normalized)))


def find_image_with_base(base_name: str, *, token: bool) -> Path | None:
    if not IMAGES_DIR.exists():
        return None

    suffix = "_token" if token else ""
    for ext in IMAGE_EXTENSIONS:
        candidate = IMAGES_DIR / f"{base_name}{suffix}{ext}"
        if candidate.exists():
            return candidate
    return None


def fallback_generic_image(gender: str) -> Path | None:
    if gender == "female" and GENERIC_FEMALE_IMAGE.exists():
        return GENERIC_FEMALE_IMAGE
    if GENERIC_MALE_IMAGE.exists():
        return GENERIC_MALE_IMAGE
    if GENERIC_FEMALE_IMAGE.exists():
        return GENERIC_FEMALE_IMAGE
    return None


def scan_image_matches(normalized_name: str) -> tuple[Path | None, Path | None]:
    image_path: Path | None = None
    token_path: Path | None = None
    if not IMAGES_DIR.exists() or not normalized_name:
        return image_path, token_path

    for candidate in IMAGES_DIR.glob("*"):
        if not candidate.is_file() or candidate.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        candidate_norm = normalize_name(candidate.stem)
        if normalized_name not in candidate_norm and candidate_norm not in normalized_name:
            continue
        if "_token" in candidate.stem.lower() and token_path is None:
            token_path = candidate
        elif image_path is None:
            image_path = candidate
    return image_path, token_path


def build_image_payload(name: str, gender: str, source: str, image_path: Path | None, token_path: Path | None) -> dict:
    resolved_image = image_path
    resolved_token = token_path or image_path
    return {
        "name": name,
        "gender": gender,
        "source": source,
        "hasImage": resolved_image is not None,
        "hasToken": resolved_token is not None,
        "imagePath": resolved_image,
        "tokenPath": resolved_token,
    }


def resolve_npc_assets(name: str, gender: str) -> dict:
    sheet = find_sheet_by_name(name)
    source = "fallback"
    normalized = normalize_name(name)
    image_path: Path | None = None
    token_path: Path | None = None

    if sheet is not None:
        base = sheet.stem
        image_path = find_image_with_base(base, token=False)
        token_path = find_image_with_base(base, token=True)
        source = "sheet-name"
    if image_path is None:
        scanned_image, scanned_token = scan_image_matches(normalized)
        image_path = scanned_image or image_path
        token_path = token_path or scanned_token
        source = "image-scan" if image_path is not None else source

    if image_path is None:
        image_path = fallback_generic_image(gender)
        source = "generic"

    payload = build_image_payload(name, gender, source, image_path, token_path)
    payload["hasSheet"] = sheet is not None
    payload["sheetPath"] = str(sheet.relative_to(REPO_ROOT)).replace("\\", "/") if sheet else ""
    return payload


def image_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    if ext == ".gif":
        return "image/gif"
    return "image/png"


def send_image(handler: SimpleHTTPRequestHandler, path: Path) -> None:
    raw = path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", image_content_type(path))
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def journal_file(character_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", character_id).lower()
    return JOURNAL_DIR / f"{safe}.json"


def load_journal_entries(character_id: str) -> list[dict]:
    path = journal_file(character_id)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    out: list[dict] = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            continue
        entry_id = str(item.get("id", "")).strip() or f"{character_id}-{idx}"
        text = str(item.get("text", "")).strip()
        timestamp = str(item.get("timestamp", "")).strip()
        if not text or not timestamp:
            continue
        out.append({"id": entry_id, "timestamp": timestamp, "text": text})
    return out


def save_journal_entries(character_id: str, entries: list[dict]) -> None:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    path = journal_file(character_id)
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def section_lines(section_text: str, max_items: int = 6) -> list[str]:
    if not section_text:
        return []
    lines = []
    for raw in section_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        if line.startswith("**") and line.endswith("**"):
            continue
        lines.append(line)
    return lines[:max_items]


def extract_references(markdown_text: str, limit: int = 12) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for label, path in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", markdown_text):
        if path.startswith("#"):
            continue
        key = (label.strip(), path.strip())
        if key in seen:
            continue
        seen.add(key)
        refs.append({"label": key[0], "path": key[1]})
        if len(refs) >= limit:
            break
    return refs


def build_character_profile() -> dict:
    sheet_text = CHARACTER_SHEET.read_text(encoding="utf-8") if CHARACTER_SHEET.exists() else ""
    rel_text = CHARACTER_REL.read_text(encoding="utf-8") if CHARACTER_REL.exists() else ""

    sheet_tree = parse_markdown_tree(sheet_text)
    rel_tree = parse_markdown_tree(rel_text)
    profile_sections = render_section_tree(list(sheet_tree.get("sections", [])))
    if rel_tree.get("sections"):
        profile_sections.append(
            {
                "title": "Relacionamentos",
                "level": 2,
                "content": "",
                "children": render_section_tree(list(rel_tree.get("sections", []))),
            }
        )

    refs = extract_references(sheet_text + "\n" + rel_text)

    return {
        "characterId": CHARACTER_ID,
        "hero": {
            "title": str(sheet_tree.get("title", "Ryan Wireghost Voss")).strip() or "Ryan Wireghost Voss",
            "introLines": [line for line in sheet_tree.get("introLines", []) if str(line).strip()],
        },
        "sourceSheet": "fichas/techie - ryan_wireghost_voss.md",
        "sourceRelationships": "relacionamentos/ryan_relacionamentos.md",
        "imageUrl": f"/api/character-image/{CHARACTER_ID}",
        "sections": profile_sections,
        "references": refs,
    }


def handle_character_profile(handler: SimpleHTTPRequestHandler) -> None:
    json_response(handler, 200, build_character_profile())


def handle_npc_asset(handler: SimpleHTTPRequestHandler, query: dict[str, list[str]]) -> None:
    name = str(query.get("name", [""])[0]).strip()
    gender = str(query.get("gender", ["male"])[0]).strip().lower() or "male"
    if not name:
        json_response(handler, 400, {"error": "Parâmetro 'name' é obrigatório"})
        return
    assets = resolve_npc_assets(name, "female" if gender == "female" else "male")
    image_url = f"/api/npc-image?name={quote(name)}&variant=full&gender={quote(gender)}"
    token_url = f"/api/npc-image?name={quote(name)}&variant=token&gender={quote(gender)}"
    json_response(
        handler,
        200,
        {
            "name": assets["name"],
            "gender": assets["gender"],
            "source": assets["source"],
            "hasSheet": assets["hasSheet"],
            "sheetPath": assets["sheetPath"],
            "hasImage": assets["hasImage"],
            "hasToken": assets["hasToken"],
            "imageUrl": image_url,
            "tokenUrl": token_url,
        },
    )


def handle_npc_image(handler: SimpleHTTPRequestHandler, query: dict[str, list[str]]) -> None:
    name = str(query.get("name", [""])[0]).strip()
    variant = str(query.get("variant", ["full"])[0]).strip().lower()
    gender = str(query.get("gender", ["male"])[0]).strip().lower() or "male"
    if not name:
        handler.send_error(400, "Parâmetro name é obrigatório")
        return
    assets = resolve_npc_assets(name, "female" if gender == "female" else "male")
    path = assets["tokenPath"] if variant == "token" else assets["imagePath"]
    if path is None or not path.exists():
        handler.send_error(404, "Imagem do NPC nao encontrada")
        return
    send_image(handler, path)


def handle_journal_get(handler: SimpleHTTPRequestHandler, character_id: str) -> None:
    entries = load_journal_entries(character_id)
    json_response(
        handler,
        200,
        {
            "characterId": character_id,
            "storage": str(journal_file(character_id).relative_to(REPO_ROOT)).replace("\\", "/"),
            "entries": entries,
        },
    )


def handle_journal_post(handler: SimpleHTTPRequestHandler, character_id: str) -> None:
    try:
        data = safe_read_json(handler)
    except json.JSONDecodeError:
        json_response(handler, 400, {"error": "JSON invalido"})
        return

    text = str(data.get("text", "")).strip()
    timestamp = str(data.get("timestamp", "")).strip()
    if not text:
        json_response(handler, 400, {"error": "Campo 'text' é obrigatório"})
        return
    if not timestamp:
        json_response(handler, 400, {"error": "Campo 'timestamp' é obrigatório"})
        return

    entries = load_journal_entries(character_id)
    entry_id = f"{character_id}-{len(entries) + 1}-{abs(hash(timestamp + text)) % 1000000}"
    entries.append({"id": entry_id, "timestamp": timestamp, "text": text})
    save_journal_entries(character_id, entries)
    json_response(
        handler,
        201,
        {
            "characterId": character_id,
            "storage": str(journal_file(character_id).relative_to(REPO_ROOT)).replace("\\", "/"),
            "entries": entries,
        },
    )


def handle_journal_delete(handler: SimpleHTTPRequestHandler, character_id: str, entry_id: str) -> None:
    entries = load_journal_entries(character_id)
    filtered = [entry for entry in entries if str(entry.get("id", "")) != entry_id]
    if len(filtered) == len(entries):
        json_response(handler, 404, {"error": "Entrada não encontrada"})
        return

    save_journal_entries(character_id, filtered)
    json_response(
        handler,
        200,
        {
            "characterId": character_id,
            "storage": str(journal_file(character_id).relative_to(REPO_ROOT)).replace("\\", "/"),
            "entries": filtered,
        },
    )


def generate_reply(message: str, mode: str) -> str:
    missing = engine.check_integrity()
    if missing:
        return "Nao foi possivel responder porque arquivos obrigatorios estao ausentes."

    context_paths = engine.select_context_files(message)
    prompt = engine.build_prompt(message, context_paths, mode)

    if PROVIDER in REAL_PROVIDERS:
        try:
            return engine.run_grok(prompt)
        except Exception as exc:  # pragma: no cover
            return format_provider_failure(PROVIDER, exc)

    if PROVIDER in {"chatgpt", "gemini", "copilot"}:
        return (
            f"Provider de teste '{PROVIDER}' selecionado. "
            "Integração real ainda não configurada; usando resposta local de validação."
        )

    if mode == "narrador":
        return "Canal narrador ativo. Estou respondendo fora da cronologia principal."
    return "Canal principal ativo. Mensagem recebida para narracao da historia."


class NarracaoRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        clean_path = parsed.path
        query = parse_qs(parsed.query)
        if self.handle_journal_request(clean_path, "GET"):
            return

        if clean_path == "/api/character-profile":
            handle_character_profile(self)
            return

        if clean_path == "/api/npc-asset":
            handle_npc_asset(self, query)
            return

        if clean_path == "/api/npc-image":
            handle_npc_image(self, query)
            return

        if clean_path.startswith("/api/journal/"):
            character_id = clean_path.rsplit("/", 1)[-1].strip()
            if not character_id:
                json_response(self, 400, {"error": "characterId inválido"})
                return
            entries = load_journal_entries(character_id)
            json_response(
                self,
                200,
                {
                    "characterId": character_id,
                    "storage": f"logs/journal/{re.sub(r'[^a-zA-Z0-9_-]', '_', character_id).lower()}.json",
                    "entries": entries,
                },
            )
            return

        if clean_path.startswith("/api/character-image/"):
            char_id = clean_path.rsplit("/", 1)[-1]
            if char_id != CHARACTER_ID or not CHARACTER_IMAGE.exists():
                self.send_error(404, "Imagem do personagem nao encontrada")
                return
            send_image(self, CHARACTER_IMAGE)
            return

        if clean_path in {"/cyberblade.png", "/frontend/cyberblade.png", "/cyberblade.jpg"}:
            if CHARACTER_IMAGE.exists():
                send_image(self, CHARACTER_IMAGE)
                return
            self.send_error(404, "Imagem nao encontrada")
            return
        super().do_GET()

    def handle_journal_request(self, clean_path: str, method: str) -> bool:
        if not clean_path.startswith(JOURNAL_API_PREFIX):
            return False

        parts = clean_path.strip("/").split("/")
        if method == "GET":
            if len(parts) != 3:
                json_response(self, 400, {"error": "Formato esperado: /api/journal/{characterId}"})
                return True
            _, _, character_id = parts
            handle_journal_get(self, character_id)
            return True

        if method == "POST":
            if len(parts) != 3:
                json_response(self, 400, {"error": "Formato esperado: /api/journal/{characterId}"})
                return True
            _, _, character_id = parts
            handle_journal_post(self, character_id)
            return True

        if method == "DELETE":
            if len(parts) != 4:
                json_response(self, 400, {"error": "Formato esperado: /api/journal/{characterId}/{entryId}"})
                return True
            _, _, character_id, entry_id = parts
            handle_journal_delete(self, character_id, entry_id)
            return True

        json_response(self, 405, {"error": "Método não suportado"})
        return True

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if self.handle_journal_request(parsed.path, "POST"):
            return

        if parsed.path not in {"/api/narracao", "/api/narrador"}:
            json_response(self, 404, {"error": "Endpoint nao encontrado"})
            return

        try:
            data = safe_read_json(self)
        except json.JSONDecodeError:
            json_response(self, 400, {"error": "JSON invalido"})
            return

        message = str(data.get("message", "")).strip()
        if not message:
            json_response(self, 400, {"error": "Campo 'message' e obrigatorio"})
            return

        channel = "narrador" if self.path == "/api/narrador" else "narracao"
        mode = "narrador" if channel == "narrador" else "gestor"

        reply = generate_reply(message, mode)
        json_response(
            self,
            200,
            {
                "channel": channel,
                "provider": PROVIDER,
                "reply": reply,
            },
        )

    def do_DELETE(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if not self.handle_journal_request(parsed.path, "DELETE"):
            json_response(self, 404, {"error": "Endpoint nao encontrado"})


def main() -> int:
    global PROVIDER
    PROVIDER = choose_provider(PROVIDER)

    if not FRONTEND_DIR.exists():
        print(f"Frontend nao encontrado em: {FRONTEND_DIR}")
        return 2

    server = ThreadingHTTPServer((HOST, PORT), NarracaoRequestHandler)
    print(f"Servidor iniciado em http://{HOST}:{PORT}")
    print(f"Provider: {PROVIDER} - {provider_display_name(PROVIDER)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
