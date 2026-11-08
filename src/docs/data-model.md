# CNT Gestor — Modelo de Dados

## 1. Objetivo

Este documento define o modelo de dados do CNT Gestor, descrevendo como as informações do domínio serão persistidas no banco de dados.

O modelo apresenta as entidades persistentes, seus atributos, identificadores, relacionamentos e restrições necessários para representar os principais conceitos e operações do sistema, incluindo:

- Cadastro e acompanhamento de pacientes.
- Tipos de insulina e modelos de canetas aplicadoras.
- Histórico de tratamentos.
- Controle de estoque por lote.
- Movimentações de estoque.
- Dispensações realizadas aos pacientes.
- Controle das canetas em posse dos pacientes.
- Registro de perdas e danos.
- Controle de reposições.
- Histórico cadastral e rastreabilidade das operações.

Este documento é baseado no Modelo de Domínio do CNT Gestor e servirá como referência para a implementação do banco de dados e da camada de persistência da aplicação.

As regras de negócio, os conceitos do domínio e os comportamentos esperados do sistema são definidos no documento `domain-model.md`. Este documento concentra-se na representação persistente dessas informações.

## 2. Convenções do Modelo

### 2.1 Identificadores

Todas as entidades persistentes possuirão uma chave primária denominada `id`.

Os identificadores utilizarão valores inteiros gerados automaticamente pelo banco de dados.

### 2.2 Nomenclatura

Os nomes das tabelas e colunas utilizarão o padrão `snake_case`.

As tabelas utilizarão nomes no plural.

Os atributos utilizarão nomes descritivos e adequados ao contexto da informação representada.

As chaves primárias serão identificadas pelo nome `id`.

As chaves estrangeiras utilizarão o nome da entidade referenciada seguido do sufixo `_id`.

Exemplos:

- Tabela: `patients`
- Chave primária: `id`
- Atributos: `name`, `cns`, `birth_date`
- Chave estrangeira: `patient_id`

### 2.3 Chaves estrangeiras

As chaves estrangeiras serão utilizadas para estabelecer relacionamentos entre entidades e garantir a integridade referencial dos dados.

Cada chave estrangeira deverá referenciar a chave primária da entidade correspondente.

As regras de exclusão e atualização deverão considerar a natureza dos registros relacionados.

Registros históricos e transacionais não deverão ser removidos em cascata quando isso comprometer a rastreabilidade.

### 2.4 Datas e horários

Campos que representam apenas uma data utilizarão nomes terminados em `_date`.

Campos que representam data e horário utilizarão nomes terminados em `_at`.

Exemplos:

- `birth_date`
- `dispensation_date`
- `created_at`
- `updated_at`
- `changed_at`

A escolha entre data e data/hora deverá considerar a natureza da informação representada.

### 2.5 Auditoria

As entidades e operações que exigirem rastreabilidade poderão possuir campos de auditoria, conforme sua natureza.

Os campos poderão incluir:

- `created_at`
- `updated_at`
- `operator_id`

Quando for necessário identificar o responsável por uma operação, essa informação deverá ser representada por uma chave estrangeira para `operators`.

Registros relacionados a dispensações, movimentações de estoque, ocorrências e alterações cadastrais deverão preservar informações suficientes para permitir a identificação e rastreabilidade das operações realizadas.

### 2.6 Exclusão e inativação de registros

Registros históricos ou transacionais não deverão ser removidos fisicamente quando sua exclusão comprometer a rastreabilidade ou a integridade do histórico do sistema.

Isso se aplica especialmente a:

- Movimentações de estoque.
- Dispensações.
- Ocorrências.
- Registros históricos de tratamento.
- Histórico de situação cadastral.
- Períodos de acompanhamento territorial.
- Registros de unificação.

Entidades cadastrais poderão utilizar mecanismos de inativação quando necessário, preservando os registros históricos relacionados.

A estratégia específica de exclusão, inativação ou restrição de remoção será definida de acordo com a natureza de cada entidade e seus relacionamentos.

## 3. Entidades do Modelo

### 3.1 Instituições (`institutions`)

Representa as instituições envolvidas no acompanhamento territorial, no recebimento, na movimentação e na dispensação de canetas.

A entidade deverá permitir o cadastro de diferentes tipos de instituições, incluindo UBS, CAF, órgãos estaduais e instituições de outros municípios.

**Atributos previstos:**

- `id`
- `name`
- `institution_type`
- `is_active`
- `created_at`
- `updated_at`

O campo `institution_type` identificará a categoria da instituição.

