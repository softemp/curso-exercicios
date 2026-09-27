# Módulo 0 — Preparando a máquina

## Onde rodar
`curso-exercicios` (a raiz deste repositório). Confira com `pwd` antes de começar.

## Objetivo
Sair com todas as ferramentas instaladas, o projeto-exemplo baixado, o estado do curso criado e a skill `/curso` disponível.

## Antes de começar
Nada. Este é o primeiro módulo.

## Passos
1. [agente] Rode `for f in git python3 jq claude; do command -v $f >/dev/null && echo "✓ $f" || echo "✗ $f"; done` e mostre o resultado.
2. [aluno] Instale o que apareceu com `✗`: git e jq pelo gerenciador de pacotes do sistema; Python 3.12+ em python.org; Claude Code em claude.com/claude-code; Obsidian em obsidian.md. Avise quando terminar. Verificação: repetir o comando do passo 1 sem nenhum `✗`.
3. [agente] Rode `git submodule update --init --recursive` e confirme que `projeto-exemplo/package.json` existe.
4. [aluno] Escolha onde o seu cérebro vai morar. O padrão é `~/meu-cerebro`; qualquer caminho fora deste repositório serve. Diga o caminho ao agente. Verificação: o agente repete o caminho e o aluno confirma.
5. [agente] Crie `.curso.json` a partir de `.curso.json.exemplo`, preenchendo `cerebro` com o caminho escolhido e `exercicios` com `pwd`. Mostre o arquivo. (Fora do cérebro, o curso só toca este arquivo, a skill em `~/.claude/skills/curso/` e, no módulo 4, `~/.claude/CLAUDE.md`.)
6. [agente] Rode `bash instalar-skill.sh`. A partir de agora `/curso` funciona em qualquer diretório.
7. [aluno] Abra o Obsidian e adicione `gabarito/completo` como vault, só para ver o grafo do cérebro inteiro que você vai montar. Não edite nada nele. Verificação: o aluno descreve o que viu no grafo (cores, quantidade de nós).

## Saiu rodando
`./checar_modulo.sh 0` — todo `✓`. Um `✗` aponta o passo a refazer.

## Compare com o gabarito
Não se aplica neste módulo (ainda não há cérebro). `comparar.sh 0` não existe.

## Como adaptar
Idêntico em qualquer agente: cole o conteúdo deste arquivo no agente e siga os passos. A skill `/curso` é só um atalho do Claude Code.

## Fechamento
Grave em `.curso.json`: `modulo_atual = 1` e `checks["0"] = <data de hoje, AAAA-MM-DD>`. Diga ao aluno: "Módulo 1 quando quiser: `/curso`."
