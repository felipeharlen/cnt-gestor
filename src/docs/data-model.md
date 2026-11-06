# CNT Gestor — Modelo de Dados

## 1. Objetivo

Este documento define o modelo de dados do CNT Gestor, descrevendo como as informações do domínio serão persistidas no banco de dados.

O modelo apresenta as entidades persistentes, seus atributos, identificadores, relacionamentos e restrições necessárias para representar o controle de estoque, movimentações e dispensações de canetas aplicadoras de insulina.

Este documento é baseado no Modelo de Domínio do CNT Gestor e servirá como referência para a implementação do banco de dados e da camada de persistência da aplicação.

## 2. Convenções do Modelo

### 2.1 Identificadores

Todas as entidades persistentes possuirão uma chave primária denominada `id`.

Os identificadores utilizarão valores inteiros gerados automaticamente pelo banco de dados.

### 2.2 Nomenclatura

Os nomes das tabelas e colunas utilizarão o padrão `snake_case`.

As tabelas utilizarão nomes no plural, enquanto os atributos utilizarão nomes descritivos no singular, conforme o contexto.

As chaves primárias serão identificadas pelo nome `id`.

As chaves estrangeiras utilizarão o nome da entidade referenciada seguido do sufixo `_id`.

Exemplos:

- Tabela: `patients`
- Chave primária: `id`
- Atributos: `name`, `cns`, `birth_date`
- Chave estrangeira: `patient_id`

### 2.3 Chaves estrangeiras

As chaves estrangeiras serão utilizadas para estabelecer relacionamentos entre as entidades e garantir a integridade referencial dos dados.

Cada chave estrangeira deverá referenciar a chave primária da entidade correspondente.

Exemplos:

- `patient_id` referencia `patients.id`;
- `product_id` referencia `products.id`;
- `batch_id` referencia `batches.id`.

### 2.4 Datas e horários

Campos que representam data e horário utilizarão tipos temporais apropriados.

Os nomes seguirão o padrão:

- `*_date` para datas;
- `*_at` para datas e horários.

Exemplos:

- `delivery_date`
- `created_at`
- `updated_at`

### 2.5 Auditoria

As entidades que necessitarem de rastreabilidade possuirão campos de auditoria, conforme necessário, como:

- `created_at`
- `updated_at`

Campos adicionais de auditoria, como identificação do usuário responsável por uma operação, serão definidos de acordo com as necessidades de cada entidade e operação.

### 2.6 Exclusão de registros

Registros relacionados a movimentações de estoque, dispensações e rastreabilidade não deverão ser removidos fisicamente quando isso comprometer o histórico do sistema.

A estratégia de exclusão ou inativação será definida conforme a natureza de cada entidade.