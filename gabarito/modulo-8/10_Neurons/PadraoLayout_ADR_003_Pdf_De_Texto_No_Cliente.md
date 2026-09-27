---
type: neuron
status: evergreen
aliases: [ADR 003 padraoLayout, pdf no cliente, jspdf autotable, quando gerar pdf no servidor, exportar listagem]
summary: "Decisão: listagem operacional gera PDF de TEXTO no cliente (jsPDF+autoTable, import dinâmico); documento auditável continua no servidor — e rasterizar a tela não é opção em nenhum dos dois."
tags: [status/evergreen, area/frontend, tipo/parecer, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · ADR 003 — PDF de texto no cliente

## 💡 Conceito

**Contexto.** O modelo precisa exportar listagem em CSV, PDF e impressão, sem backend. Três
caminhos existiam: rasterizar a tela (`html-to-image` + jsPDF), gerar PDF de texto no cliente,
ou deixar tudo para um servidor que aqui não existe.

**Decisão.** **PDF de texto no cliente** com `jspdf` + `jspdf-autotable`, carregado por
**import dinâmico**; documento auditável (contrato, nota, recibo) permanece responsabilidade do
servidor no projeto real.

**Por quê.** Rasterizar produz um arquivo pesado, não pesquisável e que diverge entre
dispositivos — e some do arquivo justamente a coluna que a pessoa queria buscar. O PDF de texto
sai pesquisável e selecionável, e a `autoTable` traz de graça o que é caro fazer à mão:
cabeçalho repetido em toda folha e linha que não parte ao meio.

**Consequência.** Entram ~400 KB de dependência, que **não viajam no bundle inicial**: só baixam
quando alguém clica em PDF. E fica registrado o limite: PDF que precisa ser gerado sem
navegador (cron, envio por WhatsApp) exige pipeline no servidor —
ProjetoBC_BetReceipt_PDF_Pipeline.

## 🛠️ Aplicação Técnica

- `showHead: 'everyPage'` (cabeçalho em toda folha) + `rowPageBreak: 'avoid'` (linha inteira desce) + margem inferior reservada para o rodapé "Página X de Y", escrito em **segunda passada** porque o total só existe no fim.
- Colunas por **peso relativo** (`peso`), convertidas em milímetros sobre a largura útil: a soma bate exatamente com a área da folha.
- Uma definição de colunas (`ColunaExport`) serve CSV, PDF e impressão; `valorCsv` opcional entrega **número cru** para a planilha somar.
- Verificação feita fora do navegador com as 247 linhas de exemplo: 18 páginas, cabeçalho nas 18, texto extraível por `pdftotext`.

## ⚠️ Pontos de atenção
- `jspdf-autotable` é CommonJS e a função sai em `default.default` conforme o interop — resolver em tempo de execução ([[PadraoLayout_Gotchas]]).
- Impressão não é o mesmo caminho: usa a folha `@media print` do `index.css`, não o jsPDF. São dois artefatos com a mesma definição de colunas.
- Exportar sempre a lista **inteira com os filtros aplicados**, nunca a página visível — o operador que exporta espera o recorte, não a tela.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]]
- Padrão genérico extraído: Base_Export_Tres_Formatos_Quebra_De_Pagina
- Escolha por stack: Base_Frontend_Listagens_DataTable · pipeline no servidor: ProjetoBC_BetReceipt_PDF_Pipeline
- Peso de bundle: ProjetoBC_Frontend_Bundle_Size
