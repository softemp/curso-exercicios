# Módulo 7 — Multi-máquina

## Onde rodar
`<cerebro>`. Uma parte acontece numa segunda máquina ou num container.

## Objetivo
O cérebro é infraestrutura: sobe em máquina nova com um script, registra seus hooks globais e acusa quando a máquina sai do padrão.

## Antes de começar
`<exercicios>/checar_modulo.sh 6` todo `✓`. Para o caminho do container, Docker instalado (`docker --version`).

## Passos
1. [agente] Copie de `<exercicios>/gabarito/modulo-7/` para os mesmos caminhos: `50_System/bootstrap-maquina.sh`, `checar_maquina.py`, `sync_wiki.sh`, `backup_cofre.sh`, `ecossistema.json`, `INSTALL_OUTRA_MAQUINA.md`, `hooks/checar-maquina-sessao.sh`, `grafo_cores.json`, `grafo_cores.py`, `50_System/tests/`, `30_Atlas/Legenda_Cores_Grafo.md`, e o neurônio `Cofre_Grafo_Cores_Configuracao_Versionada` (linha no Index). Mantenha os `.sh` executáveis.
2. [aluno] Leia `50_System/INSTALL_OUTRA_MAQUINA.md` com o agente resumindo em 6 linhas: pré-requisitos (git, Python 3 só com stdlib, cron); clonar o cérebro; reinstalar o gate `pre-commit` a cada clone (`install-hooks.sh`, não é versionado); criar `~/backups/meu-cerebro`; crontab com backup diário (`backup_cofre.sh`) e revisão mensal (`monthly_review.sh`: frescor + drift); ajustar caminhos absolutos em `backup_cofre.sh` e `symbols.py`; verificação final com `lint.py`, `symbol_index.py`, `drift.py`. O agente acrescenta o que o runbook não cobre: `bootstrap-maquina.sh` roda `checar_maquina.py --corrigir` (que compara a máquina com `ecossistema.json` e registra hooks globais) e cria `CLAUDE.md` nos projetos de `projetos-com-gatilho.txt`. Verificação: o aluno diz o que o `ecossistema.json` descreve.
3. [aluno] Rode `python3 50_System/checar_maquina.py` **nesta** máquina e leia o relatório. Itens de plugin ou cron que você não usa podem ficar como aviso. Antes do bootstrap, os hooks globais ainda não registrados aparecem como **erro**: é o esperado (o `bootstrap-maquina.sh` só roda no destino, passo 4). Verificação: o aluno cola a linha final `N erro(s), M aviso(s)`.
4. [aluno] Escolha o destino: (a) uma segunda máquina sua com git e Python, ou (b) o container: `bash <exercicios>/roteiros/modulo-7/entrar.sh <cerebro>`. No destino: `git clone /origem ~/meu-cerebro` (no container) ou `git clone <seu remoto ou caminho> ~/meu-cerebro` (máquina real); `cd ~/meu-cerebro && bash 50_System/bootstrap-maquina.sh`. No container, avisos sobre `claude` ausente e plugins são esperados: o que se prova é o clone subir e o `checar_maquina.py` rodar. Verificação: `python3 50_System/checar_maquina.py` roda no destino e imprime o relatório.
5. [aluno] Ainda no destino, provoque um desvio e rode `python3 50_System/checar_maquina.py` de novo:
   - **No container:** apague `~/.claude/settings.json` à vontade (o container é descartável).
   - **Numa segunda máquina real:** primeiro `cp ~/.claude/settings.json ~/.claude/settings.json.bak`; depois remova só a entrada de hook que o bootstrap registrou (ou renomeie o arquivo); rode o `checar_maquina.py` e veja a acusação; por fim restaure com `cp ~/.claude/settings.json.bak ~/.claude/settings.json`. Nunca apague configuração real sem backup.
   Verificação: o relatório acusa o hook ausente. Saia do container (ou restaure a máquina).
6. [agente] Rode `python3 50_System/grafo_cores.py` e mostre `30_Atlas/Legenda_Cores_Grafo.md`: as cores do grafo agora são versionadas e iguais em toda máquina.
7. [agente] `git add -A && git commit -m "módulo 7: bootstrap, paridade de máquina, cores do grafo"`.

## Saiu rodando
`<exercicios>/checar_modulo.sh 7` — todo `✓`.

## Compare com o gabarito
`<exercicios>/comparar.sh 7`. O gabarito traz MOCs temáticos vazios (`MOC_Frontend`, `MOC_Seguranca`, …) que você ainda não tem: **escolha sua** (crie quando tiver neurônios para eles). Scripts de `50_System/` ausentes são **lacuna**.

## Como adaptar
Hooks globais e `CLAUDE.md` são do Claude Code; o restante (clone, bootstrap, `checar_maquina.py`, cron) é git e Python. Em outro agente, o equivalente do hook global é o arquivo global dele: Codex, `~/.codex/AGENTS.md`; Gemini CLI, `~/.gemini/GEMINI.md`; Cursor, "User Rules" nas configurações.

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 8` e `checks["7"] = <data>`. Acrescente ao `Wiki_Log`: `## [<data>] curso | módulo 7 concluído` e `- cérebro sobe em máquina nova; checar_maquina.py acusa desvio.` Commit. Diga: "Módulo 8, o último: estudo de caso e comparação final. Rode a partir do `curso-exercicios`."
