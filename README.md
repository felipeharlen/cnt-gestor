# CNT Gestor

Projeto full-stack para o desenvolvimento de um sistema de gerenciamento de canetas aplicadoras reutilizáveis de insulina.

---

## Visão Geral

O CNT Gestor é um sistema desenvolvido para controlar o estoque, as movimentações e as dispensações de canetas aplicadoras reutilizáveis de insulina, além de acompanhar as necessidades e a quantidade de canetas em posse dos pacientes.

Seu objetivo é proporcionar uma gestão organizada, confiável e rastreável desses materiais no contexto da assistência farmacêutica na atenção básica.

---

## Domínio do Problema

Gerenciar canetas aplicadoras reutilizáveis de insulina vai além do simples controle de estoque. Sua dispensação depende de regras relacionadas à prescrição terapêutica, à quantidade de canetas em posse do paciente e aos critérios de elegibilidade para novas dispensações.

A quantidade necessária é calculada conforme os tipos de insulina registrados no tratamento vigente e os respectivos modelos de caneta compatíveis.

Na configuração inicial:

| Insulinas utilizadas | NPH/Regular | Glargina/Lantus |
|---|---:|---:|
| NPH | 1 | 0 |
| Regular | 1 | 0 |
| NPH + Regular | 2 | 0 |
| Glargina | 0 | 1 |
| Glargina + Regular | 1 | 1 |

O sistema também deve considerar o histórico de tratamentos e dispensações, as quantidades ainda utilizáveis em posse dos pacientes e as ocorrências de perda ou dano.

O prazo administrativo para nova dispensação é de três anos por ciclo de recebimento. A data da dispensação será utilizada como referência operacional quando a data do primeiro uso não estiver disponível. Registros históricos sem data conhecida deverão permanecer identificados como indeterminados, sem atribuição de datas presumidas.

Dessa forma, o CNT Gestor busca integrar o controle de estoque à gestão das necessidades dos pacientes, mantendo o histórico das operações e a rastreabilidade das movimentações.

---

## Tecnologias Utilizadas

**Backend**
- Python
- FastAPI
- SQLAlchemy 2.x

**Banco de Dados**
- SQLite (fase inicial)

**Frontend**
- Planejado (interface web)

**Ambiente e ferramentas**
- Git e GitHub
- Visual Studio Code
- WSL 2 com Ubuntu

---

## Status do Projeto

**Estágio atual:** Implementação inicial da persistência de dados e dos modelos ORM.

**Implementado**
- Estrutura básica do projeto.
- Configuração inicial da aplicação FastAPI.
- Endpoint de verificação de funcionamento (`/health`).
- Documentação do modelo de domínio.
- Documentação do modelo de dados.
- Configuração da conexão com o banco SQLite.
- Criação automática do diretório de dados.
- Configuração da classe-base declarativa do SQLAlchemy.
- Primeiro modelo ORM (`Institution`).
- Restrições e índice parcial de unicidade no modelo `Institution`, com validações manuais em banco SQLite.

**Próximas etapas**
- Implementação dos demais modelos ORM.
- Definição dos relacionamentos e restrições de integridade.
- Criação e gerenciamento das tabelas do banco de dados.
- Implementação de testes automatizados.
- Implementação das regras de negócio.
- Desenvolvimento dos endpoints REST.
- Desenvolvimento da interface web.
- Implantação.

---

## Documentação

- [Modelo de Domínio](docs/domain-model.md)
- [Modelo de Dados](docs/data-model.md)

---

## Estrutura do Projeto

```text
cnt-gestor/
├── data/                     # Criado automaticamente; não versionado
│   └── app.db                # Banco SQLite; criado na primeira conexão
│
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
├── tests/                    # Testes automatizados
│
├── .gitignore
├── requirements.txt
└── README.md
```

A estrutura será ampliada conforme a implementação das novas funcionalidades.

O diretório `data/` e o banco `app.db` são gerados automaticamente durante a execução e não devem ser enviados ao repositório.
