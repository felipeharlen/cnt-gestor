# CNT Gestor — Modelo de Dados

## 1. Objetivo

Este documento define o modelo de dados do CNT Gestor, descrevendo as entidades persistentes, seus atributos, relacionamentos e restrições de integridade.

O modelo deverá atender às regras descritas em `domain-model.md`.

A primeira versão controlará o estoque de uma única UBS. Instituições externas poderão ser identificadas como origens de recebimentos, fornecedoras de dispensações externas ou destinos de saídas, mas não haverá sincronização de estoques entre unidades.

## 2. Convenções

### 2.1. Identificadores

- Todas as tabelas terão uma chave primária chamada `id`.
- Inicialmente, as chaves primárias serão inteiros autoincrementais.
- As chaves estrangeiras utilizarão o nome da entidade referenciada seguido de `_id`, quando necessário.
- Não serão utilizados prefixos redundantes nos nomes das colunas.

### 2.2. Nomenclatura

- Nomes de tabelas no plural.
- Nomes de tabelas e colunas em `snake_case`.
- Nomes de tabelas e colunas em inglês, mantendo a documentação em português.
- Nomes de campos deverão representar claramente seu conteúdo.

### 2.3. Chaves estrangeiras

As relações entre entidades deverão ser representadas por chaves estrangeiras.

O SQLite deverá operar com integridade referencial habilitada (`PRAGMA foreign_keys = ON`).

Exclusões em cascata deverão ser evitadas em registros históricos e operacionais.

### 2.4. Datas e horários

O modelo deverá distinguir:

- Data efetiva: quando o evento ocorreu.
- Data de registro: quando o evento foi lançado no sistema.

Convenções:

- `*_date`: datas sem horário.
- `*_at`: datas e horários.
- Datas e horários deverão ser armazenados em formato ISO 8601 compatível com SQLite.
- A aplicação deverá padronizar o tratamento de fuso horário dos registros.
- Datas desconhecidas deverão ser representadas por `NULL`, nunca por datas estimadas.

### 2.5. Auditoria

As operações deverão identificar o operador responsável.

Os registros operacionais deverão preservar, quando aplicável:

- `operator_id`.
- `effective_date` ou `effective_at`.
- `recorded_at`.

O sistema não deverá permitir operações operacionais sem operador responsável.

### 2.6. Exclusão e inativação

Registros que participam de históricos não deverão ser excluídos fisicamente quando isso comprometer a rastreabilidade.

Cadastros que deixarem de ser utilizados deverão ser inativados quando aplicável.

Correções de operações deverão preservar a informação original e identificar a alteração realizada.

## 3. Entidades

### 3.1. `institutions`

Representa a UBS responsável pelo estoque local e as instituições externas envolvidas em fornecimentos ou saídas.

A primeira versão deverá identificar uma única instituição como responsável pelo estoque controlado.

Atributos:

- `id`: chave primária.
- `name`: nome da instituição.
- `institution_type`: tipo da instituição (`ubs`, `caf`, `state`, `municipality`, `other`).
- `is_local_stock_owner`: indica se é a instituição cujo estoque é controlado.
- `is_active`: indica se o cadastro está ativo.
- `created_at`: data e hora do cadastro.
- `updated_at`: data e hora da última atualização.

Restrições:

- Deve existir no máximo uma instituição marcada como responsável pelo estoque local.
- A instituição responsável pelo estoque não deverá ser confundida com a UBS de acompanhamento territorial do paciente.
- Instituições externas poderão ser cadastradas sem que seus estoques sejam controlados.

### 3.2. `operators`

Representa os usuários responsáveis pelas operações realizadas no sistema.

Atributos:

- `id`: chave primária.
- `name`: nome do operador.
- `is_active`: indica se o operador pode realizar novas operações.
- `created_at`: data e hora do cadastro.
- `updated_at`: data e hora da última atualização.

O operador responsável deverá ser identificado em movimentações de estoque, dispensações, ocorrências, alterações de tratamento e operações cadastrais que exijam rastreabilidade.

### 3.3. `patients`

Representa o cadastro único de cada pessoa.

Atributos:

- `id`: chave primária.
- `name`: nome completo.
- `birth_date`: data de nascimento.
- `cpf`: CPF, quando informado.
- `cns`: Cartão Nacional de Saúde, quando informado.
- `status`: situação cadastral (`active`, `inactive`, `merged`).
- `merged_into_patient_id`: cadastro principal, quando o registro tiver sido incorporado a outro.
- `created_at`: data e hora do cadastro.
- `updated_at`: data e hora da última atualização.

