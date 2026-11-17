-- MIGRAÇÃO APLICADA NO PROJETO SUPABASE UBS CAIC
-- Limite combinado de 10 registros para perfil 'demonstracao'.
-- Não provisiona usuários Auth: crie a conta pelo painel Supabase Authentication > Users.
-- Depois vincule-a ao perfil 'demonstracao' com o comando de configuração do guia.

alter table public.usuarios_operadores
  drop constraint if exists usuarios_operadores_perfil_acesso_check;
alter table public.usuarios_operadores
  add constraint usuarios_operadores_perfil_acesso_check
  check (perfil_acesso in ('recepcao', 'coordenacao', 'demonstracao'));

create or replace function public.limitar_registros_conta_demo()
returns trigger
language plpgsql
security invoker
set search_path = ''
as $$
declare
  total integer;
begin
  if exists (
    select 1 from public.usuarios_operadores p
    where p.id_operador = new.id_operador and p.perfil_acesso = 'demonstracao'
  ) then
    perform pg_catalog.pg_advisory_xact_lock(
      pg_catalog.hashtextextended(new.id_operador::text, 27011)
    );
    select
      (select count(*) from public.agendamentos_consultas a where a.id_operador = new.id_operador) +
      (select count(*) from public.exames_preventivos e where e.id_operador = new.id_operador)
    into total;
    if total >= 10 then
      raise exception 'Limite da conta DEMO: 10 registros (consultas + exames). Exclua um registro antes de cadastrar outro.'
        using errcode = '23514';
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists limite_demo_consultas on public.agendamentos_consultas;
create trigger limite_demo_consultas
before insert on public.agendamentos_consultas
for each row execute function public.limitar_registros_conta_demo();

drop trigger if exists limite_demo_exames on public.exames_preventivos;
create trigger limite_demo_exames
before insert on public.exames_preventivos
for each row execute function public.limitar_registros_conta_demo();

revoke all on function public.limitar_registros_conta_demo() from public, anon, authenticated;
