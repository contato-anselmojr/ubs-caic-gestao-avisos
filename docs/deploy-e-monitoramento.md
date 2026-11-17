# Implantação e monitoramento — Experiência Prática IV

## Endereço final da aplicação

**https://ubs-caic-gestao-avisos.vercel.app**

A interface final de demonstração está publicada na **Vercel** e vinculada à branch `main` deste repositório GitHub. O deploy foi confirmado no estado `READY` e a URL pública foi verificada por GitHub Actions.

A implantação anterior no Supabase Edge Functions foi preservada como alternativa técnica: https://vxaxhuxisigohsojsyct.supabase.co/functions/v1/ubs-caic-demo.

## Infraestrutura

- **GitHub:** repositório público, versionamento e testes automáticos.
- **Vercel:** hospedagem estática gratuita no escopo do projeto (HTML5, CSS3 e JavaScript), HTTPS e deploy pelo GitHub.
- **Supabase:** PostgreSQL 17 gerenciado, projeto `ubs-caic-gestao-avisos` na região `sa-east-1`, independente de outras aplicações.
- **Banco PostgreSQL:** tabelas `usuarios_operadores`, `agendamentos_consultas`, `exames_preventivos` e `notificacoes_demo`, com Row Level Security (RLS) habilitado.
- **Supabase Cron/pg_cron:** job ativo a cada minuto para processar eventos de lembretes simulados das consultas.
- **Python:** versão local baixável com `app.py` e `iniciar_teste.py`, sem usar banco de dados.

Esses provedores oferecem modalidades gratuitas utilizadas no contexto do MVP, sujeitas a cotas e eventuais mudanças de política.

## Operação dos modos de teste

O modo público da Vercel funciona **sem login** e utiliza informações fictícias temporárias, sem gravar no Supabase. A conta DEMO do modo autenticado foi criada, confirmada e observada em uso na interface em 17/11/2026; o PostgreSQL registrava 1 consulta, 1 exame e 1 aviso manual simulado naquele levantamento. O modo autenticado contém operações de leitura, escrita, atualização e exclusão por Supabase Auth/Data API com RLS, além de programação de lembretes demonstrativos. **A validação observada não equivale a ensaio formal completo de todos os cenários**, como reentrada depois de atualizar a página e bloqueio da 11ª inclusão. Nenhum dado real de pacientes deve ser inserido.

## Monitoramento de disponibilidade

O workflow `.github/workflows/monitoramento.yml` executa verificações automáticas agendadas a cada **15 minutos** no GitHub Actions. São verificadas:

1. A **URL final da Vercel**, incluindo a resposta HTTP e a presença de elementos principais da página HTML.
2. A **implantação alternativa do Supabase Edge Functions**.
3. O endpoint de saúde `https://vxaxhuxisigohsojsyct.supabase.co/functions/v1/ubs-caic-demo/health`, que testa conexão com PostgreSQL e retorna `status=ok` e `database=reachable` quando os recursos respondem.

Uma execução em **Success** indica que as verificações passaram naquele instante; uma execução **Failure** sinaliza a necessidade de investigar indisponibilidade ou erro de conteúdo. O agendamento do GitHub Actions pode sofrer atrasos; não foi implementado alerta externo dedicado por SMS ou email.

**Evidência técnica:** https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions/runs/44149438168 — execução nº 16, concluída com `Success`, incluindo verificações da Vercel, da Edge Function e do endpoint de saúde do Supabase. Esse monitoramento confirma disponibilidade pontual, **não** o êxito de notificações reais ou a redução de faltas de pacientes.

## Capturas de tela necessárias para a entrega

1. **Deploy:** navegador maximizado com a interface da UBS CAIC e barra de endereço contendo `https://ubs-caic-gestao-avisos.vercel.app`.
2. **Monitoramento:** GitHub Actions com o job `verificar-disponibilidade` em `Success` e os passos de checagem visíveis.

## Indicadores e conexão com o ODS 3

O planejamento relaciona o MVP à redução do absenteísmo, ao melhor aproveitamento de vagas e à diminuição de deslocamentos para buscar resultados de exames preventivos (**ODS 3 — Saúde e Bem-Estar; metas 3.7 e 3.8**). As métricas técnicas disponíveis no levantamento de 17/11/2026 foram **1 consulta fictícia, 1 exame fictício e 1 aviso manual simulado**. Não há dados de pacientes reais que permitam comprovar redução de faltas, realocação de consultas ou economia de viagens. A experiência do autor como ex-ACS fundamentou o diagnóstico; ela não se confunde com avaliação independente do parceiro externo.

## Limites técnicos, éticos e operacionais

O sistema é um protótipo acadêmico, **não é uma solução oficial ou homologada de saúde**. Não realiza envio real de WhatsApp/SMS, consulta a sistemas SUS, comunicação com laboratórios nem tratamento autorizado de dados de pacientes. O uso do PostgreSQL não equivale à segurança suficiente para produção clínica.

Para roteiro de demonstração, consulte [GUIA_DO_AVALIADOR.md](../GUIA_DO_AVALIADOR.md).