Restrições:

- Pelo menos um entre `cpf` e `cns` deverá ser informado.
- CPF e CNS deverão ser únicos quando presentes.
- Documentos ausentes deverão utilizar `NULL`.
- Um paciente com status `merged` deverá apontar para o cadastro principal.
- Um cadastro incorporado não poderá receber novas operações.
- A referência de incorporação não poderá apontar para o próprio registro.
- O cadastro principal deverá ser diferente do cadastro incorporado.

A situação cadastral não deverá ser confundida com o acompanhamento territorial.

### 3.4. `patient_status_history`

Registra alterações na situação cadastral dos pacientes.

Atributos:

- `id`: chave primária.
- `patient_id`: paciente afetado.
- `previous_status`: situação anterior.
- `new_status`: nova situação.
- `reason_code`: código do motivo.
- `reason_description`: descrição complementar, obrigatória quando o motivo for `other`.
- `effective_date`: data efetiva da alteração.
- `changed_at`: data e hora em que a alteração foi registrada.
- `operator_id`: operador responsável.

O falecimento deverá ser registrado por meio de uma alteração para `inactive`, com motivo próprio.

Nesse caso, `effective_date` representará a data do óbito, quando conhecida, e `changed_at` representará quando a informação foi lançada no sistema.

Restrições:

- Toda alteração deverá preservar o status anterior e o novo status.
- O operador responsável será obrigatório.
- A alteração deverá ocorrer em transação.
- A correção de um falecimento registrado equivocadamente deverá preservar o evento original e sua correção.

### 3.5. `patient_merges`

Registra operações de unificação de cadastros.

Atributos:

- `id`: chave primária.
- `merged_patient_id`: cadastro incorporado.
- `primary_patient_id`: cadastro principal.
- `operator_id`: operador responsável.
- `merged_at`: data e hora da unificação.
- `notes`: observações, quando necessárias.

Restrições:

- Ambos os cadastros deverão estar ativos no momento da unificação.
- Os dois identificadores deverão ser diferentes.
- O cadastro incorporado deverá passar para `merged`.
- `patients.merged_into_patient_id` deverá apontar para o cadastro principal.
- A operação deverá ser atômica.
- O histórico original deverá permanecer associado ao cadastro de origem, permitindo sua rastreabilidade e consulta por meio do cadastro principal.

### 3.6. `patient_follow_ups`

Registra os períodos de acompanhamento territorial de cada paciente.

Atributos:

- `id`: chave primária.
- `patient_id`: paciente acompanhado.
- `institution_id`: UBS responsável pelo acompanhamento.
- `start_date`: início do acompanhamento.
- `end_date`: término do acompanhamento, quando houver.
- `created_at`: data e hora do registro.

Regras:

- `end_date = NULL` indica acompanhamento vigente.
- Um paciente poderá possuir, no máximo, um acompanhamento vigente.
- A instituição deverá corresponder a uma UBS.
- A mudança de UBS encerra o período anterior e cria outro.
- O retorno à mesma UBS cria novo período.
- O encerramento do acompanhamento não altera o cadastro, a posse ou o histórico de dispensações.
- Pacientes inativos não poderão possuir acompanhamento vigente.

No SQLite, a restrição de um único acompanhamento vigente deverá ser implementada por índice único parcial ou validação transacional equivalente.

### 3.7. `insulin_types`

Representa os tipos de insulina cadastrados.

Atributos:

- `id`: chave primária.
- `name`: nome do tipo de insulina.
- `description`: descrição, quando necessária.
- `is_active`: indica se o tipo pode ser utilizado em novos tratamentos.
- `created_at`: data e hora do cadastro.
- `updated_at`: data e hora da última atualização.

Os tipos de insulina deverão ser cadastrados independentemente dos modelos de caneta.

### 3.8. `pens`

Representa os modelos de caneta reutilizável.

Atributos:

- `id`: chave primária.
- `name`: nome ou identificação do modelo.
- `brand`: marca.
- `description`: descrição, quando necessária.
- `is_active`: indica se o modelo pode ser utilizado em novos registros.
- `created_at`: data e hora do cadastro.
- `updated_at`: data e hora da última atualização.

Modelos iniciais:

- NPH/Regular.
- Glargina/Lantus.

O sistema deverá permitir o cadastro de novos modelos.

