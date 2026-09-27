# curso-exercicios

Material prático do curso **"Como criar um cérebro para o seu agente de código"**.

| Pasta | O que é |
|---|---|
| `starter/` | Esqueleto do seu cérebro. Copie para o caminho gravado em `.curso.json` (padrão `~/meu-cerebro`) no módulo 2 e construa em cima. |
| `gabarito/modulo-N/` | Como o seu cérebro deve estar ao fim do módulo N. Compare com `./comparar.sh N`. |
| `gabarito/completo/` | O cérebro inteiro que o curso monta (igual ao `modulo-8`). |
| `projeto-exemplo/` | O padraoLayout, projeto que você extrai no módulo 5 (submódulo git). |
| `roteiros/` | Roteiros que o agente segue em cada módulo. |

Clone com submódulos:

```bash
git clone --recurse-submodules https://github.com/softemp/curso-exercicios.git
```

## Ordem dos módulos
0. Preparando a máquina
1. O problema
2. Fundamentos
3. Starter vivo
4. Regras
5. Extrair um projeto
6. Manutenção
7. Multi-máquina
8. Estudo de caso

`gabarito/` e `starter/` são **gerados** a partir de um cérebro real. Não edite: o seu cérebro fica no caminho gravado em `.curso.json` (padrão `~/meu-cerebro`).

## Como começar
1. Clone com submódulos (comando acima).
2. Abra o Claude Code neste diretório e diga **"vamos começar o curso"** (ou cole o conteúdo de `roteiros/modulo-0.md` em qualquer agente).
3. O módulo 0 instala a skill `/curso`; a partir daí, `/curso` continua de onde você parou.

Gate de cada módulo: `./checar_modulo.sh N`. Comparação com o gabarito: `./comparar.sh N`.

## Aviso para quem já tem outro Cofre na máquina
`50_System/checar_maquina.py --corrigir`, `bootstrap-maquina.sh` e `install-hooks.sh` registram hooks globais do Claude Code apontando para o vault de onde são executados. Rode-os só a partir do **seu** cérebro, no caminho gravado em `.curso.json` (padrão `~/meu-cerebro`), nunca de dentro de `gabarito/`.