A instituição responsável pelo acompanhamento territorial de um paciente não será necessariamente a instituição responsável por uma dispensação.

### 3.2 Operadores (`operators`)

Representa os usuários responsáveis pelas operações realizadas no sistema.

O operador será identificado nos registros que exigirem rastreabilidade, como dispensações, movimentações de estoque, ocorrências e alterações cadastrais.

**Atributos previstos:**

- `id`
- `name`
- `is_active`
- `created_at`
- `updated_at`

A autenticação e o gerenciamento de permissões poderão ser detalhados posteriormente.

### 3.3 Pacientes (`patients`)

Representa o cadastro único de cada paciente no sistema.

O cadastro deverá ser independente da instituição responsável pelo acompanhamento territorial. Um paciente não deverá possuir cadastros distintos apenas por mudar de UBS ou município.

**Atributos previstos:**

- `id`
- `name`
- `birth_date`
- `cpf`
- `cns`
- `status`
- `merged_into_patient_id`
- `created_at`
- `updated_at`

O campo `status` representará a situação cadastral atual, utilizando os seguintes valores:

- `active`: cadastro ativo.
- `inactive`: cadastro inativo.
- `merged`: cadastro incorporado a outro cadastro durante uma unificação.

O campo `merged_into_patient_id` será uma chave estrangeira autorreferenciada a `patients.id`. Será preenchido quando o cadastro for incorporado a outro, identificando o cadastro principal.

Os documentos CPF e CNS serão armazenados como texto, preservando zeros à esquerda e evitando conversões numéricas.

Pelo menos um dos documentos deverá estar informado. Quando presentes, CPF e CNS deverão ser únicos entre os cadastros.

A ausência de um documento será representada por `NULL`, nunca por uma string vazia.

O cadastro deverá preservar os históricos de dispensação, tratamento, acompanhamento, posse de canetas e ocorrências, independentemente de sua situação atual.

### 3.4 Histórico de situação cadastral (`patient_status_history`)

Registra as alterações de situação cadastral dos pacientes.

A tabela permitirá preservar o histórico de inativações, reativações e outras alterações de situação sem depender de campos que seriam sobrescritos na tabela `patients`.

**Atributos previstos:**

- `id`
- `patient_id`
- `previous_status`
- `new_status`
- `reason_code`
- `reason_description`
- `effective_date`
- `operator_id`
- `changed_at`

O campo `reason_code` representará o motivo da alteração por meio de valores controlados.

O campo `reason_description` será utilizado para informações complementares, especialmente quando o motivo selecionado for `other`.

O campo `effective_date` representará a data em que a alteração passou a produzir efeito. Já `changed_at` registrará quando a operação foi efetivamente realizada no sistema.

No caso de falecimento, `effective_date` poderá representar a data do óbito, enquanto `changed_at` registrará quando o falecimento foi informado e registrado.

A tabela deverá permitir identificar o operador responsável por cada alteração.

A definição dos códigos de motivo e das regras de preenchimento será detalhada na implementação.

### 3.5 Unificações de pacientes (`patient_merges`)

Registra as operações de unificação de cadastros duplicados.

A tabela permitirá identificar os cadastros envolvidos, o cadastro principal escolhido e o operador responsável pela operação.

**Atributos previstos:**

- `id`
- `source_patient_id`
- `target_patient_id`
- `operator_id`
- `merged_at`

O campo `source_patient_id` identificará o cadastro incorporado.

O campo `target_patient_id` identificará o cadastro principal que permanecerá ativo.

O campo `merged_at` registrará a data e o horário da unificação.

A operação deverá preservar os históricos e a origem dos registros envolvidos.

O campo `patients.merged_into_patient_id` permitirá localizar diretamente o cadastro principal a partir do cadastro incorporado.

A tabela `patient_merges` preservará o registro específico da operação, permitindo sua auditoria.

A estrutura deverá impedir que um cadastro seja incorporado a si próprio e deverá preservar a integridade das referências entre os cadastros envolvidos.

### 3.6 Acompanhamento territorial (`patient_follow_ups`)

Representa os períodos em que um paciente esteve vinculado territorialmente a determinada instituição.

Cada registro representará um período específico de acompanhamento.

**Atributos previstos:**

- `id`
- `patient_id`
- `institution_id`
- `start_date`
- `end_date`
- `created_at`

O campo `institution_id` identificará a UBS responsável pelo acompanhamento territorial.

O campo `end_date` será nulo enquanto o acompanhamento estiver vigente.

