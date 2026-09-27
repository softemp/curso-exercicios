---
type: neuron
status: evergreen
tags: [status/evergreen, area/engenharia, tipo/arquitetura, tipo/referencia, wiki]
created: 2026-05-04
summary: "Estratégia para evitar a degradação do Atlas Central (Index) ao lidar com múltiplos projetos simultâneos."
source: "Governança do Cofre de Neurônios"
---

# 🛡️ Padrão de Isolamento de Projetos no Wiki

Estratégia para evitar a degradação do **Atlas Central (Index)** ao lidar com múltiplos projetos simultâneos.

## 🚩 O Problema: Poluição de Contexto
Quando uma Wiki começa a crescer, neurônios específicos de um projeto (ex: regras de negócio, arquitetura de um cliente) tendem a subir para o índice principal. Isso causa:
*   **Perda de Foco**: O usuário é exposto a detalhes irrelevantes para o contexto global.
*   **Rigidez**: Dificulta a adição de novos projetos sem redesenhar o índice.
*   **Ruído Cognitivo**: Mistura padrões de engenharia globais com exceções de implementação.

## 🟢 A Solução: MOC de Projetos (Camada de Abstração)
O padrão propõe o isolamento de informações específicas em uma estrutura dedicada:

1.  **Index Central**: Mantém-se agnóstico a projetos. Aponta apenas para "MOC Projetos".
2.  **MOC Projetos**: Atua como um diretório de ecossistemas. Organiza os projetos por nome/cliente.
3.  **Hub de Projeto**: Cada projeto possui sua própria seção (ou MOC próprio se for gigante) dentro do MOC de Projetos.

## 🏆 Benefícios
*   **Escalabilidade Horizontal**: Pode-se adicionar infinitos projetos sem poluir o Atlas Central.
*   **Reusabilidade**: Padrões globais (ex: Prisma, Docker) permanecem em seus MOCs temáticos, enquanto o uso específico desses padrões fica no contexto do projeto.
*   **Higiene Mental**: Facilita a transição de contexto (context-switching) entre diferentes frentes de trabalho.

---
- MOC: [[Index]]
- Relacionados: [[Wiki_Scalability_MOC_Pattern]], [[MOC_Projetos]]
