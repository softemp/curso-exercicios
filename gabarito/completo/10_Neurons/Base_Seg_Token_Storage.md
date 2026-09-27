---
type: neuron
status: evergreen
aliases: [onde guardar o token, localStorage proibido, cookie httpOnly, access token em memória, refresh token]
summary: "Access token em memória (curto), refresh token em cookie httpOnly+Secure+SameSite; localStorage/sessionStorage proibidos para token (XSS rouba)."
tags: [status/evergreen, area/seguranca, area/frontend, tipo/pattern]
source: "Stack Base SoftEmp v1"
created: 2026-06-16
updated: 2026-06-16
---
# Base · Onde o Token Vive (fora do localStorage)

## 💡 Conceito
`localStorage`/`sessionStorage` são legíveis por JS → XSS rouba o token. **Proibido** guardar token ali. Padrão seguro:
- **Access token** (~15min) → **em memória** (estado do app). Some no refresh, tudo bem.
- **Refresh token** → **cookie `httpOnly` + `Secure` + `SameSite=Lax`** → invisível ao JS.

## 🛠️ Aplicação Técnica
- Login: servidor seta o cookie de refresh (httpOnly); front guarda o access em memória.
- Renovação: endpoint de refresh lê o cookie (vai sozinho) → novo access token.
- Contraparte no front (`[[ProjetoBC_Auth_Tri_Contextual_Frontend]]`): AuthContext em memória + interceptor que, no 401, chama refresh e repete a request; refresh falhou → logout.
- **CSRF:** refresh anda em cookie → `SameSite=Lax/Strict` + token anti-CSRF. Access vai no header `Authorization` → imune a CSRF.

## ⚠️ Pontos de atenção
- "Guardar no localStorage pra persistir login" é o atalho que mais cria XSS-grave. Persistência vem do **refresh cookie**, não do access.
- Sem `Secure` em produção → token trafega em claro se cair em HTTP.

## 🔗 Conexões
- MOC: [[MOC_Stack_Base]] · [[MOC_Seguranca]]
- Relacionados: Base_Seg_Token_Escopado_Por_Painel, Base_Seg_Refresh_Rotacao_Revogacao, ProjetoBC_Auth_Tri_Contextual_Frontend, [[Axios_Interceptor_Erro_Tipado]]
