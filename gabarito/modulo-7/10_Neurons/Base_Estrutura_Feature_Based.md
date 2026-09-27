---
type: neuron
status: evergreen
aliases: [estrutura de pastas, feature-based, painéis, organização do projeto, dev.sh]
summary: "Organizar o código por feature/painel (não por tipo técnico), com shared/ comum, front e back independentes e um dev.sh que sobe tudo."
tags: [status/evergreen, area/engenharia, tipo/pattern]
source: "Stack Base SoftEmp v1"
created: 2026-06-16
updated: 2026-06-16
---
# Base · Estrutura de Pastas Feature/Painel-Based

## 💡 Conceito
Organizar o código **por feature/painel** (domínio), não por tipo técnico (`controllers/`, `services/` no topo). Cada painel (`cliente`, `admin`, …) é uma fatia vertical com sua própria auth, API e features; o comum vive em `shared/`. Referência: `bulletproof-react`.

## 🛠️ Aplicação Técnica
**Backend** — feature owns rota+service+repo:
```
src/
  panels/<painel>/
    <feature>/  { <feature>.routes.ts  .service.ts  .repository.ts }
  shared/  { auth/ rbac/ db/ redis/ errors/ middlewares/ config/ logger/ }
```
**Frontend** — cada painel com auth/api próprios:
```
src/
  panels/<painel>/  { auth/  api/  features/  routes.tsx }
  shared/lib/  (base reaproveitada)
```
- **Front e back independentes** (deploys/escala separados); contrato os une.
- **`dev.sh`** sobe front+back local num comando — conteúdo canônico em Base_Infra_Dev_Sh_Padrao (`docker compose up` só se o projeto exigir, Base_Infra_Docker_Multistage).
- Cada rota carrega seu próprio middleware (`[[Base_Backend_Rota_Fina_Cinto]]`) — nada de auth global mágico.

## ⚠️ Pontos de atenção
- Isolar painel no **frontend** é organização/UX — **não é segurança** (`[[Base_Seg_Frontend_Nao_Confiavel]]`).
- `shared/` é cola, não despejo: se algo é de um painel só, fica no painel.

## 🔗 Conexões
- MOC: [[MOC_Stack_Base]] · [[MOC_Desenvolvimento]]
- Relacionados: Base_Backend_Rota_Fina_Cinto, [[Multi_Painel_Auth_Isolado]], Base_Selecao_Stack_Por_Sinais
