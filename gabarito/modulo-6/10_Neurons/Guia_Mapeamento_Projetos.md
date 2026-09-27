---
type: neuron
status: evergreen
aliases: [Guia de Mapeamento, Project Mapping, Como Mapear Projetos]
tags: [status/evergreen, area/engenharia, tipo/tutorial, meta, wiki]
source: "Análise interna — sessão de bootstrap do Cofre"
created: 2026-05-06
summary: "Define o que deve e o que não deve ser mapeado de um projeto dentro do Cofre de Neurônios."
---

# Guia_Mapeamento_Projetos — O que Capturar de um Projeto

## 💡 Conceito
Define o que **deve** e o que **não deve** ser mapeado de um projeto dentro do Cofre de Neurônios. O objetivo é capturar o conhecimento que **não está no código** — o porquê, como se conecta e o contexto que se perde com o tempo.

---

## 🛠️ Aplicação Técnica

### Regra de Ouro

> [!important] **Se está no código, não duplique.** Capture apenas o que o código não diz: decisões, contexto, armadilhas, fluxos e padrões.

### ❌ O que NÃO mapear

| Tipo | Por quê não |
|------|-------------|
| Código de componentes | Já está no VS Code, duplicar cria dessincronia |
| Documentação de libs (React, Prisma) | Google encontra em 5 segundos |
| Props de componentes | Muda toda hora, fica desatualizado |
| Conteúdo de arquivos `.env` | Risco de segurança |

### ✅ O que mapear

| Nível | O que capturar | Atualização |
|-------|----------------|-------------|
| **Arquitetura geral** | Stack, módulos, fluxos macro | A cada mudança estrutural |
| **Mapa de módulos** | O que faz, com quem conversa, padrão interno | Quando criar/alterar módulo |
| **Padrões recorrentes** | CRUD pattern, auth pattern, middleware | Quando validar padrão novo |
| **Gotchas/armadilhas** | Bugs conhecidos, workarounds, edge cases | Sempre que encontrar um |
| **ADRs (decisões)** | "Por que Vite e não Next.js?" | A cada decisão importante |
| **Fluxos de negócio** | Regras que não são óbvias no código | Quando regra muda |

### Estrutura sugerida por projeto

```
10_Neurons/
├── PROJETO_Arquitetura.md      → Visão macro (stack, módulos, deploy)
├── PROJETO_Modulos.md          → Mapa de cada módulo e dependências
├── PROJETO_Patterns.md         → Padrões recorrentes validados
├── PROJETO_Gotchas.md          → Armadilhas e workarounds
└── PROJETO_ADR_NomeDaDecisao.md → Uma decisão por arquivo
```

### O valor real

> [!tip] **Onboarding instantâneo.** Em vez de gastar 1-2 horas relembrando a estrutura de um projeto parado, você lê 2-3 neurônios em 5 minutos e já está contextualizado. E quando alimentar uma IA com esses neurônios, ela já sabe toda a arquitetura sem precisar explorar o código do zero.

---

## 🔗 Conexões
- MOC: [[Index]] (Governança)
- Relacionados: [[Parecer_Estrategico_Engenharia]], [[MOC_Projetos]], MOC_Desenvolvimento
