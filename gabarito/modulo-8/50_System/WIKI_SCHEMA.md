# LLM Wiki Schema

Este documento define as diretrizes e fluxos de trabalho para a manutenção do Cofre de Neurônios (Claude Code / LLM). Cofre **unificado** em 2026-06-13 (absorveu o vault `brain`): taxonomia hierárquica de tags ([[Tags_Taxonomy]]), Dashboard Dataview ([[Dashboard]]) e catálogo versionado ([[Catalogo_Neuronios]]).

## 🏗️ Arquitetura
- **Raw Sources (`00_Inbox/`)**: Fontes imutáveis (artigos, clips, PDFs).
- **The Wiki (`10_Neurons/`)**: Notas atômicas e interligadas geradas pelo LLM.
- **Maps of Content (`30_Atlas/MOC_*.md`)**: Índices temáticos que agrupam neurônios por domínio.
- **Index Central (`30_Atlas/Index.md`)**: Catálogo central que orquestra os MOCs.
- **Log (`20_Projects/Wiki_Log.md`)**: Registro cronológico de operações.

## 📐 Padrão de Organização (MOCs)
A Wiki segue o padrão de **MOCs em Camadas** (ver [[Wiki_Scalability_MOC_Pattern]]). 
1. Novos neurônios DEVEM ser indexados em um MOC temático.
2. Se um domínio crescer demais, ele deve ser ramificado em um novo MOC.
3. Cada neurônio deve possuir um link de retorno para seu MOC pai no rodapé.

## 🔄 Workflows Operacionais

### 📥 Ingest (Ingestão)
Sempre que uma nova fonte for adicionada à `00_Inbox/`:
1. **Ler**: Analisar o conteúdo da fonte.
2. **Sintetizar**: Identificar novos conceitos ou atualizações para conceitos existentes.
3. **Escrever**:
   - Criar novas notas em `10_Neurons/` usando o `Neuron Template.md`.
   - Atualizar notas existentes se houver novas informações ou contradições.
   - Manter links bidirecionais entre notas.
4. **Indexar**: Adicionar novos itens ao `30_Atlas/Index.md`.
5. **Logar**: Registrar a ação em `20_Projects/Wiki_Log.md` no formato `## [YYYY-MM-DD] ingest | Nome da Fonte`.

### 🔍 Query (Consulta)
Para responder perguntas complexas:
1. **Pesquisar**: Consultar `30_Atlas/Index.md` para encontrar páginas relevantes.
2. **Ler**: Analisar as páginas do Wiki e, se necessário, as fontes originais.
3. **Sintetizar**: Gerar a resposta.
4. **Persistir**: Se a síntese for valiosa, salvá-la como uma nova nota no Wiki ou em `20_Projects/`.

### 🧹 Lint (Manutenção)
Validador versionado: **`50_System/lint.py`** (rodar `python3 50_System/lint.py` na raiz). Cobre:
1. **Frontmatter**: presença do mínimo + `status` em vocabulário válido. `source` ausente → aviso.
2. **Órfãos**: todo neurônio referenciado em ≥1 MOC (arquivos `generated: true` no Atlas não contam — senão o catálogo mascararia órfãos).
3. **Links**: wikilinks resolvíveis (ignora crase e blocos cercados).
4. **Taxonomia de tags** (lê [[Tags_Taxonomy]]): toda tag ∈ vocabulário; exatamente 1 `status/<x>` (= campo `status`); ≥1 `area/`; ≥1 `tipo/`.
5. **Fontes arquivadas**: toda fonte em `40_Archive/` deve linkar ≥1 neurônio (crase não conta) — evita fonte solta no grafo.

**Advisory (não-fatal, qualidade — não conta p/ o status 0/0):** o lint também reporta um backlog informativo:
- `[estrutura]` — sem `## 💡 …` (abertura conceitual) ou `## 🛠️ …` (aplicação). O marcador é o **emoji**, não a palavra literal.
- `[frescor]` — `tipo/implementacao|arquitetura|debug` **verificável contra repo** sem `validated:` ou validado há > 180 dias. "Verificável" = tem tag `projeto/<x>` com repo mapeado em `symbols.py` (mesmo critério do `drift.py`). Um padrão de engenharia ou nota de documentação (`tipo/arquitetura` sem projeto) **não** entra na fila: não existe código contra o que revalidar, e cobrá-lo dessensibiliza o advisory.
- `[repo]` — neurônio de código com `projeto/<x>` **sem repo mapeado** em `symbols.py`. O buraco é no **mapa**, não no neurônio: enquanto o projeto não tiver repo, seu frescor é incontrolável. Fila de "mapear o repo" (ou arquivar o projeto).
- `[linha]` — cita código por **linha** (`arquivo.ts:178`) em vez de por símbolo. Proibido pelo contrato (apodrece).
- `[proveniencia]` — neurônio de código que **afirma um gap/brecha** (proposta não implementada) sem declarar `implemented:` no frontmatter. Evita que a LLM leia proposta como comportamento real.

Use `python3 50_System/lint.py -v` para detalhar. É a fila de melhoria de **excelência**, não um erro.

**Catálogo navegável:** `50_System/catalog.py` gera `30_Atlas/Catalogo_Neuronios.md` (`generated: true`) — panorama + visão por projeto/MOC/tag com a frase-conceito de cada neurônio. Regenerar após cada ingest (o `sync_wiki.sh` já o faz). É só leitura: nunca editar à mão.

