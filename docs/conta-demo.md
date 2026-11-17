# Conta DEMO compartilhada — UBS CAIC

## Objetivo

Permitir que professor e interessados testem a **persistência fictícia** no Supabase PostgreSQL usando uma única conta de avaliação, sem acesso a GitHub, Vercel ou ao painel Supabase.

**URL:** https://ubs-caic-gestao-avisos.vercel.app  
**Email de login da conta DEMO (criada e confirmada):** `avaliador.ubs.caic@example.com`  
**Senha pública da conta de avaliação:** `teste1234567` — divulgada a pedido do proprietário para permitir testes por qualquer interessado. **Não concede acesso administrativo** aos painéis GitHub, Vercel ou Supabase. **Qualquer pessoa que conheça essas credenciais poderá acessar e excluir os dados fictícios compartilhados**.

**Estado de implantação (17/11/2026):** usuário Auth **criado, email confirmado e perfil `demonstracao` vinculado** à tabela `usuarios_operadores`. Triggers de limite aplicados ao PostgreSQL; interface com contador e exclusão publicada na Vercel. **O acesso autenticado e o contador de uso da conta foram observados na interface; o PostgreSQL continha 1 consulta e 1 exame fictícios no levantamento de 17/11/2026.** Não está documentado ensaio formal completo de reentrada após atualização ou do bloqueio da 11ª inclusão.

## Provisionamento realizado (para auditoria e reprodução)

1. **Concluído:** o proprietário criou a conta em https://supabase.com/dashboard/project/vxaxhuxisigohsojsyct/auth/users.
2. **Concluído:** o usuário está presente no Supabase Authentication → Users.
3. **Concluído:** email `avaliador.ubs.caic@example.com` confirmado. A senha foi definida pelo proprietário e não é recuperável em texto simples.
4. **Concluído:** conta salva. O proprietário optou por publicar exclusivamente a senha da conta DEMO compartilhada; não utilizar essa senha em nenhuma conta pessoal ou administrativa.
5. **Executado com sucesso no banco UBS CAIC:** o comando abaixo vinculou o perfil `demonstracao` à conta Auth:

```sql
insert into public.usuarios_operadores
    (id_operador, nome_completo, perfil_acesso)
select id, 'Avaliador DEMO UBS CAIC', 'demonstracao'
from auth.users
where email = 'avaliador.ubs.caic@example.com'
on conflict (id_operador)
do update set nome_completo = excluded.nome_completo,
              perfil_acesso = excluded.perfil_acesso;
```

6. **Confirmado:** o perfil `demonstracao` foi vinculado ao usuário. Para consultar novamente:

```sql
select p.nome_completo, p.perfil_acesso
from public.usuarios_operadores p
join auth.users u on u.id = p.id_operador
where u.email = 'avaliador.ubs.caic@example.com';
```

O resultado deve conter exatamente uma linha com `perfil_acesso = demonstracao`.

7. **Acesso autenticado observado em 17/11/2026:** a interface da Vercel mostrou a conta DEMO e o contador **2/10 registros utilizados**. A quantidade muda conforme os avaliadores criam ou excluem dados fictícios.
8. **Roteiro recomendado ao avaliador:** crie uma consulta fictícia e um exame fictício; recarregue a página, **entre novamente** e confirme que os registros reaparecem. Teste exclusão e o contador. A sessão não é restaurada automaticamente ao recarregar.
9. Teste o limite: ao chegar a 10 registros somados, uma 11ª tentativa deve falhar. Após excluir um registro, o próximo cadastro deve ser permitido.

## Regras de segurança

- A conta DEMO é **apenas uma identidade de autenticação do sistema UBS CAIC**; não concede acesso aos painéis GitHub, Vercel ou Supabase.
- O PostgreSQL aplica o limite de **10 registros simultâneos somados** entre `agendamentos_consultas` e `exames_preventivos`, por operador do perfil `demonstracao`.
- Os triggers `limite_demo_consultas` e `limite_demo_exames` fazem a verificação dentro da transação e serializam tentativas simultâneas do mesmo operador.
- As políticas RLS limitam leitura, edição e exclusão aos registros do próprio operador.
- O botão **Excluir** apaga o registro selecionado e libera uma vaga.
- Os usuários compartilham a mesma conta, portanto **todos os avaliadores dessa conta podem ver e apagar os mesmos registros fictícios**. Não é adequado para dados reais nem para informações privadas.
- O formulário de **criar conta** foi ocultado na interface, mas isso **não desabilita** o endpoint de inscrição do Supabase Auth. Para impedir criação de contas por fora do site, o proprietário deve **desabilitar novos cadastros** nas configurações de Supabase Authentication (verificar o nome atual do controle no painel). O login de contas existentes continua funcionando.
- **Exceção deliberada para esta conta de demonstração:** a senha DEMO é pública para facilitar a avaliação, portanto não deve ser reutilizada. Troque-a ou desative a conta se houver abuso. **Nunca publique senhas de contas reais, administrativas, tokens ou chaves de API.**
- O limite não substitui controle de requisições ou proteção contra abuso de API. O Supabase pode aplicar cotas e rate limits.

## Arquivos relacionados

- `db/schema_supabase.sql`: tabelas e políticas RLS.
- `db/limite_conta_demo.sql`: migração com o limite da DEMO, **já aplicada ao banco**.
- `index.html`: contador, login, exclusão e mensagens de erro.
- `tests/test_demo_web.py`: verificação estrutural de recursos DEMO.

**Privacidade:** dados de saúde reais, telefones verdadeiros e identificações reais não devem ser utilizados em nenhuma modalidade. Não há envio real de WhatsApp/SMS.

## Lembretes e avisos simulados — implementação ativa, sem SMS real

No modo autenticado, o gatilho `trg_programar_lembretes_demo` agenda eventos **48 e 24 horas antes** de consultas futuras elegíveis na tabela `public.notificacoes_demo`. O job ativo `ubs-caic-lembretes-simulados` do **Supabase Cron/pg_cron** processa os eventos vencidos **a cada minuto**, mesmo com a página fechada. A Central de Notificações também permite registrar manualmente **avisos simulados** de resultados marcados como disponíveis na aba Fila e Alertas, com histórico fictício e sem divulgar conteúdo clínico. A migração correspondente é `db/notificacoes_demo.sql`.

**Não há integração com operadora de SMS ou API WhatsApp, envio ao paciente, confirmação de entrega ou acompanhamento clínico real.** Para envio efetivo seriam necessários serviço autorizado, consentimento ou outra base legal aplicável, governança de dados, auditoria e tratamento de falhas. Não use dados pessoais verdadeiros neste MVP.
