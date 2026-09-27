---
type: neuron
status: evergreen
aliases: [ADR 001 padraoLayout, api falsa com contrato real, mock com latência, por que não fixtures estáticos]
summary: "Decisão: o modelo usa uma API FALSA que pagina, ordena, filtra e demora — em vez de fixtures estáticos — porque é isso que faz os estados de carregando, vazio e erro existirem no layout."
tags: [status/evergreen, area/frontend, tipo/parecer, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · ADR 001 — API falsa com contrato real

## 💡 Conceito

**Contexto.** O modelo não tem backend, e a tentação óbvia é `const clientes = [...]` importado
direto na tela.

**Decisão.** `src/shared/api/` implementa funções `async` que **paginam, ordenam, filtram e
esperam** (latência simulada de 200–600 ms), devolvendo o envelope canônico
`{ data, meta: { total, totalPages, page, perPage } }`.

**Consequência.** O layout exibe de verdade o que um array em memória esconde:

- **carregando** — a tabela mostra esqueleto na primeira carga e mantém a página anterior nas seguintes (`keepPreviousData`), em vez de piscar em branco;
- **vazio** — filtro sem resultado tem tela própria, com o caminho de volta;
- **erro** — a consulta pode falhar e a tela sabe o que dizer;
- **ordem estável** — a ordenação desempata por `id`, senão a paginação repete e perde linhas entre páginas, defeito que só aparece com dado real.

O custo é escrever o filtro/ordenação duas vezes (aqui e no backend do projeto real). Vale:
trocar por HTTP é substituir o corpo das funções, e o contrato já é o que a casa usa.

## 🛠️ Aplicação Técnica

- Contrato: `page`, `perPage`, `sortBy`, `sortDir`, `search`, `filters[<chave>]` → `{ data, meta }`.
- PRNG com **semente fixa** (`mulberry32` em `mock-db.ts`): os mesmos números em qualquer máquina — sem isso, comparar dois screenshots é impossível.
- Mutações mudam o estado em memória (`moverParaLixeira()`, `darBaixa()`, `salvarPermissoesDoPapel()`), e as telas invalidam as consultas certas pelo Query — inclusive as **contagens de badge**, que não podem discordar da tabela ao lado.
- Regras de negócio moram na "API", não na tela: `estaVencido()` é derivado na leitura, `darBaixa()` recusa registro pago, `criarLancamento()` barra duplicidade.

## ⚠️ Pontos de atenção
- Não deixar regra vazar para o componente: se a tela decidir sozinha o que é "vencido", o projeto real vai duplicar a regra no frontend.
- Latência simulada é feature, não enfeite: remover para "ficar rápido" apaga justamente o que a decisão foi comprar.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]]
- Hub: [[PadraoLayout_Arquitetura]] · gotchas: [[PadraoLayout_Gotchas]]
- Contrato de listagem: Base_UI_Listagem_Tabela_Obrigatorio · custo no banco: Base_DB_Indice_Da_Ordem_Da_Pagina
