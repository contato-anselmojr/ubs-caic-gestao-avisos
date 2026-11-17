# Sistema de Gestao de Agendamentos e Notificacao de Exames — UBS CAIC

Projeto academico de **Projeto de Software**, Curso Superior de Tecnologia em Analise e Desenvolvimento de Sistemas (3º semestre).

**Unidade parceira:** UBS Sueli Dutra Alves (CAIC), Conjunto Nilson Neves, Paranagua - PR.

**ODS relacionado:** ODS 3 — Saude e Bem-Estar.

## Problema e objetivo

O projeto busca apoiar a recepcao da UBS na organizacao de consultas, identificacao de vagas canceladas e acompanhamento da disponibilidade de exames preventivos, reduzindo esquecimento de consultas e deslocamentos desnecessarios.

## Estado atual da implementacao

Esta versao e um **prototipo web demonstrativo**, desenvolvido com Python e HTML/CSS/JavaScript. **Nao e um sistema apto para dados reais de saude ou operacao em producao.**

O arquivo `app.py` utiliza `http.server` da biblioteca padrao do Python. A arquitetura planejada com Django, banco de dados e integracao de mensagens ainda nao foi implementada nesta versao.

### Telas demonstradas

1. Painel de resumo do turno, com contadores atualizados a partir dos registros ficticios em memoria.
2. Cadastro rapido de consultas e protocolos de exames preventivos.
3. Fila e alertas, com simulacao de mudanca do status de aviso.

**Limites relevantes:** nao existe autenticacao real, banco de dados, persistencia apos recarregar a pagina ou envio efetivo de WhatsApp/SMS. As informacoes usadas na interface sao ficticias. O botao de saida e apenas demonstrativo.

## Requisitos

- Python 3.12 (sem pacotes externos nesta etapa)
- Navegador web atual

## Executar localmente

No Git Bash, na pasta do projeto:

```bash
python app.py
```

Abrir no navegador: http://127.0.0.1:5000

Para encerrar, pressionar `Ctrl+C` no terminal.

## Testes automatizados

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem respostas HTTP (200 e 404), presenca das telas do prototipo e o codigo do contador de consultas. Nao validam integracao com mensageria ou seguranca em producao.

Um workflow em `.github/workflows/testes.yml` executa esses testes em push e Pull Request direcionado a `main`.

## Proximos passos planejados

- Migrar o prototipo para a arquitetura monolitica em camadas com Django.
- Adicionar modelos persistentes de operadores, consultas e exames.
- Implementar login, permissoes, CSRF e demais controles de seguranca.
- Desenvolver integracao desacoplada com provedor oficial de WhatsApp/SMS.
- Testar acessibilidade, desempenho, cadastros e fluxo de mensagens com dados ficticios.

## Privacidade

Nao cadastrar nomes, telefones ou informacoes de saude reais nesta versao publica. O projeto nao exibe diagnosticos, resultados de exames nem documentos clinicos.

## Versionamento

Commits semanticos registram a publicacao do prototipo, correcao do contador, testes, integracao continua e documentacao.
