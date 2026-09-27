# Módulo 6 — Manutenção

## Onde rodar
`<cerebro>`.

## Objetivo
O cérebro não vira cemitério de notas falsas: lint como gate de commit, catálogo e índice gerados, revalidação e drift contra o código, diário no `Wiki_Log`.

## Antes de começar
`<exercicios>/checar_modulo.sh 5` todo `✓`.

## Passos
1. [agente] Copie de `<exercicios>/gabarito/modulo-6/` para os mesmos caminhos: `50_System/lint.py`, `lint_wiki.py`, `catalog.py`, `symbols.py`, `symbol_index.py`, `revalidate.py`, `drift.py`, `install-hooks.sh`, `monthly_review.sh`, `projetos-com-gatilho.txt`, `.claude/skills/revalidar/`, e os neurônios `Wiki_Bootstrap_Protocol`, `Wiki_Scalability_MOC_Pattern`, `Project_Isolation_Pattern_Wiki`, `Parecer_Arquitetura_Cofre`, `Parecer_Estrategico_Engenharia`. Acrescente cada neurônio na seção de governança do `Index.md` (uma linha `- [[Nome]]: <summary do frontmatter>`).
2. [aluno] Rode `bash 50_System/install-hooks.sh` e leia `.git/hooks/pre-commit`. Verificação: o aluno explica em uma frase o que o hook faz (roda o lint e bloqueia o commit se houver erro fatal).
3. [aluno] Crie `10_Neurons/Teste_Orfao.md` a partir do template, com frontmatter válido mas **sem** linha `- MOC:` e sem acrescentar no Index. Tente `git add -A && git commit -m "teste"`. Verificação: o commit é recusado com `[órfão] Teste_Orfao`. Depois apague o arquivo (`git rm -f` ou `rm`).
4. [agente] Rode `python3 50_System/catalog.py` e `python3 50_System/symbol_index.py`. Mostre `30_Atlas/Catalogo_Neuronios.md` (gerado, `generated: true`, não conta para órfão) e explique em 3 linhas o `Indice_Simbolos`.
5. [aluno] Abra `50_System/symbols.py` e confira `REPO_CANDIDATES`: o `padraolayout` precisa apontar para `<exercicios>/projeto-exemplo`; ajuste se o seu caminho for outro. Depois, provoque um drift numa **cópia** (nunca no submódulo):
   1. `cp -r <exercicios>/projeto-exemplo /tmp/pl`.
   2. Em `REPO_CANDIDATES` de `50_System/symbols.py`, ponha `"/tmp/pl"` como primeiro candidato do `padraolayout`.
   3. Em `/tmp/pl`, renomeie (`mv`) um arquivo citado num neurônio `PadraoLayout_*`.
   4. Rode `python3 50_System/drift.py`. Verificação: o drift acusa o arquivo sumido.
   5. Abra uma sessão nova em `<cerebro>` para a skill `revalidar` carregar, rode `/revalidar padraolayout` e veja o que ela propõe (não aceite as mudanças).
   6. Restaure: tire `"/tmp/pl"` de `REPO_CANDIDATES` e `rm -rf /tmp/pl`.
6. [aluno] Crie `20_Projects/Wiki_Log.md` com o frontmatter `type: log`, `status: evergreen`, `tags: [log, meta, projects]`, `created: <hoje>` e a primeira entrada `## [<hoje>] curso | módulos 2 a 6` com uma linha por engrenagem montada. Exemplo: `<exercicios>/gabarito/modulo-6/20_Projects/Wiki_Log.md`. Verificação: o arquivo existe e tem uma seção `## [`.
7. [agente] `python3 50_System/lint.py` (0 erros), depois `git add -A && git commit -m "módulo 6: lint, catálogo, revalidação, log"`. O hook roda o lint no commit.

## Saiu rodando
`<exercicios>/checar_modulo.sh 6` — todo `✓`.

## Compare com o gabarito
`<exercicios>/comparar.sh 6`. Texto do `Wiki_Log` e do Index é **escolha sua**; ausência de qualquer script de `50_System/` listado no passo 1 é **lacuna**; `Catalogo_Neuronios.md` e `Indice_Simbolos.md` diferentes são **ruído** (gerados a partir do seu conteúdo).

## Como adaptar
Todos os scripts são Python puro e rodam à mão. Só a skill `revalidar` é do Claude Code: em outro agente, cole `.claude/skills/revalidar/SKILL.md` como prompt. Codex (lê `AGENTS.md`), Cursor (chat) e Gemini CLI (`GEMINI.md`) rodam os scripts pelo terminal do mesmo jeito; o `pre-commit` é git, vale para todos.

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 7` e `checks["6"] = <data>`. Acrescente ao `20_Projects/Wiki_Log.md`: `## [<data>] curso | módulo 6 concluído` e uma linha `- lint no pre-commit, catálogo, índice de símbolos, revalidação e drift ativos.` Commit. Diga: "Módulo 7: o cérebro em outra máquina."
