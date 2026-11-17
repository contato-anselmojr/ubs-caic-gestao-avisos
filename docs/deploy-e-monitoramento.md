# Implantação pública — Experiência Prática IV

## Status

- Supabase project: `ubs-caic-gestao-avisos` (região sa-east-1, PostgreSQL 17).
- Projeto separado da loja Bella Pink.
- Tabelas `usuarios_operadores`, `agendamentos_consultas` e `exames_preventivos` criadas, com Row Level Security (RLS) habilitado e acesso segregado pelo operador autenticado.
- Interface pública de demonstração em **Supabase Edge Functions (Deno/TypeScript)**, preservando o layout HTML/CSS/JavaScript do protótipo Python.
- Modo visitante: dados **fictícios e temporários**, sem persistência.
- Modo operador: requer conta de testes no Supabase Auth; após login, operações de cadastro/listagem e atualização de exame utilizam a Data API protegida por token e políticas RLS.
- Nenhuma mensagem WhatsApp/SMS é enviada. **Não utilizar dados reais de pacientes**.

## Endereço da aplicação

https://vxaxhuxisigohsojsyct.supabase.co/functions/v1/ubs-caic-demo

## Endpoint de monitoramento

https://vxaxhuxisigohsojsyct.supabase.co/functions/v1/ubs-caic-demo/health

O endpoint HTTP verifica a disponibilidade da Edge Function e tenta uma leitura mínima no PostgreSQL com credencial de serviço **restrita ao ambiente server-side** da função. Retorna `200 {"status":"ok","service":"ubs-caic-demo","database":"reachable"}` quando ambos respondem e `503 {"status":"down"}` em caso de falha. Nenhum dado de paciente é exposto por esse endpoint.

## Monitoramento GitHub Actions

Arquivo: `.github/workflows/monitoramento.yml`.

Gatilhos: agendamento a cada 15 minutos em UTC, execução manual e envio da própria configuração. Utiliza `curl` e falha se o endpoint retornar HTTP não 2xx ou se os indicadores `status=ok` e `database=reachable` não estiverem presentes. O resultado fica registrado em GitHub Actions como **Success (UP)** ou **Failure (possível DOWN)**. Não há ainda alertas externos por email/SMS configurados; a detecção depende de consultar o painel ou as notificações habituais do GitHub.

## Distinção do protótipo anterior

O arquivo local `app.py` continua disponível para executar a interface como protótipo com `http.server`. O deploy público utiliza a implementação da interface em **Edge Function Deno**, não hospeda Python. Essa adaptação minimiza a necessidade de contratar uma segunda hospedagem, mas diverge da arquitetura Django/MVT planejada na Experiência Prática 2.

## Testes e limitações

- O SQL aplicado foi verificado no banco de dados e as três tabelas estão vazias por padrão.
- O painel do Supabase indica a Edge Function como ativa. A disponibilidade pública é verificada pelo workflow de monitoramento após o merge para a branch principal.
- Cadastro/login dependem das configurações de email do Supabase Auth; se a confirmação de email estiver habilitada, o operador deverá confirmar a conta.
- A interface pode exibir formulários para cadastro, mas não deve ser utilizada para informações de pacientes reais. Este projeto não é um sistema clínico de produção e não foi submetido a homologação por uma unidade de saúde.
- A verificação de cobertura de 71% feita na Experiência Prática III corresponde ao **backend Python anterior**, não à execução Deno e à integração real com PostgreSQL.

## Evidências sugeridas

1. Screenshot do navegador exibindo a URL pública acima na barra de endereço e a tela principal.
2. Screenshot do GitHub Actions com o job `verificar-disponibilidade` verde e a resposta `UP`.
3. Captura opcional do Supabase Table Editor com as três tabelas e RLS habilitado, sem informação sensível.