### 3.9. `pen_insulin_types`

Relaciona modelos de caneta aos tipos de insulina compatíveis.

Atributos:

- `id`: chave primária.
- `pen_id`: modelo de caneta.
- `insulin_type_id`: tipo de insulina.

Restrições:

- A combinação `pen_id` e `insulin_type_id` deverá ser única.
- A associação deverá ser utilizada no cálculo automático da necessidade de canetas.
- Alterações futuras na compatibilidade não deverão modificar retroativamente os registros históricos de tratamento e dispensação.

### 3.10. `treatments`

Registra os períodos de tratamento prescritos para cada paciente.

Atributos:

- `id`: chave primária.
- `patient_id`: paciente.
- `start_date`: início da vigência.
- `end_date`: término da vigência, quando houver.
- `prescriber_name`: nome do médico prescritor.
- `prescriber_crm`: número do CRM.
- `prescriber_uf`: UF do CRM.
- `operator_id`: operador responsável pelo registro.
- `recorded_at`: data e hora do registro.
- `notes`: observações, quando necessárias.

Restrições:

- Um paciente não deverá possuir dois tratamentos vigentes simultaneamente.
- A alteração de tratamento deverá encerrar o período anterior e criar um novo.
- A vigência deverá ser independente da data de registro.
- O histórico deverá ser preservado.
- A alteração deverá exigir prescrição, conforme a regra de domínio.

### 3.11. `treatment_insulin_types`

Relaciona os tratamentos aos tipos de insulina prescritos.

Atributos:

- `id`: chave primária.
- `treatment_id`: tratamento.
- `insulin_type_id`: tipo de insulina.

Restrições:

- A combinação `treatment_id` e `insulin_type_id` deverá ser única.
- A composição do tratamento deverá permanecer preservada historicamente.

### 3.12. `batches`

Representa os lotes de fabricação das canetas.

Atributos:

- `id`: chave primária.
- `pen_id`: modelo de caneta.
- `batch_code`: identificação do lote, quando conhecida.
- `manufactured_date`: data de fabricação, quando disponível.
- `manufacturer_expiry_date`: validade do fabricante, quando aplicável.
- `created_at`: data e hora do cadastro.

Restrições:

- Um lote deverá estar associado a um modelo de caneta.
- A combinação entre modelo e código de lote deverá ser única quando o código estiver informado.
- A ausência de lote em dispensações externas ou registros históricos será representada por `NULL`.
- Lotes externos poderão ser cadastrados para preservar a identificação de origem, sem que isso implique entrada no estoque local.

### 3.13. `dispensations`

Representa uma operação de recebimento de canetas por um paciente.

Atributos:

- `id`: chave primária.
- `patient_id`: paciente beneficiado.
- `origin_type`: origem (`local_ubs`, `external`, `historical`).
- `institution_id`: instituição fornecedora, quando conhecida.
- `dispensation_date`: data efetiva da dispensação ou recebimento, quando conhecida.
- `replacement_authorization_id`: autorização estadual vinculada, quando aplicável.
- `operator_id`: operador responsável pelo lançamento.
- `recorded_at`: data e hora do lançamento.
- `notes`: observações, quando necessárias.

Regras:

- Uma dispensação poderá conter vários itens.
- `local_ubs` representa uma dispensação realizada pelo estoque local.
- `external` representa fornecimento por outra instituição.
- `historical` representa registro de recebimento anterior, inclusive quando a origem for desconhecida.
- A data efetiva poderá ser nula somente quando desconhecida em um registro histórico.
- A data de registro deverá ser obrigatória.
- Dispensações locais deverão identificar a instituição responsável pelo estoque.
- Dispensações externas não movimentarão o estoque local.
- Uma dispensação estadual vinculada a reposição antecipada deverá referenciar a autorização correspondente.
- O operador responsável pelo lançamento será obrigatório.

### 3.14. `dispensation_items`

Representa os itens de cada dispensação.

Atributos:

- `id`: chave primária.
- `dispensation_id`: dispensação.
- `pen_id`: modelo de caneta.
- `batch_id`: lote, quando conhecido.
- `quantity`: quantidade recebida.

Restrições:

- A quantidade deverá ser maior que zero.
- O lote poderá ser nulo quando desconhecido ou não disponível.
- Em dispensações locais de estoque, o lote será obrigatório.
- O modelo da caneta deverá corresponder ao lote informado.
- A quantidade recebida deverá ser preservada e não poderá ser sobrescrita por ocorrências ou vencimentos.

