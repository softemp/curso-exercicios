---
type: neuron
status: evergreen
aliases: [padraoLayout, modelo de layout, layout de referência, projeto modelo de frontend, esqueleto de projeto novo, template de frontend SoftEmp]
summary: "Frontend de referência da SoftEmp (React 18/Vite/TS, dados mocados, sem backend): materializa o piso de UI em telas navegáveis para ser COPIADO no início de projeto novo — não é biblioteca, é ponto de partida."
tags: [status/evergreen, area/frontend, area/web, tipo/arquitetura, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04 (2026-08-31 → 2026-08-31, construído com o autor)"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · Arquitetura

## 💡 Conceito

O `padraoLayout` é o **modelo de layout da SoftEmp**: um frontend completo, navegável e
**sem backend**, que existe para ser o ponto de partida de projeto novo. Ele transforma o
contrato escrito em Base_UI_Kit_Padrao_Projeto em tela que se abre e se clica.

**Não é biblioteca, é ponto de partida.** Ninguém instala o padraoLayout; copia-se o esqueleto
e apaga-se o que não serve. A distinção importa: biblioteca versionada obrigaria a manter
compatibilidade com produtos que evoluíram para lados diferentes, e é exatamente o custo que
uma casa de software pequena não paga. O que atravessa projetos é o **pacote e a forma do
componente**, nunca o arquivo copiado de um produto para outro
(Base_Gate_Piso_UI_Novo_Projeto).

**Por que dados mocados e não um backend de brinquedo:** o objetivo é decidir layout, não
arquitetura de servidor. Um backend real no modelo viraria uma segunda base para manter, e o
primeiro projeto que copiasse levaria junto decisões de banco que não são dele.

## 🛠️ Aplicação Técnica

### Stack (decidida, não escolhida por projeto)

| Papel | Pacote |
|---|---|
| Build | `vite` 5 + `@vitejs/plugin-react` + TypeScript 5 (Node 18 no ambiente do autor) |
| Rotas | `react-router-dom` 6, com `lazy()` por rota |
| Estado de servidor | `@tanstack/react-query` 5 |
| Estado global de UI | `zustand` 5 (só UI — tema e sidebar) |
| Tabela | `@tanstack/react-table` 8 (headless, server-side) |
| Formulário | `react-hook-form` + `zod` + `@hookform/resolvers` |
| Estilo | `tailwindcss` 3 sobre design tokens em CSS vars |
| Gráficos | `recharts` 2 |
| Exportação | `jspdf` + `jspdf-autotable` (import dinâmico) |
| Ícones | emoji — sem lib de SVG |

### Topologia

```
src/
  app/         providers (Query), navegação, auth-config
  features/    uma pasta por tela: auth, dashboard, clientes, financeiro,
               financeiro/contas, acessos, auditoria, relatorios,
               configuracoes, componentes, perfil, sistema
  shared/
    ui/        o kit: AppShell, Sidebar, Navbar, DataTable, Modal, Button…
    charts/    ChartCard + gráficos + tokens de cor de série
    api/       API FALSA (mock-db, api, rbac, operacao, financeiro)
    export/    CSV, PDF e documento de impressão
    hooks/     useTableState, useDebouncedValue, useMediaQuery
    lib/       cn, format (pt-BR), ui-prefs, identificador
  store/       estado global de UI (tema, sidebar)
  index.css    DESIGN TOKENS — a única fonte de cor
```

Estrutura **por feature**, não por tipo técnico ([[Base_Estrutura_Feature_Based]]): a tela e o
que só ela usa moram juntos; o que atravessa telas sobe para `shared/`.

### Fronteira que sustenta o resto: a API falsa tem contrato real

`src/shared/api/` não é um punhado de fixtures: é uma API que **pagina, ordena, filtra e
demora**. `listarClientes()`, `listarLancamentos()` e `listarFaturas()` recebem
`{ page, perPage, sortBy, sortDir, search, filters }` e devolvem `{ data, meta }` — o contrato
canônico da casa. Trocar por HTTP de verdade é substituir o corpo das funções.

É o que faz os estados de **carregando, vazio e erro** existirem no modelo em vez de aparecerem
só em produção — ver [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]].

### Telas entregues