Quando o paciente mudar para a área de cobertura de outra UBS, o período anterior será encerrado e um novo registro será criado para a nova instituição.

Caso o paciente retorne a uma área anteriormente atendida, deverá ser criado outro período de acompanhamento, sem reabrir o registro histórico anterior.

O encerramento do acompanhamento territorial não deverá apagar o cadastro do paciente nem seu histórico de posse de canetas e dispensações.

### 3.7 Tipos de insulina (`insulin_types`)

Representa os tipos de insulina utilizados nos tratamentos dos pacientes.

**Atributos previstos:**

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

A tabela deverá permitir o cadastro de novos tipos de insulina sem exigir alterações estruturais no banco de dados.

### 3.8 Modelos de caneta (`pens`)

Representa os modelos de canetas aplicadoras reutilizáveis disponíveis no sistema.

Não haverá identificação individual de cada unidade física de caneta. O controle será realizado por modelo, lote e quantidade.

**Atributos previstos:**

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

Os modelos iniciais previstos são:

- NPH/Regular.
- Glargina/Lantus.

A tabela deverá permitir o cadastro de novos modelos de caneta.

### 3.9 Compatibilidade entre canetas e insulinas (`pen_insulin_types`)

Representa a relação entre os modelos de caneta e os tipos de insulina compatíveis.

A separação dessa relação permite que um modelo de caneta seja compatível com mais de um tipo de insulina e que novos modelos sejam cadastrados sem modificar a estrutura das tabelas.

**Atributos previstos:**

- `id`
- `pen_id`
- `insulin_type_id`

A combinação entre `pen_id` e `insulin_type_id` deverá ser única.

### 3.10 Tratamentos (`treatments`)

Representa os períodos de tratamento prescritos para cada paciente.

Cada registro deverá preservar a composição do tratamento durante determinado período, permitindo consultar alterações anteriores.

**Atributos previstos:**

- `id`
- `patient_id`
- `prescriber_name`
- `prescriber_crm`
- `prescriber_uf`
- `start_date`
- `end_date`
- `operator_id`
- `created_at`

O prescritor será identificado por nome, CRM e UF.

O operador será responsável pelo registro da alteração no sistema, não pela decisão clínica.

O campo `end_date` será nulo enquanto o tratamento estiver vigente.

A documentação comprobatória da prescrição deverá ser preservada ou referenciada conforme a solução de armazenamento de documentos definida para a aplicação.

Uma alteração de tratamento deverá gerar um novo registro, encerrando o período anterior.

### 3.11 Tipos de insulina do tratamento (`treatment_insulin_types`)

Representa os tipos de insulina que compõem determinado tratamento.

**Atributos previstos:**

- `id`
- `treatment_id`
- `insulin_type_id`

A combinação entre `treatment_id` e `insulin_type_id` deverá ser única.

A separação dessa relação permite representar tratamentos com um ou mais tipos de insulina, preservando a composição histórica de cada período.

### 3.12 Lotes (`batches`)

Representa os lotes de fabricação das canetas recebidas pelo sistema.

O controle de estoque será realizado por modelo de caneta e lote, sem identificação individual de cada unidade física.

**Atributos previstos:**

- `id`
- `pen_id`
- `batch_number`
- `expiration_date`
- `created_at`

O número do lote deverá ser associado ao modelo de caneta correspondente.

A combinação entre modelo de caneta e número do lote deverá ser única.

A data de validade do produto deverá ser preservada para permitir o controle de estoque e a identificação dos lotes.

### 3.13 Movimentações de estoque (`stock_movements`)

Registra as movimentações de entrada e saída de canetas no estoque das instituições.

**Atributos previstos:**

- `id`
- `batch_id`
- `institution_id`
- `movement_type`
- `quantity`
- `operator_id`
- `reason`
- `occurred_at`
- `created_at`

O campo `batch_id` identificará o lote movimentado.

O campo `institution_id` identificará a instituição cujo estoque foi afetado pela movimentação.

O campo `movement_type` identificará a natureza da movimentação, como entrada, saída, ajuste positivo ou ajuste negativo.

A quantidade será armazenada como valor positivo. O tipo de movimentação determinará se o efeito será de entrada ou saída no estoque.

O campo `reason` permitirá registrar justificativas para operações que exigirem explicação, como ajustes de estoque.

As movimentações de estoque deverão preservar a identificação de sua origem operacional. Para isso, deverão poder ser associadas aos registros específicos que as originaram, como entradas, dispensações ou transferências.