A posse utilizável será calculada a partir dos itens de dispensação, das ocorrências vinculadas e do prazo administrativo.

Não será criada uma tabela de posse duplicada.

### 3.15. `stock_movements`

Registra todas as alterações no estoque local.

Atributos:

- `id`: chave primária.
- `movement_type`: tipo de movimentação.
- `batch_id`: lote movimentado.
- `quantity`: quantidade movimentada.
- `related_institution_id`: instituição de origem ou destino, quando aplicável.
- `dispensation_item_id`: item de dispensação relacionado, quando o movimento corresponder a uma dispensação.
- `reason_code`: código do motivo, quando aplicável.
- `reason_description`: justificativa complementar.
- `operator_id`: operador responsável.
- `effective_at`: data e hora efetiva da movimentação.
- `recorded_at`: data e hora do registro.
- `reverses_movement_id`: movimentação original, quando se tratar de estorno.

Tipos iniciais de movimentação:

- `inbound`: entrada no estoque local.
- `dispensation`: saída por dispensação a paciente.
- `outbound`: saída destinada a outra instituição.
- `adjustment_increase`: ajuste positivo.
- `adjustment_decrease`: ajuste negativo.

Regras:

- A quantidade deverá ser maior que zero.
- Toda movimentação deverá possuir operador responsável.
- Toda movimentação deverá estar associada a um lote.
- A movimentação de dispensação deverá estar vinculada ao item correspondente.
- Ajustes deverão possuir justificativa.
- Saídas não poderão resultar em estoque negativo.
- Correções deverão preservar a movimentação original.
- Uma saída para outra instituição não criará automaticamente uma entrada nessa instituição.
- A tabela representa exclusivamente o estoque local controlado pelo sistema.

O saldo de cada lote será calculado pela soma das entradas e ajustes positivos, subtraída das saídas, dispensações e ajustes negativos.

### 3.16. `occurrences`

Registra ocorrências que tornam quantidades de canetas não utilizáveis pelo paciente.

Atributos:

- `id`: chave primária.
- `patient_id`: paciente.
- `occurrence_date`: data efetiva da ocorrência, quando conhecida.
- `operator_id`: operador responsável pelo registro.
- `recorded_at`: data e hora do registro.
- `notes`: observações e referências documentais.

A ocorrência não movimenta o estoque local.

A ocorrência não gera automaticamente uma reposição.

### 3.17. `occurrence_items`

Relaciona uma ocorrência às quantidades afetadas de dispensações anteriores.

Atributos:

- `id`: chave primária.
- `occurrence_id`: ocorrência.
- `dispensation_item_id`: item da dispensação de origem.
- `quantity`: quantidade afetada.

Restrições:

- A quantidade deverá ser maior que zero.
- O item de dispensação deverá pertencer ao paciente da ocorrência.
- O total de quantidades afetadas não poderá superar o saldo utilizável da origem.
- Uma ocorrência poderá afetar mais de um item de dispensação.
- O vínculo com a dispensação de origem deverá ser preservado.
- Não haverá identificação individual das canetas.

A validação do saldo deverá considerar ocorrências anteriores e o prazo administrativo, dentro de uma transação.

### 3.18. `replacement_authorizations`

Registra solicitações e autorizações estaduais para reposição antecipada.

Atributos:

- `id`: chave primária.
- `occurrence_id`: ocorrência relacionada.
- `requested_quantity`: quantidade solicitada.
- `authorized_quantity`: quantidade autorizada, quando houver.
- `status`: situação (`requested`, `authorized`, `denied`, `cancelled`).
- `authority_reference`: protocolo ou identificação da autorização estadual.
- `requested_at`: data e hora da solicitação.
- `authorized_at`: data e hora da autorização, quando concedida.
- `operator_id`: operador responsável pelo registro.
- `notes`: observações.

Regras:

- A autorização deverá estar vinculada a uma ocorrência.
- A autorização não representa o recebimento efetivo da reposição.
- A dispensação estadual efetivamente recebida deverá ser registrada separadamente em `dispensations`.
- A dispensação de reposição deverá referenciar a autorização correspondente.
- A reposição estadual não movimentará o estoque local.

## 4. Relacionamentos principais

