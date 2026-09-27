---
type: nota
status: evergreen
aliases: [Extração de Projeto, Onboarding de Projeto, Mapear Projeto]
summary: "Playbook para extrair conhecimento de um projeto novo para o Cofre com padrão de excelência."
tags: [meta, wiki, governanca, tipo/tutorial, status/evergreen]
source: "Padrão validado nos projetos Wbot/criptoChatSE/AnonEcom (vault brain) + unificação"
created: 2026-06-14
updated: 2026-06-14
---
# 🏗️ EXTRACAO_PROJETO — Modelo de Extração de Conhecimento

Playbook para transformar **um projeto seu** (código que você cria/mantém) em conhecimento
de **excelência** no Cofre — otimizado para o Claude consumir de forma orgânica. Invocável
pela skill `extrair-projeto`. Complementa [[Guia_Mapeamento_Projetos]] (o *que* mapear).

## 🎯 Princípio
Capture o **não-óbvio** — o que você NÃO relê do código em 5 minutos: **decisões** (por quê),
**gotchas** (o que quebra), **padrões** (convenções implícitas), **arquitetura** (como as peças
se ligam). Não documente o que o código já diz trivialmente. O repo-fonte é **read-only**
(nunca editar o projeto fonte: só `Read`/`grep`/`git log`/Explore).

## 🧩 O "kit canônico" por projeto
Todo projeto rende, no mínimo, estes neurônios (`projeto/<slug>` + naming `<Projeto>_<Conceito>`):

| Neurônio | `tipo/` | Conteúdo |
|---|---|---|
| `<Projeto>_Arquitetura` | `arquitetura` | Visão geral: stack, topologia, fronteiras, fluxo principal. **Hub** do projeto. |
| `<Projeto>_Modulos` | `referencia` | Mapa dos módulos: o que cada um faz, com quem conversa, onde mora a lógica. |
| `<Projeto>_Patterns` | `pattern` | Convenções repetidas e **não-óbvias** (quem não conhece introduz bug). |
| `<Projeto>_Gotchas` | `debug` | Pegadinhas/bugs/limitações reais, **priorizadas por severidade** (segurança/financeiro primeiro). |
| `<Projeto>_ADR_<NNN>_<slug>` | `parecer` | 1 por **decisão arquitetural** relevante (contexto → decisão → consequência). |
| *(domínio)* | vário | Fluxos e regras de negócio específicos conforme a riqueza do projeto. |

> Padrão **reutilizável** (vale em qualquer projeto) → neurônio próprio em MOC_Padroes_Reutilizaveis, **sem** `projeto/` tag. Não enterre o genérico dentro do projeto.

## 🔄 Passos

**0. Registrar o projeto**
- Adicionar `projeto/<slug>` em [[Tags_Taxonomy]].
- Criar `30_Atlas/MOC_<Projeto>.md` (sub-hub) e registrá-lo em [[MOC_Projetos]].
- Adicionar o grupo de cor em `50_System/grafo_cores.json` e rodar `python3 50_System/grafo_cores.py` (gera o `graph.json` e a Legenda_Cores_Grafo).

**1. Capturar (read-only)**
- Apontar o Claude ao repo: estrutura de pastas, `git log --oneline`, `README`/`docs`, pontos de entrada.
- Dump bruto da sessão em `00_Inbox/` (use o template de sessão), citando **repo@commit**.

**2. Sintetizar o kit** — criar os neurônios do kit + os de domínio, com a forma previsível
(`💡 Conceito` / `🛠️ Aplicação` / `🔗 Conexões`).

**3. Frontmatter de excelência** (por neurônio) — ver [[WIKI_SCHEMA]]:
- `projeto/<slug>` + `area/` + `tipo/`; `status` (`seedling` no rascunho → `incubating` ao revisar → `evergreen` ao validar).
- `source: <repo>@<commit>`; **`validated: <data>`** (conferido contra o código); `summary`; `aliases`.
- **Citar por símbolo** (`Service.metodo()`), nunca por linha.

**4. Conectar e indexar** — wikilinks bidirecionais; cada neurônio no `MOC_<Projeto>`; genérico cruza com MOC_Padroes_Reutilizaveis e/ou MOC_Seguranca.

**5. Validar e fechar** — `python3 50_System/lint.py` (0/0; mirar zero advisory de estrutura/frescor) + `python3 50_System/catalog.py`; mover a fonte bruta p/ `40_Archive/` com rodapé `## 🔗 Conexões`; registrar em Wiki_Log.

## ✅ Definição de "pronto" (Definition of Done)
- Kit canônico criado; cada neurônio com `summary` + `validated` + cita por símbolo.
- `MOC_<Projeto>` no Atlas, cor no grafo, `projeto/` na taxonomia.
- `lint.py` 0/0 **e** zero `[estrutura]`/`[frescor]` para os neurônios novos.
- Fonte arquivada e linkada; Wiki_Log atualizado.

## 🔗 Conexões
- MOC: [[Index]] (Governança)
- Relacionados: [[WIKI_SCHEMA]], [[Tags_Taxonomy]], [[GUIA_USO_COFRE]], [[Guia_Mapeamento_Projetos]], MOC_Padroes_Reutilizaveis