O saldo disponível deverá ser obtido a partir das movimentações registradas, evitando divergências entre um saldo armazenado e o histórico efetivo das operações.

### 3.14 Dispensações (`dispensations`)

Representa cada operação de dispensação realizada a um paciente.

Uma dispensação poderá conter um ou mais itens, permitindo registrar entregas parciais ou a entrega de diferentes modelos de caneta em uma mesma operação.

**Atributos previstos:**

- `id`
- `patient_id`
- `institution_id`
- `operator_id`
- `treatment_id`
- `dispensation_date`
- `dispensation_type`
- `created_at`

O campo `institution_id` identificará a instituição responsável pela dispensação, independentemente da UBS responsável pelo acompanhamento territorial.

O campo `treatment_id` poderá referenciar o tratamento considerado na operação, preservando a relação entre a dispensação e a necessidade registrada naquele momento.

O campo `dispensation_type` permitirá distinguir dispensações regulares de operações de reposição, quando aplicável.

A data da dispensação deverá ser preservada mesmo quando for diferente da data em que o registro foi inserido no sistema.

Para dispensações históricas cuja data seja desconhecida, deverá ser possível registrar essa ausência sem atribuir uma data fictícia. A possibilidade de `dispensation_date` ser nula deverá ser restrita a esse cenário.

### 3.15 Itens de dispensação (`dispensation_items`)

Representa os modelos, lotes e quantidades de canetas entregues em cada dispensação.

**Atributos previstos:**

- `id`
- `dispensation_id`
- `pen_id`
- `batch_id`
- `quantity`

Cada item deverá identificar o modelo de caneta, o lote e a quantidade entregue.

Uma dispensação poderá possuir vários itens, inclusive de lotes diferentes do mesmo modelo.

O lote deverá ser obrigatório nas novas dispensações realizadas a partir do estoque controlado da instituição.

Para registros históricos ou dispensações externas cujo lote seja desconhecido, a possibilidade de utilizar `NULL` deverá ser permitida conforme as regras de registro histórico.

### 3.16 Ocorrências (`occurrences`)

Registra situações relacionadas às canetas que já foram dispensadas aos pacientes, como perdas e danos.

**Atributos previstos:**

- `id`
- `patient_id`
- `occurrence_type`
- `description`
- `operator_id`
- `occurred_at`
- `created_at`

O campo `occurrence_type` identificará a natureza da ocorrência.

O campo `description` permitirá registrar informações complementares sobre a situação relatada.

A ocorrência deverá preservar o histórico da situação informada e identificar o operador responsável pelo registro.

### 3.17 Itens de ocorrência (`occurrence_items`)

Representa os modelos, lotes e quantidades de canetas relacionados a uma ocorrência.

Essa entidade permite que uma ocorrência envolva mais de um modelo ou lote de caneta.

**Atributos previstos:**

- `id`
- `occurrence_id`
- `pen_id`
- `batch_id`
- `quantity`

O lote poderá ser nulo quando não houver informação suficiente para identificá-lo, conforme as regras definidas para ocorrências históricas ou externas.

A quantidade deverá representar as unidades afetadas pela ocorrência.

A representação da condição da caneta e de seu efeito sobre a disponibilidade do paciente deverá ser detalhada na implementação, distinguindo situações como perda e dano.

### 3.18 Autorizações de reposição (`replacement_authorizations`)

Representa as autorizações necessárias para reposições excepcionais de canetas antes do prazo administrativo regular.

**Atributos previstos:**

- `id`
- `occurrence_id`
- `authorization_reference`
- `authorized_at`
- `created_at`

A entidade deverá permitir associar uma autorização à ocorrência que motivou a solicitação.

Os dados específicos da autorização estadual, incluindo sua identificação documental e demais informações exigidas, poderão ser detalhados conforme o procedimento operacional definido.

A existência de uma ocorrência, isoladamente, não deverá ser considerada autorização suficiente para realizar uma reposição excepcional.

## 4. Relacionamentos entre Entidades

Os principais relacionamentos previstos são:

