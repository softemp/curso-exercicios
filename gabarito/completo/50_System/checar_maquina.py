#!/usr/bin/env python3
"""
Confere ESTA máquina contra o manifesto do ecossistema (50_System/ecossistema.json) e aponta o que
falta ou diverge: plugins, marketplaces, CLAUDE.md global, skills do Cofre, hooks globais, hooks de
git do Cofre, cron, Cartographer e se o próprio Cofre está atualizado com o origin.

  python3 50_System/checar_maquina.py              # relatório completo
  python3 50_System/checar_maquina.py --corrigir   # aplica o que é seguro (ver CORRIGIVEL) e relata
  python3 50_System/checar_maquina.py --sessao     # modo hook SessionStart: silencioso se tudo ok

Não corrige sozinho (só aponta o comando): ferramentas do sistema (apt/sudo), cron, e Cofre com
mudança local ou divergente do origin. Nunca copia credencial nem permissão aprovada: isso é por
máquina de propósito. Ver o neurônio Eco_Paridade_Entre_Maquinas.
"""
import json, os, re, shutil, subprocess, sys, time

COFRE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TOOLS = os.path.join(os.path.dirname(COFRE), "tools")
HOME = os.path.expanduser("~")
CLAUDE_DIR = os.path.join(HOME, ".claude")
SETTINGS = os.path.join(CLAUDE_DIR, "settings.json")
MANIFESTO = os.path.join(COFRE, "50_System", "ecossistema.json")
CMD_CORRIGIR = f"python3 {COFRE}/50_System/checar_maquina.py --corrigir"

MODO_SESSAO = "--sessao" in sys.argv
CORRIGIR = "--corrigir" in sys.argv

achados = []  # (nivel, item, detalhe, comando_sugerido)


def achar(nivel, item, detalhe="", comando=""):
    achados.append((nivel, item, detalhe, comando))


def rodar(cmd, cwd=None, timeout=120):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                           shell=isinstance(cmd, str))
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return 1, str(e)


def expandir(s):
    return os.path.expanduser(s.replace("{COFRE}", COFRE).replace("{TOOLS}", TOOLS))


def ler_json(caminho, padrao):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return padrao


def tem_cmd(cmd, caminho_extra=None):
    if shutil.which(cmd):
        return True
    return bool(caminho_extra) and os.path.exists(os.path.join(os.path.expanduser(caminho_extra), cmd))


def symlink_para(link, alvo, rotulo):
    """Garante link → alvo. Arquivo comum no lugar vai para ~/.claude/backups antes."""
    if os.path.islink(link) and os.path.realpath(link) == os.path.realpath(alvo):
        return True
    if not CORRIGIR:
        return False
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if os.path.lexists(link):
        bkp = os.path.join(CLAUDE_DIR, "backups", f"{os.path.basename(link)}.{time.strftime('%Y%m%d-%H%M%S')}")
        os.makedirs(os.path.dirname(bkp), exist_ok=True)
        shutil.move(link, bkp)
        achar("info", rotulo, f"versão anterior guardada em {bkp}")
    os.symlink(alvo, link)
    achar("corrigido", rotulo, f"{link} → {alvo}")
    return True


# ───────────────────────────── checagens ─────────────────────────────

