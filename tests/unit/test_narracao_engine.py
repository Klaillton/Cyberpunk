from __future__ import annotations

from pathlib import Path

import pytest

import narracao_engine as engine


def test_check_integrity_passes_on_real_repo(repo_root: Path) -> None:
    missing = engine.check_integrity()
    assert missing == [], f"Arquivos ausentes: {missing}"


def test_select_context_files_includes_heat_for_exposure_message() -> None:
    paths = engine.select_context_files("Qual o nivel de heat e exposicao da crew?")
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "heat.md" in rel
    assert "event_queue.md" in rel


def test_select_context_files_includes_relationships_for_npc_names() -> None:
    paths = engine.select_context_files("Quero falar com Valk e Alex sobre o pack")
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert any("relacionamentos" in item for item in rel)


def test_select_context_files_respects_max_files() -> None:
    paths = engine.select_context_files("heat reputacao economia npc pulso", max_files=3)
    assert len(paths) <= 3


def test_build_prompt_contains_user_message_and_mode() -> None:
    paths = engine.select_context_files("Como esta a economia?")
    prompt = engine.build_prompt("Como esta a economia?", paths, mode="gestor")
    assert "Como esta a economia?" in prompt
    assert "Modo GESTOR" in prompt
    assert "Regras obrigatorias" in prompt


def test_build_prompt_narrador_mode_hint() -> None:
    paths = engine.select_context_files("Descreva a cena")
    prompt = engine.build_prompt("Descreva a cena", paths, mode="narrador")
    assert "Modo NARRADOR" in prompt


def test_select_context_files_ollama_skips_heavy_sistema_docs() -> None:
    paths = engine.select_context_files("Quero falar com Valk sobre heat", provider="ollama")
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "board/board_campanha.md" in rel
    assert "sistema/instrucoes_projeto.md" not in rel
    assert "sistema/registro_arquivos.md" not in rel
    assert len(paths) <= engine.DEFAULT_OLLAMA_MAX_CONTEXT_FILES


def test_build_prompt_ollama_respects_max_chars() -> None:
    message = "Ryan observa o acampamento do Pack ao entardecer. Valk prepara o Mule."
    paths = engine.select_context_files(message, provider="ollama")
    prompt = engine.build_prompt(
        message,
        paths,
        mode="narrador",
        provider="ollama",
        max_prompt_chars=8000,
    )
    assert len(prompt) <= 8000
    assert "board/board_campanha.md" in prompt
    assert "Nao cite caminhos de arquivos" in prompt
    assert message in prompt


def test_normalize_channel_maps_narrador_to_mestre() -> None:
    assert engine.normalize_channel("narrador") == "mestre"
    assert engine.normalize_channel("mestre") == "mestre"
    assert engine.normalize_channel("narracao") == "narracao"
    assert engine.normalize_channel("sistema") == "sistema"


def test_build_prompt_ollama_mestre_channel_hint() -> None:
    paths = engine.select_context_files("Quem faz parte da crew?", provider="ollama", channel="mestre")
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    prompt = engine.build_prompt(
        "Quem faz parte da crew?",
        paths,
        mode="mestre",
        provider="ollama",
        channel="mestre",
        max_prompt_chars=8000,
    )
    assert "MESTRE off-game" in prompt
    assert "Plano futuro:" in prompt
    assert "relacionamentos/crew_relacionamentos.md" in rel
    assert "relacionamentos/crew_polycule_ryan_valk_alex_reina.md" in rel
    assert len(paths) <= 5


def test_build_prompt_ollama_main_channel_hint() -> None:
    paths = engine.select_context_files("Observo o acampamento.", provider="ollama", channel="narracao")
    prompt = engine.build_prompt(
        "Observo o acampamento.",
        paths,
        mode="narrador",
        provider="ollama",
        channel="narracao",
        max_prompt_chars=8000,
    )
    assert "Canal NARRACAO PRINCIPAL" in prompt


def test_sanitize_ollama_reply_strips_echoed_question() -> None:
    raw = "E quanto a Reina, Alex, Jax e Kaz?\n\n- Reina: protecao\n- Alex: rival"
    cleaned = engine.sanitize_ollama_reply(raw, channel="mestre")
    assert not cleaned.startswith("E quanto")
    assert cleaned.startswith("- Reina")


def test_sanitize_ollama_reply_strips_menu_choices() -> None:
    raw = (
        "Ryan esta em downtime. Voce quer: A) Fortalecer defesas B) Ensinar tecnicas "
        "C) Gerenciar Biotechnica D) Equilibrar com Valk. Escolha uma opcao para avancar."
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="mestre")
    assert "Voce quer" not in cleaned
    assert "Escolha uma opcao" not in cleaned
    assert "A)" not in cleaned