- Uma instituição poderá estar associada a vários períodos de acompanhamento territorial.
- Uma instituição poderá possuir várias movimentações de estoque.
- Uma instituição poderá realizar várias dispensações.
- Um operador poderá ser responsável por várias operações.
- Um paciente poderá possuir vários registros históricos de situação cadastral.
- Um paciente poderá possuir vários períodos de acompanhamento territorial.
- Um paciente poderá possuir vários tratamentos ao longo do tempo.
- Um paciente poderá possuir várias dispensações.
- Um paciente poderá possuir várias ocorrências.
- Um paciente poderá participar de operações de unificação como cadastro incorporado ou cadastro principal.
- Um tratamento poderá conter vários tipos de insulina.
- Um tipo de insulina poderá participar de vários tratamentos.
- Um modelo de caneta poderá ser compatível com vários tipos de insulina.
- Um tipo de insulina poderá ser compatível com vários modelos de caneta.
- Um modelo de caneta poderá possuir vários lotes.
- Um lote poderá estar associado a várias movimentações de estoque.
- Uma dispensação poderá possuir vários itens.
- Um item de dispensação deverá identificar um modelo de caneta, um lote, quando conhecido, e uma quantidade.
- Uma ocorrência poderá possuir vários itens.
- Uma ocorrência poderá estar associada a uma autorização de reposição, quando aplicável.

## 5. Restrições de Integridade e Consistência

Além das chaves primárias e estrangeiras, o banco de dados deverá contemplar restrições que protejam a consistência das informações.

### 5.1 Pacientes

- Pelo menos um entre CPF e CNS deverá estar informado.
- CPF e CNS deverão ser únicos quando preenchidos.
- A situação cadastral deverá aceitar somente os valores previstos: `active`, `inactive` e `merged`.
- Um cadastro com situação `merged` deverá referenciar o cadastro principal.
- Um cadastro não poderá ser incorporado a si próprio.
- Um cadastro não poderá ser utilizado em novas operações enquanto estiver `inactive` ou `merged`.
- Um cadastro inativo não poderá possuir acompanhamento territorial vigente.
- Um cadastro incorporado não poderá possuir acompanhamento territorial vigente.
- A unificação deverá preservar os históricos dos cadastros envolvidos.

### 5.2 Histórico de situação cadastral

- Toda alteração de situação deverá identificar o paciente e o operador responsável.
- A situação anterior e a nova situação deverão ser registradas.
- A justificativa deverá ser obrigatória para operações que exigirem motivo.
- Quando `reason_code` for `other`, a descrição complementar deverá ser obrigatória.
- A correção de um registro de falecimento deverá preservar a informação sobre o registro original e sua correção.

### 5.3 Acompanhamento territorial

- Um paciente não poderá possuir mais de um acompanhamento territorial vigente simultaneamente.
- A data de encerramento deverá ser posterior ou igual à data de início.
- Um paciente inativo ou incorporado não poderá possuir acompanhamento vigente.
- O encerramento de um período não deverá remover seu histórico.
- A criação de um novo acompanhamento deverá preservar os períodos anteriores.
- A reativação deverá criar um novo período de acompanhamento.

### 5.4 Unificação de cadastros

- O cadastro incorporado e o cadastro principal deverão ser distintos.
- Ambos deverão estar ativos antes da unificação.
- O cadastro incorporado deverá passar para a situação `merged`.
- O cadastro principal deverá permanecer ativo.
- A operação deverá ser executada integralmente ou não ser aplicada.
- O histórico da unificação deverá identificar os cadastros envolvidos e o operador responsável.

### 5.5 Tratamentos

- Um paciente poderá possuir vários tratamentos históricos.
- Um tratamento encerrado deverá preservar sua composição original.
- A combinação entre `treatment_id` e `insulin_type_id` deverá ser única.
- Uma alteração de tratamento deverá gerar um novo registro histórico, encerrando o período anterior.
- A alteração não deverá modificar os registros de dispensação anteriores.

### 5.6 Estoque e lotes

- A quantidade de uma movimentação deverá ser maior que zero.
- Toda movimentação de estoque deverá identificar o lote correspondente.
- Uma saída não poderá gerar saldo negativo no estoque da instituição.
- Movimentações históricas não deverão ser apagadas para corrigir erros; deverão ser registradas operações de correção apropriadas.
- A combinação entre modelo de caneta e número de lote deverá ser única.

### 5.7 Dispensações

- Toda dispensação deverá identificar o paciente, a instituição responsável e o operador.
- Toda dispensação deverá possuir pelo menos um item.
- A quantidade de cada item deverá ser maior que zero.
- Novas dispensações deverão respeitar a situação cadastral do paciente.
- Os itens de dispensação deverão identificar o lote utilizado quando a operação ocorrer a partir do estoque controlado.
- Dispensações externas poderão possuir informações incompletas, desde que essa condição seja registrada sem inventar dados.

### 5.8 Ocorrências e reposições

