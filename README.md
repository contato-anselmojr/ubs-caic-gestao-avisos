# Sistema de Gestão de Agendamentos e Notificação de Exames — UBS CAIC

**Projeto acadêmico de Projeto de Software** — Tecnologia em Análise e Desenvolvimento de Sistemas (3º semestre).  
**Unidade de referência do estudo:** UBS Sueli Dutra Alves (CAIC), Paranaguá/PR.  
**ODS relacionado:** ODS 3 — Saúde e Bem-Estar.

> **Atenção:** este é um **MVP acadêmico demonstrativo**, não um sistema oficial ou homologado da UBS. Não cadastre pacientes, contatos, resultados de exames ou outros dados reais de saúde. Utilize exclusivamente informações fictícias.

## Como avaliar o projeto

Existem **três maneiras** de avaliar as telas e os fluxos, com objetivos diferentes:

| Modalidade | Como acessar | Precisa de conta? | Os dados permanecem após atualizar a página? |
| --- | --- | --- | --- |
| **1. Teste local (download + Python)** | Baixar este repositório e executar `iniciar_teste.py` | **Não** | **Não**. Apenas arrays temporários no navegador. |
| **2. Versão online — demonstração** | [Abrir a aplicação na Vercel](https://ubs-caic-gestao-avisos.vercel.app) | **Não** | **Não**. Os dados de visitantes são demonstrativos e temporários. |
| **3. Versão online — conta DEMO compartilhada** | Mesmo endereço da Vercel; entrar com credenciais de avaliação fornecidas pelo responsável | **Sim, conta de demonstração** | **Previsto: sim**, com até **10 registros somados (consultas + exames)**, protegidos por RLS. A autenticação e persistência ainda exigem teste real após o provisionamento da conta. |

O **link público final do trabalho acadêmico** é:

**https://ubs-caic-gestao-avisos.vercel.app**

O avaliador pode explorar a versão online **sem cadastro ou login**: painel, cadastro demonstrativo de consultas, protocolos de exames e fila/alertas. Os dados inseridos no modo visitante não são encaminhados ao Supabase; somem ao recarregar a página.

O login é necessário **apenas para testar a modalidade com persistência no banco**; não é necessário para visualizar o projeto. A conta compartilhada DEMO tem limite de **10 registros simultâneos**, somando consultas e exames: ao chegar a 10, o avaliador precisa **excluir um registro fictício** para liberar espaço. O limite é aplicado por um trigger no **PostgreSQL**, inclusive contra tentativas de contornar o navegador. Mesmo com login, o sistema **não deve receber dados reais**.

**Conta DEMO ativada (17/11/2026):** login `avaliador.ubs.caic@example.com`, com email confirmado no **Supabase Auth** e perfil `demonstracao` associado no PostgreSQL. **Senha pública de demonstração:** `teste1234567` — destinada exclusivamente a esta conta compartilhada, sem acesso administrativo. A interface foi publicada na Vercel, mas a jornada de login/persistência ainda requer validação prática. A criação livre de contas foi ocultada na interface; o bloqueio de novas inscrições diretamente na API exige desabilitar o signup no painel Supabase Auth.

### Acesso público de avaliação

| Campo | Informação |
| --- | --- |
| Site | https://ubs-caic-gestao-avisos.vercel.app |
| Login | `avaliador.ubs.caic@example.com` |
| Senha DEMO | `teste1234567` |
| Permissão | Somente registros fictícios do sistema UBS CAIC |
| Limite | 10 registros no total: consultas + exames |
| Para liberar espaço | Excluir um registro já existente |

**Atenção:** estas credenciais são intencionalmente públicas e compartilhadas, apenas para testes. Qualquer pessoa pode acessar e apagar os registros fictícios dessa conta. Não use dados reais, senhas reutilizadas ou informações privadas.

### Central de Notificações — implementação demonstrativa ativa

**Automático:** ao cadastrar uma consulta futura na modalidade autenticada, um trigger PostgreSQL agenda os lembretes **48 e 24 horas antes** (quando ainda houver tempo para cada um). Um job **Supabase Cron / pg_cron a cada minuto** marca os avisos vencidos como **simulados**, mesmo com o navegador fechado. A programação e o histórico ficam em `public.notificacoes_demo`, protegidos por RLS. Cancelamentos removem os avisos ainda agendados.

**Manual:** na aba **Notificações**, pesquise pelo nome, telefone ou protocolo do paciente fictício. Na aba **Fila e Alertas**, marque o resultado como **disponível**. Depois selecione o exame na Central e clique em **Registrar aviso manual simulado**. O evento fica registrado no histórico, sem incluir informações clínicas.

**Modo público sem login:** demonstração local em memória, sem persistência nem processamento cron em segundo plano.

**Importante:** **não há envio real de SMS ou WhatsApp** nem integração com provedor de mensagens. “Simulada” significa somente que o sistema processou o evento internamente, **não** que uma mensagem foi entregue. A integração real dependeria de provedor, consentimento do destinatário e controles de privacidade/LGPD. Não inserir dados reais de pacientes.

**Banco:** migração versionada em [db/notificacoes_demo.sql](db/notificacoes_demo.sql). O limite de **10 registros** da conta DEMO continua abrangendo **somente consultas e exames**, não os eventos de notificação.


## 1. Baixar e executar a versão de teste local

A versão local foi mantida especificamente para **avaliação do código e dos fluxos no próprio computador**, sem internet, sem banco de dados, sem conta no Supabase e sem instalação de pacotes de terceiros.

### Passo 1 — baixar o projeto

1. Nesta página do GitHub, clique em **Code**.
2. Clique em **Download ZIP**.
3. Extraia o ZIP para uma pasta do computador. **Não execute os arquivos de dentro do ZIP.**

### Passo 2 — iniciar no Windows (maneira mais fácil)

1. Instale **Python 3** (recomendado Python 3.12) em https://www.python.org/downloads/ e marque **Add Python to PATH** durante a instalação, caso necessário.
2. Dentro da pasta extraída, dê **dois cliques em `iniciar_teste.bat`**.
3. O script chama o Python, inicia o servidor local e tenta abrir o navegador automaticamente.
4. Se o navegador não abrir, acesse manualmente **http://127.0.0.1:5000**.

Se preferir, abra um terminal na pasta extraída e execute:

```powershell
python iniciar_teste.py
```

### macOS ou Linux

Abra o terminal na pasta do projeto e execute:

```bash
python3 iniciar_teste.py
```

O navegador será aberto automaticamente quando possível. Caso contrário, visite **http://127.0.0.1:5000**.

**Para encerrar:** mantenha o terminal aberto enquanto avalia e pressione `Ctrl+C` quando terminar.

**Alternativa com o arquivo original:** `python app.py` (no macOS/Linux, `python3 app.py`). Em seguida, abra `http://127.0.0.1:5000` manualmente. O arquivo `app.py` depende apenas de `http_headers.py` e da biblioteca padrão do Python.

**Importante:** a versão local **não acessa o banco Supabase**. Todos os nomes e telefones exibidos e inseridos devem ser fictícios. Ela é adequada para avaliar interface e fluxos simulados, e não prova persistência.

### O que testar na versão local

1. Abrir o **Painel Resumo do Turno** e conferir os indicadores.
2. Acessar **Cadastro Rápido** e criar uma consulta fictícia com data e hora futuras.
3. Tentar cadastrar uma consulta no passado e observar a validação.
4. Cadastrar um **exame preventivo fictício** com protocolo não utilizado.
5. Abrir **Fila e Alertas** e registrar uma alteração de status demonstrativa.
6. Atualizar a página para verificar que os dados temporários voltam ao estado inicial.

## 2. Avaliar a versão online final na Vercel

**Link:** https://ubs-caic-gestao-avisos.vercel.app

- **Sem login:** a interface funciona em modo público demonstrativo, com dados fictícios em memória. O avaliador pode navegar e testar os formulários sem fazer cadastro.
- **Com a conta DEMO compartilhada:** o frontend utiliza o **Supabase Auth** para autenticação e a **Data API do Supabase PostgreSQL** para gravar, consultar e **excluir** registros permitidos pelas políticas RLS. O limite de **10 registros** é aplicado no banco, com contador na interface.
- **Persistência autenticada:** há código para cadastro, leitura, atualização de exame e exclusão de consultas/exames, mas **a jornada completa de login e persistência ainda não foi homologada**. A sessão de login não é mantida ao atualizar a página; entre novamente para consultar registros persistidos. O envio de mensagens WhatsApp/SMS não está implementado.
- As telas online são um **MVP demonstrativo**. Nenhuma modalidade constitui autorização para uso assistencial real.

## 3. Tecnologias e arquitetura

| Camada / finalidade | Tecnologia adotada |
| --- | --- |
| Código-fonte e versionamento | **GitHub** — repositório público, Pull Requests e GitHub Actions |
| Interface web do deploy final | **HTML5, CSS3 e JavaScript** — `index.html` |
| Hospedagem pública | **Vercel** — site estático em HTTPS integrado à branch `main` |
| Banco de dados | **Supabase PostgreSQL 17** — projeto isolado `ubs-caic-gestao-avisos` |
| Autenticação | **Supabase Auth** |
| Controle de acesso a registros | **PostgreSQL Row Level Security (RLS)**, segregação por operador |
| Servidor do protótipo local | **Python 3 / biblioteca padrão `http.server`** |
| Implantação alternativa de demonstração | **Supabase Edge Functions (Deno/TypeScript)** |
| Testes e disponibilidade | **Python unittest + GitHub Actions** |

**Arquitetura da demonstração online:** navegador → site estático na **Vercel** → **Supabase Auth / Data API** → **PostgreSQL**, com validações e políticas RLS. O modo visitante **não grava no banco**.

**Arquitetura da demonstração local:** navegador → servidor **Python `http.server`** → interface com dados apenas na memória do navegador.

### Por que GitHub, Vercel e Supabase?

Essas ferramentas foram escolhidas para viabilizar a entrega de um **projeto acadêmico individual** com código público, hospedagem acessível por HTTPS e banco de dados gerenciado, **utilizando modalidades gratuitas disponíveis para o projeto**. O uso gratuito está sujeito a limites e às políticas de cada provedor; não significa hospedagem ilimitada nem garantia de disponibilidade permanente.

O GitHub permite auditoria do código-fonte. A Vercel publica a interface e faz deploy automático a partir da branch principal. O Supabase oferece PostgreSQL gerenciado, autenticação e políticas RLS, evitando a manutenção manual de um servidor de banco de dados.

## 4. Organização dos arquivos principais

```text
.
├── README.md                     # Este guia: execução local e acesso online
├── GUIA_DO_AVALIADOR.md          # Roteiro passo a passo para avaliação
├── iniciar_teste.bat             # Inicialização com dois cliques (Windows)
├── iniciar_teste.py              # Inicialização local + abertura do navegador
├── app.py                        # Protótipo local (Python http.server)
├── http_headers.py               # Cabeçalhos HTTP do protótipo local
├── index.html                    # Interface da versão Vercel
├── vercel.json                   # Cabeçalhos de segurança na Vercel
├── db/schema_supabase.sql        # Estrutura PostgreSQL e políticas RLS
├── db/limite_conta_demo.sql      # Trigger de limite de 10 registros da conta DEMO
├── supabase/functions/           # Implantação alternativa em Edge Functions
├── tests/                        # Testes automatizados de Python
└── .github/workflows/            # Testes e monitoramento
```

Para verificar os testes automatizados localmente, na pasta do repositório:

```bash
python -m unittest discover -s tests -v
```

## 5. Monitoramento, privacidade e limitações

O workflow [Monitoramento de disponibilidade — UBS CAIC](https://github.com/contato-anselmojr/ubs-caic-gestao-avisos/actions) consulta periodicamente (agendamento **a cada 15 minutos**) a URL final na Vercel, o endpoint de saúde da Edge Function e a conectividade com PostgreSQL. As execuções bem-sucedidas aparecem como `Success` e as falhas como `Failure`. As verificações podem sofrer atrasos do agendador do GitHub Actions.

**Não há** integração real de WhatsApp/SMS, fila FIFO automática, acesso a sistemas oficiais do SUS, resultados clínicos ou autorização institucional para implantação na UBS. O protótipo é acadêmico e trabalha **exclusivamente com informações fictícias**.

### Documentação complementar

- [Guia do avaliador](GUIA_DO_AVALIADOR.md)
- [Configuração da conta DEMO](docs/conta-demo.md)
- [Arquitetura e decisão Supabase](docs/ADR-001-supabase-postgresql.md)
- [Deploy e monitoramento](docs/deploy-e-monitoramento.md)
- [Deploy pela Vercel](docs/deploy-vercel.md)
