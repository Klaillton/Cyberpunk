from __future__ import annotations

from typing import Literal

SheetTier = Literal["protagonist", "crew_full", "npc_reference", "npc_generic"]

VALID_TIERS: frozenset[str] = frozenset(
    {"protagonist", "crew_full", "npc_reference", "npc_generic"}
)

TIER_LABELS: dict[str, str] = {
    "protagonist": "Protagonista",
    "crew_full": "Crew (CPR completa)",
    "npc_reference": "NPC de referência",
    "npc_generic": "NPC genérico / arquétipo",
}

REQUIRED_SECTIONS: dict[str, frozenset[str]] = {
    "protagonist": frozenset(
        {
            "identidade",
            "atributos",
            "skills",
            "humanidade e cyberware",
            "background",
        }
    ),
    "crew_full": frozenset(
        {
            "identidade",
            "atributos",
            "skills",
            "background",
        }
    ),
    "npc_reference": frozenset({"identidade", "background"}),
    "npc_generic": frozenset({"identidade"}),
}

CREW_FULL_SLUGS: frozenset[str] = frozenset(
    {
        "lena_valk_kane",
        "jax_razor_kane",
        "kaz_the_broker_takahashi",
        "stephania_doc_voss",
        "reina_bearclaw_morales",
        "alex_specter_kane",
    }
)

TIER_BY_SLUG: dict[str, SheetTier] = {
    "ryan_wireghost_voss": "protagonist",
    "lena_valk_kane": "crew_full",
    "jax_razor_kane": "crew_full",
    "kaz_the_broker_takahashi": "crew_full",
    "stephania_doc_voss": "crew_full",
    "reina_bearclaw_morales": "crew_full",
    "alex_specter_kane": "crew_full",
    "reyes": "npc_reference",
    "tio_gringo": "npc_reference",
    "lira": "npc_reference",
    "rusty": "npc_reference",
    "mara_recruit": "npc_reference",
    "elias_recruit": "npc_reference",
    "tomas_recruit": "npc_reference",
    "sasha": "npc_reference",
    "archetype_raffen_shiv": "npc_generic",
}


def normalize_tier(value: str | None, *, slug: str | None = None) -> SheetTier:
    clean = (value or "").strip().lower()
    if clean in VALID_TIERS:
        return clean  # type: ignore[return-value]
    if slug and slug in TIER_BY_SLUG:
        return TIER_BY_SLUG[slug]
    return "npc_reference"


def tier_for_slug(slug: str) -> SheetTier:
    return TIER_BY_SLUG.get(slug.strip().lower(), "npc_reference")