- Toda ocorrência deverá identificar o paciente e o operador responsável pelo registro.
- A quantidade de cada item de ocorrência deverá ser maior que zero.
- Uma reposição excepcional deverá possuir autorização correspondente.
- O registro de uma ocorrência não deverá alterar automaticamente o estoque da instituição.
- A ocorrência deverá preservar o histórico da quantidade afetada e sua relação com a posse do paciente.

## 6. Histórico e Rastreabilidade

O modelo deverá preservar o histórico das operações realizadas, permitindo reconstruir a situação administrativa de um paciente e os movimentos das canetas ao longo do tempo.

Deverão ser preservados especialmente:

- Alterações de situação cadastral.
- Registros e correções de falecimento.
- Unificações de cadastros.
- Períodos de acompanhamento territorial.
- Alterações de tratamento.
- Tipos de insulina associados a cada tratamento.
- Dispensações e respectivos itens.
- Lotes envolvidos nas operações.
- Movimentações de estoque.
- Ocorrências e respectivas quantidades.
- Autorizações de reposição.
- Operadores responsáveis pelas operações.

Os registros históricos e transacionais deverão permanecer consultáveis mesmo quando o paciente ou uma entidade cadastral deixar de estar ativa.

O modelo deverá permitir identificar a origem dos registros incorporados durante uma unificação, sem apagar ou substituir indevidamente sua rastreabilidade.

## 7. Decisões Pendentes de Detalhamento

Alguns aspectos do modelo dependem de definições operacionais mais específicas e deverão ser detalhados antes da implementação definitiva.

### 7.1 Cadastro de instituições

Definir os tipos de instituição aceitos, seus atributos complementares e as regras de identificação.

### 7.2 Cadastro de operadores

Definir os dados necessários para identificação dos operadores e a integração com o mecanismo de autenticação.

### 7.3 Documentos de prescrição

Definir como as prescrições serão armazenadas, incluindo a possibilidade de anexar arquivos e consultar documentos históricos.

### 7.4 Movimentações entre instituições

Detalhar a representação de transferências, incluindo a relação entre a saída de uma instituição e a entrada na instituição de destino.

### 7.5 Dispensações externas

Definir como serão registradas dispensações realizadas por outras instituições quando não houver acesso ao lote ou aos detalhes completos da operação.

### 7.6 Histórico de dispensações sem lote ou data conhecida

Definir os critérios para registrar informações antigas incompletas sem inventar datas ou números de lote.

### 7.7 Posse atual das canetas

Detalhar a forma de cálculo da quantidade de canetas em posse do paciente, considerando dispensações, perdas, danos, reposições e eventuais recebimentos ou devoluções.

Também deverá ser definida a representação da diferença entre posse física e disponibilidade para utilização.

### 7.8 Prazo administrativo de substituição

Definir como o sistema calculará a elegibilidade considerando a data de dispensação, a ausência de informação sobre a data de primeiro uso e as autorizações excepcionais.

### 7.9 Motivos de inativação e reativação

Definir as opções específicas das listas controladas de motivos, incluindo os critérios para utilização da opção `other`.

### 7.10 Correção de falecimento

Detalhar o procedimento formal para corrigir um registro de falecimento realizado equivocadamente, incluindo as autorizações e os registros necessários.

### 7.11 Transferências de estoque

Definir a estrutura definitiva para registrar uma transferência como operação única, preservando a saída da instituição de origem e a entrada na instituição de destino.

### 7.12 Ajustes de estoque

Definir os tipos de ajuste permitidos, as justificativas obrigatórias e os níveis de autorização necessários.

### 7.13 Origem das movimentações

Detalhar como cada movimentação será vinculada à operação que a originou, incluindo entradas, dispensações, transferências e ajustes.

## 8. Observações para Implementação

Este documento representa a estrutura lógica inicial do banco de dados, não necessariamente o esquema SQL definitivo.

Antes da implementação, deverão ser definidos:

- Os tipos de dados concretos de cada coluna.
- As restrições `NOT NULL`, `UNIQUE` e `CHECK`.
- Os índices necessários para consultas frequentes.
- As regras de integridade referencial e exclusão.
- As transações necessárias para operações que envolvam várias tabelas.
- As restrições que dependerem de validação na camada de aplicação.
- Os mecanismos para garantir que operações compostas sejam executadas integralmente ou não sejam aplicadas.

A implementação deverá preservar as regras estabelecidas no Modelo de Domínio e evitar que a estrutura do banco de dados permita operações incompatíveis com essas regras.