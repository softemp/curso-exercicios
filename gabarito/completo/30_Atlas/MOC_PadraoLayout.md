---
type: moc
status: evergreen
aliases: [MOC padraoLayout, hub do modelo de layout]
summary: "Hub do padraoLayout — o frontend de referência que os projetos novos copiam."
tags: [meta, wiki, status/evergreen, area/frontend, tipo/referencia, projeto/padraolayout]
source: "padraoLayout@7088ea6"
created: 2026-08-31
updated: 2026-08-31
---
# 🎨 MOC: padraoLayout — Modelo de Layout SoftEmp

Hub do **padraoLayout** — frontend de referência (React 18/Vite/TS, **dados mocados, sem
backend**) que materializa o piso de UI da casa em telas navegáveis, para ser **copiado** no
início de projeto novo. Ramificado de [[MOC_Projetos]] (padrão [[Project_Isolation_Pattern_Wiki]]).

> O contrato que ele cumpre é Base_UI_Kit_Padrao_Projeto; o que faz o contrato ser aplicado
> é Base_Gate_Piso_UI_Novo_Projeto. Este projeto é a **implementação de referência** dos dois.

## 🏛️ Arquitetura & Mapas
- [[PadraoLayout_Arquitetura]]: stack decidida, topologia por feature, a API falsa como fronteira, telas entregues.
- [[PadraoLayout_Modulos]]: o que cada peça de `shared/ui`, `charts`, `export` e `api` faz — e o que copiar primeiro.
- [[PadraoLayout_Patterns]]: estado da listagem na URL, cor só por token, `ui-prefs` como único acesso ao storage, saldo só por movimento.
- [[PadraoLayout_Gotchas]]: as sete pegadinhas reais — quatro delas passavam pelo build.

## 📐 Decisões (ADRs)
- [[PadraoLayout_ADR_001_Api_Falsa_Com_Contrato_Real]]: mock que pagina, ordena e demora — para os estados de carregando/vazio/erro existirem no modelo.
- [[PadraoLayout_ADR_002_Matriz_De_Permissoes]]: matriz módulo × ação em vez de caixas por módulo; gravação da matriz inteira.
- [[PadraoLayout_ADR_003_Pdf_De_Texto_No_Cliente]]: PDF de texto no cliente por import dinâmico; auditável segue no servidor.

## 💰 Domínio
- [[PadraoLayout_Financeiro_Contas]]: contas a pagar/receber — vencido derivado, competência × caixa, recorrência materializada, pago imutável.

---
- MOC Pai: [[MOC_Projetos]] · vizinhos: [[MOC_Frontend]] · [[MOC_Stack_Base]] · [[MOC_Padroes_Reutilizaveis]]
