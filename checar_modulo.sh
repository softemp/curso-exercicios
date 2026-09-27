#!/usr/bin/env bash
# checar_modulo.sh N [vault] — gate de comportamento do módulo N do curso (spec 3, seção 4).
# Saída: 0 tudo ✓ · 1 algum ✗ · 2 uso inválido. CHECAR_SEM_MAQUINA=1 pula checks que dependem desta máquina.
set -u
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
N="${1:-}"
VAULT="${2:-}"
if [ -z "$VAULT" ]; then
  if [ -f "$AQUI/.curso.json" ]; then
    if command -v jq >/dev/null 2>&1; then
      VAULT="$(jq -r '.cerebro // empty' "$AQUI/.curso.json")"
    else
      echo "· aviso: jq ausente, usando ~/meu-cerebro" >&2
    fi
  fi
  VAULT="${VAULT:-$HOME/meu-cerebro}"
fi
VAULT="${VAULT/#\~/$HOME}"

[[ "$N" =~ ^[0-8]$ ]] || { echo "uso: checar_modulo.sh N (0-8) [vault]" >&2; exit 2; }
if [ "$N" -ge 2 ] && [ ! -d "$VAULT" ]; then echo "✗ vault inexistente: $VAULT" >&2; exit 2; fi

FALHAS=0
ok()  { local d="$1"; shift; if "$@" >/dev/null 2>&1; then echo "✓ $d"; else echo "✗ $d"; FALHAS=$((FALHAS+1)); fi; }
maq() { if [ "${CHECAR_SEM_MAQUINA:-0}" = "1" ]; then echo "· $1 (pulado: CHECAR_SEM_MAQUINA)"; else ok "$@"; fi; }
tem()   { [ -e "$VAULT/$1" ]; }
exec_() { [ -x "$VAULT/$1" ]; }
cita()  { grep -qF -- "$2" "$VAULT/$1" 2>/dev/null; }
no_path() { command -v "$1" >/dev/null 2>&1; }
py() { PYTHONDONTWRITEBYTECODE=1 python3 "$@"; }

