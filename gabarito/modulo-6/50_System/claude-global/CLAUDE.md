# Diretivas Globais — Claude Code

## Idioma e tom (default)
- Idioma: PT-BR.
- Tom: técnico, pragmático, direto. Sem preâmbulos.

## Convenções de engenharia (todos os projetos)
- **Banco — nomenclatura:** toda **coluna e tabela em `snake_case`**, sempre, em projeto novo ou existente. Em Prisma o field fica camelCase + `@map("snake_case")` (tabela: `@@map`); FK = `<entidade>_id` (ex.: `permission_id`, `user_id`); timestamps `created_at`/`updated_at` (`deleted_at` p/ soft-delete); booleans `is_*`/`has_*`. Ao criar/editar schema, nunca deixar coluna camelCase sem `@map`. Rename de coluna existente = `RENAME COLUMN`/`RENAME TABLE` (nunca o DROP+ADD que o Prisma migrate gera cru — perde dados). Detalhe canônico no neurônio `[[Base_DB_Naming_Convention]]` do Cofre (consultar antes de mexer em schema).
- **Docs e scripts — nome com timestamp:** todo documento novo (manuais, runbooks, planos, relatórios — em `doc/`, `docs/` etc.) e todo **script one-shot** (migração, importador, backfill — em `scripts/`) nasce com data e hora no **início** do nome: `YYYY-MM-DD_HH-MM_slug-kebab.md` (hora local, 24h, hífen entre hora e minuto; obter com `date '+%Y-%m-%d_%H-%M'`). Exceções: nomes de contrato exigidos por ferramenta (README.md, CLAUDE.md, CHANGELOG.md, ADRs numeradas `adr/NNNN-*`, templates) e entrypoints com nome fixo (`dev.sh`, `deploy.sh`, scripts do `package.json` apontam para o arquivo datado). Docs existentes não renomear em massa — só quando já for tocar no doc (ou quando o operador pedir a revisão), atualizando referências. Canônico: `[[Base_Docs_Naming_Timestamp]]` no Cofre.

## Superpowers (plugins) — precedência
Plugins instalados (scope user): `superpowers`, `superpowers-chrome`, `superpowers-developing-for-claude-code` (marketplace `obra/superpowers-marketplace`). O Superpowers impõe um fluxo próprio (brainstorming → spec → plano → execução em incrementos → TDD RED-GREEN-REFACTOR → review → finish em git worktree). Use esse fluxo por padrão em projetos que sejam repo git.
- **Precedência:** estas Diretivas Globais e o Cofre de Neurônios **vencem** o fluxo do Superpowers sempre que houver conflito. O fluxo dele define *como* trabalhar; as regras SoftEmp definem *o que é obrigatório*.
- Antes de decidir schema/stack/estrutura/segurança/listagens, **consultar o Cofre primeiro** (ver seção abaixo), mesmo dentro do brainstorming do Superpowers. Nunca deixar o fluxo dele improvisar schema sem passar pelo `[[Base_DB_Naming_Convention]]` (snake_case + `@map`, etc.).
- Worktrees exigem repositório git inicializado; em dir sem git, ou `git init` primeiro ou rodar o fluxo sem a etapa de worktree.

## Vaults / Cofres conhecidos
Quando o working directory for um destes, é um **Vault Obsidian** gerenciado como Cofre de Neurônios (Zettelkasten + MOC). Antes de qualquer ação, ler `30_Atlas/Index.md` e `50_System/WIKI_SCHEMA.md` daquele Vault e respeitar o contrato (atomicidade, Wikilinks `[[...]]`, MOCs sem órfãos, log em `20_Projects/Wiki_Log.md`).

- `~/projetos/IA/meu-cerebro` — **Cofre único e ativo**. Ler também `50_System/Tags_Taxonomy.md`.
