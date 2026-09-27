---
type: moc
status: evergreen
tags: [moc, status/evergreen, area/engenharia, tipo/referencia]
aliases: [stack base softemp, kit base, padrões base de projeto, MOC Stack Base]
summary: "Hub do kit prescritivo Stack Base SoftEmp v1: normas atômicas por camada (arquitetura→testes) para criar projeto novo e corrigir falhas com padrão consistente."
created: 2026-06-16
updated: 2026-09-12
---
# 🧱 MOC · Stack Base SoftEmp v1

Kit **prescritivo** (norma opinada, `tipo/pattern`, sem `validated` — não é drift de código) para
dois momentos: **criar** projeto novo e **corrigir** falhas com padrão consistente. Cada item é
um neurônio atômico (abrir só o que precisa). Derivado do caderno de trabalho `doc/` (fora do Cofre).

> Convenção: neurônios novos têm prefixo `Base_`. Itens **♻️** são neurônios já existentes
> (derivados de código real) reaproveitados aqui.

## 📁 Estrutura
- [[Base_Estrutura_Feature_Based]] — feature/painel-based + `shared/` + front/back independentes + `dev.sh`.

## 🗄️ Dados / Banco
- [[Base_DB_Naming_Convention]] — coluna/tabela sempre snake_case (Prisma: field camelCase + `@map`); FK `<ent>_id`, `created_at`/`updated_at`, bool `is_*`; rename via RENAME, nunca DROP+ADD.

## 🔒 Segurança
- [[Base_Seg_Token_Storage]] — access em memória + refresh cookie httpOnly; localStorage proibido.

## 🔗 Conexões
- Hubs temáticos: [[MOC_Frontend]] · [[MOC_Seguranca]] · [[MOC_Infraestrutura]] · [[MOC_Desenvolvimento]] · [[MOC_Padroes_Reutilizaveis]]
- Índice geral: [[Index]]
