# Conta DEMO compartilhada — UBS CAIC

## Objetivo

Permitir que professor e interessados testem a **persistência fictícia** no Supabase PostgreSQL usando uma única conta de avaliação, sem acesso a GitHub, Vercel ou ao painel Supabase.

**URL:** https://ubs-caic-gestao-avisos.vercel.app  
**Email reservado para a conta DEMO:** `avaliador.ubs.caic@example.com`  
**Senha:** definida no painel Supabase Auth pelo responsável e **não deve ser publicada no GitHub**. Compartilhar somente com os avaliadores.

**Estado de implantação:** trigger de limite aplicado ao PostgreSQL; interface com contador, exclusão e login preparada. A conta Supabase Auth precisa ser provisionada pelo responsável. **Não declarar a conta funcional até completar as etapas abaixo e testar o login.**

## Provisionar a conta (ação manual do proprietário)

1. Abra https://supabase.com/dashboard/project/vxaxhuxisigohsojsyct/auth/users.
2. No menu **Authentication → Users**, clique em **Add user** / **Create new user**.
3. Informe o email `avaliador.ubs.caic@example.com` e uma senha exclusiva para demonstração (pelo menos 12 caracteres). Se o painel oferecer a opção, marque o email como confirmado / **Auto Confirm User**, pois `example.com` é um domínio reservado para exemplos e não recebe email de confirmação.
4. Salve a conta. **Não envie a senha para este repositório.**
5. No SQL Editor do **mesmo projeto UBS CAIC**, execute:

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

6. Verifique a existência do perfil:

```sql
select p.nome_completo, p.perfil_acesso
from public.usuarios_operadores p
join auth.users u on u.id = p.id_operador
where u.email = 'avaliador.ubs.caic@example.com';
```

O resultado deve conter exatamente uma linha com `perfil_acesso = demonstracao`.

7. Entre na Vercel com esse email e senha. O site deve mostrar **Conta DEMO: 0/10 registros utilizados**.
8. Crie uma consulta fictícia e um exame fictício; recarregue a página, **entre novamente** e confirme que os registros reaparecem. Teste exclusão e o contador.
9. Teste o limite: ao chegar a 10 registros somados, uma 11ª tentativa deve falhar. Após excluir um registro, o próximo cadastro deve ser permitido.

## Regras de segurança

- A conta DEMO é **apenas uma identidade de autenticação do sistema UBS CAIC**; não concede acesso aos painéis GitHub, Vercel ou Supabase.
- O PostgreSQL aplica o limite de **10 registros simultâneos somados** entre `agendamentos_consultas` e `exames_preventivos`, por operador do perfil `demonstracao`.
- Os triggers `limite_demo_consultas` e `limite_demo_exames` fazem a verificação dentro da transação e serializam tentativas simultâneas do mesmo operador.
- As políticas RLS limitam leitura, edição e exclusão aos registros do próprio operador.
- O botão **Excluir** apaga o registro selecionado e libera uma vaga.
- Os usuários compartilham a mesma conta, portanto **todos os avaliadores dessa conta podem ver e apagar os mesmos registros fictícios**. Não é adequado para dados reais nem para informações privadas.
- O formulário de **criar conta** foi ocultado na interface, mas isso **não desabilita** o endpoint de inscrição do Supabase Auth. Para impedir criação de contas por fora do site, o proprietário deve **desabilitar novos cadastros** nas configurações de Supabase Authentication (verificar o nome atual do controle no painel). O login de contas existentes continua funcionando.
- Não publique senhas em arquivos versionados ou no frontend. Altere a senha da DEMO periodicamente ou após a avaliação se houver uso indevido.
- O limite não substitui controle de requisições ou proteção contra abuso de API. O Supabase pode aplicar cotas e rate limits.

## Arquivos relacionados

- `db/schema_supabase.sql`: tabelas e políticas RLS.
- `db/limite_conta_demo.sql`: migração com o limite da DEMO, **já aplicada ao banco**.
- `index.html`: contador, login, exclusão e mensagens de erro.
- `tests/test_demo_web.py`: verificação estrutural de recursos DEMO.

**Privacidade:** dados de saúde reais, telefones verdadeiros e identificações reais não devem ser utilizados em nenhuma modalidade. Não há envio real de WhatsApp/SMS.
