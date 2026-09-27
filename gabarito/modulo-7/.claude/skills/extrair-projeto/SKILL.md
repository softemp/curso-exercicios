---
name: extrair-projeto
description: Extrai conhecimento de um projeto de código para o Cofre de Neurônios seguindo o padrão de excelência (kit canônico Arquitetura/Módulos/Patterns/Gotchas/ADRs). Use quando o usuário quer mapear/onboard um projeto novo que ele cria ou mantém, ou pedir para "extrair conhecimento", "mapear o projeto X", "adicionar o projeto Y ao cérebro". Argumento: caminho do repositório-fonte.
---

# Extrair Projeto → Cofre de Neurônios

Você está operando dentro do vault `meu-cerebro`. Execute o playbook `50_System/EXTRACAO_PROJETO.md`
para o repositório indicado pelo usuário (argumento = caminho do repo, ex.: `~/curso-exercicios/projeto-exemplo`).

## Regras inegociáveis
- O repositório-fonte é **READ-ONLY**: só `Read`, `Bash` com `git log`/`grep`/`find`/`ls`, agentes Explore. **Nunca** Edit/Write/commit no projeto-fonte.
- Todo neurônio segue o contrato: ler `50_System/WIKI_SCHEMA.md` + `50_System/Tags_Taxonomy.md` antes de criar.
- Capture o **não-óbvio** (decisões, gotchas, padrões, arquitetura) — não o que o código diz trivialmente.

## Passos
1. **Explorar (read-only)** o repo: estrutura, `git log --oneline -30`, README/docs, pontos de entrada, stack. Use 1-3 agentes Explore em paralelo se for grande.
2. **Registrar o projeto**: escolher `slug`; adicionar `projeto/<slug>` em `50_System/Tags_Taxonomy.md`; criar `30_Atlas/MOC_<Projeto>.md` (use `50_System/Templates/Projeto Kit Template.md`) e registrar em `30_Atlas/MOC_Projetos.md`; adicionar cor em `.obsidian/graph.json` + `30_Atlas/Legenda_Cores_Grafo.md`.
3. **Criar o kit canônico** em `10_Neurons/` (`<Projeto>_Arquitetura/Modulos/Patterns/Gotchas` + `<Projeto>_ADR_NNN_*`) + neurônios de domínio. Use `Neuron Template.md` e `ADR Template.md`. Frontmatter completo: `projeto/<slug>` + `area/` + `tipo/`, `summary`, `aliases`, `source: <repo>@<commit>`, `validated: <hoje>`. **Citar por símbolo, nunca por linha.** Padrões reutilizáveis genéricos → neurônio próprio em `MOC_Padroes_Reutilizaveis` (sem tag `projeto/`).
4. **Conectar**: wikilinks bidirecionais; cada neurônio no `MOC_<Projeto>`; cruzar com `MOC_Seguranca`/`MOC_Padroes_Reutilizaveis` quando couber.
5. **Fechar**: `python3 50_System/lint.py` (0/0 e **zero** advisory de estrutura/frescor nos novos) + `python3 50_System/catalog.py`; arquivar o dump da sessão em `40_Archive/` com rodapé `## 🔗 Conexões`; registrar em `20_Projects/Wiki_Log.md`; commit.

## Definition of Done
Kit completo + sub-MOC + cor + taxonomia + lint 0/0 sem advisory novo + fonte arquivada + Wiki_Log. Reporte ao usuário a lista de neurônios criados e o que ficou pendente de validação.
