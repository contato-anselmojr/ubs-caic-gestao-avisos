# Guia rápido para o avaliador — UBS CAIC

Este arquivo orienta a avaliação do **MVP acadêmico** de gestão de consultas e exames preventivos da UBS CAIC. Os dois ambientes abaixo permitem verificar telas e fluxos sem utilizar dados reais de saúde.

## Opção A — Testar sem cadastro diretamente na internet

**URL oficial do projeto:** https://ubs-caic-gestao-avisos.vercel.app

Abra esse endereço no navegador. **Não é necessário fazer login para avaliar o funcionamento demonstrativo.**

1. Confira o **Painel Resumo do Turno**.
2. Acesse **Cadastro Rápido** e simule uma consulta com nome e telefone fictícios.
3. Verifique a validação de campos e o impedimento de data anterior à atual.
4. Simule o cadastro de um exame preventivo com protocolo fictício.
5. Acesse **Fila e Alertas**, visualize as informações simuladas e registre um aviso demonstrativo.
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

## Opção C — Testar cadastro e persistência (modo autenticado online)

A interface publicada na Vercel também contém um modo autenticado que **integra Supabase Auth e PostgreSQL**.

1. Abra https://ubs-caic-gestao-avisos.vercel.app.
2. Informe um email controlado pelo avaliador e uma senha para a **conta de testes**; clique em **Criar conta de testes**.
3. Se solicitado, confirme a conta por email e use **Entrar — modo persistente**.
4. Tente cadastrar uma consulta ou exame fictício e verifique se o registro permanece depois de recarregar a página.

**Estado dessa opção:** a integração existe no código, mas **o fluxo completo de autenticação e gravação ainda requer validação prática com uma conta de teste**. A confirmação de email depende das configurações do Supabase Auth. Não interpretar esse roteiro como prova de homologação para uso clínico.

## Código-fonte, hospedagem e banco de dados

- **GitHub:** código-fonte integral, aberto à leitura e à auditoria em https://github.com/contato-anselmojr/ubs-caic-gestao-avisos.
- **Vercel:** hospedagem estática da interface final por HTTPS, associada ao GitHub; versão online em https://ubs-caic-gestao-avisos.vercel.app.
- **Supabase PostgreSQL:** armazenamento da modalidade autenticada, com Supabase Auth e Row Level Security (RLS).
- **Python:** servidor HTTP local da demonstração baixável, sem conexão com banco de dados.
- **GitHub Actions:** testes automatizados e monitoramento programado da disponibilidade do site e do banco.

As modalidades gratuitas desses serviços foram escolhidas por serem adequadas ao escopo acadêmico e reduzirem os custos de operação; os provedores podem aplicar limites de uso.

## Evidências da Experiência Prática IV

- **Deploy:** captura de tela da versão **Vercel**, com a barra de endereço e URL completa visíveis.
- **Monitoramento:** captura de uma execução **Success** em https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions, preferencialmente mostrando as verificações da Vercel e do Supabase.

## Privacidade e limites

**Todos os nomes, telefones, agendamentos e protocolos devem ser fictícios.** Não há envio real de mensagens, acesso a resultados de exames ou integração com o SUS. Este MVP não é sistema oficial da UBS, nem está autorizado a tratar dados reais de pacientes.
