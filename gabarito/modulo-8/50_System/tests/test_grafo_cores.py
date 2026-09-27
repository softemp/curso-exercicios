"""Testes do grafo_cores.py — unittest (stdlib), sobre um mini-vault em diretório temporário.
Rodar: python3 -m unittest discover -s 50_System/tests -v
"""
import json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafo_cores as gc


def _w(root, rel, txt):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(txt)


def _vault(root):
    _w(root, "10_Neurons/Proj_A.md", "---\ntags: [status/evergreen, projeto/proj]\n---\n# A\n")
    _w(root, "10_Neurons/Proj_B.md", "# B sem frontmatter\n")
    _w(root, "10_Neurons/Base_X.md", "---\ntags: [projeto/vailonge, area/web]\n---\n# X\n")
    _w(root, "10_Neurons/Solto_Y.md", "---\ntags: [projeto/semgrupo]\n---\n# Y\n")
    _w(root, "30_Atlas/Index.md", "# Index\n")
    _w(root, ".git/objects/lixo.md", "# não conta\n")
    _w(root, "50_System/grafo_cores.json", json.dumps({"grupos": [
        {"id": "proj", "emoji": "🟠 Laranja", "cor": "#F0883E", "nome": "Proj", "prefixos": ["Proj_"], "tags": ["projeto/proj"], "paths": []},
        {"id": "vailonge", "emoji": "🧡 Coral", "cor": "#FF7F50", "nome": "VaiLonge", "prefixos": [], "tags": ["projeto/vailonge"], "paths": []},
        {"id": "vazio", "emoji": "⚪ Cinza", "cor": "#8A8F98", "nome": "Vazio", "prefixos": ["Nada_"], "tags": [], "paths": []},
        {"id": "atlas", "emoji": "⬜ Branco", "cor": "#FFFFFF", "nome": "Atlas", "prefixos": [], "tags": [], "paths": ["30_Atlas"]},
    ]}))
    _w(root, ".obsidian/graph.json", json.dumps({"scale": 2.5, "colorGroups": [{"query": "velho", "color": {"a": 1, "rgb": 1}}], "close": True}))


class GrafoCores(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        _vault(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_query_gerada(self):
        g = {"prefixos": ["A_", "B_"], "tags": ["projeto/x"], "paths": ["30_Atlas"]}
        self.assertEqual(gc.query(g), "file:A_ OR file:B_ OR tag:#projeto/x OR path:30_Atlas")

    def test_rgb(self):
        self.assertEqual(gc.rgb("#E0A526"), 14722342)
        self.assertEqual(gc.rgb("#FFFFFF"), 16777215)

    def test_contagem_por_prefixo_tag_e_path_ignora_git(self):
        r = gc.gerar(self.root, dry_run=True, hoje="2026-09-26")
        self.assertEqual(r["contagem"], {"proj": 2, "vailonge": 1, "vazio": 0, "atlas": 1})
        self.assertEqual(r["vazios"], ["vazio"])
        self.assertEqual(r["orfas"], {"projeto/semgrupo": 1})

    def test_dry_run_nao_escreve(self):
        gc.gerar(self.root, dry_run=True, hoje="2026-09-26")
        self.assertFalse(os.path.exists(os.path.join(self.root, gc.LEGENDA_REL)))
        g = json.load(open(os.path.join(self.root, gc.GRAPH_REL)))
        self.assertEqual(g["colorGroups"][0]["query"], "velho")

    def test_gera_graph_preservando_outras_chaves(self):
        gc.gerar(self.root, hoje="2026-09-26")
        g = json.load(open(os.path.join(self.root, gc.GRAPH_REL)))
        self.assertEqual(g["scale"], 2.5)
        self.assertEqual([c["query"] for c in g["colorGroups"]],
                         ["file:Proj_ OR tag:#projeto/proj", "tag:#projeto/vailonge", "file:Nada_", "path:30_Atlas"])
        self.assertEqual(g["colorGroups"][0]["color"], {"a": 1, "rgb": 15763518})

    def test_podar_omite_vazios_dos_dois_artefatos(self):
        gc.gerar(self.root, podar=True, hoje="2026-09-26")
        g = json.load(open(os.path.join(self.root, gc.GRAPH_REL)))
        self.assertEqual(len(g["colorGroups"]), 3)
        leg = open(os.path.join(self.root, gc.LEGENDA_REL), encoding="utf-8").read()
        self.assertNotIn("Vazio", leg)
        self.assertIn("| 🟠 Laranja | `#F0883E` | **Proj** | `file:Proj_ OR tag:#projeto/proj` | 2 |", leg)

    def test_legenda_tem_frontmatter_gerado_e_links(self):
        gc.gerar(self.root, hoje="2026-09-26")
        leg = open(os.path.join(self.root, gc.LEGENDA_REL), encoding="utf-8").read()
        self.assertTrue(leg.startswith("---\ntype: reference\ngenerated: true\n"))
        self.assertIn("created: 2026-09-26", leg)
        self.assertIn("[[Cofre_Grafo_Cores_Configuracao_Versionada]]", leg)
        self.assertIn("| ⚪ Cinza | `#8A8F98` | **Vazio** | `file:Nada_` | 0 |", leg)

    def test_graph_ausente_nasce_minimo(self):
        os.remove(os.path.join(self.root, gc.GRAPH_REL))
        gc.gerar(self.root, hoje="2026-09-26")
        g = json.load(open(os.path.join(self.root, gc.GRAPH_REL)))
        self.assertIn("linkDistance", g)
        self.assertEqual(len(g["colorGroups"]), 4)


if __name__ == "__main__":
    unittest.main()


class PrimeiroGrupoQueCasa(unittest.TestCase):
    def test_nota_conta_so_no_primeiro_grupo(self):
        with tempfile.TemporaryDirectory() as root:
            _w(root, "10_Neurons/Proj_A.md", "# A\n")
            _w(root, "50_System/grafo_cores.json", json.dumps({"grupos": [
                {"id": "amplo", "emoji": "⚫", "cor": "#000000", "nome": "Amplo", "prefixos": ["Proj"], "tags": [], "paths": []},
                {"id": "estreito", "emoji": "⚪", "cor": "#FFFFFF", "nome": "Estreito", "prefixos": ["Proj_"], "tags": [], "paths": []},
            ]}))
            r = gc.gerar(root, dry_run=True, hoje="2026-09-26")
            self.assertEqual(r["contagem"], {"amplo": 1, "estreito": 0})
