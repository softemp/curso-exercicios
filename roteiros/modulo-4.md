# Módulo 4 — Regras que o agente obedece

## Onde rodar
`<cerebro>`.

## Objetivo
Escrever uma regra uma vez e vê-la aplicada em todo projeto: neurônios `Base_*`, o MOC de stack e o `CLAUDE.md` global apontando o cérebro.

## Antes de começar
`<exercicios>/checar_modulo.sh 3` todo `✓`.

## Passos
1. [agente] Copie de `<exercicios>/gabarito/modulo-4/10_Neurons/` para `10_Neurons/`: `Base_DB_Naming_Convention.md`, `Base_Estrutura_Feature_Based.md`, `Base_Seg_Token_Storage.md`. Liste os três.
2. [aluno] Leia `Base_DB_Naming_Convention.md` com o agente resumindo em 5 linhas: regra (snake_case em coluna e tabela, `@map` no Prisma), porquê (banco legível, migração sem surpresa) e como aplicar (nunca camelCase sem `@map`; rename é `RENAME COLUMN`). Verificação: o aluno diz qual seria a coluna certa para "createdAt".
3. [aluno] Crie `30_Atlas/MOC_Stack_Base.md` à mão: título, uma linha de propósito ("kit prescritivo por camada para projeto novo") e uma lista com os três `Base_*` linkados (`- [[Base_DB_Naming_Convention]]: …`), terminando com `- MOC Pai: [[Index]]`. O `Index.md` do starter ainda não tem seção de MOCs: crie nele a seção `## 🧭 Mapas de Conteúdo (MOCs)` e acrescente ali a linha `- [[MOC_Stack_Base]]: kit prescritivo por camada.` Exemplo: `<exercicios>/gabarito/modulo-4/30_Atlas/MOC_Stack_Base.md`. Verificação: `grep -c "\[\[Base_" 30_Atlas/MOC_Stack_Base.md` dá 3.
4. [aluno] Crie `~/.claude/CLAUDE.md` (ou acrescente ao existente) a partir de `<exercicios>/gabarito/modulo-4/50_System/claude-global/CLAUDE.md`, trocando o caminho do vault pelo seu `<cerebro>`. É o único arquivo fora do cérebro que este módulo toca. Verificação: o caminho do vault (em qualquer forma, `~/…` ou absoluta) aparece em `~/.claude/CLAUDE.md` (`grep -cF -e "<cerebro>" -e "<cerebro com ~ no lugar do $HOME>" ~/.claude/CLAUDE.md` ≥ 1).
5. [agente] `git add -A && git commit -m "módulo 4: regras Base_* e MOC_Stack_Base"`.
6. [aluno] Volte ao projeto do módulo 1, abra uma sessão nova e repita o pedido do modelo `Pedido` com timestamps. Verificação: o aluno cola o schema; as colunas devem sair `created_at`/`updated_at` com `@map` sem que ele tenha pedido.

## Saiu rodando
`<exercicios>/checar_modulo.sh 4` — todo `✓`.

## Compare com o gabarito
`<exercicios>/comparar.sh 4`. `MOC_Stack_Base.md` com texto próprio é **escolha sua**; ausência de um `Base_*` ou do link no Index é **lacuna**.

## Como adaptar
O global do Codex é `~/.codex/AGENTS.md`; do Gemini CLI, `~/.gemini/GEMINI.md`; no Cursor, "User Rules" nas configurações. O conteúdo é o mesmo: "antes de decidir schema, estrutura ou segurança, leia `<cerebro>/30_Atlas/MOC_Stack_Base.md`".

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 5` e `checks["4"] = <data>`. Diga: "Módulo 5: extrair um projeto inteiro para o cérebro."
