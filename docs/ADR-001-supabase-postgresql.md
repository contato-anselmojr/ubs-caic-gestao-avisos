# ADR-001 — Persistência de dados demonstrativos com Supabase PostgreSQL

**Projeto:** Sistema de Gestão de Agendamentos e Notificação de Exames — UBS CAIC  
**Data da decisão:** 17/11/2026  
**Status:** Proposta aprovada para desenvolvimento; integração ainda não implementada

## Contexto

O protótipo atual usa Python `http.server` para servir a interface HTML/CSS/JavaScript. Consultas e exames são armazenados apenas em arrays JavaScript durante a sessão. Atualizar a página apaga os novos registros, o que limita os testes de fluxo e a demonstração de persistência.

Na Experiência Prática 2, foram planejados Django/MVT, SQLite no desenvolvimento e PostgreSQL em produção. Para a Experiência Prática 4, foi escolhida uma evolução incremental com **Supabase PostgreSQL** como banco gerenciado, preservando inicialmente a interface do protótipo.

## Decisão arquitetural

1. Criar um **projeto Supabase exclusivo para a UBS CAIC**; não reutilizar o projeto já existente de outra aplicação.
2. Manter a interface em HTML5, CSS3 e JavaScript e adicionar uma camada **backend Python** responsável por validar requisições e consultar o banco.
3. Modelar `usuarios_operadores`, `agendamentos_consultas` e `exames_preventivos`, seguindo os requisitos da Experiência Prática 2, com dados estritamente fictícios.
4. Implementar cadastro, listagem e atualização de status no servidor; substituir gradualmente os arrays em memória por respostas persistidas.
5. Proteger o acesso: credenciais apenas no backend, `.env` ignorado no Git, permissões mínimas, RLS quando aplicável, nenhuma tabela sensível exposta a visitantes anônimos.
6. Executar testes automatizados, realizar consultas de verificação após a criação de tabelas e registrar commits semânticos.
7. Somente publicar a demonstração na internet após estabelecer autenticação/autorização adequadas ou limitar a interface pública a dados demonstrativos sem acesso irrestrito a escrita.

## O que existe hoje (antes da integração)

- Três telas navegáveis: painel inicial, cadastro e fila/alertas.
- Cadastro e atualização de status **simulados no navegador**, sem persistência.
- Testes de servidor HTTP e GitHub Actions.
- Refatoração dos cabeçalhos HTTP e validação de datas desenvolvidas na branch de revisão da Experiência Prática 3.

## O que ainda falta implementar e comprovar

- Criar o projeto isolado no Supabase e verificar sua disponibilidade.
- Criar tabelas, restrições, índices e políticas adequadas.
- Conectar o backend ao banco sem expor credenciais.
- Implementar endpoints protegidos, persistência, consultas e atualização de status.
- Executar testes de integração com banco real e medir a cobertura novamente.
- Integrar branches à `main`, realizar deploy e monitoramento.

## Diferenças em relação ao planejamento

O PostgreSQL em nuvem passa a ser adotado **diretamente no ambiente de testes**, sem SQLite obrigatório como primeira etapa. A escolha do Supabase reduz o esforço de manutenção do servidor de banco. Isso **não significa** que Django/MVT, autenticação, envio de WhatsApp/SMS ou o módulo FIFO tenham sido entregues; seguem pendentes até sua implementação e verificação.

## Limites éticos e operacionais

O sistema é demonstrativo e não deve receber dados reais de pacientes, números telefônicos reais, laudos, diagnósticos ou informações clínicas. Uma conexão a um banco gerenciado não equivale a certificação de segurança nem autorização de uso por uma unidade de saúde.
