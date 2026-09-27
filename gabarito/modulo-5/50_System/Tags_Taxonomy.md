---
type: neuron
status: evergreen
aliases: [Taxonomia, Tags, Categorias]
tags: [meta, wiki, governanca, status/evergreen, area/engenharia, tipo/referencia]
source: "Unificação claudio+brain — taxonomia formal de tags"
created: 2026-06-13
updated: 2026-08-29
---
# Tags_Taxonomy — Taxonomia Formal de Tags

## 💡 Conceito
Vocabulário **controlado** de tags do Cofre. Toda tag de neurônio deve sair daqui — evita
duplicação, sinônimos e degradação das queries (Dashboard/Dataview e `catalog.py`). O
`50_System/lint.py` **valida** este contrato (tags fora da taxonomia = erro).

> Hierarquia obrigatória: nunca tags soltas (`react`); use `area/web` + `linguagem/typescript`.
> Tudo minúsculo. Sem sinônimos (um conceito = um nome).

---

## 🛠️ Categorias

### `status/` — ciclo de vida (OBRIGATÓRIA, exatamente 1; deve casar com o campo `status` do frontmatter)
| Tag | | Significado |
|---|---|---|
| `status/seedling` | 🌱 | Rascunho — conteúdo incompleto |
| `status/incubating` | 🌿 | Em revisão — escrito, aguardando validação/enriquecimento |
| `status/evergreen` | 🌳 | Maduro/estável — validado e confiável |
| `status/archived` | 🗄️ | Obsoleto — mover para `40_Archive/` |

### `area/` — domínio de conhecimento (OBRIGATÓRIA, ≥1)
| Tag | Domínio |
|---|---|
| `area/engenharia` | Engenharia de software em geral, padrões transversais |
| `area/web` | Desenvolvimento web (frontend e backend) |
| `area/frontend` | UI/UX, React, canvas, design system (subconjunto de web, quando o foco é a interface) |
| `area/dados` | Banco de dados, modelagem, Prisma, SQL, migrações |
| `area/devops` | Docker, CI/CD, deploy, multi-tenancy, infraestrutura |
| `area/seguranca` | Segurança da informação, auth, hardening, OWASP |
| `area/financeiro` | Pagamentos, gateways, carteira, comissões, trading |
| `area/mensageria` | WhatsApp, bots, filas, notificações multi-canal |
| `area/redes` | Redes, P2P, protocolos, DHT, onion routing, libp2p |
| `area/embedded` | Sistemas embarcados, IoT, firmware (ESP-IDF, RTOS) |
| `area/ia` | IA, LLMs, prompt engineering, agentes |
| `area/pessoal` | Princípios, memórias e insights autorais do autor — não-técnico, define tom e valores |

### `tipo/` — natureza do conteúdo (OBRIGATÓRIA, ≥1)
| Tag | Tipo |
|---|---|
| `tipo/conceito` | Explicação teórica de um conceito |
| `tipo/pattern` | Design pattern / padrão arquitetural reutilizável |
| `tipo/arquitetura` | Descrição arquitetural de um sistema/módulo |
| `tipo/implementacao` | Registro de implementação concreta (feature entregue, refs de código) |
| `tipo/debug` | Solução de bug/gotcha encontrado |
| `tipo/parecer` | Análise crítica, ADR, revisão técnica |
| `tipo/ferramenta` | Documentação de ferramenta/biblioteca |
| `tipo/tutorial` | Guia passo a passo |
| `tipo/referencia` | Folha de referência/runbook (estado, comandos) — não é passo a passo |

### `projeto/` — projeto específico (OPCIONAL; conhecimento transversal não leva)
| Tag | Projeto |
|---|---|
| `projeto/padraolayout` | Modelo de layout SoftEmp — frontend de referência (React/Vite, dados mocados) que os projetos novos copiam |
| `projeto/cofre` | Este Cofre de Neurônios (governança/meta) |

### `linguagem/` — linguagem (OPCIONAL)
`linguagem/typescript` · `linguagem/python` · `linguagem/bash` · `linguagem/sql` · `linguagem/php` · `linguagem/go`

### `plataforma/` — SO/plataforma alvo (OPCIONAL)
`plataforma/windows` · `plataforma/ios` · `plataforma/android`

### Tags de governança (OPCIONAL, para notas meta)
`meta` · `wiki` · `governanca`

---

## ⚠️ Regras
1. **Nunca crie tag fora desta taxonomia** sem registrá-la aqui antes (o lint barra).
2. Tudo **minúsculo**; **hierárquico** (`area/...`, nunca solto).
3. **Sem sinônimos** — um conceito, um nome (ex.: `seguranca`, nunca `security`).
4. Todo neurônio: **1 `status/`** (= campo `status`) **+ ≥1 `area/` + ≥1 `tipo/`**.
5. Revisão mensal: consolidar duplicatas, remover tags de uso único.

## 🔗 Conexões
- MOC: [[Index]] (Governança)
- Relacionados: [[WIKI_SCHEMA]], [[GUIA_USO_COFRE]], Dashboard
