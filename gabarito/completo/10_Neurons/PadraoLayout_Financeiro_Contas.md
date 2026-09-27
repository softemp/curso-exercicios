---
type: neuron
status: evergreen
aliases: [contas a pagar e receber, modelo financeiro, vencido derivado, competência x caixa, recorrência materializada, baixa parcial, estorno, financeiro do padraoLayout]
summary: "Modelo de contas a pagar/receber do padraoLayout: vencido é derivado, período tem base competência × caixa, recorrência nasce materializada, pago é imutável (volta por estorno) e todo saldo muda por movimento com saldo_após."
tags: [status/evergreen, area/frontend, area/financeiro, tipo/implementacao, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04 (regras derivadas de ProjetoBC_Gestao_Financeira_Contas e ProjetoBC_CompanyAccount_Ledger)"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · Contas a pagar e a receber

## 💡 Conceito

O módulo financeiro do modelo (`/financeiro/contas`) existe porque o autor não tinha, em nenhum
projeto, uma referência boa de contas a pagar/receber. Ele não inventa regra: **materializa em
tela** o que o Cofre já sabia do projetobc (ProjetoBC_Gestao_Financeira_Contas,
ProjetoBC_CompanyAccount_Ledger), que é conhecimento caro de reconstruir.

Cinco invariantes fazem a diferença entre um CRUD de lançamentos e um módulo financeiro que
aguenta uso real.

## 🛠️ Aplicação Técnica

### 1. "Vencido" é derivado, nunca gravado
`estaVencido(l)` = pendente ou parcial **e** vencimento no passado. Não existe status
`VENCIDO` em lugar nenhum: ele é opção de **filtro** e é **selo** na tabela. Gravar o estado
quebraria tudo que exige "pendente" (baixa, cobrança automática, cancelamento de série) e
criaria um valor que envelhece sozinho — quem grava precisa de um cron para consertar o que o
tempo estragou.

### 2. Duas bases de período no mesmo lugar: competência × caixa
Um botão na barra de recorte troca o eixo de data de **todas** as abas:
- **competência** → pelo `vencimento` (o mês a que o fato pertence, o que o contador vê);
- **caixa** → pelo `pagamentoEm ?? vencimento` (pagos entram pela data do pagamento; pendentes seguem pelo vencimento).

Sem esse seletor, a tela financeira e o relatório contábil mostram números diferentes e ninguém
sabe qual está certo. O fim do período é o **dia inteiro** (23:59:59) — comparar com 00:00 corta
silenciosamente o último dia.

### 3. Recorrência materializada na criação
Marcar "repetir" cria as N parcelas **agora**, cada uma um registro com vencimento, valor
integral e baixa próprios (`criarLancamento()`). Guardar só a regra empurra para o futuro a
pergunta "quanto tenho a pagar em março?" — que é justamente a pergunta que o módulo existe
para responder. `somarMeses()` fixa o dia 1 antes de somar: `setMonth` faz dia 31 transbordar
de mês.

### 4. Trava de duplicidade que mostra o que já existe
Mesma contraparte, mesmo valor, vencimento a até 3 dias e ainda em aberto → a criação é barrada
com `DuplicidadeError`, o formulário **exibe o lançamento existente** e oferece confirmação
consciente. Bloquear de vez faz o operador cadastrar torto (valor 0,01 a mais) para escapar da
trava — e aí a duplicata existe e não é detectável.

### 5. Pago é imutável; a volta é o estorno, pelo livro-razão
`darBaixa()` recusa registro já pago; editar e cancelar ficam desabilitados na tabela. O caminho
de volta é `estornarBaixa()`, que lança um **movimento novo** na conta com o saldo resultante —
o saldo nunca é reescrito. Baixa **parcial** é caminho normal: o registro fica em `parcial` com
o saldo em aberto e recebe outra baixa. Lançamento sem conta vinculada não move saldo nenhum.

### Telas
Visão geral (entradas × saídas por semana, saldo acumulado em cartão separado — dois eixos y
inventariam correlação; próximos vencimentos; para onde vai o dinheiro), A receber, A pagar,
Categorias (com **slug estável**: renomear no painel não quebra relatório) e Contas bancárias
com o extrato de movimentos.

## ⚠️ Pontos de atenção
- **Competência ≠ vencimento.** O formulário pede os dois e explica: competência é o mês do fato, vencimento é a data do dinheiro. Deduzir um do outro é o erro que faz o relatório mensal não fechar.
- A categoria pertence ao tipo: trocar "a pagar" por "a receber" **limpa** a categoria escolhida, senão nasce despesa dentro da receita.
- No projeto real, o filtro de vencido, a base caixa e a busca textual viram condições com `OR` interno — e todas precisam viver dentro de um `AND` no `where` do Prisma (ProjetoBC_Gestao_Financeira_Contas).

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]] · [[MOC_Financeiro]]
- Leitura dos mesmos lançamentos por outros eixos: Base_Relatorio_Financeiro_Tres_Oticas
- Origem das regras: ProjetoBC_Gestao_Financeira_Contas · ProjetoBC_CompanyAccount_Ledger · ProjetoBC_Client_Ledger_Adjustments
- Hub: [[PadraoLayout_Arquitetura]] · convenções: [[PadraoLayout_Patterns]]
