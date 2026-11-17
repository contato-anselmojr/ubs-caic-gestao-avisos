# Guia rápido para o avaliador — UBS CAIC

Este arquivo orienta a avaliação do **MVP acadêmico** de gestão de consultas e exames preventivos da UBS CAIC. Os dois ambientes abaixo permitem verificar telas e fluxos sem utilizar dados reais de saúde.

## Opção A — Testar sem cadastro diretamente na internet

**URL oficial do projeto:** https://ubs-caic-gestao-avisos.vercel.app

Abra esse endereço no navegador. **Não é necessário fazer login para avaliar o funcionamento demonstrativo.**

1. Confira o **Painel Resumo do Turno**.
2. Acesse **Cadastro Rápido** e simule uma consulta com nome e telefone fictícios.
3. Verifique a validação de campos e o impedimento de data anterior à atual.
4. Simule o cadastro de um exame preventivo com protocolo fictício.
5. Acesse **Fila e Alertas**, marque um exame fictício como disponível e, na aba **Notificações**, registre o aviso manual simulado. Nenhuma mensagem é entregue a um telefone.
6. Recarregue a página para observar que o **modo visitante não persiste registros**.

Neste ambiente, os dados de visitantes ficam em **arrays JavaScript no navegador**. O uso do banco real exige conta autenticada e não faz parte do teste público sem login.

## Opção B — Baixar e testar na própria máquina

**Requisitos:** computador com Python 3 (recomendado Python 3.12) e navegador atualizado. Não é necessário instalar bibliotecas com `pip`, criar conta no Supabase nem dispor de internet durante a execução.

1. No GitHub, clique em **Code → Download ZIP**.
2. Extraia o ZIP.
3. **Windows:** dentro da pasta extraída, dê dois cliques em `iniciar_teste.bat`.
4. **macOS/Linux:** abra um terminal na pasta extraída e execute `python3 iniciar_teste.py`.
5. O navegador deve abrir em **http://127.0.0.1:5000**. Se não abrir, cole esse endereço manualmente.
6. Execute o mesmo roteiro de navegação acima.
7. Para parar o servidor, pressione `Ctrl+C` no terminal.

**Alternativa:** execute `python app.py` na pasta do projeto e acesse `http://127.0.0.1:5000` manualmente. A versão local é **um protótipo de teste independente** do banco e do deploy.

Se o script informar que a porta 5000 está ocupada, feche a instância anterior ou outro programa que esteja utilizando essa porta. Se o computador não reconhecer o comando `python`, instale o Python 3 e configure o PATH.

## Opção C — Testar persistência com a conta DEMO compartilhada

A interface publicada na Vercel contém um modo autenticado integrado ao **Supabase Auth e PostgreSQL**. A conta de avaliação é criada pelo responsável, não pelo visitante.

1. Abra https://ubs-caic-gestao-avisos.vercel.app.
2. Use o email de demonstração `avaliador.ubs.caic@example.com` e a senha pública de teste `teste1234567`. Clique em **Entrar — modo persistente**. Nunca use dados próprios, senha pessoal ou informações clínicas.
3. Confirme que aparece o contador **Conta DEMO: 0/10 registros utilizados** (ou o número atual).
4. Cadastre consultas e exames com dados fictícios. O total máximo é de **10 registros somados**, independentemente do tipo.
5. Ao atingir 10, o sistema impede novos registros. Use **Excluir** em uma consulta ou exame para liberar uma vaga.
6. Recarregue a página, **entre novamente** e confirme que os registros cadastrados continuam disponíveis no banco.

**Estado dessa opção em 17/11/2026:** a identidade DEMO foi criada e confirmada no Supabase Auth, o perfil `demonstracao` está associado e foi observado acesso autenticado com contador de 2/10 registros. O banco apresentava 1 consulta e 1 exame fictícios, além de 1 aviso manual simulado. Ainda não há comprovação de ensaio formal de todos os cenários (inclusive a 11ª inserção e a reentrada após atualização). O acesso compartilhado permite que diferentes avaliadores vejam e excluam os mesmos dados fictícios. Não utilizar informações reais.

## Código-fonte, hospedagem e banco de dados

- **GitHub:** código-fonte integral, aberto à leitura e à auditoria em https://github.com/contato-anselmojr/ubs-caic-gestao-avisos.
- **Vercel:** hospedagem estática da interface final por HTTPS, associada ao GitHub; versão online em https://ubs-caic-gestao-avisos.vercel.app.
- **Supabase PostgreSQL:** armazenamento da modalidade autenticada, com Supabase Auth e Row Level Security (RLS).
- **Python:** servidor HTTP local da demonstração baixável, sem conexão com banco de dados.
- **Supabase Cron / PostgreSQL:** programação e processamento de lembretes **simulados** de consultas 48 e 24 horas antes, a cada minuto, em contas autenticadas.
- **GitHub Actions:** testes automatizados e monitoramento de disponibilidade do site e do endpoint de saúde do Supabase (agendamento a cada 15 minutos, sujeito a atrasos).

As modalidades gratuitas desses serviços foram escolhidas por serem adequadas ao escopo acadêmico e reduzirem os custos de operação; os provedores podem aplicar limites de uso.

## Evidências da Experiência Prática IV

- **Deploy:** captura de tela da versão **Vercel**, com a barra de endereço e URL completa visíveis.
- **Monitoramento:** captura de uma execução **Success** em https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions, preferencialmente mostrando as verificações da Vercel e do Supabase.

## O que a avaliação comprova

Os testes públicos e os registros fictícios permitem demonstrar a viabilidade técnica do MVP. **Não comprovam** redução real de faltas, reaproveitamento de vagas, diminuição de deslocamentos, envio de SMS/WhatsApp ou validação institucional. O autor é ex-ACS da unidade de referência; sua experiência fundamenta o problema, mas não substitui avaliação por um parceiro externo independente.

## Privacidade e limites

**Todos os nomes, telefones, agendamentos e protocolos devem ser fictícios.** Não há envio real de mensagens, acesso a resultados de exames ou integração com o SUS. Este MVP não é sistema oficial da UBS, nem está autorizado a tratar dados reais de pacientes.

## Central de Notificações — roteiro de demonstração

1. Entre no site com a conta DEMO. Abra **Novo Cadastro** e registre uma consulta fictícia para daqui a mais de 48 horas.
2. Abra a aba **Notificações** e confirme dois lembretes com status **Agendada — simulação**, programados para 48h e 24h antes.
3. O job do Supabase Cron verifica os lembretes vencidos a cada minuto, **mesmo com o site fechado**, alterando-os para **Simulada — não enviada**. Para visualizar a mudança, recarregue e entre novamente.
4. Registre um exame preventivo fictício. Em **Fila e Alertas**, clique em **Registrar disponibilidade** para indicar que o resultado chegou.
5. Abra **Notificações**, pesquise o paciente por nome, telefone ou protocolo, selecione o exame e clique em **Registrar aviso manual simulado**.
6. Confira o histórico de eventos. **Nenhum SMS ou WhatsApp real foi enviado**; o sistema apenas demonstra o agendamento, processamento e registro interno.

O modo público sem login utiliza dados em memória, e não executa o processamento de lembretes em segundo plano. A modalidade autenticada usa PostgreSQL e Supabase Cron.
