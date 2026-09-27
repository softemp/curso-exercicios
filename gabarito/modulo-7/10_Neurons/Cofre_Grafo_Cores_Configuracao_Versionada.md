---
type: neuron
status: evergreen
aliases: [Cores do Graph View entre máquinas, Versionar graph.json, Configuração portátil do grafo]
summary: "As cores do Graph View têm UMA fonte (50_System/grafo_cores.json); grafo_cores.py gera colorGroups no graph.json versionado e a Legenda — nunca editar os dois à mão."
tags: [meta, wiki, governanca, status/evergreen, area/engenharia, tipo/pattern]
source: "Decisão de governança do Cofre — sessão 2026-07-15"
created: 2026-07-15
updated: 2026-09-26
---
# Cofre_Grafo_Cores_Configuracao_Versionada

## 💡 Conceito
O Cofre versiona `.obsidian/graph.json` para que os grupos de cores do Graph View acompanhem o Vault automaticamente entre máquinas. A nota [[Legenda_Cores_Grafo]] documenta a convenção humana; o JSON é a configuração executável que o Obsidian carrega ao abrir o Cofre.

## 🛠️ Aplicação Técnica
- **Fonte única:** `50_System/grafo_cores.json` — um grupo por entrada: `id`, `emoji`, `cor` (hex), `nome`, `prefixos` (início do nome do arquivo), `tags` (ex.: `projeto/x`), `paths` (ex.: `30_Atlas`). Ninguém escreve query do Obsidian à mão.
- **Gerador:** `python3 50_System/grafo_cores.py` monta a query de cada grupo, conta as notas que ele casa de verdade, reescreve **só** `colorGroups` em `.obsidian/graph.json` (o resto do arquivo é preservado) e regenera [[Legenda_Cores_Grafo]] (`generated: true`, com a contagem). Relata grupo com zero notas e tag `projeto/*` com notas mas sem grupo — os dois sinais de JSON desatualizado. Flags: `--dry-run` (só relatório), `--podar` (omite grupos vazios; é o que o vault derivado do curso usa, ver [[Cofre_Derivacao_Vault_Curso]]).
- **Quando roda:** no `sync_wiki.sh` ao lado do `catalog.py`, e sempre que um projeto novo entra (o [[EXTRACAO_PROJETO]] e o Projeto Kit mandam "entrada no JSON + rodar o script"). Testes: `python3 -m unittest discover -s 50_System/tests`.
- `.obsidian/graph.json` **continua versionado** (é o que o Obsidian lê; viaja com o vault entre máquinas). `.obsidian/workspace*` e `cache` continuam no `.gitignore`.
- Em máquina nova: clonar e abrir como Vault. O `graph.json` já vem com as cores.

## ⚠️ Pontos de atenção
- A legenda sozinha **não aplica** cores; ela é gerada e serve de documentação. Editar a legenda à mão é perdido na próxima geração — edite o JSON.
- Se `colorGroups` virar `[]`, todas as cores somem. Como o arquivo é versionado, o Git passa a revelar a regressão e permite restaurá-la.
- Não versionar `workspace.json`: sincronizar estado de janelas e painéis causa ruído e conflitos desnecessários entre dispositivos.
- **Depois de rodar o script, no Obsidian (1.13.x), nesta ordem: (1) fechar toda aba de Graph View; (2) `Ctrl+P` → "Reload app without saving"; (3) abrir o grafo de novo (`Ctrl+G`).** Motivo, verificado em 2026-09-26: o Obsidian não relê o `graph.json` com o vault aberto e regrava os grupos que tem em memória sempre que salva o estado do grafo (abrir as configurações já basta). Fechar e reabrir o app normalmente **grava antes de fechar** e desfaz a geração. E uma aba de grafo **aberta durante o reload** é restaurada sem opções, nasce com `colorGroups` vazio e grava isso por cima do arquivo antes de ler — foi o que deixou o Cofre todo branco três vezes. Se já regravou: `git checkout .obsidian/graph.json` e repetir os 3 passos.
- As cores que valem são as do `graph.json` (o que o Obsidian aplica). Em 2026-09-26 a legenda manual estava com 8 hex diferentes do arquivo; a fonte única foi ajustada para as cores reais.
- Histórico: até 2026-09-26 a tabela e o `colorGroups` eram editados à mão "no mesmo commit" — e divergiram (Banca Central estava no `graph.json` e não na legenda). Foi o que motivou a fonte única.

## 🔗 Conexões
- MOC: [[Index]] (Governança)
- Relacionados: [[Legenda_Cores_Grafo]], [[GUIA_USO_COFRE]], [[WIKI_SCHEMA]]
