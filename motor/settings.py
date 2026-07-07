from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_PROVIDERS = frozenset({"none", "ollama", "grok", "chatgpt", "gemini", "copilot"})
VALID_ROUTING_POLICIES = frozenset({"local_only", "local_preferred", "hybrid", "cloud_preferred"})

PROVIDER_OPTIONS: dict[str, tuple[str, str]] = {
    "1": ("none", "Desativado / fallback local"),
    "2": ("ollama", "Ollama / LLM local"),
    "3": ("grok", "Grok / provider externo"),
    "4": ("chatgpt", "ChatGPT (teste / sem integração real)"),
    "5": ("gemini", "Gemini (teste / sem integração real)"),
    "6": ("copilot", "Copilot (teste / sem integração real)"),
}


@dataclass
class Settings:
    repo_root: Path
    frontend_dir: Path
    host: str = "127.0.0.1"
    port: int = 8787
    provider: str = "none"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model_narration: str = "llama3.1:8b"
    character_id: str = "ryan_wireghost_voss"
    journal_dir: Path = field(default_factory=Path)
    data_dir: Path = field(default_factory=Path)
    db_path: Path = field(default_factory=Path)
    faiss_dir: Path = field(default_factory=Path)
    campanha_root: Path = field(default_factory=Path)
    llm_routing_policy: str = "local_preferred"
    cloud_fallback_enabled: bool = False
    cloud_provider: str = "grok"
    ollama_model_classifier: str = "phi3:mini"
    ollama_max_prompt_chars: int = 8000
    ollama_max_context_files: int = 5
    update_proposals_enabled: bool = False

    @classmethod
    def from_env(cls, repo_root: Path | None = None) -> Settings:
        root = repo_root or Path(__file__).resolve().parent.parent
        provider = os.environ.get("NARRACAO_PROVIDER", "none").strip().lower()
        if provider not in VALID_PROVIDERS:
            provider = "none"
        data_dir = Path(os.environ.get("DATA_DIR", str(root / "data")))
        campanha_root = Path(os.environ.get("CAMPANHA_ROOT", str(root)))
        routing_policy = os.environ.get("LLM_ROUTING_POLICY", "local_preferred").strip().lower()
        if routing_policy not in VALID_ROUTING_POLICIES:
            routing_policy = "local_preferred"
        cloud_fallback = os.environ.get("CLOUD_FALLBACK_ENABLED", "false").strip().lower() in {
            "1",
            "true",
            "yes",
        }
        cloud_provider = os.environ.get("CLOUD_PROVIDER", "grok").strip().lower()
        if cloud_provider not in VALID_PROVIDERS or cloud_provider in {"none", "ollama"}:
            cloud_provider = "grok"
        update_proposals_raw = os.environ.get("UPDATE_PROPOSALS_ENABLED", "").strip().lower()
        if update_proposals_raw in {"1", "true", "yes"}:
            update_proposals_enabled = True
        elif update_proposals_raw in {"0", "false", "no"}:
            update_proposals_enabled = False
        else:
            update_proposals_enabled = provider == "grok"
        return cls(
            repo_root=root,
            frontend_dir=root / "frontend",
            host=os.environ.get("NARRACAO_API_HOST", "127.0.0.1"),
            port=int(os.environ.get("NARRACAO_API_PORT", "8787")),
            provider=provider,
            ollama_base_url=os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip(),
            ollama_model_narration=os.environ.get("OLLAMA_MODEL_NARRATION", "llama3.1:8b").strip(),
            character_id=os.environ.get("PROTAGONIST_ID", "ryan_wireghost_voss").strip(),
            journal_dir=Path(os.environ.get("JOURNAL_DIR", str(root / "logs" / "journal"))),
            data_dir=data_dir,
            db_path=Path(os.environ.get("DB_PATH", str(data_dir / "motor.db"))),
            faiss_dir=Path(os.environ.get("FAISS_DIR", str(data_dir / "faiss"))),
            campanha_root=campanha_root,
            llm_routing_policy=routing_policy,
            cloud_fallback_enabled=cloud_fallback,
            cloud_provider=cloud_provider,
            ollama_model_classifier=os.environ.get("OLLAMA_MODEL_CLASSIFIER", "phi3:mini").strip(),
            ollama_max_prompt_chars=int(os.environ.get("OLLAMA_MAX_PROMPT_CHARS", "8000")),
            ollama_max_context_files=int(os.environ.get("OLLAMA_MAX_CONTEXT_FILES", "5")),
            update_proposals_enabled=update_proposals_enabled,
        )

    @property
    def character_sheet(self) -> Path:
        return self.repo_root / "fichas" / "techie - ryan_wireghost_voss.md"

    @property
    def character_image(self) -> Path:
        return self.repo_root / "imagens" / "techie - ryan_wireghost_voss.jpg"

    @property
    def character_relationships(self) -> Path:
        return self.repo_root / "relacionamentos" / "ryan_relacionamentos.md"

    @property
    def images_dir(self) -> Path:
        return self.repo_root / "imagens"


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def reset_settings(repo_root: Path | None = None) -> Settings:
    global _settings
    _settings = Settings.from_env(repo_root)
    return _settings


def choose_provider(default_provider: str | None = None) -> str:
    settings = get_settings()
    default = (default_provider or settings.provider).strip().lower()
    if default not in VALID_PROVIDERS:
        default = "none"

    if os.environ.get("NARRACAO_SKIP_PROVIDER_PROMPT", "").strip().lower() in {"1", "true", "yes"}:
        settings.provider = default
        return default
    if not sys.stdin.isatty():
        settings.provider = default
        return default

    print("\nSelecione o provider de narracao:")
    for key, (value, description) in PROVIDER_OPTIONS.items():
        marker = "[padrão]" if value == default else ""
        print(f"  {key}. {value} - {description} {marker}".rstrip())

    selected = input(f"Escolha [1-6] (Enter = {default}): ").strip()
    if not selected:
        settings.provider = default
        return default

    provider_entry = PROVIDER_OPTIONS.get(selected)
    if provider_entry is None:
        print(f"Provider invalido: {selected}. Usando {default}.")
        settings.provider = default
        return default

    settings.provider = provider_entry[0]
    return settings.provider


def provider_display_name(provider: str | None = None) -> str:
    settings = get_settings()
    name = provider or settings.provider
    labels = {
        "none": "Desativado / fallback local",
        "ollama": f"Ollama local ({settings.ollama_model_narration})",
        "grok": "Grok / provider externo",
        "chatgpt": "ChatGPT (teste / sem integração real)",
        "gemini": "Gemini (teste / sem integração real)",
        "copilot": "Copilot (teste / sem integração real)",
    }
    return labels.get(name, name)