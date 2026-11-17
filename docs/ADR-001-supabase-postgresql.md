# ADR-001 — Persistência demonstrativa com Supabase PostgreSQL

**Projeto:** Sistema de Gestão de Agendamentos e Notificação de Exames — UBS CAIC  
**Decisão inicial:** 17/11/2026  
**Status atualizado:** arquitetura e infraestrutura **implantadas**; conta DEMO ativada, login e dados fictícios observados em avaliação técnica em 17/11/2026. **Sem homologação clínica ou ensaio formal de todos os cenários de ponta a ponta**.

## Contexto

O protótipo inicial utilizava Python `http.server`, HTML/CSS/JavaScript e arrays locais no navegador, sem persistência. A Experiência Prática 2 previa Django/MVT, SQLite no desenvolvimento e PostgreSQL futuramente.

Para a Experiência Prática IV foi adotado **Supabase PostgreSQL gerenciado** e **Vercel para a interface pública**, preservando-se o protótipo local Python para auditoria e teste baixável. A mudança permite demonstração pública sem manter uma instância Python em nuvem.

## Arquitetura implementada

1. **Repositório público no GitHub:** contém o código, o SQL e os workflows.
2. **Hospedagem final:** https://ubs-caic-gestao-avisos.vercel.app — interface estática HTML5/CSS3/JavaScript disponibilizada pela Vercel a partir da branch `main`.
3. **Supabase PostgreSQL 17:** projeto independente `ubs-caic-gestao-avisos` na região `sa-east-1`.
4. **Estrutura de dados criada:** `usuarios_operadores`, `agendamentos_consultas`, `exames_preventivos` e `notificacoes_demo`; restrições, relacionamentos, índices e políticas Row Level Security (RLS) por operador.
5. **Autenticação e persistência:** o cliente utiliza Supabase Auth e a Data API com chave pública para operar após login. A conta DEMO foi provisionada e confirmada; acesso autenticado e contador foram observados na interface. O PostgreSQL registrou 1 consulta, 1 exame e 1 notificação manual fictícia no levantamento de 17/11/2026. Ainda não há ensaio formal completo de reentrada e do bloqueio da 11ª inserção.
6. **Modo visitante público:** dados fictícios **apenas em memória no navegador**; não grava no Supabase. Não precisa de login.
7. **Teste local baixável:** `app.py`/`iniciar_teste.py` servem um protótipo Python isolado, sem dependências externas e sem banco de dados.
8. **Alternativa:** Supabase Edge Function `ubs-caic-demo`, usada também no endpoint de saúde.
9. **Processamento de notificações simuladas:** gatilho no PostgreSQL agenda lembretes 48h/24h antes de consultas futuras; Supabase Cron executa processamento a cada minuto, sem envio externo. A interface também registra avisos manuais de exames disponíveis.

## Verificação realizada

- Aplicadas as estruturas de `db/schema_supabase.sql`, `db/limite_conta_demo.sql` e `db/notificacoes_demo.sql`. Confirmadas quatro tabelas com RLS ativo e o job `ubs-caic-lembretes-simulados` ativo com execução programada a cada minuto.
- Edge Function implantada e verificada como ativa.
- Site na Vercel publicado com estado `READY` e acessado pelo workflow GitHub Actions.
- Workflow de monitoramento validou as URLs públicas e conexão com PostgreSQL (Status `Success`) e agenda verificações a cada 15 minutos.
- A interface autenticada e o contador DEMO foram observados em funcionamento; o banco continha 1 consulta, 1 exame e 1 aviso manual simulado em 17/11/2026. Os testes Python validam código e estruturas demonstrativas, mas **não substituem** ensaios E2E completos ou validação com pacientes reais.

## Divergências justificadas

- **Django/MVT e SQLite:** não usados na versão publicada; a interface é hospedada como site estático e o Supabase disponibiliza Auth e Data API.
- **Servidor Python:** mantido para avaliação local, sem conexão ao PostgreSQL.
- **Mensagens reais por WhatsApp/SMS e fila FIFO automática:** continuam fora do MVP. **Lembretes e avisos internos simulados**, inclusive cron, foram implementados.
- **Autenticação:** login da conta DEMO observado; ausência de teste formal documentado para todos os cenários (reentrada, concorrência, bloqueio da 11ª inserção).

Essa adaptação reduz o custo e o esforço de implantação de um projeto individual, mantendo rastreabilidade técnica no GitHub. Foram utilizadas modalidades gratuitas disponíveis no escopo acadêmico, sujeitas a limites dos provedores.

## Privacidade

Os modos público e local utilizam **somente dados fictícios**. A modalidade autenticada também não deve receber informações reais de pacientes, exames ou prontuários. A publicação e o uso de Supabase RLS **não equivalem a homologação, autorização institucional ou conformidade completa** para um sistema clínico.
