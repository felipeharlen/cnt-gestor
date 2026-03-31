# CNT Gestor

Projeto full-stack para o desenvolvimento de um sistema de gerenciamento de canetas aplicadoras de insulina.

---

## Visão Geral

O CNT Gestor é um sistema desenvolvido para registrar e monitorar entradas e saídas de canetas aplicadoras de insulina, oferecendo controle básico de inventário e rastreabilidade. Seu objetivo é manter uma gestão confiável desses insumos em contextos relacionados à saúde.

---

## Domínio do Problema

Gerenciar insumos vai além do simples controle de estoque. Neste contexto, canetas aplicadoras de insulina são dispensadas a indivíduos insulino-dependentes conforme regras específicas de elegibilidade previamente estabelecidas.

A quantidade de canetas fornecidas a cada indivíduo é definida pela sua prescrição terapêutica. O uso de um único tipo de insulina (NPH ou Regular) dá direito a **uma caneta**, enquanto o uso combinado de NPH e Regular dá direito a **duas canetas**.  
Uma vez dispensada, cada caneta possui validade de **três anos** a partir da primeira utilização. O sistema deve, portanto, manter o histórico de dispensações, permitindo identificar quantas canetas um indivíduo já recebeu e quando ele se tornará elegível para uma nova dispensação.

O CNT Gestor deverá ser capaz de aplicar essas regras, mantendo um histórico claro e auditável das movimentações, de modo a prover controle de inventário e gestão de elegibilidade.

---

## Tecnologias Utilizadas

**Backend**
- Python
- FastAPI

**Banco de Dados**
- SQLite (fase inicial)

**Frontend**
- Planejado (interface web)

---

## Status do Projeto

**Estágio atual:** Desenvolvimento inicial

### Implementado
- Estrutura básica do projeto
- Configuração da aplicação FastAPI
- Endpoint de status da aplicação (`/health`)

### Em Andamento
- Configuração do banco de dados
- Modelagem do domínio de movimentações de estoque

### Planejado
- Persistência das movimentações de estoque
- Registro das dispensações de canetas por indivíduo
- Cálculo de elegibilidade com base nas datas de dispensação
- Endpoints REST para operações de estoque e dispensação
- Frontend web
- Implantação

---

## Estrutura do Projeto
```
cnt-gestor/
├── src/
│ ├── __init__.py
│ ├── main.py
│ │
│ ├── api/
│ │ ├── __init__.py
│ │ └── health.py
│ │
│ ├── core/
│ │ └── config.py
│ │
│ ├── db/
│ │ └── db.py
│
└── README.md
```