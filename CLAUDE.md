# curso-exercicios — diretivas para agentes

Este repositório é o material prático do curso "Como criar um cérebro para o seu agente de código".

## Para continuar o curso
1. Leia `.curso.json` (se não existir, o aluno ainda não fez o módulo 0: abra `roteiros/modulo-0.md`).
2. Abra `roteiros/modulo-<modulo_atual>.md` e siga-o literalmente, respeitando as marcas `[aluno]` e `[agente]` e a seção "Onde rodar".
3. No Claude Code, `/curso` faz exatamente isso.

## Regras
- `gabarito/` e `starter/` são gerados. Nunca edite; aponte para eles.
- Só escreva no cérebro do aluno (`.cerebro` do `.curso.json`) e em `.curso.json` (exceções explícitas nos roteiros 0 (`.curso.json`, skill global), 1 (`notas-modulo-1.md`) e 4 (`~/.claude/CLAUDE.md`)).
- Nunca faça `git push`. Nunca rode `checar_maquina.py --corrigir`, `bootstrap-maquina.sh` ou `install-hooks.sh` a partir de `gabarito/`.
