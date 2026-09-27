# Módulo 1 — O problema

## Onde rodar
`curso-exercicios`. Os experimentos acontecem num projeto do aluno, mas as anotações ficam aqui.

## Objetivo
Sentir na prática as três falhas que o cérebro resolve: o agente que improvisa convenção, o que repete um erro já corrigido e o contexto que morre com a sessão.

## Antes de começar
`./checar_modulo.sh 0` todo `✓`.

## Passos
1. [aluno] Escolha um projeto seu que tenha banco de dados (qualquer stack). Abra uma sessão do agente nele e peça: "crie um modelo `Pedido` com os campos usuais e timestamps de criação e atualização". Anote o nome que o agente deu às colunas de data (camelCase? snake_case? você pediu algum?). Verificação: o aluno cola aqui o trecho do schema gerado.
2. [aluno] Feche essa sessão. Abra outra no mesmo projeto e pergunte: "o que decidimos sobre o nome das colunas de data?". Anote a resposta. Verificação: o aluno cola a resposta.
3. [aluno] Ainda no seu projeto, pense num bug que você já corrigiu duas vezes com o agente (ou um padrão que precisou explicar de novo). Escreva uma frase sobre ele. Verificação: a frase existe.
4. [agente] Crie `notas-modulo-1.md` na raiz deste repositório (ele está no `.gitignore`) com três seções: "Convenção improvisada", "Memória que morreu", "Erro repetido", e cole embaixo de cada uma o que o aluno anotou. Confirme que o arquivo tem pelo menos 3 linhas de conteúdo.
5. [agente] Explique em até 8 linhas por que isso acontece: o agente lê o que está no diretório e no prompt; a "memória" da sessão não é memória do projeto; regra que não está escrita num lugar que ele lê antes de agir não existe. É isso que o cérebro corrige: um lugar único, versionado, que o agente lê antes de qualquer trabalho.

## Saiu rodando
`./checar_modulo.sh 1` — todo `✓` (repete os checks do módulo 0; o que prova este módulo é o `notas-modulo-1.md` com as três observações).

## Compare com o gabarito
Não se aplica: este módulo não monta nada de propósito. O gabarito começa no módulo 2.

## Como adaptar
Idêntico em qualquer agente.

## Fechamento
Grave em `.curso.json`: `modulo_atual = 2` e `checks["1"] = <data>`. Diga: "No módulo 2 você cria o seu cérebro e o primeiro neurônio."
