from http.server import BaseHTTPRequestHandler, HTTPServer

from http_headers import send_html_headers

PAGE = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UBS Sueli Dutra Alves (CAIC) | Gestão de Avisos</title>
  <style>
    :root {
      --navy: #0d3b66;
      --navy-dark: #082b4b;
      --blue-soft: #eaf2f9;
      --ink: #1a252f;
      --muted: #64748b;
      --line: #dbe3ec;
      --surface: #ffffff;
      --background: #f3f6fa;
      --green: #16834a;
      --green-soft: #e8f6ee;
      --red: #bd3030;
      --red-soft: #fff0f0;
      --amber: #946200;
      --amber-soft: #fff7df;
      --shadow: 0 8px 24px rgba(22, 44, 68, .07);
      font-family: Inter, "Segoe UI", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--background); color: var(--ink); font-size: 15px; line-height: 1.5; }
    button, input, select { font: inherit; }
    button:focus-visible, input:focus-visible, select:focus-visible {
      outline: 3px solid #ffbf00; outline-offset: 2px;
    }
    .topbar { background: var(--navy); color: #fff; box-shadow: 0 3px 12px rgba(4, 27, 49, .18); }
    .topbar-inner { max-width: 1180px; margin: 0 auto; padding: 15px 22px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    .brand { display: flex; align-items: center; gap: 12px; min-width: 250px; }
    .brand-mark { width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; background: rgba(255,255,255,.15); font-size: 23px; }
    .brand-title { font-weight: 750; letter-spacing: .1px; }
    .brand-subtitle { color: #d7e5f2; font-size: 12px; margin-top: 1px; }
    .nav { display: flex; align-items: center; flex-wrap: wrap; justify-content: flex-end; gap: 7px; }
    .nav button { border: 1px solid rgba(255,255,255,.3); color: #fff; background: transparent; border-radius: 8px; padding: 10px 13px; min-height: 42px; cursor: pointer; font-weight: 650; }
    .nav button:hover, .nav button.active { background: rgba(255,255,255,.16); border-color: rgba(255,255,255,.65); }
    .nav .logout { background: #b83232; border-color: #b83232; }
    .container { width: min(1180px, calc(100% - 40px)); margin: 28px auto 54px; }
    .screen { display: none; }
    .screen.active { display: block; animation: appear .16s ease-out; }
    @keyframes appear { from { opacity: .65; transform: translateY(3px); } to { opacity: 1; transform: none; } }
    .page-heading { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; flex-wrap: wrap; margin-bottom: 23px; }
    h1 { color: var(--navy); margin: 0 0 5px; font-size: clamp(23px, 3vw, 29px); line-height: 1.2; }
    h2 { color: var(--navy); margin: 0; font-size: 19px; }
    .subtitle { margin: 0; color: var(--muted); }
    .button-row { display: flex; gap: 9px; flex-wrap: wrap; }
    .btn { border: 1px solid transparent; min-height: 43px; border-radius: 8px; padding: 10px 15px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 700; cursor: pointer; text-decoration: none; }
    .btn-primary { color: #fff; background: var(--navy); }
    .btn-primary:hover { background: var(--navy-dark); }
    .btn-dark { color: #fff; background: #263746; }
    .btn-outline { color: var(--navy); border-color: #9aafc3; background: #fff; }
    .btn-outline:hover { background: var(--blue-soft); }
    .btn-success { color: #fff; background: var(--green); }
    .btn-danger { color: #fff; background: var(--red); }
    .btn-small { min-height: 36px; padding: 7px 10px; font-size: 13px; }
    .card { background: var(--surface); border: 1px solid var(--line); border-radius: 13px; box-shadow: var(--shadow); }
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 17px; margin: 22px 0; }
    .stat-card { padding: 22px 23px; min-height: 165px; border-left: 5px solid var(--navy); }
    .stat-card.red { border-left-color: var(--red); }
    .stat-card.green { border-left-color: var(--green); }
    .stat-top { display: flex; justify-content: space-between; gap: 10px; color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .6px; text-transform: uppercase; }
    .stat-icon { font-size: 23px; }
    .stat-number { color: var(--navy); font-size: 43px; line-height: 1.15; font-weight: 800; margin: 11px 0 7px; }
    .stat-card.red .stat-number { color: var(--red); }
    .stat-card.green .stat-number { color: var(--green); }
    .stat-description { margin: 0; color: #536273; font-size: 13px; }
    .notice { display: flex; gap: 12px; align-items: flex-start; border: 1px solid #d4e1ec; border-radius: 10px; background: #f8fbfe; color: #34495e; padding: 15px 17px; margin-top: 20px; }
    .notice-icon { font-size: 20px; }
    .notice strong { color: var(--navy); }
    .demo-strip { margin-top: 17px; border-radius: 9px; padding: 10px 13px; background: var(--amber-soft); color: #6d4b00; font-size: 13px; border: 1px solid #f1dda0; }
    .panel { padding: 24px; }
    .panel-heading { display: flex; justify-content: space-between; align-items: center; gap: 15px; flex-wrap: wrap; margin-bottom: 18px; }
    .tabs { display: flex; gap: 8px; border-bottom: 1px solid var(--line); margin: 18px 0 22px; }
    .tab { color: #526477; background: transparent; border: 0; border-bottom: 3px solid transparent; padding: 12px 14px; cursor: pointer; font-weight: 700; }
    .tab.active { color: var(--navy); border-bottom-color: var(--navy); }
    .form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    .field { display: flex; flex-direction: column; gap: 6px; }
    label { color: var(--navy); font-weight: 750; font-size: 14px; }
    input, select { width: 100%; min-height: 46px; border: 1.7px solid #9aa8b6; border-radius: 8px; padding: 10px 12px; background: #fff; color: #111827; }
    input::placeholder { color: #8793a0; }
    .help { color: var(--muted); font-size: 12px; }
    .form-actions { display: flex; gap: 10px; margin-top: 22px; flex-wrap: wrap; }
    .error { padding: 12px 14px; border-radius: 8px; background: var(--red-soft); border: 1px solid #efb3b3; color: #982323; font-weight: 650; margin-bottom: 17px; }
    .success { padding: 13px 16px; border-radius: 9px; background: var(--green-soft); border: 1px solid #b9dfc8; color: #145c36; font-weight: 700; margin-bottom: 18px; }
    .hidden { display: none !important; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; }
    table { width: 100%; border-collapse: collapse; min-width: 700px; }
    th, td { padding: 13px 14px; border-bottom: 1px solid #e5ebf1; text-align: left; vertical-align: middle; }
    th { color: #34495e; background: #f1f5f9; font-size: 12px; letter-spacing: .35px; text-transform: uppercase; }
    td { font-size: 14px; }
    tbody tr:last-child td { border-bottom: 0; }
    tbody tr:hover { background: #fafcff; }
    .patient { font-weight: 750; color: #24384b; }
    .badge { display: inline-flex; align-items: center; gap: 6px; border-radius: 999px; padding: 7px 10px; font-size: 12px; font-weight: 800; white-space: nowrap; }
    .badge.ready { background: var(--blue-soft); color: #15558b; }
    .badge.sent { background: var(--green-soft); color: #17613b; }
    .badge.cancelled { background: var(--red-soft); color: #a32323; }
    .badge.confirmed { background: #edf5ff; color: #215b95; }
    .empty { padding: 22px; color: var(--muted); text-align: center; }
    .section-gap { margin-top: 22px; }
    .screen-footer { text-align: center; color: #7b8794; font-size: 12px; margin-top: 26px; }
    @media (max-width: 850px) {
      .topbar-inner { align-items: flex-start; flex-direction: column; }
      .nav { justify-content: flex-start; }
      .stats { grid-template-columns: 1fr; }
      .stat-card { min-height: 145px; }
    }
    @media (max-width: 620px) {
      .container { width: min(100% - 24px, 1180px); margin-top: 19px; }
      .topbar-inner { padding: 13px 14px; }
      .nav button { flex: 1 1 auto; padding: 9px 10px; }
      .brand { min-width: 0; }
      .panel { padding: 17px; }
      .form-grid { grid-template-columns: 1fr; }
      .tabs { flex-direction: column; border-bottom: 0; }
      .tab { text-align: left; border: 1px solid var(--line); border-radius: 7px; }
      .tab.active { border: 1px solid var(--navy); background: var(--blue-soft); }
      .page-heading { align-items: flex-start; }
    }
    @media print {
      @page { size: A4 landscape; margin: 12mm; }
      body { background: #fff; font-size: 12px; }
      .topbar, .no-print, .screen-footer { display: none !important; }
      .container { width: 100%; max-width: none; margin: 0; }
      .screen { display: none !important; }
      .screen.active { display: block !important; }
      .card { box-shadow: none; break-inside: avoid; }
      .table-wrap { overflow: visible; }
      table { min-width: 0; }
      th, td { padding: 8px; }
      .panel { padding: 14px; }
    }
  </style>
</head>
<body>
  <header class="topbar no-print">
    <div class="topbar-inner">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">✚</div>
        <div>
          <div class="brand-title">UBS Sueli Dutra Alves (CAIC)</div>
          <div class="brand-subtitle">Sistema demonstrativo de gestão de avisos • SUS</div>
        </div>
      </div>
      <nav class="nav" aria-label="Navegação principal">
        <button type="button" class="active" data-view="inicio">⌂ Início</button>
        <button type="button" data-view="cadastro">＋ Novo Cadastro</button>
        <button type="button" data-view="fila">♧ Fila e Alertas</button>
        <button type="button" id="printButton">⎙ Imprimir tela</button>
        <button type="button" class="logout" id="logoutButton">Sair</button>
      </nav>
    </div>
  </header>

  <main class="container">
    <div id="globalSuccess" class="success hidden" role="status" aria-live="polite"></div>

    <!-- TELA 1: PAINEL INICIAL -->
    <section id="inicio" class="screen active" aria-labelledby="titleInicio">
      <div class="page-heading">
        <div>
          <h1 id="titleInicio">Painel Resumo do Turno — UBS CAIC</h1>
          <p class="subtitle">Conjunto Nilson Neves • Paranaguá — PR | Gestão de lembretes e exames preventivos</p>
        </div>
        <div class="button-row no-print">
          <button class="btn btn-primary" type="button" data-go="cadastro">＋ Novo Cadastro Rápido</button>
          <button class="btn btn-dark" type="button" data-go="fila">☷ Abrir Fila e Alertas</button>
        </div>
      </div>

      <div class="stats">
        <article class="card stat-card">
          <div class="stat-top"><span>Consultas monitoradas (48h)</span><span class="stat-icon">▦</span></div>
          <div class="stat-number" id="countConsultas">2</div>
          <p class="stat-description">Registros acompanhados para lembretes de consulta.</p>
        </article>
        <article class="card stat-card red">
          <div class="stat-top"><span>Vagas canceladas (realocar)</span><span class="stat-icon">⚠</span></div>
          <div class="stat-number" id="countCanceladas">1</div>
          <p class="stat-description">Pacientes desmarcaram; vagas disponíveis para encaixe.</p>
        </article>
        <article class="card stat-card green">
          <div class="stat-top"><span>Exames preventivos prontos</span><span class="stat-icon">♧</span></div>
          <div class="stat-number" id="countExames">1</div>
          <p class="stat-description">Resultados aguardando registro de aviso ao paciente.</p>
        </article>
      </div>

      <div class="notice">
        <div class="notice-icon" aria-hidden="true">🔒</div>
        <div><strong>Ambiente de demonstração:</strong> operador recepcao.caic01. Esta tela representa um protótipo visual; não há autenticação real nem armazenamento em banco de dados.</div>
      </div>
      <div class="demo-strip">Atenção: os dados exibidos são fictícios para apresentação. Os botões de aviso apenas simulam a alteração de status — nenhuma mensagem é enviada pelo WhatsApp.</div>
    </section>

    <!-- TELA 2: CADASTRO -->
    <section id="cadastro" class="screen" aria-labelledby="titleCadastro">
      <div class="card panel">
        <div class="page-heading" style="margin-bottom: 5px;">
          <div>
            <h1 id="titleCadastro">Cadastro Rápido no Balcão</h1>
            <p class="subtitle">Registro demonstrativo de consultas e exames preventivos.</p>
          </div>
        </div>

        <div class="tabs no-print" role="tablist" aria-label="Tipo de cadastro">
          <button class="tab active" id="tabConsulta" type="button" role="tab" aria-selected="true">▦ Nova Consulta (Médico / Dentista)</button>
          <button class="tab" id="tabExame" type="button" role="tab" aria-selected="false">▤ Novo Exame Preventivo (+45 dias)</button>
        </div>

        <div id="formError" class="error hidden" role="alert"></div>
        <form id="registrationForm" novalidate>
          <div class="form-grid">
            <div class="field">
              <label for="nome">1. Nome completo do paciente *</label>
              <input type="text" id="nome" name="nome" value="Maria Helena da Silva" autocomplete="off" required>
            </div>
            <div class="field">
              <label for="whatsapp">2. WhatsApp com DDD (11 dígitos) *</label>
              <input type="tel" id="whatsapp" name="whatsapp" value="(41) 98888-0001" inputmode="numeric" maxlength="15" required>
              <span class="help">Exemplo: (41) 98888-0001</span>
            </div>
            <div class="field" id="fieldSpecialty">
              <label for="especialidade">3. Especialidade / atendimento *</label>
              <select id="especialidade" name="especialidade">
                <option value="Odontologia">Odontologia (Dentista)</option>
                <option value="Clínico Geral">Clínico Geral</option>
                <option value="Pediatria">Pediatria</option>
                <option value="Enfermagem">Enfermagem / Pré-Natal</option>
              </select>
            </div>
            <div class="field hidden" id="fieldProtocol">
              <label for="protocolo">3. Protocolo do exame preventivo *</label>
              <input type="text" id="protocolo" name="protocolo" value="PREV-2026-105">
            </div>
            <div class="field">
              <label for="dataRegistro" id="dateLabel">4. Data e horário da consulta *</label>
              <input type="datetime-local" id="dataRegistro" name="dataRegistro" value="2026-12-20T09:00" required>
            </div>
          </div>
          <div class="form-actions no-print">
            <button type="submit" class="btn btn-primary">✓ Salvar Registro</button>
            <button type="button" class="btn btn-outline" data-go="inicio">Cancelar e Voltar</button>
          </div>
        </form>
      </div>
    </section>

    <!-- TELA 3: FILA E ALERTAS -->
    <section id="fila" class="screen" aria-labelledby="titleFila">
      <div class="card panel">
        <div class="panel-heading">
          <div>
            <h2 id="titleFila">♧ Resultados de Exames Preventivos</h2>
            <p class="subtitle">Acompanhamento dos avisos de resultados prontos.</p>
          </div>
          <button class="btn btn-outline btn-small no-print" type="button" id="newExamButton">＋ Registrar Protocolo</button>
        </div>
        <div class="table-wrap">
          <table aria-label="Resultados de exames preventivos">
            <thead><tr><th>Protocolo</th><th>Paciente</th><th>WhatsApp</th><th>Status</th><th class="no-print">Ação</th></tr></thead>
            <tbody id="examTableBody"></tbody>
          </table>
        </div>
      </div>

      <div class="card panel section-gap">
        <div class="panel-heading">
          <div>
            <h2>▦ Consultas Agendadas e Retorno de Lembretes</h2>
            <p class="subtitle">Consultas registradas e situação do lembrete.</p>
          </div>
          <button class="btn btn-outline btn-small no-print" type="button" id="newAppointmentButton">＋ Agendar Consulta</button>
        </div>
        <div class="table-wrap">
          <table aria-label="Consultas agendadas">
            <thead><tr><th>Paciente</th><th>WhatsApp</th><th>Especialidade</th><th>Data / Horário</th><th>Status</th></tr></thead>
            <tbody id="appointmentTableBody"></tbody>
          </table>
        </div>
      </div>
      <div class="demo-strip">Simulação de interface: os status podem ser alterados para demonstrar o fluxo, mas não há integração com WhatsApp, laboratório ou sistema oficial do SUS.</div>
    </section>

    <div class="screen-footer">Protótipo demonstrativo • UBS Sueli Dutra Alves (CAIC) • Paranaguá — PR</div>
  </main>

  <script>
    let currentMode = 'consulta';

    const appointments = [
      { name: 'João Carlos Pereira', phone: '(41) 98888-1101', specialty: 'Clínico Geral', date: '15/11/2026 08:30', status: 'cancelled' },
      { name: 'Maria Helena da Silva', phone: '(41) 98888-1102', specialty: 'Odontologia', date: '18/11/2026 10:00', status: 'confirmed' }
    ];

    const exams = [
      { protocol: 'PREV-2026-084', name: 'Ana Paula Costa', phone: '(41) 98888-2201', status: 'ready' },
      { protocol: 'PREV-2026-041', name: 'Sônia Maria Souza', phone: '(41) 98888-2202', status: 'sent' }
    ];

    function showView(viewId) {
      document.querySelectorAll('.screen').forEach(section => section.classList.toggle('active', section.id === viewId));
      document.querySelectorAll('.nav [data-view]').forEach(button => button.classList.toggle('active', button.dataset.view === viewId));
      hideMessages();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    document.querySelectorAll('[data-view]').forEach(button => {
      button.addEventListener('click', () => showView(button.dataset.view));
    });
    document.querySelectorAll('[data-go]').forEach(button => {
      button.addEventListener('click', () => showView(button.dataset.go));
    });

    function setMode(mode) {
      currentMode = mode;
      const isConsultation = mode === 'consulta';
      document.getElementById('tabConsulta').classList.toggle('active', isConsultation);
      document.getElementById('tabExame').classList.toggle('active', !isConsultation);
      document.getElementById('tabConsulta').setAttribute('aria-selected', String(isConsultation));
      document.getElementById('tabExame').setAttribute('aria-selected', String(!isConsultation));
      document.getElementById('fieldSpecialty').classList.toggle('hidden', !isConsultation);
      document.getElementById('fieldProtocol').classList.toggle('hidden', isConsultation);
      const dateInput = document.getElementById('dataRegistro');
      const dateLabel = document.getElementById('dateLabel');
      if (isConsultation) {
        dateLabel.textContent = '4. Data e horário da consulta *';
        dateInput.type = 'datetime-local';
        dateInput.value = '2026-12-20T09:00';
      } else {
        dateLabel.textContent = '4. Data da coleta na UBS *';
        dateInput.type = 'date';
        dateInput.value = '2026-11-13';
      }
      hideMessages();
    }

    document.getElementById('tabConsulta').addEventListener('click', () => setMode('consulta'));
    document.getElementById('tabExame').addEventListener('click', () => setMode('exame'));

    function hideMessages() {
      document.getElementById('formError').classList.add('hidden');
      document.getElementById('globalSuccess').classList.add('hidden');
    }

    function showSuccess(message) {
      const box = document.getElementById('globalSuccess');
      box.textContent = message;
      box.classList.remove('hidden');
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      })[char]);
    }

    function renderTables() {
      const examBody = document.getElementById('examTableBody');
      examBody.innerHTML = '';
      exams.forEach((exam, index) => {
        const ready = exam.status === 'ready';
        const status = ready
          ? '<span class="badge ready">♧ Exame pronto (+45 dias)</span>'
          : '<span class="badge sent">✓ Aviso registrado (simulação)</span>';
        const action = ready
          ? `<button type="button" class="btn btn-success btn-small no-print" data-notify="${index}">Registrar aviso</button>`
          : '<span class="help">Ação concluída</span>';
        examBody.insertAdjacentHTML('beforeend', `<tr>
          <td class="patient">${escapeHtml(exam.protocol)}</td>
          <td>${escapeHtml(exam.name)}</td>
          <td>${escapeHtml(exam.phone)}</td>
          <td>${status}</td>
          <td class="no-print">${action}</td>
        </tr>`);
      });

      const appointmentBody = document.getElementById('appointmentTableBody');
      appointmentBody.innerHTML = '';
      appointments.forEach(appointment => {
        let status = '<span class="badge confirmed">✓ Confirmado (demonstração)</span>';
        if (appointment.status === 'cancelled') status = '<span class="badge cancelled">✕ Cancelado — vaga livre</span>';
        appointmentBody.insertAdjacentHTML('beforeend', `<tr>
          <td class="patient">${escapeHtml(appointment.name)}</td>
          <td>${escapeHtml(appointment.phone)}</td>
          <td>${escapeHtml(appointment.specialty)}</td>
          <td>${escapeHtml(appointment.date)}</td>
          <td>${status}</td>
        </tr>`);
      });

      document.getElementById('countExames').textContent = exams.filter(exam => exam.status === 'ready').length;
      document.getElementById('countCanceladas').textContent = appointments.filter(item => item.status === 'cancelled').length;
      document.getElementById('countConsultas').textContent = appointments.length;
    }

    document.getElementById('examTableBody').addEventListener('click', event => {
      const button = event.target.closest('[data-notify]');
      if (!button) return;
      const exam = exams[Number(button.dataset.notify)];
      if (!exam || exam.status !== 'ready') return;
      exam.status = 'sent';
      renderTables();
      showSuccess(`Aviso de ${exam.protocol} marcado como concluído (simulação). Nenhuma mensagem foi enviada.`);
    });

    function formatDate(value, isConsultation) {
      if (!value) return '';
      const parts = value.split('T');
      const [year, month, day] = parts[0].split('-');
      const date = `${day}/${month}/${year}`;
      if (!isConsultation || !parts[1]) return date;
      return `${date} ${parts[1]}`;
    }

    document.getElementById('registrationForm').addEventListener('submit', event => {
      event.preventDefault();
      hideMessages();
      const name = document.getElementById('nome').value.trim();
      const phone = document.getElementById('whatsapp').value.trim();
      const digits = phone.replace(/\D/g, '');
      const dateValue = document.getElementById('dataRegistro').value;
      const error = document.getElementById('formError');

      let message = '';
      if (name.length < 3) message = 'Informe o nome completo do paciente.';
      else if (digits.length !== 11) message = 'Telefone inválido: informe DDD + 9 dígitos (11 números ao todo).';
      else if (!dateValue) message = 'Informe a data do registro.';
      else if (currentMode === 'exame' && !document.getElementById('protocolo').value.trim()) message = 'Informe o protocolo do exame preventivo.';

      if (message) {
        error.textContent = message;
        error.classList.remove('hidden');
        return;
      }

      if (currentMode === 'consulta') {
        appointments.unshift({
          name,
          phone,
          specialty: document.getElementById('especialidade').value,
          date: formatDate(dateValue, true),
          status: 'confirmed'
        });
        renderTables();
        showView('fila');
        showSuccess(`Consulta de ${name} cadastrada no protótipo com sucesso.`);
      } else {
        const protocol = document.getElementById('protocolo').value.trim();
        if (exams.some(item => item.protocol.toLowerCase() === protocol.toLowerCase())) {
          error.textContent = 'Esse protocolo já está cadastrado na demonstração. Informe outro número.';
          error.classList.remove('hidden');
          return;
        }
        exams.unshift({ protocol, name, phone, status: 'ready' });
        renderTables();
        showView('fila');
        showSuccess(`Exame preventivo ${protocol} registrado no protótipo. Data informada: ${formatDate(dateValue, false)}.`);
      }
      document.getElementById('nome').value = '';
      document.getElementById('whatsapp').value = '';
    });

    document.getElementById('newExamButton').addEventListener('click', () => {
      setMode('exame');
      showView('cadastro');
    });
    document.getElementById('newAppointmentButton').addEventListener('click', () => {
      setMode('consulta');
      showView('cadastro');
    });
    document.getElementById('printButton').addEventListener('click', () => window.print());
    document.getElementById('logoutButton').addEventListener('click', () => {
      alert('Este é um protótipo de apresentação. Não existe sessão real para encerrar.');
    });

    renderTables();
  </script>
</body>
</html>'''


class UBSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Página não encontrada")
            return

        body = PAGE.encode("utf-8")
        self.send_response(200)
        send_html_headers(self, len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Mantém o terminal limpo durante a demonstração.
        return


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = HTTPServer((host, port), UBSHandler)
    print("Protótipo UBS CAIC disponível em: http://127.0.0.1:5000")
    print("Para encerrar, pressione CTRL+C neste terminal.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
