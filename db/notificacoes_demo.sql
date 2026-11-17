-- UBS CAIC: notificacoes SIMULADAS. Aplicado no Supabase em 17/11/2026.
-- Nao ha integracao com SMS, WhatsApp ou dados reais.
create schema if not exists internal_ubs;
alter table public.exames_preventivos drop constraint if exists exames_preventivos_status_laudo_check;
alter table public.exames_preventivos add constraint exames_preventivos_status_laudo_check
 check(status_laudo in ('aguardando_laboratorio','disponivel','disponivel_notificado','retirado_paciente'));
create table if not exists public.notificacoes_demo (
 id_notificacao uuid primary key default gen_random_uuid(),
 id_operador uuid not null references public.usuarios_operadores(id_operador),
 id_agendamento uuid references public.agendamentos_consultas(id_agendamento) on delete cascade,
 id_exame uuid references public.exames_preventivos(id_exame) on delete cascade,
 tipo text not null check(tipo in ('lembrete_48h','lembrete_24h','resultado_disponivel')),
 origem text not null check(origem in ('automatico','manual')),
 nome_paciente text not null,
 telefone_destino text not null,
 mensagem text not null,
 programada_para timestamptz not null,
 simulada_em timestamptz,
 status text not null default 'agendada' check(status in ('agendada','simulada','cancelada')),
 constraint notificacao_origem_consistente check (
  (tipo='resultado_disponivel' and id_exame is not null and id_agendamento is null and origem='manual')
  or (tipo in ('lembrete_48h','lembrete_24h') and id_agendamento is not null and id_exame is null and origem='automatico')),
 constraint lembrete_unico unique(id_agendamento,tipo)
);
create index if not exists idx_notificacoes_demo_vencimento on public.notificacoes_demo(programada_para) where status='agendada';
create index if not exists idx_notificacoes_demo_operador on public.notificacoes_demo(id_operador,programada_para desc);
alter table public.notificacoes_demo enable row level security;
revoke all on public.notificacoes_demo from anon;
grant select,insert on public.notificacoes_demo to authenticated;
drop policy if exists "operador ve suas notificacoes" on public.notificacoes_demo;
create policy "operador ve suas notificacoes" on public.notificacoes_demo for select to authenticated using(id_operador=(select auth.uid()));
drop policy if exists "operador registra aviso manual de exame proprio" on public.notificacoes_demo;
create policy "operador registra aviso manual de exame proprio" on public.notificacoes_demo for insert to authenticated
with check(id_operador=(select auth.uid()) and tipo='resultado_disponivel' and origem='manual' and status='simulada' and simulada_em is not null
 and exists(select 1 from public.exames_preventivos e where e.id_exame=id_exame and e.id_operador=(select auth.uid()) and e.status_laudo in ('disponivel','disponivel_notificado')));
create or replace function internal_ubs.programar_lembretes_demo()
returns trigger language plpgsql security definer set search_path='' as $$
declare h integer; when_at timestamptz;
begin
 if tg_op='UPDATE' then
  delete from public.notificacoes_demo where id_agendamento=new.id_agendamento and status='agendada';
 end if;
 if new.status_confirmacao='cancelado' then return new; end if;
 foreach h in array array[48,24] loop
  when_at:=new.data_hora_consulta-make_interval(hours=>h);
  if when_at>now() then
   insert into public.notificacoes_demo(id_operador,id_agendamento,tipo,origem,nome_paciente,telefone_destino,mensagem,programada_para)
   values(new.id_operador,new.id_agendamento,case when h=48 then 'lembrete_48h' else 'lembrete_24h' end,'automatico',new.nome_paciente,new.telefone_whatsapp,
    'UBS CAIC (SIMULACAO): lembrete de consulta em '||to_char(new.data_hora_consulta at time zone 'America/Sao_Paulo','DD/MM/YYYY "as" HH24:MI')||'.',when_at)
   on conflict(id_agendamento,tipo) do update set programada_para=excluded.programada_para,status='agendada',simulada_em=null,mensagem=excluded.mensagem,nome_paciente=excluded.nome_paciente,telefone_destino=excluded.telefone_destino;
  end if;
 end loop;
 return new;
end $$;
revoke all on function internal_ubs.programar_lembretes_demo() from public,anon,authenticated;
drop trigger if exists trg_programar_lembretes_demo on public.agendamentos_consultas;
create trigger trg_programar_lembretes_demo after insert or update of data_hora_consulta,status_confirmacao,nome_paciente,telefone_whatsapp
on public.agendamentos_consultas for each row execute function internal_ubs.programar_lembretes_demo();
create or replace function internal_ubs.processar_lembretes_demo()
returns integer language plpgsql security definer set search_path='' as $$
declare qtd integer;
begin
 update public.notificacoes_demo n set status='simulada',simulada_em=now()
 where n.status='agendada' and n.programada_para<=now()
 and exists(select 1 from public.agendamentos_consultas a where a.id_agendamento=n.id_agendamento and a.status_confirmacao<>'cancelado' and a.data_hora_consulta>now());
 get diagnostics qtd=row_count;
 update public.notificacoes_demo n set status='cancelada'
 where n.status='agendada' and n.programada_para<=now()
 and (n.id_agendamento is null or not exists(select 1 from public.agendamentos_consultas a where a.id_agendamento=n.id_agendamento and a.status_confirmacao<>'cancelado' and a.data_hora_consulta>now()));
 return qtd;
end $$;
revoke all on function internal_ubs.processar_lembretes_demo() from public,anon,authenticated;
create extension if not exists pg_cron with schema pg_catalog;
-- Em caso de reexecucao, remover o job anterior para evitar duplicidade.
select cron.unschedule(jobid) from cron.job where jobname='ubs-caic-lembretes-simulados';
select cron.schedule('ubs-caic-lembretes-simulados','* * * * *','select internal_ubs.processar_lembretes_demo();');
