-- UBS CAIC — esquema demonstrativo para Supabase PostgreSQL.
-- Somente dados ficticios. Aplicacao nao autorizada para operacao com pacientes reais.
-- Aplicar APENAS a um projeto novo e isolado da UBS CAIC.
-- Auth: credenciais e hashes ficam no Supabase Auth, nunca nas tabelas publicas.

create table if not exists public.usuarios_operadores (
    id_operador uuid primary key references auth.users(id) on delete cascade,
    nome_completo text not null check (char_length(trim(nome_completo)) between 3 and 120),
    perfil_acesso text not null default 'recepcao'
       check (perfil_acesso in ('recepcao', 'coordenacao')),
    ativo boolean not null default true,
    data_criacao timestamptz not null default now()
);

create table if not exists public.agendamentos_consultas (
    id_agendamento uuid primary key default gen_random_uuid(),
    id_operador uuid not null default auth.uid()
        references public.usuarios_operadores(id_operador),
    nome_paciente text not null check (char_length(trim(nome_paciente)) between 3 and 120),
    telefone_whatsapp text not null check (telefone_whatsapp ~ '^[0-9]{11}$'),
    especialidade text not null check
       (especialidade in ('clinico_geral','odontologia','pediatria','enfermagem')),
    data_hora_consulta timestamptz not null,
    status_confirmacao text not null default 'pendente'
       check (status_confirmacao in ('pendente','lembrete_enviado','confirmado','cancelado','realocado')),
    em_fila_espera boolean not null default false,
    data_registro timestamptz not null default now()
);

create table if not exists public.exames_preventivos (
    id_exame uuid primary key default gen_random_uuid(),
    id_operador uuid not null default auth.uid()
        references public.usuarios_operadores(id_operador),
    protocolo_coleta text not null unique
        check (char_length(trim(protocolo_coleta)) between 3 and 40),
    nome_paciente text not null check (char_length(trim(nome_paciente)) between 3 and 120),
    telefone_whatsapp text not null check (telefone_whatsapp ~ '^[0-9]{11}$'),
    data_coleta date not null,
    status_laudo text not null default 'aguardando_laboratorio'
        check (status_laudo in ('aguardando_laboratorio','disponivel_notificado','retirado_paciente')),
    data_notificacao timestamptz
);

create index if not exists idx_agendamentos_operador_data
    on public.agendamentos_consultas (id_operador, data_hora_consulta);
create index if not exists idx_exames_operador_status
    on public.exames_preventivos (id_operador, status_laudo);

alter table public.usuarios_operadores enable row level security;
alter table public.agendamentos_consultas enable row level security;
alter table public.exames_preventivos enable row level security;

-- Limites explicitos para Data API (mesmo que a instancia tenha defaults permissivos).
revoke all on public.usuarios_operadores from anon;
revoke all on public.agendamentos_consultas from anon;
revoke all on public.exames_preventivos from anon;
grant select, insert, update on public.usuarios_operadores to authenticated;
grant select, insert, update, delete on public.agendamentos_consultas to authenticated;
grant select, insert, update, delete on public.exames_preventivos to authenticated;

drop policy if exists "operador consulta propria ficha" on public.usuarios_operadores;
create policy "operador consulta propria ficha" on public.usuarios_operadores
    for select to authenticated
    using ((select auth.uid()) = id_operador);

drop policy if exists "operador cria propria ficha" on public.usuarios_operadores;
create policy "operador cria propria ficha" on public.usuarios_operadores
    for insert to authenticated
    with check ((select auth.uid()) = id_operador and perfil_acesso = 'recepcao');

-- Perfil coordenacao nao pode ser autoconcedido via frontend.
drop policy if exists "operador atualiza propria ficha" on public.usuarios_operadores;
create policy "operador atualiza propria ficha" on public.usuarios_operadores
    for update to authenticated
    using ((select auth.uid()) = id_operador and perfil_acesso = 'recepcao')
    with check ((select auth.uid()) = id_operador and perfil_acesso = 'recepcao');

drop policy if exists "operador le agendamentos" on public.agendamentos_consultas;
create policy "operador le agendamentos" on public.agendamentos_consultas
    for select to authenticated
    using (id_operador = (select auth.uid()));

drop policy if exists "operador registra agendamentos" on public.agendamentos_consultas;
create policy "operador registra agendamentos" on public.agendamentos_consultas
    for insert to authenticated
    with check (id_operador = (select auth.uid()));

drop policy if exists "operador atualiza agendamentos" on public.agendamentos_consultas;
create policy "operador atualiza agendamentos" on public.agendamentos_consultas
    for update to authenticated
    using (id_operador = (select auth.uid()))
    with check (id_operador = (select auth.uid()));

drop policy if exists "operador exclui agendamentos" on public.agendamentos_consultas;
create policy "operador exclui agendamentos" on public.agendamentos_consultas
    for delete to authenticated
    using (id_operador = (select auth.uid()));

drop policy if exists "operador le exames" on public.exames_preventivos;
create policy "operador le exames" on public.exames_preventivos
    for select to authenticated
    using (id_operador = (select auth.uid()));

drop policy if exists "operador registra exames" on public.exames_preventivos;
create policy "operador registra exames" on public.exames_preventivos
    for insert to authenticated
    with check (id_operador = (select auth.uid()));

drop policy if exists "operador atualiza exames" on public.exames_preventivos;
create policy "operador atualiza exames" on public.exames_preventivos
    for update to authenticated
    using (id_operador = (select auth.uid()))
    with check (id_operador = (select auth.uid()));

drop policy if exists "operador exclui exames" on public.exames_preventivos;
create policy "operador exclui exames" on public.exames_preventivos
    for delete to authenticated
    using (id_operador = (select auth.uid()));
