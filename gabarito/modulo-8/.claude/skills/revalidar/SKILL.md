---
name: revalidar
description: Re-valida neurônios derivados de código contra o repositório-fonte atual — conferindo o que MUDOU desde o commit registrado em `source:` — e atualiza `validated`/`source`. Use quando o usuário quer reconferir/atualizar o conhecimento de um projeto contra o código, ou pede "revalidar X", "conferir se os neurônios de Y ainda batem com o código". Argumento opcional: slug do projeto.
---

# Revalidar conhecimento contra o código

Você está no vault `meu-cerebro`. Objetivo: reconferir neurônios que citam código e mantê-los
confiáveis — o que inclui **descobrir o que o código ganhou e o Cofre ainda não sabe**.

## Passo 1 (SEMPRE PRIMEIRO) — o diff desde o commit documentado

As ferramentas do Cofre medem **idade** (`revalidate.py`, > 180 dias) e **símbolo sumido**
(`drift.py`). Nenhuma das duas enxerga **conteúdo novo**: código acrescentado deixa as duas
verdes e o Cofre desatualizado. Isso aconteceu nas três primeiras revalidações do
`padraoLayout` — trate como o caso comum, não como exceção.

```bash
# commit registrado nos neurônios do projeto
grep -h "^source:" 10_Neurons/<Projeto>_*.md | head -3
# repo-fonte: mapa em 50_System/symbols.py
cd <repo> && git diff --stat <commit-do-source> HEAD && git log --oneline <commit-do-source>..HEAD
```

Leia o diff e responda: **o que entrou? contradiz algum neurônio, ou só acrescenta?** O repo é
**READ-ONLY** (Read/grep/git log/Explore — nunca editar o projeto-fonte).

## Passo 2 — as ferramentas, como complemento
- `python3 50_System/revalidate.py [<projeto>]` — neurônios `tipo/implementacao|arquitetura|debug` sem `validated` ou com > 180 dias.
- `python3 50_System/drift.py [<projeto>]` — símbolos e arquivos citados que sumiram (drift forte) ou não resolveram (a revisar).

## Passo 3 — reconferir e corrigir
Para cada neurônio afetado pelo diff (e para o backlog dos passos anteriores):
- **Bate** → `validated:` (e `updated:`) para hoje; promover `status` se couber.
- **Mudou** → corrigir o conteúdo (citar por símbolo, nunca por linha) e registrar o que mudou.
- **Obsoleto** → `status: archived`, ou reescrever.
- **Entrou coisa nova** → acrescentar ao neurônio certo do kit (`_Arquitetura` para telas/módulos novos, `_Modulos` para peças, `_Patterns` para convenção nova, `_Gotchas` para pegadinha).
- **`source:` de TODOS os neurônios do projeto** passa a apontar o commit conferido agora.

## Passo 3.1 — menu novo? o catálogo tem de saber

**Um item de menu é um módulo** (Base_Catalogo_Modulos_Gestao). Se o diff acrescentou rota
e entrada em `app/navigation.ts`, o módulo **precisa entrar na tabela do catálogo** com o mesmo
rótulo do menu, a rota, os arquivos (`shared/api/<slug>.ts` · `features/<slug>/`), a invariante
que ele já resolve e de quais módulos depende. Sem isso a entrevista de `novo-projeto` deixa de
oferecê-lo — o módulo existe e ninguém o encontra.

Confira por **rota distinta**, não por rótulo: item pai é agrupador e filho com a mesma rota
mais query (`/clientes?status=…`) é vista salva, não módulo.

```bash
grep -oE "rota: '[^']+'" <repo>/src/app/navigation.ts | sed "s/rota: '//;s/'//;s/?.*//" | sort -u > /tmp/rotas.txt
grep -oE '^\| \*\*[^|]+\| `/[^`]*`' 10_Neurons/Base_Catalogo_Modulos_Gestao.md \
  | grep -oE '`/[^`]*`' | tr -d '`' | sort -u > /tmp/catrotas.txt
comm -23 /tmp/rotas.txt /tmp/catrotas.txt   # vazio = catálogo em dia
```

## Passo 4 — o que é genérico sai do projeto
Se o código novo trouxe uma regra que **vale em qualquer projeto**, ela vira neurônio próprio em
[[MOC_Padroes_Reutilizaveis]] (+ MOC temático), **sem** tag `projeto/` — e o neurônio do projeto
só aponta para ela. Enterrar o genérico dentro do projeto é o jeito mais comum de perder
conhecimento reutilizável.

## Passo 5 — fechar
`python3 50_System/lint.py` (0/0, sem advisory novo) + `python3 50_System/catalog.py` +
`python3 50_System/symbol_index.py`; registrar em `20_Projects/Wiki_Log.md`; commit.
Antes de escrever no Cofre, `git fetch`/`pull` — o vault roda em mais de uma máquina.

## Saída
Reporte: o que o diff revelou, quantos neurônios foram bumpados, corrigidos ou arquivados,
quais padrões genéricos saíram para fora do projeto, e o frescor restante.
