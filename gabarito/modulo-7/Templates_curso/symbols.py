#!/usr/bin/env python3
# Cópia curada para o curso: só o projeto-exemplo. Acrescente os seus projetos aqui.
"""
symbols.py — biblioteca compartilhada de extração de "âncoras de código" dos neurônios.

Desde a limpeza de citações (#2/#2b), todo neurônio derivado de código cita por SÍMBOLO
no formato canônico:  `Symbol.metodo()` em `arquivo.ext`  (ou `Classe::metodo()`, etc).
Essas citações viram âncoras verificáveis contra o repo-fonte. Este módulo as extrai uma
vez e serve tanto o drift.py (símbolo ainda existe?) quanto o symbol_index.py (recall reverso).

Não tem efeitos colaterais; é importado pelos dois scripts.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# projeto/<tag> → CANDIDATOS de caminho do repo-fonte local, em ordem de preferência.
# É lista porque o mesmo Cofre roda em máquinas com raízes diferentes — o primeiro
# candidato que EXISTIR vence. Projeto sem candidato existente = não verificável
# (drift.py o reporta como "sem repo mapeado", nunca como drift).
REPO_CANDIDATES = {
    "padraolayout": ["~/curso-exercicios/projeto-exemplo",
                     "~/projetos/curso-exercicios/projeto-exemplo",
                     "~/projetos/IA/curso-exercicios/projeto-exemplo"],
}


def _resolve(cands):
    """Primeiro candidato existente; senão o primeiro (o consumidor checa isdir)."""
    paths = [os.path.expanduser(c) for c in cands]
    return next((p for p in paths if os.path.isdir(p)), paths[0])


REPOS = {proj: _resolve(c) for proj, c in REPO_CANDIDATES.items()}

_fm   = re.compile(r"^---\n(.*?)\n---", re.S)
_fence = re.compile(r"```.*?```", re.S)  # blocos de código cercados (imports de exemplo → ignorar)
# "em `<arquivo.ext>`" ancora a citação; o símbolo é o token-em-crase mais próximo à esquerda.
_file_in_ctx = re.compile(r"\bem\s+`([\w./@-]+\.[A-Za-z]+)`")  # \b evita casar "n[em]", "s[em]"
_btok = re.compile(r"`([^`]+)`")  # qualquer token entre crases
# token-em-crase que é um caminho/arquivo (p/ verificar existência isolada)
_file_tok = re.compile(r"`([\w./@-]+\.[A-Za-z][A-Za-z0-9]*)`")
# extensões que tratamos como "fonte de código verificável"
_CODE_EXT = ("ts","tsx","js","jsx","mjs","cjs","vue","svelte","py","php","rb","go",
             "java","kt","c","h","cpp","hpp","cs","rs","sql")
# extensões cuja EXISTÊNCIA vale verificar (código + config estável). Exclui voláteis/ilustrativos
# (env/md/txt/log/lock/example/sample) que dariam falso "sumiu".
_VERIF_EXT = set(_CODE_EXT) | {"json","yml","yaml","prisma","toml","css","scss","html"}

def read(p):
    return open(p, encoding="utf-8").read()

def project_of(body):
    """Primeira tag projeto/<x> do frontmatter (mapeia para REPOS)."""
    m = re.search(r"projeto/([a-z0-9-]+)", body)
    return m.group(1) if m else None

def method_name(symbol_text):
    """Extrai o identificador verificável de um símbolo citado.
    `WithdrawalService.requestWithdrawal()` -> requestWithdrawal
    `PlanController::checkout()`             -> checkout
    `evaluateMilharCentena()`                -> evaluateMilharCentena
    Retorna None se não houver um identificador de método/função claro (`()`)."""
    m = re.search(r"([A-Za-z_]\w*)\(\)", symbol_text)
    return m.group(1) if m else None

def extract_refs(txt):
    """Varre linha a linha. Para cada "em `arquivo.ext`", associa o símbolo-método mais
    próximo à esquerda (último token-em-crase com `()` ou `::`; senão o último token)."""
    refs = []
    for line in txt.splitlines():
        prev_end = 0  # cada âncora só enxerga o texto desde a âncora anterior na mesma linha
        for fm in _file_in_ctx.finditer(line):
            fname = fm.group(1)
            left = line[prev_end:fm.start()]
            prev_end = fm.end()
            ext = fname.rsplit(".", 1)[-1].lower()
            if ext not in _CODE_EXT:
                continue
            toks = _btok.findall(left)
            # token ADJACENTE (o mais próximo de "em `arquivo`") — preciso na associação.
            # Não recuar atrás de um `()` distante: isso roubaria símbolo de outra cláusula.
            sym = toks[-1] if toks else None
            base = os.path.basename(fname.split("@")[0])  # tira sufixo @commit se houver
            refs.append(((sym or fname).strip(), method_name(sym or ""), base))
    return refs

# linha que descreve arquivo a CRIAR (proposta) ou REMOVIDO — não é código atual a verificar
_propose_ctx = re.compile(
    r"\bcriar\b|\bcria-se\b|\bnov[oa]s?\b|\bopcional\b|propost|sugeri|sugest|"
    r"\bremov|\bdeletad|\bexclu[íi]|🔭|a criar|ser[áa] criad", re.I)

def extract_files(txt):
    """Arquivos citados isoladamente (fora de blocos de código), p/ checar EXISTÊNCIA.
    Retorna lista de (citação_original, basename), só de extensões em _VERIF_EXT.
    Pula linhas de proposta/remoção (arquivo a criar ou já removido ≠ drift)."""
    body = _fence.sub("", txt)  # remove ```fences``` — imports de exemplo não são citações
    seen, out = set(), []
    for line in body.splitlines():
        if _propose_ctx.search(line):
            continue
        for cit in _file_tok.findall(line):
            ext = cit.rsplit(".", 1)[-1].lower()
            if ext not in _VERIF_EXT:
                continue
            base = os.path.basename(cit.split("@")[0])
            if base.startswith("."):  # padrão de sufixo (`.test.ts`, `.d.ts`), não arquivo real
                continue
            key = (cit, base)
            if key in seen:
                continue
            seen.add(key)
            out.append((cit, base))
    return out

def parse_neuron(path):
    """Retorna dict do neurônio: nome, projeto, refs=[(symbol_text, method, filename)],
    files=[(citação, basename)] (arquivos citados, p/ verificar existência)."""
    txt = read(path)
    fmm = _fm.match(txt)
    body_fm = fmm.group(1) if fmm else ""
    proj = project_of(body_fm)
    refs = extract_refs(txt)
    im = re.search(r"^implemented:\s*(\S+)", body_fm, re.M)
    return {
        "name": os.path.splitext(os.path.basename(path))[0],
        "path": path,
        "project": proj,
        "refs": refs,
        "files": extract_files(txt),
        "implemented": im.group(1).strip().strip("'\"").lower() if im else None,
    }

def all_neurons():
    for f in sorted(glob.glob(os.path.join(ROOT, "10_Neurons", "*.md"))):
        yield parse_neuron(f)

# cache simples de listagem de arquivos por repo (basename -> [caminhos absolutos])
_repo_cache = {}
def repo_files(repo_path):
    if repo_path not in _repo_cache:
        idx = {}
        for r, _dirs, files in os.walk(repo_path):
            if "/.git" in r or "/node_modules" in r or "/vendor" in r:
                continue
            for fn in files:
                idx.setdefault(fn, []).append(os.path.join(r, fn))
        _repo_cache[repo_path] = idx
    return _repo_cache[repo_path]
