---
type: nota
status: evergreen
aliases: [Painel, Visao Geral]
tags: [meta, wiki, atlas, status/evergreen]
source: "Unificação claudio+brain — painel dinâmico"
created: 2026-06-13
updated: 2026-06-13
---
# 📊 Dashboard — Painel Dinâmico do Cofre

> [!note] Requer o plugin **Dataview** instalado/ativado no Obsidian. A versão **versionada e
> portátil** (sem plugin) está em [[Catalogo_Neuronios]] (gerada por `50_System/catalog.py`).

---
## 📥 Inbox (pendentes de processamento)
```dataview
TABLE file.ctime AS "Criado"
FROM "00_Inbox"
SORT file.ctime DESC
```

## 🗂️ Neurônios por Projeto
```dataview
TABLE rows.file.link AS "Neurônios", length(rows) AS "Qtd"
FROM "10_Neurons"
FLATTEN file.etags AS tag
WHERE startswith(tag, "#projeto/")
GROUP BY tag AS "Projeto"
SORT length(rows) DESC
```

## 🧠 Conhecimento por Tipo
```dataview
TABLE rows.file.link AS "Neurônios", length(rows) AS "Qtd"
FROM "10_Neurons"
FLATTEN file.etags AS tag
WHERE startswith(tag, "#tipo/")
GROUP BY tag AS "Tipo"
SORT length(rows) DESC
```

## 🧭 Conhecimento por Área
```dataview
TABLE rows.file.link AS "Neurônios", length(rows) AS "Qtd"
FROM "10_Neurons"
FLATTEN file.etags AS tag
WHERE startswith(tag, "#area/")
GROUP BY tag AS "Área"
SORT length(rows) DESC
```

## 🚦 Maturidade — a revisar (não-evergreen)
```dataview
TABLE status AS "Status", file.link AS "Neurônio"
FROM "10_Neurons"
WHERE status != "evergreen" AND status != "archived"
SORT status ASC, file.name ASC
```

## 📈 Estatísticas por status
```dataview
TABLE length(rows) AS "Qtd"
FROM "10_Neurons"
GROUP BY status
```

## ✏️ Atualizados recentemente
```dataview
TABLE status, updated AS "Atualizado"
FROM "10_Neurons"
WHERE updated
SORT updated DESC
LIMIT 15
```

---
## 🔗 Conexões
- MOC: [[Index]]
- Relacionados: [[Catalogo_Neuronios]], [[Tags_Taxonomy]], [[WIKI_SCHEMA]]