Acesso (login com identificador único, 2FA, recuperação por canal), dashboard, clientes
(listagem + lixeira + página de conta com livro-razão), **contratos** de cliente **e de fornecedor** (carteira com alerta de
aviso prévio, aditivos, assinaturas e o confronto preço contratado × praticado —
Base_Acordo_Confrontado_Com_A_Execucao — Base_Alerta_Antes_Do_Prazo_De_Decisao),
**metas e indicadores** (dez KPIs **derivados dos outros módulos**, com ritmo e contrapeso —
Base_Indicador_Se_Calcula_Nao_Se_Digita), **chamados** (fila por SLA com dois relógios e pausa — Base_Sla_Relogio_Que_Pausa),
**reservas** de hospedagem (mapa de ocupação unidade × noite, check-in/out, bloqueio de
manutenção e cadastro de quartos/cabanas com comodidade × inventário —
Base_Reserva_De_Periodo_Semiaberto),
**chat de atendimento** (fila, três relógios e transferência com aceite entre atendentes
pré-definidos — Base_Repasse_Mantem_Dono_E_Relogio),
**projetos** (carteira com consumo × entrega + planejamento por fases e tarefas com estimativa,
prazo e capacidade — Base_Metrica_Que_So_Vale_Em_Par), **RH** (quadro, relógio das férias e
desligamento, com o dado sensível fora do alcance de quem
não precisa — Base_Seg_Dado_Sensivel_Na_Tela), **comissões** (apuração por vendedor ligada ao recebimento: provisionado × liberado × pago × estornado, pagamento em lote e a
base sobre margem — Base_Obrigacao_Provisionada_Vs_Devida),
**vendas** (orçamento → reserva → faturamento,
com a margem no gatilho do desconto —
Base_Limite_Na_Grandeza_Certa, Base_Valor_Copiado_No_Momento_Da_Decisao),
**compras** (pedido com alçada, conferência a três pontas e recebimento que gera estoque e
conta a pagar — Base_Seg_Segregacao_De_Funcoes, Base_Divergencia_Bloqueia_O_Irreversivel),
**estoque** (posição com ponto de pedido + kardex com custo médio —
Base_Custo_Medio_Vs_Lotes, Base_Saldo_Disponivel_Vs_Fisico), **tarefas** (quadro com
limite por coluna + lista — Base_Limite_Que_Recusa,
Base_UI_Interacao_Com_Caminho_Paralelo), **documentos** (repositório com versões, validade e
link externo com prazo —
Base_Anexo_Sempre_Vinculado, Base_Seg_Link_Externo_Com_Prazo), financeiro
([[PadraoLayout_Financeiro_Contas]], faturas, recebimentos, conciliação, **relatórios
financeiros em três óticas** — Base_Relatorio_Financeiro_Tres_Oticas), relatórios,
auditoria, acessos/RBAC em matriz, **configurações da empresa** (dados, endereço com busca por
CEP, marca, fiscal com certificado digital, unidades), comunicação, integrações, **perfil do
usuário** (dados, preferências, matriz de notificações por canal, segurança, sessões ativas e
histórico de acesso — ver Base_Seg_Conta_Do_Usuario_Na_Tela) e o inventário de componentes.

## ⚠️ Pontos de atenção
- **Node 18 no ambiente atual** obrigou Vite 5 e react-router 6 (as versões seguintes exigem Node 20+). Ao copiar num ambiente mais novo, subir as versões é seguro — o código não usa nada removido.
- **`npm run dev` na 5273**; o `dev.sh` de outros projetos não se aplica: aqui não há backend para subir.
- A pasta `features/sistema` guarda a rota `/em-construcao` e o 404 — no projeto real, a primeira some.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]] · [[MOC_Frontend]]
- Contrato que este projeto materializa: Base_UI_Kit_Padrao_Projeto · gate: Base_Gate_Piso_UI_Novo_Projeto
- Kit do projeto: [[PadraoLayout_Modulos]] · [[PadraoLayout_Patterns]] · [[PadraoLayout_Gotchas]]
- Decisões: [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]] · [[PadraoLayout_ADR_002_Matriz_De_Permissoes]] · [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]]
- Base da stack: [[Base_Estrutura_Feature_Based]] · Base_Frontend_Estado_Servidor_Vs_Ui · Base_Layout_Design_Tokens
