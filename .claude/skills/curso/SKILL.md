---
name: curso
description: Conduz o módulo atual do curso "Como criar um cérebro para o seu agente de código" seguindo roteiros/modulo-N.md. Use quando o aluno disser /curso, "continuar o curso", "próximo módulo", "onde parei", "vamos começar o curso".
---

# /curso — conduzir o módulo atual

Argumentos: nenhum (continua do `.curso.json`) · `N` (abre o módulo N sem alterar o estado) · `status`.

## 1. Localizar o estado
1. Procure `.curso.json` no diretório atual.
2. Se não houver, leia `~/.claude/skills/curso/exercicios.path` (caminho do `curso-exercicios`) e procure `.curso.json` lá.
3. Se ainda não houver: diga "Rode o módulo 0 a partir do `curso-exercicios`" e abra `<exercicios>/roteiros/modulo-0.md`.

`status`: mostre `modulo_atual`, `cerebro` e as datas em `checks`; pare.

## 2. Conferir onde rodar
Leia `<exercicios>/roteiros/modulo-<N>.md` (N = argumento ou `modulo_atual`). A seção **Onde rodar** diz `curso-exercicios` ou `<cerebro>` (o caminho está em `.curso.json`). Se o diretório atual não for esse, diga qual abrir e **pare**.

## 3. Seguir o roteiro
Siga as seções na ordem. Em **Passos**:
- `[aluno]`: explique em até 5 linhas o quê e por quê; aponte o exemplo do gabarito quando o passo indicar (`gabarito/modulo-N/<arquivo>`), sem colar o conteúdo; peça que o aluno faça e **espere**. Depois verifique no disco com o comando do passo. Se falhar, mostre a diferença; não corrija por ele.
- `[agente]`: execute o comando indicado, mostre a saída, avance.

## 4. Fechar
Só execute **Fechamento** quando **Saiu rodando** (`checar_modulo.sh N`) estiver todo `✓`. Atualize `modulo_atual` e `checks` em `.curso.json`. A partir do módulo 6, acrescente a entrada no `Wiki_Log` do cérebro como o roteiro manda.

## Regras
- Escreva apenas em `<cerebro>` e em `.curso.json` (exceções explícitas nos roteiros 0 (`.curso.json`, skill global), 1 (`notas-modulo-1.md`) e 4 (`~/.claude/CLAUDE.md`)).
- Nunca edite `gabarito/` ou `starter/`. Nunca faça `git push`.
- Nunca rode `checar_maquina.py --corrigir`, `bootstrap-maquina.sh` ou `install-hooks.sh` a partir de `gabarito/`.
