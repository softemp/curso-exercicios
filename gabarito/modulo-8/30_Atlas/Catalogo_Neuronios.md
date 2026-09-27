---
type: catalog
generated: true
status: evergreen
tags: [meta, indice, catalogo]
created: 2026-09-27
---
# 📇 Catálogo de Neurônios

> ⚠️ **Arquivo gerado** por `50_System/catalog.py` — não editar à mão. Regenere após cada ingest. Última geração: **2026-09-27**.

Ponto de entrada único para navegar todo o acervo: panorama, por projeto, por MOC (com a frase-conceito de cada neurônio) e por tag. Para o mapa curado e a governança, ver [[Index]].

## 📊 Panorama
- **20 neurônios** · 0 fontes arquivadas · 23 tags distintas.
- Maturidade: 🌱 seedling 1 · 🌳 evergreen 19.
- Por MOC: [[MOC_Financeiro]] 1 · [[MOC_Desenvolvimento]] 1 · [[MOC_Frontend]] 1 · [[MOC_PadraoLayout]] 8 · [[MOC_Padroes_Reutilizaveis]] 1 · [[MOC_Seguranca]] 2 · [[MOC_Stack_Base]] 3.

## 🗂️ Por Projeto / Fonte
### padraolayout (8)
[[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[PadraoLayout_Arquitetura]], [[PadraoLayout_Financeiro_Contas]], [[PadraoLayout_Gotchas]], [[PadraoLayout_Modulos]], [[PadraoLayout_Patterns]]

### cofre (1)
[[Minhas_Memorias]]

### Padrões gerais (sem projeto) (11)
[[Base_DB_Naming_Convention]], [[Base_Estrutura_Feature_Based]], [[Base_Seg_Token_Storage]], [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Guia_Mapeamento_Projetos]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]], [[Persistencia_de_Contexto]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Bootstrap_Protocol]], [[Wiki_Scalability_MOC_Pattern]]

## 🧭 Por MOC
### [[MOC_Financeiro]] (1)
- 🌳 [[PadraoLayout_Financeiro_Contas]] — O módulo financeiro do modelo (/financeiro/contas) existe porque o autor não tinha, em nenhum projeto, uma referência boa de contas a pagar/receber.

### [[MOC_Desenvolvimento]] (1)
- 🌳 [[Base_Estrutura_Feature_Based]] — Organizar o código por feature/painel (domínio), não por tipo técnico (controllers/, services/ no topo).

### [[MOC_Frontend]] (1)
- 🌳 [[PadraoLayout_Arquitetura]] — O padraoLayout é o modelo de layout da SoftEmp: um frontend completo, navegável e sem backend, que existe para ser o ponto de partida de projeto novo.

### (sem MOC declarado) (9)
- 🌳 [[Cofre_Grafo_Cores_Configuracao_Versionada]] — O Cofre versiona .obsidian/graph.json para que os grupos de cores do Graph View acompanhem o Vault automaticamente entre máquinas.
- 🌳 [[Guia_Mapeamento_Projetos]] — Define o que deve e o que não deve ser mapeado de um projeto dentro do Cofre de Neurônios.
- 🌱 [[Minhas_Memorias]] — Registro vivo de quem o operador deste cérebro é e do que o move.
- 🌳 [[Parecer_Arquitetura_Cofre]] — Análise crítica da arquitetura do Cofre de Neurônios (LLM Wiki), avaliando seus pontos fortes, fragilidades e oportunidades de melhoria.
- 🌳 [[Parecer_Estrategico_Engenharia]] — Análise estratégica sobre como o Cofre de Neurônios pode (e deve) ser utilizado para acelerar o desenvolvimento de projetos com engenharia de ponta, escalabilidade, segurança e…
- 🌳 [[Persistencia_de_Contexto]] — Este neurônio documenta o risco arquitetural de depender da "Memória Global" de uma LLM para manter a integridade do Cofre de Neurônios, e a solução adotada: tratar o Vault em…
- 🌳 [[Project_Isolation_Pattern_Wiki]] — Estratégia para evitar a degradação do Atlas Central (Index) ao lidar com múltiplos projetos simultâneos.
- 🌳 [[Wiki_Bootstrap_Protocol]] — Este neurônio contém o "Master Prompt" e o guia de inicialização necessários para replicar toda a estrutura da LLM Wiki (Cofre de Neurônios) em qualquer outro ambiente ou modelo…
- 🌳 [[Wiki_Scalability_MOC_Pattern]] — O padrão MOC é uma estratégia de organização de conhecimento que resolve o problema do "Índice Monolítico" em sistemas Zettelkasten ou Wikis pessoais.

