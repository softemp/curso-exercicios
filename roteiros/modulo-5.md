# Módulo 5 — Extrair um projeto

## Onde rodar
`<cerebro>`.

## Objetivo
Transformar um repositório em conhecimento que o agente consulta: o kit Arquitetura, Módulos, Patterns, Gotchas e ADRs, com `source:` apontando o commit.

## Antes de começar
`<exercicios>/checar_modulo.sh 4` todo `✓`. `<exercicios>/projeto-exemplo/package.json` existe (submódulo baixado).

## Passos
1. [agente] Copie de `<exercicios>/gabarito/modulo-5/` para os mesmos caminhos: `.claude/skills/extrair-projeto/`, `50_System/EXTRACAO_PROJETO.md`, `10_Neurons/Guia_Mapeamento_Projetos.md`, `50_System/Templates/Projeto Kit Template.md`, `Sessao_Extracao_Template.md`, `CLAUDE_projeto.md`. Acrescente `- [[Guia_Mapeamento_Projetos]]: o que mapear (e o que não) de um projeto.` na seção de governança do `Index.md`.
2. [aluno] Leia `50_System/EXTRACAO_PROJETO.md` com o agente resumindo em 6 linhas: o kit canônico (Arquitetura, Módulos, Patterns, Gotchas, ADRs), um neurônio por decisão, `source: "<repo>@<hash>"` em todos, MOC do projeto ligado ao `MOC_Projetos`. Depois, o agente resume `10_Neurons/Guia_Mapeamento_Projetos.md`: regra de ouro "se está no código, não duplique"; **não** se mapeia código de componentes (já está no editor; duplicar dessincroniza), documentação de libs como React e Prisma (acha-se em segundos), props de componentes (mudam toda hora) nem o conteúdo de `.env` (risco de segurança). Verificação: o aluno diz o que NÃO se mapeia e por quê.
3. [aluno] Abra uma sessão nova em `<cerebro>` e rode `/extrair-projeto <exercicios>/projeto-exemplo`. Acompanhe: o agente lê o repositório, propõe o kit, escreve os neurônios `PadraoLayout_*` e o `MOC_PadraoLayout`. Não aceite neurônio sem `source:`. Verificação: `ls 10_Neurons/PadraoLayout_*.md | wc -l` ≥ 5 e `grep -l "^source:.*b6e5c04" 10_Neurons/PadraoLayout_*.md | wc -l` ≥ 5.
4. [agente] Confira o kit: existe Arquitetura, Módulos, Patterns, Gotchas e pelo menos um ADR? `30_Atlas/MOC_PadraoLayout.md` lista todos? Mostre o que falta, se faltar.
5. [aluno] Crie `30_Atlas/MOC_Projetos.md` (hub de projetos) com a linha `- [[MOC_PadraoLayout]]: kit de layout frontend (projeto-exemplo do curso).` e `- MOC Pai: [[Index]]`; acrescente `- [[MOC_Projetos]]: por projeto.` no `Index.md`. Exemplo: `<exercicios>/gabarito/modulo-5/30_Atlas/MOC_Projetos.md`. Verificação: `grep -c "MOC_PadraoLayout" 30_Atlas/MOC_Projetos.md` ≥ 1.
6. [agente] `git add -A && git commit -m "módulo 5: padraoLayout extraído"`.
7. [aluno] Pergunte ao agente, em sessão nova: "como o padraoLayout trata permissões?". Verificação: a resposta cita um neurônio `PadraoLayout_*` (o ADR de permissões) pelo nome.
8. [aluno] Exercício aberto, sem gabarito: rode `/extrair-projeto <caminho de um projeto seu>`. Compare o que saiu com o kit do padraoLayout. Verificação: nenhuma; é o seu projeto.

## Saiu rodando
`<exercicios>/checar_modulo.sh 5` — todo `✓`.

## Compare com o gabarito
`<exercicios>/comparar.sh 5`. O **texto** dos `PadraoLayout_*` vai diferir do gabarito (**escolha sua**: dois agentes extraem diferente); a **estrutura** do kit e o `source:` com `b6e5c04` não podem faltar (**lacuna**). Stubs em `15_Stubs/` do gabarito são **ruído** aqui.

## Como adaptar
Sem skills, `50_System/EXTRACAO_PROJETO.md` é o prompt: cole inteiro no agente com o caminho do repositório. O `Sessao_Extracao_Template.md` é o roteiro da conversa.
- Codex: lê o `AGENTS.md` do cérebro; cole o `EXTRACAO_PROJETO.md` como prompt da sessão.
- Cursor: cole o `EXTRACAO_PROJETO.md` no chat, com o caminho do repositório.
- Gemini CLI: bootstrap no `GEMINI.md` do cérebro; o `EXTRACAO_PROJETO.md` vai como prompt.

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 6` e `checks["5"] = <data>`. Diga: "Módulo 6: manutenção — lint, catálogo e revalidação."
