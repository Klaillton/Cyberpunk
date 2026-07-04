# Pulso do Mundo

Simulação off-screen de NPCs e do pack enquanto Ryan não está na cena.

## Como usar

1. Leia o motor em **[sistema/pulso_procedimento.md](../sistema/pulso_procedimento.md)**.
2. A cada **dia in-game**, role a tabela em `pack_badlands/pulso_geral.md`.
3. Resolva com o pulso NPC indicado (perguntas + ganchos).
4. Registre em *Eventos Off-Screen Recentes* e arquivos de estado se necessário.

## Estrutura

```text
pulso_do_mundo/
├── template_pulso_npc.md
├── pack_badlands/     ← Ryan nas Badlands
└── crew/              ← NC / remoto / futuro
```

## Índice rápido

| Pasta | Arquivos |
| ----- | -------- |
| `pack_badlands/` | pulso_geral, reyes, tio_gringo, sasha_e_lira, criancas, recrutas |
| `crew/` | valk, kaz, alex, reina, stephania_doc, jax |