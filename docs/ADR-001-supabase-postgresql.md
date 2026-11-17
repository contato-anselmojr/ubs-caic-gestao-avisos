# ADR-001 — Persistência demonstrativa com Supabase PostgreSQL

**Projeto:** Sistema de Gestão de Agendamentos e Notificação de Exames — UBS CAIC  
**Decisão inicial:** 17/11/2026  
**Status atualizado:** arquitetura e infraestrutura **implantadas**; autenticação/gravação de ponta a ponta **ainda não homologadas com usuário de teste**.

## Contexto

O protótipo inicial utilizava Python `http.server`, HTML/CSS/JavaScript e arrays locais no navegador, sem persistência. A Experiência Prática 2 previa Django/MVT, SQLite no desenvolvimento e PostgreSQL futuramente.

Para a Experiência Prática IV foi adotado **Supabase PostgreSQL gerenciado** e **Vercel para a interface pública**, preservando-se o protótipo local Python para auditoria e teste baixável. A mudança permite demonstração pública sem manter uma instância Python em nuvem.

## Arquitetura implementada

1. **Repositório público no GitHub:** contém o código, o SQL e os workflows.
2. **Hospedagem final:** https://ubs-caic-gestao-avisos.vercel.app — interface estática HTML5/CSS3/JavaScript disponibilizada pela Vercel a partir da branch `main`.
3. **Supabase PostgreSQL 17:** projeto independente `ubs-caic-gestao-avisos` na região `sa-east-1`.
4. **Estrutura de dados criada:** `usuarios_operadores`, `agendamentos_consultas`, `exames_preventivos`; restrições, relacionamentos, índices e políticas Row Level Security (RLS) por operador.
5. **Autenticação e persistência:** código cliente utiliza Supabase Auth e a Data API com chave pública para operar apenas após login. **Não foi comprovado por teste de ponta a ponta** o ciclo de cadastro, confirmação de email, login e persistência após atualização.
6. **Modo visitante público:** dados fictícios **apenas em memória no navegador**; não grava no Supabase. Não precisa de login.
7. **Teste local baixável:** `app.py`/`iniciar_teste.py` servem um protótipo Python isolado, sem dependências externas e sem banco de dados.
8. **Alternativa:** Supabase Edge Function `ubs-caic-demo`, usada também no endpoint de saúde.

## Verificação realizada

- Aplicada migração do esquema `db/schema_supabase.sql` e confirmada a criação das três tabelas com RLS ativo.
- Edge Function implantada e verificada como ativa.
- Site na Vercel publicado com estado `READY` e acessado pelo workflow GitHub Actions.
- Workflow de monitoramento validou as URLs públicas e conexão com PostgreSQL (Status `Success`) e agenda verificações a cada 15 minutos.
- Os testes unitários Python validam o servidor local, formulários e procedimentos técnicos, **não substituindo** testes completos de login e persistência.

## Divergências justificadas

- **Django/MVT e SQLite:** não usados na versão publicada; a interface é hospedada como site estático e o Supabase disponibiliza Auth e Data API.
- **Servidor Python:** mantido para avaliação local, sem conexão ao PostgreSQL.
- **WhatsApp/SMS automático e fila FIFO:** continuam pendentes.
- **Autenticação:** implementação frontend disponível, mas a operação completa precisa ser validada com uma conta de testes.

Essa adaptação reduz o custo e o esforço de implantação de um projeto individual, mantendo rastreabilidade técnica no GitHub. Foram utilizadas modalidades gratuitas disponíveis no escopo acadêmico, sujeitas a limites dos provedores.

## Privacidade

Os modos público e local utilizam **somente dados fictícios**. A modalidade autenticada também não deve receber informações reais de pacientes, exames ou prontuários. A publicação e o uso de Supabase RLS **não equivalem a homologação, autorização institucional ou conformidade completa** para um sistema clínico.
