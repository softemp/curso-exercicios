# AGENTS.md — meu-cerebro (Cofre de Neurônios)

Este diretório é um **Vault Obsidian** gerenciado como Cofre de Neurônios (Zettelkasten + MOC) e a **memória externa de engenharia da SoftEmp**. Trate o cofre como fonte canônica: não use a memória da sessão como verdade quando houver nota no cofre.

> **Curso:** o próximo módulo está em `<exercicios>/roteiros/`; leia `<exercicios>/.curso.json`. Este arquivo é o ponto de entrada mínimo.

## Bootstrap obrigatório (antes de agir)
1. `30_Atlas/Index.md` — mapa central dos MOCs.
2. `50_System/WIKI_SCHEMA.md` — contrato de ingestão/lint/indexação.
3. `50_System/Tags_Taxonomy.md` — vocabulário de tags.
4. Repo conhecido → `30_Atlas/MOC_Projetos.md` (hub do projeto).

## Kit prescritivo — OBRIGATÓRIO ao criar ou corrigir projeto
Comece por **`30_Atlas/MOC_Stack_Base.md`** ("Stack Base SoftEmp v1"): normas atômicas `Base_*` por camada. Leia os `Base_*` das camadas que a tarefa tocar:
- frontend → `Base_Layout_*`, `Base_Frontend_*`
- backend → `Base_Backend_*`, `Base_Estrutura_Feature_Based`, `Base_Selecao_Stack_Por_Sinais`
- dinheiro/credencial/permissão (faixa Crítico) → **todos os `Base_Seg_*`**
- rodar/deployar → `Base_Infra_*`; **sempre** `Base_Test_*`

Derive stack/estrutura/gates desses neurônios e **cite-os** (`[[Base_...]]`). São norma opinada (`tipo/pattern`, sem `validated`); **o código local existente prevalece** sobre a norma.

## Consulta (cofre como passo 0)
`rg` por `summary:`/`aliases:`/`projeto/<x>`/`area/<y>`; abra **≤3 neurônios** relevantes; cite por wikilink; confira `validated:` (antigo/`seedling` = hipótese, valide no código); declare quando o cofre não cobre.

## Invariantes (faixa Crítico)
Dinheiro em **Decimal** (string formatada à borda externa); idempotência em operação repetível; DEMO/PROD inequívocos; 500 sem vazar `err.message`; **nenhum segredo** em código/log/cofre; "compila" ≠ "pronto" (rode os testes).

## Ao gerar conhecimento
Neurônio atômico em `10_Neurons/` (template em `50_System/Templates/`), ligue ao MOC, registre em `20_Projects/Wiki_Log.md`, rode `python3 50_System/lint.py` (0/0) e `python3 50_System/catalog.py`.

## Tom
PT-BR, técnico, pragmático, direto.

## 🔗 Conexões (grafo do Cofre)
- Contrato completo: CODEX · versão Gemini: GEMINI · diretivas do Claude Code: [[CLAUDE]] · globais da máquina: [[50_System/claude-global/CLAUDE|CLAUDE global]]
- Governança: [[WIKI_SCHEMA]] · [[Tags_Taxonomy]] · [[GUIA_USO_COFRE]] · [[Index]] · Wiki_Log
- Stack: MOC_Stack_Base · MOC_Projetos · Base_Estrutura_Feature_Based · Base_Selecao_Stack_Por_Sinais
