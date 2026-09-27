# 🗺️ Atlas Central

> **Gabarito do curso.** Este é o cérebro inteiro que você monta ao longo dos módulos 2 a 8.
> O seu começa vazio (`starter/`) e cresce uma engrenagem por módulo. Links para neurônios que
> ficaram de fora aparecem como stubs em `15_Stubs/` — o cérebro de origem é maior que este recorte.

> 📇 **Ver tudo de uma vez:** [[Catalogo_Neuronios]] (gerado por `catalog.py`). Pre-flight por
> arquivo de código: [[Indice_Simbolos]]. Cores do grafo: [[Legenda_Cores_Grafo]].
> 📖 **Como usar/manter o Cofre:** [[GUIA_USO_COFRE]]. Vocabulário de tags: [[Tags_Taxonomy]].

## 🏛️ Governança & Padrões
- [[WIKI_SCHEMA]]: Regras de Ingest, Lint, Indexação, Revisão e Composição.
- [[GUIA_USO_COFRE]]: Guia prático de uso e manutenção (comece aqui).
- [[Tags_Taxonomy]]: Vocabulário controlado e hierárquico de tags (o lint valida).
- [[EXTRACAO_PROJETO]]: Modelo/playbook p/ extrair um projeto novo para o Cofre (skill `extrair-projeto`).
- [[Wiki_Bootstrap_Protocol]]: Master Prompt para replicação desta Wiki.
- [[Wiki_Scalability_MOC_Pattern]]: Padrão de organização e escalabilidade do Wiki.
- [[Project_Isolation_Pattern_Wiki]]: Padrão de isolamento de projetos para evitar poluição do Atlas.
- [[Guia_Mapeamento_Projetos]]: O que mapear (e o que não) de um projeto.
- [[Persistencia_de_Contexto]]: Por que não depender da "memória" da LLM para a integridade do Cofre.
- [[Cofre_Grafo_Cores_Configuracao_Versionada]]: Política para as cores do Graph View acompanharem o Cofre entre máquinas.
- [[Parecer_Arquitetura_Cofre]] · [[Parecer_Estrategico_Engenharia]]: Pareceres sobre a arquitetura e o uso estratégico do Cofre.
- **Contratos de agente:** [[AGENTS]] (entrada mínima) · CODEX (contrato completo) · GEMINI · [[CLAUDE]] (Claude Code neste vault) · [[50_System/claude-global/CLAUDE|CLAUDE global]] (diretivas de toda máquina, copiado para `~/.claude/`).
- [[INSTALL_OUTRA_MAQUINA]]: Runbook para instalar o Cofre em outra máquina (clone, bootstrap, cron, hooks).
- **Templates** (`50_System/Templates/`): [[50_System/Templates/Neuron Template|Neuron]] · [[50_System/Templates/ADR Template|ADR]] · [[50_System/Templates/Projeto Kit Template|Projeto Kit]] · [[50_System/Templates/CLAUDE_projeto|CLAUDE_projeto]] · [[50_System/Templates/Sessao_Extracao_Template|Sessão de extração]].

## 🧭 Mapas de Conteúdo (MOCs)
- [[MOC_Projetos|📂 Projetos & Ecossistemas]]: Por projeto (ProjetoBC, ClienteBC, criptobotSoftEmp, Wbot, criptoChatSE, AnonEcom, Loteria, ESP32).
- [[MOC_Financeiro|💰 Financeiro & Pagamentos]]: Mercado Pago, Wallet, Trading e Regras.
- [[MOC_Infraestrutura|🏗️ Infraestrutura & DevOps]]: Docker, Traefik, Multi-tenancy e Shell Scripts.
- [[MOC_Desenvolvimento|💻 Desenvolvimento Backend]]: Node.js, Prisma, Zod, Testes e Padrões.
- [[MOC_Frontend|🎨 Frontend & UX]]: React, Canvas, Design Systems e Padrões de UI.
- [[MOC_Seguranca|🔒 Segurança]]: Auth, RBAC, hardening, criptografia e privacidade (cross-projeto).
- [[MOC_Padroes_Reutilizaveis|🔁 Padrões Reutilizáveis]]: Lições transversais "use quando…".
- [[MOC_Stack_Base|🧱 Stack Base SoftEmp]]: Kit prescritivo por camada (arquitetura→testes) p/ criar projeto novo e corrigir falhas.

## 🧠 Pessoal
- [[Minhas_Memorias|🧠 Minhas Memórias]]: Registro vivo de quem o operador é e do que o move — princípios e virtudes destilados das frases que ele dita, carimbadas com data e hora.

## 📜 Histórico & Logs
- [[20_Projects/Wiki_Log|Wiki Log]]: Histórico de alterações.

---
*Última atualização: 2026-09-25*