def test_sanitize_ollama_reply_strips_meta_parentheticals() -> None:
    raw = (
        "**Quais sao os membros da crew?** "
        "(Essa pergunta foi respondida pelo jogador anteriormente: Mara e Tomas) "
        "Aqui esta a cena atual: Ryan observa Valk. "
        "(Remova as perguntas feitas anteriormente que nao estao mais relevantes.)"
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="mestre")
    assert "respondida pelo jogador" not in cleaned
    assert "Remova as perguntas" not in cleaned
    assert "Aqui esta a cena atual" not in cleaned
    assert "Ryan observa Valk" not in cleaned


def test_build_prompt_ollama_prioritizes_board_over_sistema() -> None:
    message = "Descreva a cena no acampamento com Valk e Reyes."
    paths = engine.select_context_files(message, provider="ollama")
    prompt = engine.build_prompt(
        message,
        paths,
        mode="narrador",
        provider="ollama",
        max_prompt_chars=5000,
    )
    board_index = prompt.find("board/board_campanha.md")
    assert board_index >= 0
    assert board_index < len(prompt)


def test_compact_content_truncates_large_files(repo_root: Path) -> None:
    sample = repo_root / "board" / "board_campanha.md"
    if not sample.exists():
        pytest.skip("board_campanha.md ausente")
    compact = engine.compact_content(sample, max_chars=200)
    assert len(compact) <= 260
    assert "truncado" in compact


def test_select_context_files_summary_command_loads_summary_docs() -> None:
    paths = engine.select_context_files(
        "[Finalizar sessão e gerar resumo]",
        session_intent="summary",
    )
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "logs/sessao_resumo_template.md" in rel
    assert "sistema/diretrizes_ia.md" in rel


def test_build_prompt_summary_command_uses_structured_format() -> None:
    paths = engine.select_context_files(
        "[Finalizar sessão e gerar resumo]",
        session_intent="summary",
        provider="ollama",
    )
    prompt = engine.build_prompt(
        "[Finalizar sessão e gerar resumo]",
        paths,
        mode="narrador",
        provider="ollama",
        session_intent="summary",
        history=[{"role": "user", "content": "Ryan infiltra a torre Raffen"}],
        max_prompt_chars=8000,
    )
    assert "COMANDO DE RESUMO DE SESSAO" in prompt
    assert "PROIBIDO: narrar cenas" in prompt
    assert "Ryan infiltra a torre Raffen" in prompt
    assert "sessao_resumo_007.md" in prompt


def test_sanitize_narracao_reply_strips_repeated_sentences() -> None:
    previous = (
        "Voce se aproxima da destilaria. Elias esta trabalhando em uma das maquinas. "
        "Tomas ainda nao foi encontrado."
    )
    raw = (
        "Voce se aproxima da destilaria. Elias esta trabalhando em uma das maquinas. "
        "Um barulho metalico vem da oficina ao norte."
    )
    cleaned = engine.sanitize_ollama_reply(
        raw,
        channel="narracao",
        history=[{"role": "assistant", "content": f"NARRADOR: {previous}"}],
    )
    assert "barulho metalico" in cleaned
    assert "Elias esta trabalhando" not in cleaned


def test_sanitize_narracao_reply_strips_aqui_esta_uma_pergunta() -> None:
    raw = "Tomas some na oficina. Aqui esta uma pergunta: O que voce faz em seguida?"
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "Aqui esta uma pergunta" not in cleaned
    assert "O que voce faz em seguida" not in cleaned


def test_sanitize_narracao_reply_strips_narrador_prefix_and_player_echo() -> None:
    previous = "Valk abraca Tio Gringo no refeitorio."
    player = "Eu cumprimento o Tio Gringo e pergunto sobre a oficina."
    raw = (
        "NARRADOR: NARRADOR: Voce cumprimenta o Tio Gringo e pergunta sobre a oficina. "
        "Ele responde que os novatos ajudam na usinagem, mas ainda falta disciplina."
    )
    cleaned = engine.sanitize_ollama_reply(
        raw,
        channel="narracao",
        history=[
            {"role": "assistant", "content": previous},
            {"role": "user", "content": f"[HISTORIA] VOCE: {player}"},
        ],
    )
    assert not cleaned.upper().startswith("NARRADOR:")
    assert "cumprimenta o Tio Gringo e pergunta" not in cleaned.lower()
    assert "usinagem" in cleaned.lower()


