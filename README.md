# CNT Gestor

Sistema de gestão de estoque, movimentações e dispensação de canetas aplicadoras reutilizáveis de insulina no contexto da assistência farmacêutica na atenção básica.

## Visão geral

O CNT Gestor é um projeto full-stack voltado à organização e ao controle administrativo de canetas aplicadoras reutilizáveis de insulina.

A aplicação busca integrar o gerenciamento do estoque à gestão das necessidades dos pacientes, permitindo acompanhar dispensações, quantidades em posse dos pacientes, tratamentos vigentes e ocorrências que afetem a disponibilidade das canetas.

O objetivo é proporcionar rastreabilidade, consistência dos registros e maior confiabilidade nos processos de gestão desses materiais.

## Escopo do sistema

O sistema contempla:

- Cadastro e acompanhamento de pacientes.
- Registro de tratamentos e seu histórico.
- Cadastro de instituições fornecedoras e responsáveis por dispensações.
- Controle de estoque por modelo, lote e quantidade.
- Registro de entradas, saídas e ajustes de estoque.
- Histórico de dispensações, inclusive aquelas realizadas por instituições externas.
- Controle das quantidades de canetas em posse dos pacientes.
- Registro de ocorrências de perda e dano.
- Apuração das necessidades de canetas conforme o tratamento vigente.
- Acompanhamento dos critérios administrativos para novas dispensações.

O escopo está restrito às canetas aplicadoras reutilizáveis. O controle de insulina, agulhas e outros insumos não faz parte dos objetivos do sistema.

## Regras iniciais do domínio

A quantidade necessária de canetas é determinada pelos tipos de insulina utilizados no tratamento vigente e pelos respectivos modelos compatíveis.

Na configuração inicial, são consideradas as seguintes necessidades:

| Insulinas utilizadas | NPH/Regular | Glargina/Lantus |
|---|---:|---:|
| NPH | 1 | 0 |
| Regular | 1 | 0 |
| NPH + Regular | 2 | 0 |
| Glargina | 0 | 1 |
| Glargina + Regular | 1 | 1 |

O cálculo da necessidade atual não elimina o histórico de tratamentos ou as canetas anteriormente recebidas. A disponibilidade deve considerar as quantidades ainda utilizáveis em posse do paciente.

O prazo administrativo de referência para nova dispensação é de três anos por ciclo de recebimento. A data da dispensação é utilizada como referência operacional quando a data do primeiro uso não está disponível. Registros históricos sem data conhecida permanecem indeterminados, sem atribuição de datas presumidas.

As regras detalhadas do domínio estão documentadas em [Modelo de Domínio](docs/domain-model.md).

## Tecnologias

| Área | Tecnologias |
|---|---|
| Linguagem | Python 3.14 |
| API | FastAPI |
| ORM | SQLAlchemy 2.x |
| Servidor ASGI | Uvicorn |
| Banco de dados | SQLite (fase inicial) |
| Gerenciamento de dependências | uv |
| Controle de versão | Git e GitHub |
| Ambiente de desenvolvimento | WSL 2, Ubuntu e Visual Studio Code |

A interface web está prevista para uma etapa posterior do desenvolvimento.

## Requisitos

Para configurar e executar o projeto, são necessários:

- Python 3.14.
- [uv](https://docs.astral.sh/uv/).
- Git.

## Configuração do ambiente

Clone o repositório e acesse seu diretório:

```bash
git clone git@github.com:felipeharlen/cnt-gestor.git
cd cnt-gestor
```

Sincronize o ambiente:

```bash
uv sync --locked
```

O comando instala as dependências conforme as declarações do `pyproject.toml` e as versões registradas no `uv.lock`.

A versão preferencial do Python é definida no arquivo `.python-version`.

## Execução

Inicie o servidor de desenvolvimento:

```bash
uv run uvicorn src.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

O endpoint de verificação de funcionamento pode ser acessado em:

```text
http://127.0.0.1:8000/health
```

A documentação interativa da API, disponibilizada pelo FastAPI, estará acessível em:

```text
http://127.0.0.1:8000/docs
```

## Gerenciamento de dependências

O projeto utiliza o uv para gerenciar as dependências e o ambiente virtual.

Adicionar uma dependência:

```bash
uv add nome-do-pacote
```

Remover uma dependência:

```bash
uv remove nome-do-pacote
```

Sincronizar o ambiente com a configuração do projeto:

```bash
uv sync
```

As alterações nas dependências devem ser acompanhadas da atualização e versionamento dos arquivos `pyproject.toml` e `uv.lock`.

## Estrutura do projeto

```text
cnt-gestor/
├── docs/
│   ├── domain-model.md
│   └── data-model.md
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── db.py
│   │
│   └── models/
│       ├── __init__.py
│       └── institution.py
│
├── tests/
│   └── .gitkeep
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

## Documentação

- [Modelo de Domínio](docs/domain-model.md)
- [Modelo de Dados](docs/data-model.md)

## Estado do desenvolvimento

**Estágio atual:** implementação inicial da camada de persistência e dos modelos ORM.

### Implementado

- Estrutura inicial da aplicação.
- Configuração da API com FastAPI.
- Endpoint de verificação de funcionamento (`/health`).
- Configuração da conexão com SQLite.
- Criação automática do diretório de dados.
- Classe-base declarativa do SQLAlchemy.
- Primeiro modelo ORM (`Institution`).
- Restrições de integridade e índice parcial de unicidade no modelo `Institution`.
- Validações manuais das restrições do modelo em banco SQLite.
- Gerenciamento do ambiente e das dependências com uv.

### Próximas etapas

- Implementação dos demais modelos ORM.
- Definição dos relacionamentos e restrições de integridade.
- Implementação de testes automatizados.
- Implementação das regras de negócio.
- Desenvolvimento dos endpoints REST.
- Desenvolvimento da interface web.
- Preparação para implantação.