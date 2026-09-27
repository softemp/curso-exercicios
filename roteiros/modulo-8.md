# Módulo 8 — Estudo de caso

## Onde rodar
`curso-exercicios`.

## Objetivo
Ver um cérebro inteiro, entender cada diferença entre ele e o seu, e sair com o plano dos próximos neurônios do seu projeto.

## Antes de começar
`./checar_modulo.sh 7` todo `✓`.

## Passos
1. [agente] Rode `./comparar.sh 8 <cerebro>` e guarde a saída. Agrupe as diferenças em três listas: arquivos só no gabarito, arquivos só no seu cérebro, arquivos diferentes.
2. [aluno] Para cada arquivo só no gabarito, decida com o agente: **lacuna** (algo de um módulo que ficou faltando: volte lá), **escolha sua** (um MOC temático que você ainda não precisa, um neurônio de parecer) ou **ruído**. Verificação: o aluno consegue justificar cada item em uma frase.
3. [aluno] Abra `gabarito/completo` no Obsidian. Percorra: os stubs em `15_Stubs/` (o cérebro de origem é maior que o recorte: é assim que o seu vai crescer), as cores do grafo (`30_Atlas/Legenda_Cores_Grafo.md`), o `Catalogo_Neuronios.md`. Leia `10_Neurons/Parecer_Arquitetura_Cofre.md`, a revisão crítica do cofre feita no bootstrap: pontos fortes (pastas numeradas, fluxo Inbox → Neurons → Archive, `WIKI_SCHEMA` como governança, protocolo de bootstrap que segue o próprio template); oportunidades (sem `.obsidian/` pré-configurado, Inbox sem prazo, sem `MOC_Projetos`, sem convenção de nome de arquivo, sem backup); o risco (contexto dependente de "memória global" do modelo, resolvido fazendo o vault ser o contexto); e a nota v1 → v2 depois das correções. Verificação: o aluno cita uma fragilidade que reconhece no próprio cérebro ou que quer evitar.
4. [aluno] No seu cérebro, acrescente ao `20_Projects/Wiki_Log.md`: `## [<hoje>] curso | módulo 8 concluído` com duas linhas: o que o `comparar.sh 8` mostrou e os **três próximos neurônios** do seu projeto (nome e uma frase cada). Commit no cérebro. Verificação: `grep -c "curso | módulo 8" <cerebro>/20_Projects/Wiki_Log.md` dá 1.
5. [agente] Rode `./checar_modulo.sh 8`.
6. [agente] Pergunte se o aluno quer remover a skill do curso (`bash instalar-skill.sh --remover`). O cérebro fica; o curso sai.

## Saiu rodando
`./checar_modulo.sh 8` — todo `✓`.

## Compare com o gabarito
`./comparar.sh 8 <cerebro>` foi o passo 1. Aqui a comparação é a aula, não a prova.

## Como adaptar
Qualquer agente (Claude Code, Codex, Cursor, Gemini CLI): o módulo só lê e compara; `comparar.sh` é bash.

## Fechamento
Grave em `<exercicios>/.curso.json`: `modulo_atual = 9` e `checks["8"] = <data>`. Diga: "Curso concluído. O cérebro agora é seu: o próximo neurônio é o que você extrair amanhã."