- `patients` 1:N `patient_status_history`.
- `patients` 1:N `patient_follow_ups`.
- `patients` 1:N `treatments`.
- `patients` 1:N `dispensations`.
- `patients` 1:N `occurrences`.
- `patients` 1:N `patient_merges`, considerando os papéis de cadastro incorporado e principal.
- `institutions` 1:N `patient_follow_ups`.
- `institutions` 1:N `dispensations`, quando a origem for conhecida.
- `insulin_types` N:N `pens`, por meio de `pen_insulin_types`.
- `treatments` N:N `insulin_types`, por meio de `treatment_insulin_types`.
- `pens` 1:N `batches`.
- `dispensations` 1:N `dispensation_items`.
- `pens` 1:N `dispensation_items`.
- `batches` 1:N `dispensation_items`, quando o lote estiver identificado.
- `batches` 1:N `stock_movements`.
- `dispensation_items` 1:N `stock_movements`, quando houver movimentação local de dispensação.
- `occurrences` 1:N `occurrence_items`.
- `dispensation_items` 1:N `occurrence_items`.
- `occurrences` 1:N `replacement_authorizations`.
- `replacement_authorizations` 1:N `dispensations`, quando uma autorização permitir mais de uma entrega ou recebimento parcial.

## 5. Regras de integridade e cálculos derivados

### 5.1. Necessidade atual

A necessidade não será armazenada como um valor fixo em `patients`.

Será calculada a partir do tratamento vigente e das associações entre tipos de insulina e modelos de caneta.

### 5.2. Posse utilizável

A posse utilizável será calculada por paciente e modelo, considerando:

1. Quantidades recebidas em `dispensation_items`.
2. Quantidades afetadas em `occurrence_items`.
3. Quantidades cujo prazo administrativo de três anos foi cumprido.

Uma quantidade com data de referência desconhecida não poderá ser considerada vencida automaticamente.

As quantidades históricas incompletas poderão compor a posse quando sua existência e condição utilizável forem conhecidas.

### 5.3. Elegibilidade

O prazo será calculado separadamente para cada item de dispensação, utilizando a data efetiva de recebimento.

Ao completar três anos, a quantidade remanescente daquele item deixará de compor a posse utilizável.

A nova dispensação terá seu próprio ciclo.

### 5.4. Estoque local

O saldo será derivado de `stock_movements`, agrupado por lote e modelo de caneta.

A aplicação deverá validar a disponibilidade antes de confirmar saídas e dispensações.

As operações deverão ocorrer em transações para impedir saldos inconsistentes.

### 5.5. Atendimento parcial

A quantidade necessária será calculada pelo sistema.

A quantidade efetivamente dispensada deverá respeitar o estoque disponível.

A diferença permanecerá como pendência de atendimento.

## 6. Índices e restrições recomendados

Além das chaves primárias e estrangeiras, deverão ser considerados:

- Índices únicos para CPF e CNS quando não nulos.
- Índice único parcial para um acompanhamento vigente por paciente.
- Índice único parcial para um tratamento vigente por paciente.
- Índice único parcial para identificar uma única instituição responsável pelo estoque local.
- Índice único para associações entre canetas e insulinas.
- Índice único para associações entre tratamentos e insulinas.
- Índice único para código de lote dentro de um modelo, quando informado.
- Índices para consultas por paciente, data, modelo, lote e instituição.
- Restrições `CHECK` para quantidades positivas e valores controlados de status e tipo de operação.
- Restrições para impedir autorreferência em unificações e correções.

As restrições que dependem de agregações, como impedir que ocorrências ultrapassem a quantidade ainda utilizável, deverão ser validadas pela aplicação dentro de transações.

## 7. Pontos de implementação

Os seguintes itens exigem detalhamento técnico durante a implementação, mas não impedem o início da construção do banco:

1. Definir a regra determinística de alocação quando uma ocorrência não puder ser associada a uma dispensação específica informada pelo paciente.
2. Definir os códigos controlados de motivos de inativação, reativação, ocorrência e ajuste.
3. Definir o mecanismo de estorno e retificação das diferentes operações, preservando os registros originais.
4. Definir a forma de armazenar ou referenciar prescrições, Boletins de Ocorrência e autorizações estaduais.
5. Implementar e testar índices parciais e restrições específicas do SQLite.
6. Implementar consultas ou visões para necessidade, posse utilizável, elegibilidade, estoque e classificação do atendimento.

Esses detalhes deverão ser resolvidos sem alterar as regras de domínio já estabelecidas.

---

**Documento complementar:** as regras de negócio e os conceitos representados neste modelo estão descritos em `domain-model.md`.