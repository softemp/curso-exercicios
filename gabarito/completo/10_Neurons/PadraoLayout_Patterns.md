---
type: neuron
status: evergreen
aliases: [convenções do padraoLayout, padrões do modelo de layout, estado na URL, tokens de cor no layout, regras do modelo]
summary: "As convenções não-óbvias do modelo: estado de listagem na URL com chaves declaradas, cor só por token (inclusive nos gráficos), localStorage só por ui-prefs, um caminho único para saldo, e configuração de acesso fora do JSX."
tags: [status/evergreen, area/frontend, tipo/pattern, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · Patterns

## 💡 Conceito

Convenções que **quem não conhece quebra sem perceber** — cada uma nasceu de um problema real
durante a construção, não de gosto.

## 🛠️ Aplicação Técnica

### 1. Estado da listagem mora na URL — e cada tela declara suas chaves
`useTableState({ sortBy, sortDir, filtros: ['status', 'categoria', 'conta'] })` lê e escreve
`?page=&perPage=&sortBy=&sortDir=&search=&<filtros>`. Ganho: link compartilhável, F5 sem perder
o lugar, e o "voltar" do navegador devolvendo a mesma página.

**A parte que morde:** o hook só entrega em `filters` as chaves **declaradas**. Um filtro
esquecido na lista entra na URL, pinta o `<select>` de escolhido e **não chega na consulta** —
parece funcionar e não filtra nada. Aconteceu com o filtro de meio de pagamento das faturas.

### 2. Cor só por token, inclusive dentro do gráfico
Todo hex vive em `src/index.css`. Componente usa classe semântica (`bg-surface`, `text-muted`);
gráfico lê a CSS var por `useChartTokens()`, que **relê quando o tema troca**. Séries têm ordem
fixa (`--series-1..6`), validada para daltonismo nos dois temas: cor segue a entidade, nunca a
posição no ranking — filtrar uma série não pode repintar as sobreviventes.

### 3. `localStorage` só através de `ui-prefs.ts`
Um arquivo, três chaves (tema, sidebar recolhida, linhas por página). Centralizar é o que torna
verificável a regra que importa: **token nunca vai para o storage**
([[Base_Seg_Token_Storage]]). O tema é carimbado no `<html>` por um script no `index.html`
antes da primeira pintura — sem isso, o tema escuro pisca branco no carregamento.

### 4. Saldo só muda por movimento, com o saldo resultante gravado junto
Vale nos dois lugares onde há dinheiro: a conta do cliente (`registrarMovimento()` em
`mock-db.ts`) e as contas da empresa (`darBaixa()`/`estornarBaixa()` em `financeiro.ts`). O
extrato lê o último `saldoApos`; nunca soma a coluna. É o que permite responder "de onde veio
esse saldo?" linha a linha — e o que faz o estorno ser um **movimento novo**, não um número
reescrito (ProjetoBC_CompanyAccount_Ledger).

### 5. O que o produto liga é configuração, não JSX
`app/auth-config.ts` declara identificadores aceitos, 2FA e canais de recuperação;
`app/navigation.ts` declara o menu (e é a fonte do título da navbar). Ligar um canal ou uma tela
não deveria pedir edição de componente.

### 6. Auxílio externo PREENCHE, nunca trava
A busca de endereço por CEP (`buscarCep()`) preenche logradouro, bairro, cidade e UF — e quando
falha, a tela avisa e **continua aceitando o endereço digitado à mão**. Formulário que só aceita
o dado vindo do serviço externo para de funcionar junto com o serviço, e sempre no pior dia.
Vale para qualquer autocompletar de fora: CEP, CNPJ, catálogo de produto.

### 7. Ação irreversível passa por diálogo que **nomeia o alvo**
`ConfirmarAcao` exige rótulo de ação ("Excluir em definitivo", nunca "OK") e a mensagem cita o
registro. Ação reversível (mover para a lixeira) também confirma, com outro peso e outra cor.

### 8. Registro com efeito não se reescreve
Saldo muda por movimento, baixa volta por estorno, contrato assinado muda por **aditivo** — e
nenhuma tela oferece "editar" para esses registros. A forma genérica está em
Base_Correcao_Por_Registro_Novo; o que é derivado (vencido, vencendo, reajuste devido)
segue o lado oposto: calculado na leitura, nunca gravado.

### 9. Módulo-espelho reusa a forma e muda o risco
Contratos de cliente e de fornecedor têm a **mesma forma** (vigência, aditivo, aviso prévio,
reajuste) — e construir o segundo como cópia do primeiro é desperdiçar a única parte que
importa. O que muda é **de que lado o dinheiro corre risco**: no cliente, receber; no fornecedor,
pagar mais do que o acordado, renovar sozinho e pagar a quem está irregular. A pergunta ao abrir
um módulo-espelho é *"o que é diferente quando o papel se inverte?"* — a resposta é o módulo.

### 10. Estado de espera com a FORMA da tela
`Skeleton` desenha o esqueleto do conteúdo (cartões, linhas da tabela), não um spinner no meio
do vazio; e a paginação usa `keepPreviousData` do Query para a tabela não piscar em branco a
cada clique.

## ⚠️ Pontos de atenção
- **Nada de `max-w` no `<main>`** — a régua é `px-2 sm:px-4 lg:px-6` e a escala 2→4→6 vale para `gap` e `space-y` (Base_Layout_Largura_Total_E_Responsivo).
- Gráfico novo nasce com `isAnimationActive={false}` (Base_Frontend_WebView_GPU_Distorcao) e com a alternância Gráfico ↔ Tabela do `ChartCard`.
- Um eixo por gráfico: saldo acumulado e fluxo semanal vivem em **cartões separados**, porque dois eixos y inventam uma correlação que não está no dado.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]] · [[MOC_Padroes_Reutilizaveis]]
- Hub: [[PadraoLayout_Arquitetura]] · mapa: [[PadraoLayout_Modulos]] · pegadinhas: [[PadraoLayout_Gotchas]]
- Regras de base: Base_Layout_Design_Tokens · Base_Frontend_Estado_Servidor_Vs_Ui · Base_UI_Listagem_Tabela_Obrigatorio
