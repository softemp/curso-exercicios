# Módulo 2 — Fundamentos

## Onde rodar
`curso-exercicios`. O cérebro é criado neste módulo a partir de `starter/`.

## Objetivo
Ter o cérebro criado a partir do esqueleto e o primeiro neurônio escrito à mão, com frontmatter válido, tag da taxonomia e link para o Index.

## Antes de começar
`./checar_modulo.sh 1` todo `✓`. Leia `cerebro` em `.curso.json`: é para lá que o esqueleto vai.

## Passos
1. [agente] Copie `starter/` para `<cerebro>` (`cp -r starter/. <cerebro>/`). Liste o que foi criado: `50_System/WIKI_SCHEMA.md`, `50_System/Tags_Taxonomy.md`, `50_System/Templates/`, `30_Atlas/Index.md`, `.obsidian/`, `README.md`.
2. [aluno] Abra `<cerebro>` no Obsidian como um vault novo. Verificação: o aluno confirma que vê `Index.md` no explorador.
3. [aluno] Leia `50_System/WIKI_SCHEMA.md`. O agente resume antes, em 5 linhas: um neurônio = uma ideia; todo neurônio tem frontmatter com `type`, `status`, `tags`, `source`, `created`; toda tag vem do `Tags_Taxonomy.md`; todo neurônio aparece em algum mapa do `30_Atlas/`; nada de órfão. Verificação: o aluno diz, com as próprias palavras, o que é um órfão.
4. [aluno] Crie o primeiro neurônio: `mkdir -p <cerebro>/10_Neurons` e copie `50_System/Templates/Neuron Template.md` para `10_Neurons/Por_Que_O_Agente_Esquece.md` e escreva nele a lição do módulo 1 (use `notas-modulo-1.md`). Preencha o frontmatter: `status: seedling`, tags `[status/seedling, area/engenharia, tipo/conceito, projeto/cofre]`, `source: "módulo 1 do curso"`, `created` com a data de hoje e `summary:` com uma frase (a mesma que abre o "Conceito"). Na seção "Conexões", troque os links de exemplo do template: deixe só `- MOC: [[Index]]` e apague as linhas com `[[MOC_Exemplo]]` e `[[Outro_Neuronio]]` (link para nota inexistente reprova o lint do módulo 6). Exemplo de neurônio real: `gabarito/modulo-2/10_Neurons/Persistencia_de_Contexto.md`. Verificação: `grep -c "^type: neuron" <cerebro>/10_Neurons/Por_Que_O_Agente_Esquece.md` dá 1 e o arquivo tem `status/seedling`.
5. [aluno] Abra `<cerebro>/30_Atlas/Index.md` e acrescente, na seção "Governança & Padrões", a linha `- [[Por_Que_O_Agente_Esquece]]: por que a memória do agente não é memória do projeto.` Verificação: `grep -c "Por_Que_O_Agente_Esquece" <cerebro>/30_Atlas/Index.md` dá 1.
6. [agente] Peça ao aluno para abrir o grafo do Obsidian e confirmar que o novo neurônio aparece ligado ao Index. Se não aparecer, o link do passo 5 está errado.

## Saiu rodando
`./checar_modulo.sh 2` — todo `✓`.

## Compare com o gabarito
`./comparar.sh 2`. Diferenças esperadas: o gabarito tem `Persistencia_de_Contexto.md`, o seu tem `Por_Que_O_Agente_Esquece.md` (**escolha sua**); arquivos em `.obsidian/` (**ruído**). Qualquer outra diferença em `50_System/` ou no `Index` é **lacuna**.

## Como adaptar
Idêntico em qualquer agente.

## Fechamento
Grave em `.curso.json`: `modulo_atual = 3` e `checks["2"] = <data>`. Diga: "O módulo 3 roda dentro do seu cérebro: abra o agente em `<cerebro>` e chame `/curso`."
