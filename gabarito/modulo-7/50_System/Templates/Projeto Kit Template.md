---
type: nota
status: evergreen
aliases: [Kit de Projeto]
summary: "Scaffold do kit canônico de neurônios + sub-MOC para um projeto novo."
tags: [meta, wiki, tipo/referencia, status/evergreen]
source: "EXTRACAO_PROJETO"
created: 2026-06-14
updated: 2026-06-14
---
# 🧰 Kit de Projeto — Scaffold

Copie e renomeie para cada projeto novo. Ver o playbook em [[EXTRACAO_PROJETO]].
Substitua `{{Projeto}}` (PascalCase no arquivo) e `{{slug}}` (minúsculo na tag).

## Neurônios a criar (`10_Neurons/`)
- `{{Projeto}}_Arquitetura.md` — `tipo/arquitetura` — hub do projeto (stack, topologia, fluxo).
- `{{Projeto}}_Modulos.md` — `tipo/referencia` — mapa de módulos (faz / conversa com / onde mora).
- `{{Projeto}}_Patterns.md` — `tipo/pattern` — convenções não-óbvias do código.
- `{{Projeto}}_Gotchas.md` — `tipo/debug` — pegadinhas, priorizadas por severidade.
- `{{Projeto}}_ADR_001_<slug>.md` … — `tipo/parecer` — uma por decisão (ver `ADR Template.md`).
- *(domínio)* — fluxos/regras específicas conforme necessário.

## sub-MOC (`30_Atlas/MOC_{{Projeto}}.md`)
```md
# {{emoji}} MOC: {{Projeto}} ({{descrição curta}})

Hub do **{{Projeto}}** — {{1 linha}}. Ramificado de [[MOC_Projetos]] (padrão [[Project_Isolation_Pattern_Wiki]]).

## 🏛️ Arquitetura & Mapas
- [[{{Projeto}}_Arquitetura]]: …
- [[{{Projeto}}_Modulos]]: …
- [[{{Projeto}}_Patterns]]: …
- [[{{Projeto}}_Gotchas]]: …

## 📐 Decisões (ADRs)
- [[{{Projeto}}_ADR_001_<slug>]]: …

---
- MOC Pai: [[MOC_Projetos]]
```

## Registro (não esquecer)
1. `projeto/{{slug}}` em [[Tags_Taxonomy]].
2. Entrada do `MOC_{{Projeto}}` em [[MOC_Projetos]].
3. Grupo de cor em `50_System/grafo_cores.json` (`"prefixos": ["{{Projeto}}_"]`) + `python3 50_System/grafo_cores.py` (gera `graph.json` e [[Legenda_Cores_Grafo]]).
4. `lint.py` 0/0 + `catalog.py`; fonte em `40_Archive/`; [[Wiki_Log]].

## 🔗 Conexões
- MOC: [[Index]]
- Relacionados: [[EXTRACAO_PROJETO]]