### [[MOC_PadraoLayout]] (8)
- 🌳 [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]] — Contexto.
- 🌳 [[PadraoLayout_ADR_002_Matriz_De_Permissoes]] — Contexto.
- 🌳 [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]] — Contexto.
- 🌳 [[PadraoLayout_Arquitetura]] — O padraoLayout é o modelo de layout da SoftEmp: um frontend completo, navegável e sem backend, que existe para ser o ponto de partida de projeto novo.
- 🌳 [[PadraoLayout_Financeiro_Contas]] — O módulo financeiro do modelo (/financeiro/contas) existe porque o autor não tinha, em nenhum projeto, uma referência boa de contas a pagar/receber.
- 🌳 [[PadraoLayout_Gotchas]] — Sete defeitos reais, na ordem em que doem.
- 🌳 [[PadraoLayout_Modulos]] — O mapa de quem é quem.
- 🌳 [[PadraoLayout_Patterns]] — Convenções que quem não conhece quebra sem perceber — cada uma nasceu de um problema real durante a construção, não de gosto.

### [[MOC_Padroes_Reutilizaveis]] (1)
- 🌳 [[PadraoLayout_Patterns]] — Convenções que quem não conhece quebra sem perceber — cada uma nasceu de um problema real durante a construção, não de gosto.

### [[MOC_Seguranca]] (2)
- 🌳 [[Base_Seg_Token_Storage]] — localStorage/sessionStorage são legíveis por JS → XSS rouba o token.
- 🌳 [[PadraoLayout_ADR_002_Matriz_De_Permissoes]] — Contexto.

### [[MOC_Stack_Base]] (3)
- 🌳 [[Base_DB_Naming_Convention]] — Toda coluna e tabela do banco vive em snakecase — sem exceção, em projeto novo ou existente.
- 🌳 [[Base_Estrutura_Feature_Based]] — Organizar o código por feature/painel (domínio), não por tipo técnico (controllers/, services/ no topo).
- 🌳 [[Base_Seg_Token_Storage]] — localStorage/sessionStorage são legíveis por JS → XSS rouba o token.

## 🏷️ Índice de Tags
*Tags com ≥2 neurônios (as de uso único não indexam — listadas ao fim).*

- **status/evergreen** (19): [[Base_DB_Naming_Convention]], [[Base_Estrutura_Feature_Based]], [[Base_Seg_Token_Storage]], [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Guia_Mapeamento_Projetos]], [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[PadraoLayout_Arquitetura]], [[PadraoLayout_Financeiro_Contas]], [[PadraoLayout_Gotchas]], [[PadraoLayout_Modulos]], [[PadraoLayout_Patterns]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]], [[Persistencia_de_Contexto]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Bootstrap_Protocol]], [[Wiki_Scalability_MOC_Pattern]]
- **area/frontend** (9): [[Base_Seg_Token_Storage]], [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[PadraoLayout_Arquitetura]], [[PadraoLayout_Financeiro_Contas]], [[PadraoLayout_Gotchas]], [[PadraoLayout_Modulos]], [[PadraoLayout_Patterns]]
- **linguagem/typescript** (8): [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[PadraoLayout_Arquitetura]], [[PadraoLayout_Financeiro_Contas]], [[PadraoLayout_Gotchas]], [[PadraoLayout_Modulos]], [[PadraoLayout_Patterns]]
- **projeto/padraolayout** (8): [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[PadraoLayout_Arquitetura]], [[PadraoLayout_Financeiro_Contas]], [[PadraoLayout_Gotchas]], [[PadraoLayout_Modulos]], [[PadraoLayout_Patterns]]
- **wiki** (8): [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Guia_Mapeamento_Projetos]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]], [[Persistencia_de_Contexto]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Bootstrap_Protocol]], [[Wiki_Scalability_MOC_Pattern]]
- **area/engenharia** (7): [[Base_Estrutura_Feature_Based]], [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Guia_Mapeamento_Projetos]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Scalability_MOC_Pattern]]
- **meta** (5): [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Guia_Mapeamento_Projetos]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]], [[Wiki_Bootstrap_Protocol]]
- **tipo/arquitetura** (5): [[PadraoLayout_Arquitetura]], [[Parecer_Arquitetura_Cofre]], [[Persistencia_de_Contexto]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Scalability_MOC_Pattern]]
- **tipo/parecer** (5): [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]], [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]], [[Parecer_Arquitetura_Cofre]], [[Parecer_Estrategico_Engenharia]]
- **tipo/pattern** (5): [[Base_DB_Naming_Convention]], [[Base_Estrutura_Feature_Based]], [[Base_Seg_Token_Storage]], [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[PadraoLayout_Patterns]]
- **tipo/referencia** (4): [[Minhas_Memorias]], [[PadraoLayout_Modulos]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Scalability_MOC_Pattern]]
- **area/ia** (2): [[Persistencia_de_Contexto]], [[Wiki_Bootstrap_Protocol]]
- **area/seguranca** (2): [[Base_Seg_Token_Storage]], [[PadraoLayout_ADR_002_Matriz_De_Permissoes]]
- **governanca** (2): [[Cofre_Grafo_Cores_Configuracao_Versionada]], [[Wiki_Bootstrap_Protocol]]
- **tipo/tutorial** (2): [[Guia_Mapeamento_Projetos]], [[Wiki_Bootstrap_Protocol]]

> Uso único: `area/dados` · `area/financeiro` · `area/pessoal` · `area/web` · `projeto/cofre` · `status/seedling` · `tipo/debug` · `tipo/implementacao`
