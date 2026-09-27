---
type: neuron
status: evergreen
aliases: [módulos do padraoLayout, mapa do modelo de layout, o que tem no shared/ui, componentes do kit, onde mora cada coisa no layout modelo]
summary: "Mapa do padraoLayout: o que cada peça de shared/ui, shared/charts, shared/export e shared/api faz, com quem conversa e o que copiar primeiro num projeto novo."
tags: [status/evergreen, area/frontend, tipo/referencia, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · Módulos

## 💡 Conceito

O mapa de quem é quem. Serve para duas perguntas: **"onde mexo para mudar X?"** e, no projeto
novo, **"o que copio primeiro?"** — a resposta da segunda é sempre `shared/` inteiro, depois
`app/`, e as `features/` só como exemplo a apagar.

## 🛠️ Aplicação Técnica

### `shared/ui` — o kit

| Peça | Faz | Não-óbvio |
|---|---|---|
| `AppShell` | Moldura da área logada: sidebar + navbar + `<main>` | `<main>` sem `max-w`, régua `px-2 sm:px-4 lg:px-6`; um só por projeto |
| `Sidebar` | Navegação em níveis, faixa recolhível, drawer mobile | Colapso é estado de **desktop**; submenu recolhido vira flyout em portal |
| `Navbar` | Título, busca, tema, sino, dropdown do usuário | Título derivado de `navegacao` + mapa `FORA_DO_MENU` para rotas fora dela |
| `Dropdown` / `UserMenu` / `NotificationBell` | Menus da navbar | Badge do sino **some no zero**; `Perfil` e `Sair` moram aqui, não na sidebar |
| `DataTable` | Tabela única do projeto (TanStack headless) | `manualPagination/Sorting/Filtering`: não ordena nada em memória |
| `Pagination` / `PageSizeSelect` | Rodapé da tabela | `DEFAULT_PAGE_SIZE = 10`; janela de páginas com elipse |
| `Modal` / `ConfirmarAcao` | Diálogo com foco preso, Esc, clique fora, trava de rolagem | Devolve o foco a quem abriu; o botão diz a ação, nunca "OK" |
| `Button` / `Field` (`Input`, `Select`, `Checkbox`) | Controles | `Button loading` desabilita: anti-duplo-submit |
| `StatTile` / `Sparkline` / `Meter` | Números em destaque | Delta colorido por direção × o que é bom no indicador |
| `Badge` | Selo de status | Exige rótulo e desenha ícone — status nunca por cor sozinha |
| `BotaoExportar` | CSV, PDF e impressão | Formatos ligam/desligam por prop; um formato só vira botão direto |
| `Skeleton` / `EmptyState` / `PageHeader` / `Avatar` / `Card` | Apoio | Skeleton em CSS global (carrega em todos os painéis) |

- **`CartaoResumo` + `GradeResumo`** — o cartão de número que abre quase toda página (rótulo · valor · nota, com `Skeleton` embutido quando o valor ainda é nulo) e a grade canônica. Nasceu tarde, substituindo 14 cópias manuais (Base_UI_Superficie_Repetida_Vira_Primitivo).

### `shared/charts`
`tokens.ts` lê as CSS vars de série (`--series-1..6`) e as relê quando o tema troca — nenhum hex
vive dentro de gráfico. `ChartCard` embrulha todo gráfico com legenda e **alternância
Gráfico ↔ Tabela**. `ChartTooltip` substitui a tooltip da Recharts (que vem com fundo branco
fixo e quebra no tema escuro). Gráficos: `ReceitaArea`, `CanaisBarras`, `CategoriasBarras`.

### `shared/export`
`csv.ts` (separador `;` + BOM), `pdf.ts` (jsPDF + autoTable por import dinâmico),
`DocumentoImpressao.tsx` (portal + folha de impressão do `index.css`), `tipos.ts` com o
contrato `ColunaExport` que serve as três saídas. Ver
Base_Export_Tres_Formatos_Quebra_De_Pagina.

### `shared/api` — a API falsa
- `mock-db.ts` — clientes, KPIs, séries e o **livro-razão por cliente** (`registrarMovimento()` é o único caminho que mexe no saldo);
- `api.ts` — listagem canônica, lixeira (`moverParaLixeira`/`restaurarCliente`/`excluirDefinitivo`), acesso (`login`, `verificarSegundoFator`, `destinosRecuperacao`);
- `rbac.ts` — papéis, módulos, permissões e `salvarPermissoesDoPapel()`;
- `operacao.ts` — faturas, recebimentos, conciliação, auditoria, integrações;
- `financeiro.ts` — contas a pagar/receber, com `estaVencido()`, `saldoAberto()`, `criarLancamento()`, `darBaixa()`, `estornarBaixa()`;
- `comissoes.ts` — a obrigação que nasce num evento e vence noutro (Base_Obrigacao_Provisionada_Vs_Devida): `vendaFoiPaga()` confere o lançamento a receber da venda e `liberarComissao()` **recusa** enquanto o cliente não pagou; `pagarComissoes()` é lote por vendedor (só o liberado), `estornarComissao()` recusa comissão já paga — vira débito no próximo fechamento —, `percentualPorFaixa()` sai do acumulado do período e fica **copiado** no lançamento, e `simularBase()` compara faturamento × margem como base de cálculo (Base_Limite_Na_Grandeza_Certa);
- `contratos-fornecedores.ts` — o lado que paga: `renovouSemDecisao()` (aviso vencido em contrato que renova sozinho, com o custo do ciclo), `desviosDePreco()` confrontando a tabela do contrato com os pedidos reais de `compras.ts`, `temCertidaoVencida()` e `desempenhoFornecedor()` (prazo prometido × pedidos atrasados);
- `indicadores.ts` — a única API que **não tem dados próprios**: `listarIndicadores()` calcula os dez KPIs a partir de vendas, financeiro, chamados, projetos, estoque e clientes, cada um com `fonte`/`rotaFonte`, `direcao` e `contrapesoId`; `ritmo()` compara com `esperadoAteAgora()` e `farol()` respeita a direção da meta;
- `reservas.ts` — hospedagem por **noite**: `noites()` conta a unidade cobrada e `conflita()` usa intervalo semi-aberto (`aIni < bFim && aFim > bIni`), então a saída de uma reserva e a entrada de outra no mesmo dia **não** colidem; `unidadeLivre()` deriva disponibilidade das reservas (sem campo `ocupado`), `bloquearUnidade()` grava manutenção como OCUPAÇÃO e não como estado, `tarifaDaNoite()` alimenta as `diarias[]` com o valor congelado por noite, e `mapaOcupacao()` monta o **espelho** com o dia partido em duas metades (`CelulaMapa` tem `noite | chegada | saida`, desenhadas como triângulos na mesma diagonal — o dia de virada mostra dois hóspedes e segue clicável) (Base_Reserva_De_Periodo_Semiaberto);
- `chat.ts` — atendimento ao vivo com o relógio do cliente: `relogios()` devolve TRÊS (espera na fila, primeira resposta e silêncio corrente) e pausa em `aguardando_cliente`; `transferir()` cria um REGISTRO pendente de aceite (motivo obrigatório, destino pré-definido, recusa offline/ausente/no limite de capacidade) e `aceitarTransferencia()` **não toca** em `abertaEm` nem em `primeiraRespostaEm`; `devolverParaFila()` é a saída honesta e `definirStatus()` recusa sair da mesa com conversa na mão (Base_Repasse_Mantem_Dono_E_Relogio);
- `chamados.ts` — dois relógios: `minutosParaPrimeiraResposta()` (só resposta humana para o relógio) e `slaResolucaoConsumido()` sobre `minutosUteis()`, que desconta o tempo em `aguardando_cliente`; `prioridadeDe()` é matriz urgência × impacto, e `reabrir()` incrementa o contador que serve de contrapeso;
- `projetos.ts` — o par que não se separa: `consumoHoras()` × `avancoFisico()` e o `desvio()` entre eles; estrutura em fases → tarefas com `pesoFase()` **derivado das horas estimadas**, `horasPlanejadas()` para confrontar com o orçado, `capacidadeEquipe()`/`ocupacao()` (6h por dia útil) e `replanejar()`, que guarda o antes → depois sem tocar na linha de base;
- `rh.ts` — quadro de pessoas com o **salário filtrado no servidor** (`listarColaboradores()` devolve `salario: null` sem permissão) + `registrarAcessoSensivel()` na leitura, e o relógio das férias em `emDobra()`/`feriasVencendo()` sobre os períodos aquisitivo e concessivo;
- `vendas.ts` — o outro lado de compras: `confirmarVenda()` **reserva** o estoque (sem mover o físico) e recusa sem disponível, `faturarVenda()` libera a reserva + baixa no kardex + cria a conta a receber, e o gatilho de aprovação é `margemVenda()` contra `MARGEM_PISO` — com faixa não aprovável abaixo de zero;
- `compras.ts` — o módulo que **amarra** os outros: `aprovarPedido()` recusa quem criou o próprio pedido, `alcadaNecessaria()` diz a faixa pelo valor, e `receberPedido()` faz as três coisas juntas (baixa no pedido + `registrarMovimento()` no estoque com o custo da nota + `criarLancamento()` a pagar), devolvendo as divergências da conferência;
- `estoque.ts` — kardex como livro-razão (`registrarMovimento()` é o único caminho: entrada recalcula o custo médio ponderado, saída consome pelo vigente e é **recusada** acima do disponível) + os derivados `disponivel()`, `pontoDePedido()`, `precisaRepor()` e `diasDeCobertura()`;
- `tarefas.ts` — quadro e lista sobre o mesmo recorte: `obterQuadro()` agrupa por coluna (atrasada primeiro, depois prioridade), `moverTarefa()` **recusa** quando a coluna estourou o limite (com `forcar` como saída consciente) e os derivados `estaAtrasada()`, `semDono()`, `semPrazo()`;
- `documentos.ts` — repositório com vínculo obrigatório, `enviarNovaVersao()` (a anterior nunca é substituída), os derivados `estaVencendo()`/`estaVencido()` sobre a validade e `criarCompartilhamento()`/`revogarCompartilhamento()`, com prazo de 1 a 30 dias;
- `contratos.ts` — carteira de contratos com os derivados `estaVencendo()`, `prazoDeAvisoPerdido()` e `reajusteDevido()`, mais `criarAditivo()` (**único** caminho para mudar contrato assinado) e `registrarAssinatura()`, que só faz o contrato vigorar quando todas as partes assinaram;
- `relatorios-financeiros.ts` — derivações puras sobre os mesmos lançamentos: `deriveResultado()` (as três óticas, num lugar só), `obterDre()`, `obterFluxoMensal()`, `obterAging()`, `obterCurvaAbc()`, `obterInadimplencia()`;
- `perfil.ts` — perfil, preferências de notificação, `alterarSenha()` (que **exige a senha atual**), sessões (`encerrarSessao()` recusa a sessão atual; `encerrarOutrasSessoes()`), histórico de acesso e códigos de recuperação;
- `empresa.ts` — cadastro da empresa, `buscarCep()` (que **falha de propósito** em CEP inválido, para a tela exercitar o caminho manual) e `instalarCertificado()`, que devolve só metadados.

### `shared/hooks` e `shared/lib`
`useTableState()` guarda o estado da listagem **na URL** (cada tela declara suas chaves de
filtro); `useDebouncedValue()`; `useEhDesktop()`. Em `lib`: `cn()`, `format.ts` (pt-BR
centralizado — inclusive as máscaras `mascaraCnpj()`, `mascaraCep()` e `mascaraTelefoneBr()`),
`ui-prefs.ts` (**único** acesso ao `localStorage`) e `identificador.ts`
(detecta e-mail × telefone × CPF).

### `app/` e `store/`
`providers.tsx` (QueryClient), `navigation.ts` (a árvore do menu — fonte única do menu e do
título da navbar), `auth-config.ts` (o que o produto liga: identificadores, 2FA, canais).
`store/ui.ts` guarda tema e sidebar em Zustand, persistindo por `ui-prefs`.

## ⚠️ Pontos de atenção
- **Copiar `features/` inteiro é erro**: elas são exemplo. O que se copia é `shared/`, `app/`, `store/` e `index.css`.
- `navigation.ts` é fonte única: item novo no menu aparece na sidebar **e** no título da navbar. Rota fora do menu precisa entrar em `FORA_DO_MENU` no `Navbar`.
- `mock-db.ts` usa PRNG com semente fixa — os números não mudam a cada refresh, o que é o que permite comparar dois screenshots.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]]
- Hub: [[PadraoLayout_Arquitetura]] · convenções: [[PadraoLayout_Patterns]]
- Contrato de UI: Base_UI_Kit_Padrao_Projeto · shell: Base_Frontend_App_Shell
- Tabela: Base_UI_Listagem_Tabela_Obrigatorio · Base_Frontend_Listagens_DataTable
