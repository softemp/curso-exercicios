# Módulo 3 — Starter vivo

## Onde rodar
`<cerebro>` (o caminho está em `.curso.json`). Abra o agente lá.

## Objetivo
O agente passa a ler o cérebro sem ser pedido: contrato de entrada para qualquer agente, hook de sessão e git como memória.

## Antes de começar
`<exercicios>/checar_modulo.sh 2` todo `✓`. `git --version` funciona.

## Passos
1. [agente] `git init` em `<cerebro>`, `git add -A`, `git commit -m "nasce o cérebro"`. Mostre `git log --oneline`.
2. [aluno] Crie `AGENTS.md` na raiz do cérebro. Ele deve mandar qualquer agente ler `30_Atlas/Index.md`, `50_System/WIKI_SCHEMA.md` e `50_System/Tags_Taxonomy.md` antes de agir, e trazer a linha do curso: `> **Curso:** o próximo módulo está em <exercicios>/roteiros/; leia <exercicios>/.curso.json.` (troque `<exercicios>` pelo caminho real). Exemplo: `<exercicios>/gabarito/modulo-3/AGENTS.md`. Verificação: `grep -c Index AGENTS.md` ≥ 1.
3. [aluno] Crie `CLAUDE.md` com o mesmo bootstrap, dirigido ao Claude Code, e a regra "toda criação de neurônio respeita o WIKI_SCHEMA". Exemplo: `<exercicios>/gabarito/modulo-3/CLAUDE.md`. Verificação: `grep -c Index CLAUDE.md` ≥ 1.
4. [aluno] Crie `.claude/settings.json` com um hook `SessionStart` que injeta o Index: comando `cat "$CLAUDE_PROJECT_DIR/30_Atlas/Index.md"`. Exemplo exato: `<exercicios>/gabarito/modulo-3/.claude/settings.json`. Verificação: `jq -e '.hooks.SessionStart' .claude/settings.json`.
5. [agente] Copie `<exercicios>/gabarito/modulo-3/50_System/hooks/lembrete-cofre.sh` (com `chmod +x`) e `<exercicios>/gabarito/modulo-3/50_System/GUIA_USO_COFRE.md` para os mesmos caminhos no cérebro (`50_System/hooks/` e `50_System/`). Explique em 3 linhas o que o lembrete faz (hook global que lembra o agente, em outros projetos, de consultar o cérebro; ele será registrado no módulo 7).
6. [agente] `git add -A && git commit -m "módulo 3: contratos de agente e hook de sessão"`.
7. [aluno] Feche esta sessão e abra outra em `<cerebro>`. Antes de pedir qualquer coisa, observe: o Index chegou no contexto? Pergunte "o que você já sabe sobre este vault?" e veja se o agente cita o Index sem ter sido mandado. Verificação: o aluno relata o que aconteceu.

## Saiu rodando
`<exercicios>/checar_modulo.sh 3` — todo `✓`.

## Compare com o gabarito
`<exercicios>/comparar.sh 3`. Texto do `AGENTS.md` e `CLAUDE.md` diferente do gabarito é **escolha sua** desde que o bootstrap esteja lá; `.obsidian/` é **ruído**; falta de `hooks/lembrete-cofre.sh` ou `GUIA_USO_COFRE.md` é **lacuna**.

## Como adaptar
Codex e Gemini CLI leem `AGENTS.md` (o `CLAUDE.md` é ignorado). O hook `SessionStart` é do Claude Code: no Cursor, coloque o bootstrap em `.cursor/rules/cerebro.mdc`; no Gemini CLI, em `GEMINI.md`.

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 4` e `checks["3"] = <data>`. Diga: "Módulo 4: regras que o agente obedece."
