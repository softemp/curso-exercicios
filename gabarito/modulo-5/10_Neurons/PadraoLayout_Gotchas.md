---
type: neuron
status: evergreen
aliases: [pegadinhas do padraoLayout, bugs do modelo de layout, jspdf-autotable default default, StrictMode spinner travado, sidebar recolhida no mobile, filtro que não filtra]
summary: "As sete pegadinhas reais achadas construindo o modelo — do jspdf-autotable que compila e quebra no clique ao StrictMode que deixa o spinner girando para sempre."
tags: [status/evergreen, area/frontend, tipo/debug, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04 (todas encontradas na construção, 2026-08-31/09-01)"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · Gotchas

## 💡 Conceito

Sete defeitos reais, na ordem em que doem. Nenhum foi teórico: todos apareceram construindo o
modelo, e quatro deles **passavam pelo `tsc` e pelo build**.

## 🛠️ Aplicação Técnica

### 1. 🔴 `jspdf-autotable` é CommonJS: a função sai em `default.default`
`import autoTable from 'jspdf-autotable'` compila, e no navegador vira `undefined` conforme o
interop (Vite, Node e Jest resolvem diferente). **Compila e quebra no clique** — o pior tipo de
defeito, porque o build verde dá confiança falsa. Em `pdf.ts` a resolução é feita em tempo de
execução, testando `mod`, `mod.default` e `mod.default.default`.

### 2. 🔴 Filtro declarado na tela e não no hook entra na URL e não filtra
`useTableState` só devolve em `filters` as chaves passadas em `filtros: [...]`. O `<select>` de
meio de pagamento das faturas pintava a opção escolhida, a URL mudava e **a lista continuava
inteira**. Sem erro, sem aviso: o filtro simplesmente não existia para a consulta.

### 3. 🟠 `StrictMode` + guarda de "ainda montado" = spinner eterno
O padrão `const montado = useRef(true)` com `useEffect(() => () => { montado.current = false })`
quebra no `StrictMode`: o React monta, desmonta e remonta, a limpeza marca `false` e o efeito
seguinte **não desmarca**. O `finally` pulava o `setOcupado(null)` e o botão de exportar girava
para sempre — com o arquivo já baixado. Em React 18 a guarda não protege de nada: foi removida.

### 4. 🟠 Estado de desktop vazando para o mobile
A sidebar recolhida é conceito de desktop. Enquanto `recolhida` era só `sidebarCollapsed`, ao
estreitar a janela o drawer abria como faixa de ícones, sem rótulo e sem submenu — menu
quebrado. Correção: `recolhida = colapsada && ehDesktop` (`useEhDesktop()`).

### 5. 🟠 Flyout dentro de elemento com `transform` não é `fixed` de verdade
O submenu da faixa recolhida precisou ir para um **portal**: a `<aside>` tem `transform`
(as classes de translate), o que a torna o bloco de contenção de qualquer `position: fixed`
dentro dela — e ainda tem `overflow-y-auto`, que cortaria o painel.

### 6. 🟡 Impressão sem esperar a pintura sai em branco
`window.print()` chamado no mesmo tick em que o documento é montado imprime a folha vazia. O
`BotaoExportar` renderiza o `DocumentoImpressao`, espera **dois** `requestAnimationFrame` e só
então chama o diálogo; `afterprint` desmonta.

### 7. 🟡 Objeto de filtros recriado a cada render invalida o memo (e a queryKey)
`useTableState` monta o objeto `filters` toda vez. Colocá-lo na lista de dependências do
`useMemo`/`queryKey` refaz o memo e refaz a consulta sem nada ter mudado. A dependência é a
**assinatura serializada** (`JSON.stringify`), não o objeto.

### 8. 🟡 Régua de espaçamento escrita e mesmo assim derivada

O contrato canônico (`2 → 4 → 6`) existia desde o início e ainda assim conviviam **cinco paddings
de mobile diferentes** em superfícies de card. Causa: o cartão de resumo estava escrito à mão em
14 telas — `StatTile` exige um `Kpi` completo e não servia ao caso simples. Correção: o primitivo
`CartaoResumo`/`GradeResumo` em `shared/ui`, as 14 cópias substituídas, e painel aninhado na régua
truncada `p-2 sm:p-4` para nunca ter mais padding que o card que o contém
(Base_UI_Superficie_Repetida_Vira_Primitivo).

### Limites conhecidos (não são bugs)
- Os dados vivem em memória: recarregar a página devolve tudo ao estado inicial. É proposital — o modelo não tem persistência.
- O bundle do dashboard passa de 400 KB por causa da Recharts; fica em chunk próprio por `lazy()`, então não pesa em quem só abriu o login.
- A conferência visual não foi feita por captura de tela automatizada (a extensão de navegador não alcança o `localhost` desta máquina): o que valida o modelo é `npm run typecheck` + `npm run build` + olho humano.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]]
- Hub: [[PadraoLayout_Arquitetura]] · convenções: [[PadraoLayout_Patterns]]
- Parentes: Base_Frontend_WebView_GPU_Distorcao (animação de gráfico) · ProjetoBC_Frontend_Bundle_Size (peso de lib)
