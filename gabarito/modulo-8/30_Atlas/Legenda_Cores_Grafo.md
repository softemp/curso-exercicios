---
type: reference
generated: true
status: evergreen
tags: [meta, grafo, obsidian, navegacao]
created: 2026-09-27
---
# 🎨 Legenda de Cores do Grafo (Obsidian)

> ⚠️ **Arquivo gerado** por `50_System/grafo_cores.py` a partir de `50_System/grafo_cores.json` — não editar à mão. Última geração: **2026-09-27**.

Convenção de cores do **Graph View** para localizar projetos e domínios de relance. A fonte é o JSON; o script reescreve `colorGroups` em `.obsidian/graph.json` (versionado, viaja com o vault) e esta nota. Decisão e limites em [[Cofre_Grafo_Cores_Configuracao_Versionada]].

## 🗂️ Esquema

| Cor | Hex | Domínio / Projeto | Query (gerada) | Notas (1º grupo que casa) |
|---|---|---|---|---|
| ⚫ Grafite | `#4B5563` | **Stubs (neurônios fora do recorte)** | `path:15_Stubs` | 4 |
| 🟩 Verde | `#2ECC71` | **padraoLayout (modelo de layout)** | `file:PadraoLayout_ OR tag:#projeto/padraolayout` | 9 |
| 🩶 Prata | `#B0B8C4` | **Governança do Cofre & ecossistema** | `file:Eco_ OR file:Cofre_ OR file:Wiki_ OR file:Ecossistema_ OR tag:#projeto/cofre` | 6 |
| ⬜ Branco | `#FFFFFF` | **MOCs & Atlas (hubs/índices)** | `path:30_Atlas` | 12 |

Notas fora desses grupos (padrões transversais como `Idempotencia_*`, `Canvas_*`) ficam na cor neutra — por desenho, para os projetos saltarem aos olhos.

## 🛠️ Como alterar

1. Edite `50_System/grafo_cores.json` (novo grupo = `id`, `emoji`, `cor`, `nome`, `prefixos`/`tags`/`paths`).
2. Rode `python3 50_System/grafo_cores.py` com o Obsidian **fechado** (aberto, ele sobrescreve o `graph.json` ao salvar).
3. Confira o relatório: grupo com 0 notas ou tag `projeto/*` sem grupo é sinal de JSON desatualizado.

## 🔗 Conexões
- Índice: [[Index]] · catálogo: [[Catalogo_Neuronios]] · clusters de projeto: [[MOC_Projetos]].
- Política de portabilidade: [[Cofre_Grafo_Cores_Configuracao_Versionada]].
