---
type: nota
status: evergreen
aliases: [Guia de Uso, Como Usar o Cofre, Manual]
tags: [meta, wiki, governanca, tipo/tutorial, status/evergreen]
source: "Unificação claudio+brain — guia prático de uso"
created: 2026-06-13
updated: 2026-06-13
---
# 📖 GUIA_USO_COFRE — Como Usar e Manter o Cofre

> [!tip] Comece por aqui. Leia uma vez com calma; depois use como referência rápida.

## 1. O que é
Sua **memória externa de engenharia** no Obsidian: cada conhecimento vira uma **nota atômica**
(neurônio), conectada por wikilinks e MOCs. Regras de qualidade impedem que vire bagunça.

## 2. Estrutura de pastas
```
00_Inbox/    📥 captura bruta (rascunhos, dumps, fontes)
10_Neurons/  🧠 neurônios prontos (1 conceito por arquivo)
20_Projects/ 📋 logs e acompanhamento (Wiki_Log.md)
30_Atlas/    🗺️ MOCs, Index, Dashboard, Catálogo
40_Archive/  📦 fontes brutas já processadas (com link p/ os neurônios que geraram)
50_System/   ⚙️ governança: WIKI_SCHEMA, Tags_Taxonomy, lint.py, catalog.py, templates
```
- Templates versionados em `50_System/Templates/`: [[50_System/Templates/Neuron Template|Neuron Template]] (neurônio), [[50_System/Templates/ADR Template|ADR Template]] (decisão), [[50_System/Templates/Projeto Kit Template|Projeto Kit Template]] (kit de extração), [[50_System/Templates/CLAUDE_projeto|CLAUDE_projeto]] (gatilho por projeto), [[50_System/Templates/Sessao_Extracao_Template|Sessao_Extracao_Template]] (sessão de extração). Instalação em outra máquina: INSTALL_OUTRA_MAQUINA.

## 3. Fluxo: do bruto ao neurônio (Ingest)
1. **Captura** → joga em `00_Inbox/` (ou `50_System/Scripts/quick_capture.sh`, se existir).
2. **Atomiza** → 1 conceito por arquivo, com o `Templates/Neuron Template.md`.
3. **Frontmatter** → `type/status/tags/created` + `source`; tags da [[Tags_Taxonomy]] (1 `status/` + ≥1 `area/` + ≥1 `tipo/` + `projeto/` se aplicável).
4. **Conecta** → wikilinks `[[...]]` bidirecionais + 1 MOC no rodapé.
5. **Arquiva a fonte** → move o bruto p/ `40_Archive/` com rodapé `## 🔗 Conexões` linkando os neurônios derivados.
6. **Valida** → `python3 50_System/lint.py` (deve dar 0/0).
7. **Loga** → entrada em `20_Projects/Wiki_Log.md`.

## 4. Como ACHAR conhecimento (3 lentes + ferramentas)
- **Por projeto** → [[MOC_Projetos]] e cores do grafo (Legenda_Cores_Grafo).
- **Por tema** → MOCs temáticos no [[Index]].
- **Por tipo/maturidade** → [[Dashboard]] (Dataview, live) ou [[Catalogo_Neuronios]] (versionado, gerado por `catalog.py`).
- **Grafo** → Graph View do Obsidian, colorido por projeto.

## 5. Ferramentas (git-purista, versionadas)
| Comando | O quê |
|---|---|
| `python3 50_System/lint.py` `[-v]` | Valida o contrato (frontmatter, taxonomia, órfãos, links, fontes) + advisory frescor/estrutura |
| `python3 50_System/catalog.py` | Regenera o [[Catalogo_Neuronios]] |
| `python3 50_System/revalidate.py [proj]` | Lista neurônios de código a reconferir (frescor) |
| `bash 50_System/sync_wiki.sh` | Regenera catálogo + lint + commit |
| `bash 50_System/backup_cofre.sh` | Backup com rotação (cron diário 03:00) |

**Skills invocáveis:** `extrair-projeto <repo>` (onboard de projeto novo → [[EXTRACAO_PROJETO]]) · `revalidar [projeto]` (reconferir conhecimento contra o código). Cron mensal (dia 1, 09:00) gera o relatório de re-validação em `~/backups/meu-cerebro/revalidate.log`.

## 6. Manutenção
Siga a **Revisão periódica** do [[WIKI_SCHEMA]] (semanal/quinzenal/mensal) + a skill `revalidar`. Tags novas: registrar
**antes** na [[Tags_Taxonomy]] (o lint barra fora do vocabulário).

## 🔗 Conexões
- MOC: [[Index]] (Governança)
- Relacionados: [[WIKI_SCHEMA]], [[Tags_Taxonomy]], [[Dashboard]], [[Catalogo_Neuronios]], Legenda_Cores_Grafo