def test_build_prompt_narracao_uses_parsed_player_message() -> None:
    paths = engine.select_context_files("Observo o pack.", provider="ollama")
    message = 'Encosto na cerca.\n_ A manha esta lenta. *Falo baixo*'
    prompt = engine.build_prompt(
        message,
        paths,
        mode="narrador",
        provider="ollama",
        channel="narracao",
        max_prompt_chars=8000,
    )
    assert "Entrada do jogador AGORA (parseada)" in prompt
    assert "### Falas" in prompt
    assert "manha esta lenta" in prompt.lower()


def test_sanitize_narracao_reply_strips_option_menus() -> None:
    raw = (
        "Ryan trabalha nos planos. Voce pode: A) Incluir aquecimento B) Priorizar estufa. "
        "O que voce fara?"
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "Voce pode" not in cleaned
    assert "A)" not in cleaned


def test_last_narrator_text_ignores_npc_only_tail() -> None:
    history = [
        {
            "role": "assistant",
            "content": (
                "O refeitorio cheira a cafe.\n\n"
                '[NPC: Tio Gringo] "Bom dia, Ryan."'
            ),
        }
    ]
    assert engine._last_narrator_text(history) == "O refeitorio cheira a cafe."


def test_sanitize_uses_current_player_message_over_history() -> None:
    raw = "Voce observa o patio e nota pegadas frescas na lama."
    cleaned = engine.sanitize_ollama_reply(
        raw,
        channel="narracao",
        history=[{"role": "user", "content": "entro na oficina"}],
        player_message="observo o patio",
    )
    assert "observa o patio" not in cleaned.lower()


def test_sanitize_strips_npc_repeating_player_speech() -> None:
    player = (
        'Ryan fica serio.\n\n'
        '"Quanto eles ja sabem? Mover o pack e uma alternativa?"'
    )
    raw = (
        '[NPC-M: Reyes] "Quanto eles ja sabem? Mover o pack e uma alternativa?" '
        "Reyes mantem o olhar fixo em Ryan."
    )
    cleaned = engine.sanitize_ollama_reply(
        raw,
        channel="narracao",
        player_message=player,
    )
    assert "quanto eles ja sabem" not in cleaned.lower()
    assert "mantem o olhar" in cleaned.lower()


def test_sanitize_strips_meta_incompleto_phrases() -> None:
    raw = (
        "O Mule freia no acampamento. "
        "(Resumo de chat incompleto; sem detalhes registrados da incursao alem do retorno.)"
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "incompleto" not in cleaned.lower()
    assert "Mule freia" in cleaned


def test_sanitize_fixes_reyes_m_tag_format() -> None:
    raw = '[NPC placeholder] ok. [Reyes-M: Reyes] "Ei, alguem sabe quem e isso?"'
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "[Reyes-M:" not in cleaned
    assert "[NPC-M: Reyes]" in cleaned


def test_sanitize_normalizes_inline_npc_tags() -> None:
    raw = (
        "O Mule treme na estrada. [NPC-F: Lena \"Valk\" Kane] "
        '"Incursao limpa o bastante. Se o perimetro ainda estiver de pe, dormimos sem vigilia extra."'
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert 'Lena "Valk" Kane' not in cleaned
    assert "[NPC-F: Lena Valk" in cleaned
    assert "Incursao limpa" in cleaned


def test_sanitize_repairs_mojibake_from_grok() -> None:
    raw = "O rÃ¡dio chiou no habitÃ¡culo."
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "rádio" in cleaned
    assert "habitáculo" in cleaned


def test_sanitize_strips_ryan_control_sentences() -> None:
    raw = (
        "Ryan olha para Reyes com um sorriso serio, assentindo com a cabeca. "
        "Reyes mantem o olhar fixo e responde em voz baixa."
    )
    cleaned = engine.sanitize_ollama_reply(raw, channel="narracao")
    assert "ryan olha" not in cleaned.lower()
    assert "reyes mantem" in cleaned.lower()


def test_sanitize_strips_echo_but_keeps_new_detail() -> None:
    raw = "Voce observa o patio. Pegadas frescas cruzam a lama perto da cerca."
    cleaned = engine.sanitize_ollama_reply(
        raw,
        channel="narracao",
        player_message="observo o patio",
    )
    assert "observa o patio" not in cleaned.lower()
    assert "pegadas frescas" in cleaned.lower()


def test_select_context_mestre_tomas_excludes_polycule() -> None:
    message = "Tomas parece nervoso — o NPC ja se tornou traidor?"
    paths = engine.select_context_files(message, provider="ollama", channel="mestre")
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "fichas/npc/tomas_recruit.md" in rel
    assert "pulso_do_mundo/pack_badlands/recrutas.md" in rel
    assert "relacionamentos/crew_polycule_ryan_valk_alex_reina.md" not in rel


def test_select_context_mestre_crew_question_includes_polycule() -> None:
    paths = engine.select_context_files(
        "Quem faz parte da crew?",
        provider="ollama",
        channel="mestre",
    )
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "relacionamentos/crew_polycule_ryan_valk_alex_reina.md" in rel
    assert "relacionamentos/crew_relacionamentos.md" in rel


def test_build_prompt_mestre_includes_history_and_tomas_example() -> None:
    message = "Tomas parece nervoso — o NPC ja se tornou traidor?"
    paths = engine.select_context_files(message, provider="ollama", channel="mestre")
    prompt = engine.build_prompt(
        message,
        paths,
        mode="mestre",
        provider="ollama",
        channel="mestre",
        history=[{"role": "user", "content": "MESTRE VOCE: Tomas parece nervoso"}],
        max_prompt_chars=8000,
    )
    assert "Historico do canal Mestre" in prompt
    assert "Tomas parece nervoso" in prompt
    assert "suspeita / traidor" in prompt
    assert "fichas/npc/tomas_recruit.md" in prompt


def test_select_context_sistema_brief_includes_dashboard_and_session() -> None:
    paths = engine.select_context_files(
        "Como funciona o resumo da campanha? quais arquivos voce consulta?",
        provider="ollama",
        channel="sistema",
    )
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "sistema/dashboard_contexto.md" in rel
    assert "board/board_campanha.md" in rel
    assert "sistema/registro_arquivos.md" in rel
    assert any(item.startswith("logs/sessao_resumo_") for item in rel)


def test_select_context_sistema_netrunner_includes_alex_ficha() -> None:
    paths = engine.select_context_files(
        "qual a ficha da netrunner?",
        provider="ollama",
        channel="sistema",
    )
    rel = {p.relative_to(engine.REPO_ROOT).as_posix() for p in paths}
    assert "fichas/netrunner - alex_specter_kane.md" in rel
    assert "relacionamentos/ryan_relacionamentos.md" not in rel


def test_build_prompt_sistema_includes_fichas_index_for_list_question() -> None:
    prompt = engine.build_prompt(
        "quais fichas voce tem na pasta fichas?",
        engine.select_context_files(
            "quais fichas voce tem na pasta fichas?",
            provider="ollama",
            channel="sistema",
        ),
        mode="sistema",
        provider="ollama",
        channel="sistema",
        max_prompt_chars=8000,
    )
    assert "Indice de fichas" in prompt
    assert "fichas/netrunner - alex_specter_kane.md" in prompt
    assert "fichas/nomad - lena_valk_kane.md" in prompt
    assert "resumo da campanha / brief" in prompt


def test_list_campaign_sheets_includes_crew_and_npc() -> None:
    from motor.npc import list_campaign_sheets

    rel_paths = {item["rel"] for item in list_campaign_sheets()}
    assert "fichas/netrunner - alex_specter_kane.md" in rel_paths
    assert "fichas/npc/tomas_recruit.md" in rel_paths


def test_build_prompt_narracao_includes_conversation_history() -> None:
    paths = engine.select_context_files("Continuo fumando no muro.", provider="ollama")
    prompt = engine.build_prompt(
        "Continuo fumando no muro.",
        paths,
        mode="narrador",
        provider="ollama",
        channel="narracao",
        history=[{"role": "user", "content": "[HISTORIA] VOCE: encostado na parede"}],
        max_prompt_chars=8000,
    )
    assert "Historico da conversa" in prompt
    assert "encostado na parede" in prompt
    assert "CONTINUIDADE" in prompt or "continuidade" in prompt.lower()


def test_resolve_paths_skips_template_files() -> None:
    paths = engine.resolve_paths(
        [
            "board/board_campanha.md",
            "fichas/npc/npc_template.md",
            "logs/sessao_resumo_template.md",
        ]
    )
    rel = {path.relative_to(engine.REPO_ROOT).as_posix() for path in paths}
    assert "board/board_campanha.md" in rel
    assert "fichas/npc/npc_template.md" not in rel
    assert "logs/sessao_resumo_template.md" not in rel


def test_append_session_log_writes_jsonl(tmp_path: Path, monkeypatch) -> None:
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    monkeypatch.setattr(engine, "SESSIONS_DIR", sessions_dir)
    session_file = sessions_dir / "test-session.jsonl"
    engine.append_session_log(session_file, engine.ChatTurn("2026-01-01T00:00:00Z", "user", "oi"))
    lines = session_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert '"role": "user"' in lines[0]