neuronio_ligado_ao_index() {
  local f n
  for f in "$VAULT"/10_Neurons/*.md; do
    [ -e "$f" ] || return 1
    grep -q '^type: neuron' "$f" && grep -q 'status/' "$f" || continue
    n="$(basename "${f%.md}")"
    grep -qF "[[$n" "$VAULT/30_Atlas/Index.md" 2>/dev/null && return 0
  done
  return 1
}

lint_recusa_orfao() {
  [ -f "$VAULT/50_System/lint.py" ] || return 1
  local t out rc; t="$(mktemp -d)"
  if ! cp -r "$VAULT"/. "$t"/; then rm -rf "$t"; return 1; fi
  rm -rf "$t/.git"
  mkdir -p "$t/10_Neurons"
  printf -- '---\ntype: neuron\nstatus: seedling\ntags: [status/seedling, area/engenharia, tipo/conceito]\nsource: "teste"\ncreated: 2026-01-01\n---\n# Orfao_Teste\n' > "$t/10_Neurons/Orfao_Teste.md"
  out="$(py "$t/50_System/lint.py" 2>&1)"; rc=$?
  rm -rf "$t"
  [ "$rc" -ne 0 ] && grep -qF "[órfão] Orfao_Teste" <<<"$out"
}
sessao_roda() { py "$VAULT/50_System/checar_maquina.py" --sessao >/dev/null 2>&1; [ $? -lt 2 ]; }

case "$N" in
  0|1)
    maq "git no PATH (passo 1)" no_path git
    maq "python3 no PATH (passo 1)" no_path python3
    maq "jq no PATH (passo 1)" no_path jq
    ok  "projeto-exemplo baixado — projeto-exemplo/package.json (passo 3)" test -f "$AQUI/projeto-exemplo/package.json"
    maq ".curso.json válido com .cerebro (passo 5)" jq -e .cerebro "$AQUI/.curso.json"
    maq "skill /curso instalada (passo 6)" test -f "$HOME/.claude/skills/curso/exercicios.path"
    ;;
  2)
    ok "50_System/WIKI_SCHEMA.md presente (passo 1)" tem 50_System/WIKI_SCHEMA.md
    ok "50_System/Tags_Taxonomy.md presente (passo 1)" tem 50_System/Tags_Taxonomy.md
    ok "primeiro neurônio com frontmatter e tag status/, listado no Index (passos 4 e 5)" neuronio_ligado_ao_index
    ;;
  3)
    ok ".git/ no vault (passo 1)" test -d "$VAULT/.git"
    ok "AGENTS.md cita Index (passo 2)" cita AGENTS.md Index
    ok "CLAUDE.md cita Index (passo 3)" cita CLAUDE.md Index
    ok ".claude/settings.json com SessionStart (passo 4)" cita .claude/settings.json SessionStart
    ok "50_System/hooks/lembrete-cofre.sh executável (passo 5)" exec_ 50_System/hooks/lembrete-cofre.sh
    ok "50_System/GUIA_USO_COFRE.md presente (passo 5)" tem 50_System/GUIA_USO_COFRE.md
    ;;
  4)
    for b in Base_DB_Naming_Convention Base_Estrutura_Feature_Based Base_Seg_Token_Storage; do
      ok "10_Neurons/$b.md presente (passo 1)" tem "10_Neurons/$b.md"
      ok "MOC_Stack_Base linka [[$b]] (passo 3)" cita 30_Atlas/MOC_Stack_Base.md "[[$b"
    done
    maq "~/.claude/CLAUDE.md cita o vault (passo 4)" grep -qF -e "$VAULT" -e "${VAULT/#$HOME/\~}" "$HOME/.claude/CLAUDE.md"
    ;;
  5)
    ok "≥5 PadraoLayout_*.md com source b6e5c04 (passo 3)" bash -c '[ "$(grep -l "^source:.*b6e5c04" "$0"/10_Neurons/PadraoLayout_*.md 2>/dev/null | wc -l)" -ge 5 ]' "$VAULT"
    ok "30_Atlas/MOC_PadraoLayout.md presente (passo 4)" tem 30_Atlas/MOC_PadraoLayout.md
    ok "30_Atlas/MOC_Projetos.md linka MOC_PadraoLayout (passo 5)" cita 30_Atlas/MOC_Projetos.md "[[MOC_PadraoLayout"
    ok ".claude/skills/extrair-projeto/SKILL.md presente (passo 1)" tem .claude/skills/extrair-projeto/SKILL.md
    ok "50_System/EXTRACAO_PROJETO.md presente (passo 1)" tem 50_System/EXTRACAO_PROJETO.md
    ;;
  6)
    ok ".git/hooks/pre-commit cita lint.py (passo 2)" grep -q lint.py "$VAULT/.git/hooks/pre-commit"
    ok "lint.py sai 0 no vault (passo 3)" py "$VAULT/50_System/lint.py"
    ok "lint recusa neurônio órfão numa cópia (passo 3)" lint_recusa_orfao
    for s in revalidate.py drift.py catalog.py symbol_index.py; do ok "50_System/$s presente (passo 1)" tem "50_System/$s"; done
    ok "20_Projects/Wiki_Log.md presente (passo 6)" tem 20_Projects/Wiki_Log.md
    ;;
  7)
    for s in bootstrap-maquina.sh checar_maquina.py sync_wiki.sh grafo_cores.json INSTALL_OUTRA_MAQUINA.md; do ok "50_System/$s presente (passo 1)" tem "50_System/$s"; done
    maq "checar_maquina.py --sessao roda (passo 4)" sessao_roda
    ;;
  8)
    ok "comparar.sh executável (passo 1)" test -x "$AQUI/comparar.sh"
    ok "Wiki_Log registra 'curso | módulo 8' (passo 4)" cita 20_Projects/Wiki_Log.md "curso | módulo 8"
    ;;
esac

[ "$FALHAS" -eq 0 ] && exit 0 || exit 1