### 🔬 Verificação contra o código (símbolos como âncoras)
Como todo neurônio de código cita **por símbolo** (`Classe.metodo()` em `arquivo.ts`), esses símbolos viram âncoras verificáveis contra o repo-fonte. Dois utilitários exploram isso (mapa projeto→repo em `50_System/symbols.py`):
- **`drift.py`** — verifica contra o repo, em dois níveis: **(a) símbolos** (`Classe.metodo()` em `arquivo.ts` — método sumiu? = **drift forte**) e **(b) arquivos citados isoladamente** (`arquivo.ts` — existe? não = **a revisar**, menor severidade: pode ser lib externa/casing/movido). Neurônios `implemented: false` (propostas) são **pulados**. Prioriza revalidação por **mudança**, não por idade (complementa o `revalidate.py`). `python3 50_System/drift.py [projeto] [-v]`.
- **`symbol_index.py`** — gera `30_Atlas/Indice_Simbolos.md` (índice reverso `arquivo-fonte → neurônios`). **Pre-flight:** antes de editar um arquivo do código, consulte `python3 50_System/symbol_index.py <arquivo>` para ver o que o cérebro já sabe. Regenerar após ingest.

Checagens manuais complementares: resolver contradições entre fontes; propor tópicos para lacunas no índice.

## 🧬 Frontmatter

**Mínimo obrigatório (todo neurônio):** `type`, `status`, `tags`, `created`.

```yaml
---
type: neuron
status: seedling | incubating | evergreen | archived
aliases: [sinônimos, keywords de busca]
summary: "1 linha — a essência greppável do neurônio"
tags: [status/<status>, area/<area>, tipo/<tipo>]   # ver [[Tags_Taxonomy]]
source: "origem do conhecimento (repo@commit, sessão, doc)"
created: YYYY-MM-DD
updated: YYYY-MM-DD
validated: YYYY-MM-DD   # obrigatório p/ tipo/implementacao|arquitetura|debug
---
```

**Status (vocabulário canônico, único):** `seedling` → `incubating` → `evergreen` → `archived`.
- `seedling` 🌱 rascunho. `incubating` 🌿 em revisão. `evergreen` 🌳 maduro/mantido. `archived` 🗄️ obsoleto (mover p/ `40_Archive/`).
- A tag `status/<x>` **deve casar** com o campo `status`.

**Campos recomendados/reconhecidos:**
- **`summary`** — 1 linha com a essência (o que torna o neurônio achável por `grep`/scan sem abrir; alimenta o catálogo).
- **`aliases`** — sinônimos/keywords que você usaria para buscar o conceito.
- **`source`** — origem (recomendado; lint avisa se faltar). Para código: `repo@commit` ou caminho.
- **`validated: AAAA-MM-DD`** — data em que foi **conferido contra o código**. Obrigatório (advisory) em `tipo/implementacao|arquitetura|debug`; re-bumpe ao reconferir.
- **`implemented: true | false | partial`** — **proveniência no nível-neurônio.** `true` = descreve código que existe; `false` = proposta/gap/brecha **ainda não implementada** (o agente não deve citá-la como realidade); `partial` = mistura fato e proposta. Obrigatório (advisory `[proveniencia]`) quando o neurônio afirma um gap/brecha. Aceita data (`implemented: AAAA-MM-DD`) p/ marcar quando passou a existir.
- Outros: `updated`, `commits`.

**Citar por símbolo, não por linha:** referencie `Classe.metodo()` / `arquivo.ts` — **nunca** `arquivo.ts:442`. Números de linha apodrecem a cada commit; nomes de símbolo sobrevivem e mantêm o neurônio confiável por mais tempo. (Verificável por `drift.py`; indexado por `symbol_index.py`.)

**Proveniência no nível-linha (opcional, p/ neurônios mistos):** dentro de um neurônio que combina fato e proposta, marque trechos com emoji — **✅ verificado** (existe no código), **🔭 proposto** (roadmap/não implementado), **⚠️ inferido** (não confirmado contra o código). Mantém o leitor (humano ou LLM) ciente do grau de confiança de cada afirmação.

**Forma previsível (excelência p/ LLM):** todo neurônio deve ter `## 💡 Conceito`, `## 🛠️ Aplicação Técnica` e `## 🔗 Conexões` (o lint reporta advisory de estrutura). Forma estável = a LLM extrai a parte certa sem ler tudo.

## 🏷️ Tags
Vocabulário **controlado e hierárquico** definido em [[Tags_Taxonomy]] (`status/ area/ tipo/ projeto/ linguagem/ plataforma/`). Tudo minúsculo, pt-BR, sem sinônimos. O `lint.py` barra tag fora da taxonomia. Todo neurônio: 1 `status/` + ≥1 `area/` + ≥1 `tipo/`.

## ♻️ Revisão periódica (Spaced Review)
| Frequência | Ação |
|---|---|
| Semanal | `seedling` > 14 dias → promover p/ `incubating` ou arquivar |
| Quinzenal | `incubating` → promover p/ `evergreen` ou voltar p/ `seedling` |
| Mensal | Órfãos no `[[Dashboard]]`/Graph View → vincular a MOC; limpar `00_Inbox/` e `40_Archive/` |

Use o `[[Dashboard]]` (Dataview) ou `python3 50_System/catalog.py` para achar o que precisa de atenção.

## 🧩 Composição (Transclusion)
Em MOCs/visões consolidadas, use `![[Neuronio]]` (com `!`) para **embutir** conteúdo sem duplicar; `![[Neuronio#Seção]]` embute uma seção. `[[Neuronio]]` (sem `!`) é só link.

---
*Este esquema deve ser consultado antes de qualquer operação de gestão de conhecimento.*
