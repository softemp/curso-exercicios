# 🖥️ Instalar o Cofre em outra máquina (runbook)

Guia para clonar e ativar o `meu-cerebro` (gate de qualidade, backup diário e revisão mensal
frescor+drift) numa máquina nova. Não é neurônio — é doc operacional do `50_System/`.

> **Premissa de paths:** o setup atual assume usuário do operador e a árvore
> `~/projetos/IA/meu-cerebro`. Em máquina com **outro usuário ou estrutura**,
> ajuste os paths absolutos (ver §6) — senão o backup e o drift não acham os diretórios.

---

## 1. Pré-requisitos
- `git`
- `python3` ≥ 3.8 (testado em 3.12). Só usa stdlib — **sem `pip install`**.
- `bash`, `cron` (Linux) com `crontab` disponível.

## 2. Clonar o repositório
```bash
mkdir -p ~/projetos/IA && cd ~/projetos/IA
git clone <URL-do-remote-meu-cerebro> meu-cerebro     # ex.: git@github.com:softemp/meu-cerebro.git
cd meu-cerebro
```

## 3. Instalar o git hook (gate de qualidade)
O hook `pre-commit` roda o lint e **bloqueia** commits que quebrem o contrato. Não é versionado
(fica em `.git/hooks/`), então **precisa ser reinstalado a cada clone**:
```bash
bash 50_System/install-hooks.sh
```
Verifique: `test -x .git/hooks/pre-commit && echo OK`.

## 4. Criar o diretório de backups/logs
```bash
mkdir -p ~/backups/meu-cerebro
```
(É onde o backup diário grava os tarballs e a revisão mensal grava o log.)

## 5. Instalar o crontab
Duas tarefas: **backup diário** (03:00) e **revisão mensal** frescor+drift (dia 1, 09:00).

Instalação idempotente (preserva outras entradas, não duplica as do Cofre):
```bash
( crontab -l 2>/dev/null | grep -vE 'backup_cofre.sh|monthly_review.sh|revalidate.py'
  echo '0 3 * * * /home/USUARIO/projetos/IA/meu-cerebro/50_System/backup_cofre.sh'
  echo '0 9 1 * * cd /home/USUARIO/projetos/IA/meu-cerebro && bash 50_System/monthly_review.sh >> /home/USUARIO/backups/meu-cerebro/monthly_review.log 2>&1'
) | crontab -
```
Troque `USUARIO` pelo usuário real (ou use `$HOME`). Confira com `crontab -l`.

**Entradas canônicas do crontab:**

| Quando | Comando | O quê |
|---|---|---|
| `0 3 * * *` (diário 03:00) | `…/50_System/backup_cofre.sh` | tarball completo (com `.git`) em `~/backups/meu-cerebro`, rotação 14 |
| `0 9 1 * *` (dia 1, 09:00) | `cd … && bash 50_System/monthly_review.sh >> ~/backups/meu-cerebro/monthly_review.log 2>&1` | revalidate.py (frescor por idade) + drift.py (símbolo sumiu no código) |

> O `monthly_review.sh` substitui a antiga linha solta do `revalidate.py` — por isso o `grep -v`
> acima também remove `revalidate.py`, evitando rodar a revalidação duas vezes.

## 6. Ajuste de paths em máquina com outro usuário/estrutura
Dois arquivos têm paths absolutos `~/...`:
- **`50_System/backup_cofre.sh`** — `VAULT_PARENT` e `DEST`. Ajuste para a árvore local.
- **`50_System/symbols.py`** — dict `REPOS` (mapa projeto→repo-fonte do `drift.py`). Veja §7.

Se mantiver a mesma estrutura relativa ao `$HOME`, troque só o nome do usuário.

## 7. (Opcional) Repos-fonte para o drift funcionar
O `drift.py` e o `symbol_index.py` só verificam projetos cujo repo-fonte exista localmente,
mapeado em `50_System/symbols.py` → `REPOS`. Sem o repo, aquele projeto é só **pulado** (não quebra).
Para ativar a verificação numa máquina nova, clone os repos-fonte que te interessam e ajuste os
caminhos no dict `REPOS`. No curso, mapeia só o `padraolayout` (o projeto-exemplo).

## 8. Verificação final
```bash
python3 50_System/lint.py            # deve terminar com "Erros: 0 | Avisos: 0"
python3 50_System/symbol_index.py    # regenera 30_Atlas/Indice_Simbolos.md
python3 50_System/drift.py           # relatório de drift (0 se os repos estiverem em dia)
bash    50_System/monthly_review.sh  # simula a revisão mensal (frescor + drift)
crontab -l                           # confere as 2 entradas do Cofre
```

---

## Referência rápida — scripts do `50_System/`
| Script | Função | Disparo |
|---|---|---|
| `install-hooks.sh` | instala o gate `pre-commit` (lint) | manual, 1× por clone |
| `lint.py` | valida o contrato (0/0) + advisories | gate + manual |
| `catalog.py` | gera `Catalogo_Neuronios.md` | `sync_wiki.sh` |
| `symbol_index.py` | gera `Indice_Simbolos.md` (pre-flight) | `sync_wiki.sh` |
| `drift.py` | símbolo citado sumiu do repo? | revisão mensal |
| `revalidate.py` | neurônios stale por idade | revisão mensal |
| `monthly_review.sh` | frescor + drift num relatório | cron dia 1 |
| `backup_cofre.sh` | tarball rotacionado | cron diário 03:00 |
| `sync_wiki.sh` | catalog + index + lint + commit | manual pós-ingest |

## 🔗 Conexões
- Paridade entre máquinas (o porquê e o manifesto): [[Eco_Paridade_Entre_Maquinas]] · manual de comandos: 2026-09-25_11-45_manual-ecossistema-comandos
- O que os scripts geram: [[Catalogo_Neuronios]] · [[Indice_Simbolos]] · guia de uso: [[GUIA_USO_COFRE]]
