---
type: neuron
status: evergreen
tags: [status/evergreen, area/engenharia, tipo/arquitetura, tipo/referencia, wiki]
created: 2026-05-04
summary: "O padrão MOC é uma estratégia de organização de conhecimento que resolve o problema do 'Índice Monolítico' em sistemas Zettelkasten ou Wikis pessoais."
source: "Governança do Cofre de Neurônios"
---

# 🗺️ Padrão MOC (Map of Content) para Escalabilidade

O padrão MOC é uma estratégia de organização de conhecimento que resolve o problema do "Índice Monolítico" em sistemas Zettelkasten ou Wikis pessoais.

## 🧱 Arquitetura em Camadas

A estrutura utiliza uma hierarquia lógica em vez de uma hierarquia de pastas rígida:

1.  **Nível 0: Atlas Central (Index)**: Ponto de entrada único. Contém links apenas para os MOCs de primeiro nível e notas de arquitetura core.
2.  **Nível 1: MOCs Departamentais**: Mapas temáticos (ex: `MOC_WhatsApp`). Eles agrupam neurônios por domínio de conhecimento, fornecendo contexto e narrativa.
3.  **Nível 2: Neurônios Atômicos**: A unidade mínima de informação. Cada neurônio deve apontar de volta para o seu MOC de Nível 1.

## 🚀 Benefícios
*   **Baixa Carga Cognitiva**: Evita listas gigantes de links.
*   **Contextualização**: O MOC permite agrupar notas relacionadas por subtópicos (ex: "Oficial" vs "Não Oficial"), o que um índice alfabético não faz.
*   **Escalabilidade**: Novos domínios são adicionados criando um novo MOC e registrando-o no Atlas Central, sem impactar os existentes.

## 🛠️ Manutenção (Linting)
Para garantir que a estrutura não se quebre, é essencial um script de automação que verifique:
*   **Links Quebrados**: Referências a notas inexistentes.
*   **Órfãos**: Neurônios que não são citados por nenhum MOC ou pelo Index.
*   **Cobertura**: Garantir que cada neurônio pertença a pelo menos um mapa de conteúdo.

---
- MOC: [[Index]]
- Relacionados: [[WIKI_SCHEMA]], [[Project_Isolation_Pattern_Wiki]], [[Wiki_Bootstrap_Protocol]]
