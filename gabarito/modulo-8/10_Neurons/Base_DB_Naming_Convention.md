---
type: neuron
status: evergreen
aliases: [naming de banco, snake_case colunas, prisma @map, convenção de nomenclatura db, created_at updated_at, foreign key naming, db column convention, padrão de coluna]
summary: "Padrão SoftEmp: toda COLUNA/TABELA do banco em snake_case; em Prisma o field fica camelCase + @map/@@map. Timestamps created_at/updated_at, FK <ent>_id, bool is_*. Rename via RENAME, nunca DROP+ADD."
tags: [status/evergreen, area/dados, tipo/pattern]
source: "projeto do operador — sessão de normalização 2026-06-25 (58 colunas fora do padrão)"
created: 2026-06-25
updated: 2026-06-25
---
# Base · Convenção de Nomenclatura do Banco (snake_case + @map)

## 💡 Conceito
**Toda coluna e tabela do banco vive em `snake_case`** — sem exceção, em projeto novo ou existente. É a camada física (SQL), que é case-insensitive/variável por SO e lida por SQL cru, dumps e ferramentas externas; misturar `createdAt` e `created_at` na mesma base gera bug silencioso e SQL cru quebrado. O nome **idiomático da linguagem** (camelCase em TS) mora no código, não no schema físico.

A regra de ouro: **a inconsistência nasce quando o ORM deixa o nome do campo "vazar" para a coluna.** Em Prisma isso acontece quando se esquece o `@map`. Logo, a convenção é *mecânica*, não estética.

## 🛠️ Aplicação Técnica

**Regras (todas as stacks):**
- **Coluna:** `snake_case` sempre. Ex.: `permission_id`, `created_at`, `is_active`.
- **Tabela:** `snake_case` plural. Ex.: `role_permissions`, `backup_configs`.
- **PK:** `id`. **FK:** `<entidade>_id` (ex.: `user_id`, `permission_id`) — nunca `userId`/`fk_user`.
- **Timestamps:** `created_at` / `updated_at` (e `deleted_at` p/ soft-delete).
- **Booleans:** prefixo `is_` / `has_` (ex.: `is_active`, `is_processed`, `has_debt`).

**Prisma (default das stacks TS):** o field fica camelCase (idiomático) e o `@map` faz a ponte. **Zero mudança em código ORM** ao normalizar — só `@map`/`@@map`:
```prisma
model RolePermission {
  id           String   @id @default(uuid())
  permissionId String   @map("permission_id")
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt      @map("updated_at")
  @@map("role_permissions")
}
```
**Laravel/Eloquent (stacks Blade):** snake_case já é o default do framework (`created_at`/`updated_at`, FK `user_id`) — só **não burlar** com `$table`/`$primaryKey` custom.

**Projeto NOVO:** nasce com a convenção; rodar o lint de schema no Base_Test_Harness_Gate desde o primeiro commit.

**Projeto EXISTENTE com drift:** normalizar em **migrations por lote** (frias → quentes), cada coluna via **`RENAME COLUMN`/`RENAME TABLE`** (MySQL 8.0+/MariaDB 10.5.2+ — preserva tipo/null/default/charset). **NUNCA** deixar o Prisma gerar a migration crua: ele não detecta rename e emite `DROP COLUMN`+`ADD COLUMN` = **perda de dados**; reescrever o `migration.sql` à mão. Ver Base_Infra_Migrations_Deploy.

**Enforcement (o que garante "nunca mais"):** um check no gate que falha se houver coluna camelCase sem `@map`. Para Prisma:
```bash
grep -nE '^\s+[a-z]+[A-Z][A-Za-z0-9]*\s+(String|Int|BigInt|Float|Decimal|Boolean|DateTime|Json|Bytes)' \
  prisma/schema.prisma | grep -v '@map' && echo "✗ coluna sem @map" && exit 1
```

## ⚠️ Pontos de atenção
- **Field name NÃO muda** ao normalizar (continua camelCase no Prisma) → o ORM e todo código que o usa seguem iguais; só SQL cru que cite a coluna velha precisa de ajuste.
- **Rename é DDL breaking** (não-aditivo): no deploy há janela em que o container antigo consulta a coluna nova → janela curta / manutenção. Diferente de uma migration aditiva.
- **Backups/dumps antigos** carregam os nomes velhos; restaurar um dump pré-normalização recria o drift → re-rodar a migration.
- Tabela sem `@@map` no Prisma = nome do model verbatim (PascalCase!) — caso real `BackupConfig`/`BackupLog`. Conferir `@@map` em **todo** model.

## 🔗 Conexões
- MOC: [[MOC_Stack_Base]]
- Relacionados: Base_Infra_Migrations_Deploy, Base_Test_Harness_Gate, [[Base_Estrutura_Feature_Based]]
