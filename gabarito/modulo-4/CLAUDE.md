# Cofre de Neurônios — Diretivas para Claude Code

Este diretório é um **Vault Obsidian** gerenciado como Cofre de Neurônios (Zettelkasten + MOC).

> **Cérebro único** (unificado em 2026-06-13, absorveu o vault `brain`). Este é o único Cofre ativo.

## Bootstrap obrigatório
Ao iniciar uma sessão neste workspace, leia **antes de qualquer ação**:
1. `30_Atlas/Index.md` — mapa central da Wiki.
2. `50_System/WIKI_SCHEMA.md` — regras de Ingest, Lint e Indexação.
3. `50_System/Tags_Taxonomy.md` — vocabulário controlado de tags (o lint valida).

Esses arquivos definem o contrato de governança. Toda criação/edição de neurônio deve respeitá-los. Onboarding: `50_System/GUIA_USO_COFRE.md`.

## 🧭 Protocolo de consulta (use o Cofre como passo 0)
Antes de responder/agir sobre qualquer assunto que o Cofre possa cobrir (projetos conhecidos, padrões, decisões), **consulte-o primeiro**:
1. **Localize** — `grep` por `tag:#projeto/<x>` ou `tag:#area/<y>`, ou leia o hub em `30_Atlas/` (MOC do projeto/tema). O campo `summary:` no frontmatter dá a essência sem abrir o arquivo; o Catalogo_Neuronios lista tudo por projeto/MOC/tag.
2. **Leia o necessário** — abra **≤3 neurônios** mais relevantes (não varra tudo). A forma é previsível: `💡 Conceito` → `🛠️ Aplicação` → `🔗 Conexões`.
3. **Fundamente e cite** — baseie a resposta nos neurônios e **cite-os** pelo nome (`[[Nome]]`). Diga quando algo NÃO está no Cofre.
4. **Confie pelo frescor** — `status: evergreen` + `validated:` recente = confie direto. `seedling`/`incubating` ou `validated` antigo (advisory `[frescor]` no lint) = trate como ponto-no-tempo e **confira contra o código** antes de afirmar.
5. **Capture o aprendizado** — se a tarefa gerou conhecimento novo ou contradisse um neurônio, **atualize/crie** o neurônio (e bumpe `validated:` se reconferiu contra o código). Conhecimento que não vira neurônio se perde.

## ✍️ Convenções de qualidade (excelência p/ consumo por LLM)
- **`summary:`** (1 linha) no frontmatter — a essência greppável do neurônio.
- **`validated: AAAA-MM-DD`** obrigatório em `tipo/implementacao|arquitetura|debug` (derivados de código); reconferir periodicamente (lint advisory `[frescor]` > 180d).
- **Citar por símbolo, não por linha:** `SlotService.calcPrize()` em `slotService.ts`, **nunca** `slotService.ts:442` (linhas apodrecem).
- **`aliases:`** com sinônimos/keywords que você usaria para buscar o conceito.
- Extração de **projeto novo**: siga `50_System/EXTRACAO_PROJETO.md`.

## Regras-chave
- **Atomicidade:** um conceito por arquivo em `10_Neurons/`.
- **Wikilinks:** use somente o formato wikilink (duplo colchete) para links internos — preserva o grafo do Obsidian. Não use `[texto](arquivo.md)` para notas internas.
- **MOCs:** todo neurônio precisa aparecer em pelo menos um MOC sob `30_Atlas/`. Sem órfãos.
- **Log:** registre toda alteração estrutural em `20_Projects/Wiki_Log.md` (data, ação, arquivos afetados).
- **Frontmatter mínimo:** `type`, `status`, `tags`, `created` (+ `source` recomendado, `aliases`/`updated`).
- **Status:** `seedling` → `incubating` → `evergreen` → `archived`.
- **Tags:** taxonomia hierárquica de `50_System/Tags_Taxonomy.md` — 1 `status/` + ≥1 `area/` + ≥1 `tipo/` (+ `projeto/`/`linguagem/` se aplicável).
- **Validação:** rode `python3 50_System/lint.py` (0/0) e `python3 50_System/catalog.py` após mudanças estruturais.

## Tom e idioma
- PT-BR.
- Técnico, pragmático, direto. Sem preâmbulos.
