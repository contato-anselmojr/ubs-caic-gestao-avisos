# Deploy final da UBS CAIC na Vercel

## Arquitetura

- **Vercel:** hospeda a interface estática de `index.html` (HTML/CSS/JavaScript).
- **Supabase:** fornece PostgreSQL, Supabase Auth e Data API com políticas RLS por operador.
- **GitHub:** fonte versionada do código, integrado à Vercel para deploy automático da branch `main`.
- **Modo público:** somente demonstração com dados fictícios e temporários.
- **Modo autenticado:** cadastro e consultas persistidas no Supabase com token de autenticação e políticas RLS; validar com uma conta de teste antes de declarar o fluxo homologado.

O antigo endpoint Supabase Edge Functions permanece disponível como implantação alternativa. Não é necessário hospedar o Python `http.server` na Vercel; o arquivo `app.py` continua sendo o protótipo local e os testes associados.

## Publicar pelo painel Vercel

1. Entrar em https://vercel.com com o GitHub.
2. Escolher **Add New → Project** e importar `contato-anselmojr/ubs-caic-gestao-avisos`.
3. Selecionar `Other` como **Framework Preset** e manter **Root Directory** como `./`.
4. Não há build nem pacotes npm para instalar; o arquivo `index.html` fica na raiz.
5. Clicar em **Deploy** e aguardar o status **Ready**.
6. Abrir a URL real fornecida pela Vercel e testar o painel, a navegação entre as três telas e o cadastro demonstrativo.
7. Para testar o modo persistente, criar uma conta de testes, autenticar-se e confirmar que os registros permanecem após atualizar a página. Não usar nome, telefone, documentos ou informações reais de pacientes.

## Evidência acadêmica

Capturar a página publicada pela Vercel em uma janela maximizada com a barra de endereço exibindo a URL completa. Registrar o endereço exato oferecido pela Vercel; **não presumir** que será `ubs-caic-gestao-avisos.vercel.app`.

## Monitoramento

O workflow `.github/workflows/monitoramento.yml` valida atualmente a implantação alternativa no Supabase Edge Functions e sua conexão com o PostgreSQL. Após receber a URL definitiva da Vercel, atualizar o workflow para monitorar a URL final (ou configurar UptimeRobot/Better Stack) e comprovar o status **UP**.

## Segurança e limites

Nenhuma chave secreta ou `service_role` deve ser incluída no frontend. Somente a chave pública do Supabase está presente no HTML e todas as tabelas estão protegidas por RLS. O projeto é um protótipo acadêmico e não está apto para dados reais de saúde nem para utilização clínica.
