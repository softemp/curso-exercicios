---
type: neuron
status: evergreen
aliases: [ADR 002 padraoLayout, matriz de permissões, tela de RBAC, papel módulo ação, como exibir permissões]
summary: "Decisão: exibir permissões como MATRIZ módulo × ação (não caixas agrupadas por módulo), porque com o conjunto de ações fechado a matriz mostra o buraco — e gravar a matriz inteira, não célula a célula."
tags: [status/evergreen, area/frontend, area/seguranca, tipo/parecer, projeto/padraolayout, linguagem/typescript]
source: "padraoLayout@b6e5c04 (modelagem lida no projetobc: doc de permissões + formulário de papel do admin)"
created: 2026-08-31
updated: 2026-09-01
validated: 2026-09-01
implemented: true
---
# padraoLayout · ADR 002 — Permissões em matriz

## 💡 Conceito

**Contexto.** A modelagem veio do projetobc: papéis × módulos × permissões, com o conjunto de
ações **fechado** (`read`, `create`, `update`, `delete`, `print`, `export`) e um papel por
painel por usuário. Lá a tela agrupa caixas de seleção por módulo (o formulário de papel do projetobc, `RoleForm`).

**Decisão.** Manter a modelagem e trocar a exibição por uma **matriz módulo × ação**, com
atalho de linha ("Tudo/Limpar") e de coluna (conceder "ver" em todos os módulos de uma vez).

**Por quê.** Com as ações fixas, a pergunta que a tela precisa responder é *"o suporte pode
excluir cliente?"*. Na lista agrupada isso é ler 72 rótulos; na matriz é correr o olho até o
cruzamento. A matriz mostra o **buraco** — o que ninguém concedeu — que é justamente o que a
lista esconde.

**Consequência.** A tela vira uma grade densa que exige rolagem horizontal no celular
(a caixa rola, nunca o `<body>`), e ganha dois atalhos que a lista não tinha. Conceder "ver
tudo" é o pedido mais comum e ninguém deveria marcar doze caixas na mão.

## 🛠️ Aplicação Técnica

- **Gravação da matriz inteira**, não célula a célula: `salvarPermissoesDoPapel(papelId, ids[])`. Salvar por clique deixa a tela metade aplicada quando a rede cai no meio — e ninguém sabe onde parou. A barra de gravação só aparece quando há mudança e diz **quantas** são; a célula alterada fica destacada.
- **A matriz de um papel só mostra os módulos do painel dele** — permissão de um painel não é concedível no outro nem por engano de clique, porque o painel viaja no slug (`admin.client.read` — Base_RBAC_Painel_No_Papel).
- **`root` não tem matriz**: a aba mostra a explicação. Dar "todas as permissões de hoje" o deixaria sem as de amanhã — módulo novo nasceria invisível para quem deveria ver tudo. Ele é a ausência de verificação, e por isso também não declara painel.
- O rodapé da matriz diz que **o token carrega o papel, não a lista de permissões** (Base_Permissao_Por_Modulo_E_Metodo) — é o que faz "removi o acesso e ele continua podendo" não acontecer.
- Módulo novo nasce com as seis ações: não existe permissão avulsa, o catálogo é o produto módulo × ação. É o que mantém a matriz sempre completa.

## ⚠️ Pontos de atenção
- Matriz é de **um papel por vez**. Comparar dois papéis na mesma grade parece útil e leva a marcar na coluna errada.
- Com dezenas de módulos a matriz cresce muito: o filtro de módulo no cabeçalho é obrigatório, não enfeite.

## 🔗 Conexões
- MOC: [[MOC_PadraoLayout]] · [[MOC_Seguranca]]
- Modelo de acesso: Base_RBAC_Painel_No_Papel · Base_Permissao_Por_Modulo_E_Metodo · exemplo real: Wbot_Controle_De_Acesso
- Hub: [[PadraoLayout_Arquitetura]]