def checar_cofre_git():
    rc, saida = rodar(["git", "-C", COFRE, "status", "--porcelain"], timeout=10)
    sujo = rc == 0 and saida.strip() != ""
    if MODO_SESSAO:
        # fetch em segundo plano: a comparação usa o origin da última busca; a próxima sessão vê o novo.
        subprocess.Popen(["git", "-C", COFRE, "fetch", "-q", "origin"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
    else:
        rodar(["git", "-C", COFRE, "fetch", "-q", "origin"], timeout=30)
    rc, saida = rodar(["git", "-C", COFRE, "rev-list", "--left-right", "--count", "HEAD...@{u}"], timeout=10)
    if rc != 0:
        achar("aviso", "Cofre sem upstream", "não deu para comparar com o origin", f"git -C {COFRE} branch -u origin/main")
        return
    frente, atras = (int(x) for x in saida.split())
    if atras and not frente and not sujo and CORRIGIR:
        rc, out = rodar(["git", "-C", COFRE, "pull", "--ff-only", "-q"], timeout=60)
        achar("corrigido" if rc == 0 else "erro", "Cofre", f"git pull ({atras} commit(s))" if rc == 0 else out.strip()[:200])
    elif atras:
        achar("erro", "Cofre desatualizado", f"{atras} commit(s) atrás do origin" + (" e com mudança local" if sujo else ""),
              f"git -C {COFRE} pull --rebase")
    if frente:
        achar("aviso", "Cofre com commits locais", f"{frente} commit(s) não enviados", f"git -C {COFRE} push")
    if sujo:
        achar("info", "Cofre com mudança não commitada", "normal durante uma sessão; commitar ao fechar")


def checar_ferramentas(m):
    for f in m.get("ferramentas", []):
        if tem_cmd(f["cmd"], f.get("caminho_extra")):
            continue
        nivel = "erro" if f.get("obrigatoria") else "aviso"
        achar(nivel, f"ferramenta {f['cmd']}", f.get("motivo", "ausente"), f.get("instalar", ""))


def plugins_instalados():
    rc, saida = rodar(["claude", "plugin", "list", "--json"], timeout=20)
    if rc == 0:
        try:
            return {p["id"]: p for p in json.loads(saida)}
        except ValueError:
            pass
    # plano B: registro local (formato interno — pode mudar entre versões do Claude Code)
    reg = ler_json(os.path.join(CLAUDE_DIR, "plugins", "installed_plugins.json"), {}).get("plugins", {})
    habil = ler_json(SETTINGS, {}).get("enabledPlugins", {})
    return {pid: {"id": pid, "version": (v[0].get("version") if v else "?"), "enabled": habil.get(pid, False)}
            for pid, v in reg.items()}


def checar_marketplaces_e_plugins(m):
    conhecidos = ler_json(os.path.join(CLAUDE_DIR, "plugins", "known_marketplaces.json"), {})
    for mk in m.get("marketplaces", []):
        if mk["nome"] in conhecidos:
            continue
        cmd = ["claude", "plugin", "marketplace", "add", mk["fonte"]]
        if CORRIGIR and not MODO_SESSAO:
            rc, out = rodar(cmd, timeout=180)
            achar("corrigido" if rc == 0 else "erro", f"marketplace {mk['nome']}", "adicionado" if rc == 0 else out.strip()[-200:])
        else:
            achar("erro", f"marketplace {mk['nome']}", "não configurado", " ".join(cmd))

    inst = plugins_instalados()
    for p in m.get("plugins", []):
        pid = p["id"]
        if pid not in inst:
            cmd = ["claude", "plugin", "install", "-s", "user", pid]
            if CORRIGIR and not MODO_SESSAO:
                rc, out = rodar(cmd, timeout=300)
                achar("corrigido" if rc == 0 else "erro", f"plugin {pid}", "instalado" if rc == 0 else out.strip()[-300:])
            else:
                achar("erro", f"plugin {pid}", "não instalado" + (f" ({p['status']})" if p.get("status") else ""), " ".join(cmd))
        elif not inst[pid].get("enabled", True):
            achar("aviso", f"plugin {pid}", "instalado mas desabilitado", f"claude plugin enable {pid}")
        elif not MODO_SESSAO:
            achar("ok", f"plugin {pid}", inst[pid].get("version", ""))

    declarados = {p["id"] for p in m.get("plugins", [])}
    vetados = {v["nome"]: v["motivo"] for v in m.get("plugins_vetados", [])}
    for pid in inst:
        nome = pid.split("@")[0]
        if nome in vetados:
            achar("erro", f"plugin vetado {pid}", vetados[nome], f"claude plugin uninstall {pid}")
        elif pid not in declarados:
            achar("aviso", f"plugin fora do manifesto {pid}",
                  "só nesta máquina — incluir no ecossistema.json (e dar push) ou desinstalar",
                  f"claude plugin uninstall {pid}")


def checar_claude_md(m):
    alvo = os.path.join(COFRE, m["claude_md_global"])
    link = os.path.join(CLAUDE_DIR, "CLAUDE.md")
    if symlink_para(link, alvo, "CLAUDE.md global"):
        if not MODO_SESSAO and not any(a[1] == "CLAUDE.md global" for a in achados):
            achar("ok", "CLAUDE.md global", "ligado ao Cofre")
        return
    if os.path.isfile(link) and not os.path.islink(link):
        igual = open(link, encoding="utf-8").read() == open(alvo, encoding="utf-8").read()
        achar("aviso" if igual else "erro", "CLAUDE.md global",
              "cópia solta (igual ao Cofre)" if igual else "cópia solta DIFERENTE do Cofre — conferir antes de ligar",
              CMD_CORRIGIR)
    else:
        achar("erro", "CLAUDE.md global", "ausente ou apontando para outro lugar", CMD_CORRIGIR)


def checar_skills():
    base = os.path.join(COFRE, ".claude", "skills")
    for nome in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        alvo = os.path.join(base, nome)
        link = os.path.join(CLAUDE_DIR, "skills", nome)
        if not symlink_para(link, alvo, f"skill {nome}"):
            achar("erro", f"skill {nome}", "não disponível fora do Cofre", CMD_CORRIGIR)


def checar_hooks_globais(m):
    cfg = ler_json(SETTINGS, None)
    if cfg is None:
        achar("erro", "settings.json", f"{SETTINGS} ilegível ou ausente")
        return
    hooks = cfg.setdefault("hooks", {})
    mudou = False
    for h in m.get("hooks_globais", []):
        script = os.path.join(COFRE, h["script"])
        comando = f'bash "{script}"'
        grupos = hooks.setdefault(h["evento"], [])
        cmds = [(g, x) for g in grupos for x in g.get("hooks", [])]
        if any(x.get("command") == comando for _, x in cmds):
            if not MODO_SESSAO:
                achar("ok", f"hook {h['id']}", h["evento"])
            continue
        legado = [(g, x) for g, x in cmds if h.get("substitui_legado") and h["substitui_legado"] in x.get("command", "")]
        velho = [(g, x) for g, x in cmds if os.path.basename(h["script"]) in x.get("command", "")]
        if not CORRIGIR:
            achar("erro", f"hook {h['id']}", f"{h['evento']} não registrado" + (" (há a versão antiga embutida)" if legado else ""),
                  CMD_CORRIGIR)
            continue
        for g, x in legado + velho:
            g["hooks"].remove(x)
        grupos[:] = [g for g in grupos if g.get("hooks")]
        novo = {"hooks": [{"type": "command", "command": comando, "timeout": h.get("timeout", 10)}]}
        if h.get("matcher"):
            novo["matcher"] = h["matcher"]
        grupos.append(novo)
        mudou = True
        achar("corrigido", f"hook {h['id']}", f"{h['evento']} → {h['script']}" + (" (substituiu a versão antiga)" if legado or velho else ""))
    if mudou:
        bkp = os.path.join(CLAUDE_DIR, "backups", f"settings.json.{time.strftime('%Y%m%d-%H%M%S')}")
        os.makedirs(os.path.dirname(bkp), exist_ok=True)
        shutil.copy2(SETTINGS, bkp)
        with open(SETTINGS, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
            f.write("\n")
        achar("info", "settings.json", f"backup em {bkp}")


def checar_git_hooks(m):
    gh = m["git_hooks_cofre"]
    arq = os.path.join(COFRE, ".git", "hooks", gh["arquivo"])
    if os.path.isfile(arq) and gh["marca"] in open(arq, encoding="utf-8", errors="ignore").read():
        if not MODO_SESSAO:
            achar("ok", "pre-commit do Cofre", "gate de lint instalado")
        return
    if CORRIGIR:
        rc, out = rodar(["bash", os.path.join(COFRE, gh["instalador"])], cwd=COFRE)
        achar("corrigido" if rc == 0 else "erro", "pre-commit do Cofre", "instalado" if rc == 0 else out[-200:])
    else:
        achar("erro", "pre-commit do Cofre", "commit sem gate de lint", f"bash {os.path.join(COFRE, gh['instalador'])}")


def checar_cron(m):
    rc, tab = rodar(["crontab", "-l"], timeout=10)
    tab = tab if rc == 0 else ""
    for c in m.get("cron", []):
        linhas = [l for l in tab.splitlines() if c["procura"] in l and not l.lstrip().startswith("#")]
        if any(COFRE in l for l in linhas):
            if not MODO_SESSAO:
                achar("ok", f"cron {c['id']}", "agendado")
            continue
        achar("aviso", f"cron {c['id']}", "não agendado" + (" (aponta para outro caminho)" if linhas else "") + (f" — {c['nota']}" if c.get("nota") else ""),
              f"(crontab -l; echo '{expandir(c['linha'])}') | crontab -")


def checar_cartographer(m):
    c = m.get("cartographer")
    if not c:
        return
    d = expandir(c["dir"])
    nivel = "erro" if c.get("obrigatorio") else "aviso"
    if not os.path.isdir(os.path.join(d, ".git")):
        cmd = f"git clone {c['repo']} {d} && git -C {d} checkout {c['commit']} && git -C {d} apply {os.path.join(COFRE, c['patch'])}"
        if CORRIGIR and not MODO_SESSAO and tem_cmd("bun", "~/.bun/bin"):
            rc, out = rodar(cmd, timeout=300)
            if rc == 0:
                rodar(f"cd {d} && ~/.bun/bin/bun install", timeout=300)
            achar("corrigido" if rc == 0 else "erro", "Cartographer", "clonado + patch" if rc == 0 else out[-200:])
        else:
            achar(nivel, "Cartographer", "não instalado (pre-flight de impacto `carto.sh brief`)", cmd)
    else:
        rc, _ = rodar(["git", "-C", d, "apply", "--reverse", "--check", os.path.join(COFRE, c["patch"])], timeout=10)
        if rc != 0:
            achar(nivel, "Cartographer", "patch ESM (.js→.ts) não aplicado — brief sai sem impactados/testes em repo ESM",
                  f"git -C {d} apply {os.path.join(COFRE, c['patch'])}")
        elif not MODO_SESSAO:
            achar("ok", "Cartographer", "clonado com patch")
    at = c.get("atalho")
    if at and os.path.isdir(os.path.dirname(expandir(at["para"]))):
        if not symlink_para(expandir(at["para"]), os.path.join(COFRE, at["de"]), "carto.sh"):
            achar(nivel, "carto.sh", "atalho não ligado ao Cofre", CMD_CORRIGIR)


# ───────────────────────────── saída ─────────────────────────────

ICONE = {"ok": "✅", "corrigido": "🔧", "info": "ℹ️ ", "aviso": "⚠️ ", "erro": "❌"}


def main():
    m = ler_json(MANIFESTO, None)
    if m is None:
        print(f"manifesto ilegível: {MANIFESTO}", file=sys.stderr)
        return 2
    checar_cofre_git()
    checar_ferramentas(m)
    checar_marketplaces_e_plugins(m)
    checar_claude_md(m)
    checar_skills()
    checar_hooks_globais(m)
    checar_git_hooks(m)
    checar_cron(m)
    checar_cartographer(m)

    problemas = [a for a in achados if a[0] in ("erro", "aviso")]
    if MODO_SESSAO:
        if not problemas:
            return 0  # tudo certo = silêncio
        linhas = [f"{ICONE[n]} {i}: {d}" + (f"  → {c}" if c else "") for n, i, d, c in problemas]
        resumo = f"Máquina fora do padrão do ecossistema ({len(problemas)} item(ns)). Rode: {CMD_CORRIGIR}"
        print(json.dumps({
            "systemMessage": resumo + "\n" + "\n".join(linhas),
            "hookSpecificOutput": {"hookEventName": "SessionStart",
                                   "additionalContext": resumo + "\n" + "\n".join(linhas) +
                                   "\nAvise o usuário no início da resposta; não corrija sem ele pedir."},
        }, ensure_ascii=False))
        return 0

    ordem = {"erro": 0, "aviso": 1, "corrigido": 2, "info": 3, "ok": 4}
    print(f"Ecossistema — máquina {os.uname().nodename} — Cofre {COFRE}\n")
    for n, i, d, c in sorted(achados, key=lambda a: ordem[a[0]]):
        print(f"{ICONE[n]} {i}" + (f": {d}" if d else ""))
        if c and n in ("erro", "aviso"):
            print(f"     → {c}")
    erros = sum(1 for a in achados if a[0] == "erro")
    avisos = sum(1 for a in achados if a[0] == "aviso")
    print(f"\n{erros} erro(s), {avisos} aviso(s)." + ("" if CORRIGIR or not problemas else " Use --corrigir para aplicar o que é seguro."))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
