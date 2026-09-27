# {{PROJETO}} — diretivas para o Claude Code

## Cofre de Neurônios (consulta obrigatória, passo 0)

O conhecimento de stack e de domínio da casa vive em `{{COFRE}}`.
Consulte **antes** de responder ou codificar — não depois.

1. **Mapa:** `30_Atlas/Index.md` e o MOC do tema.
2. **Antes de tocar um arquivo:** `python3 {{COFRE}}/50_System/symbol_index.py <arquivo>` — mostra o que o cérebro já sabe sobre ele.
3. **Pediram um MÓDULO** (tarefas, estoque, vendas, compras, comissões, contratos, documentos, projetos, RH, chamados, chat, reservas, financeiro, indicadores…)? Leia `10_Neurons/Base_Catalogo_Modulos_Gestao.md`. A linha do módulo traz a **invariante que ele já resolve**, de quais módulos depende e os neurônios que o governam. Comece pela invariante, não pela tela.
4. **Vai criar ou refatorar tela?** `10_Neurons/Base_UI_Kit_Padrao_Projeto.md` **por inteiro** — é checklist de aceite, não sugestão.

> O que viaja entre projetos é **o modelo, a invariante e o nome do pacote** — nunca código
> copiado de outro repositório.

## Stack deste projeto (herdada — não se pergunta)

{{STACK}}

**O código local prevalece sobre a norma do Cofre.** Siga os padrões daqui; quando divergirem,
diga qual neurônio está sendo contrariado e por quê.

O `padraoLayout` é React e **não se copia para cá**: dele vem o modelo de módulo e as regras de
domínio, não os arquivos. Listagem/tabela nesta stack: ver `Base_Frontend_Listagens_DataTable`.

## Ao aprender algo

Decisão arquitetural, gotcha ou padrão novo vira **neurônio** em `meu-cerebro/10_Neurons/`,
ligado a um MOC, registrado em `20_Projects/Wiki_Log.md`, com `lint.py` e `catalog.py` rodados.
Conhecimento que não vira neurônio se perde. Antes de escrever no Cofre: `git pull` (ele roda em
mais de uma máquina).

## Invariantes inegociáveis

- "Compila" nunca é "pronto".
- Dinheiro em decimal, nunca float.
- A regra de negócio mora no **service** e **recusa**; a tela não é a defesa.
- Estado derivado (vencido, atrasado, disponível, em dobra) se calcula na leitura, **nunca se grava**.
- Registro que já produziu efeito não se reescreve: a correção é registro novo.
- Nunca afirme resultado de teste sem ter rodado.
