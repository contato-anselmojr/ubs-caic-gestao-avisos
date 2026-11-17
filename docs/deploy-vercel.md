# Deploy final do MVP demonstrativo UBS CAIC — Vercel

## Publicação confirmada

- **URL oficial para a avaliação acadêmica:** https://ubs-caic-gestao-avisos.vercel.app
- **Vercel:** projeto `ubs-caic-gestao-avisos` vinculado ao GitHub `contato-anselmojr/ubs-caic-gestao-avisos`, branch de produção `main`.
- **Estado do deploy:** `READY` após integração do arquivo `index.html`.
- **Banco:** Supabase PostgreSQL gerenciado em projeto separado, com quatro tabelas (`usuarios_operadores`, `agendamentos_consultas`, `exames_preventivos`, `notificacoes_demo`) e RLS.
- **Monitoramento:** GitHub Actions `.github/workflows/monitoramento.yml` monitora o endereço final da Vercel, a demonstração alternativa e a conexão do banco a cada 15 minutos.
- **Verificação externa:** execução nº 16 do monitoramento confirmou `Success` para a URL da Vercel, a Supabase Edge Function e o endpoint de saúde do banco. Registro: https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions/runs/44149438168.

## Explicação da arquitetura

A Vercel hospeda **somente a interface** em HTML/CSS/JavaScript. Visitantes acessam o site sem login e usam **dados demonstrativos temporários**, sem gravação no banco. Para os fluxos com persistência, a interface contém integração com Supabase Auth e Data API PostgreSQL, com controles de acesso via RLS e autenticação. A conta DEMO já foi ativada, com login e contador observados na interface. Em 17/11/2026, o banco continha 1 consulta, 1 exame e 1 notificação manual fictícia. A sessão não é mantida ao atualizar a página; é necessário entrar novamente para consultar registros persistidos. **O ensaio formal de todos os cenários, como reentrada e bloqueio da 11ª inserção, não está documentado.**

O Supabase Cron processa lembretes **simulados** de 48h e 24h antes da consulta a cada minuto; nenhuma mensagem é enviada por SMS/WhatsApp.

O programa `app.py` é o **protótipo local Python** incluído no repositório para execução baixável e independente. Não é executado na Vercel. O arquivo `iniciar_teste.py` inicia o protótipo no computador e abre o navegador.

## Reproduzir o deploy na Vercel

1. Importar o repositório `contato-anselmojr/ubs-caic-gestao-avisos` pelo painel da Vercel.
2. Selecionar a branch `main` e o preset de framework `Other`, com diretório raiz padrão.
3. Manter `index.html` na raiz; não é necessário comando de build nem pacotes NPM.
4. Fazer deploy e confirmar `READY`.
5. Abrir https://ubs-caic-gestao-avisos.vercel.app e verificar as três telas, a navegação e os fluxos demonstrativos.
6. Validar o monitoramento em GitHub Actions.

## Evidência acadêmica

A captura de tela obrigatória deve incluir **o navegador inteiro com a barra de endereço mostrando o link da Vercel**. Para monitoramento, capturar o job verde de `verificar-disponibilidade` em https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions.

## Custos, segurança e limitações

A combinação GitHub + Vercel + Supabase foi escolhida pelas modalidades **gratuitas disponíveis para o projeto acadêmico**, sujeitas a cotas e regras dos provedores. O frontend contém somente a chave pública do Supabase, nunca a `service_role`. As tabelas estão protegidas por RLS. O MVP **não** está autorizado a receber dados reais de pacientes, não envia mensagens por WhatsApp/SMS e não é uma implantação clínica homologada. Indicadores de redução de faltas e deslocamentos não foram medidos na população; os testes disponíveis comprovam somente o comportamento demonstrativo.
