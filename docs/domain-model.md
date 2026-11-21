# CNT Gestor — Modelo de Domínio

## 1. Objetivo e escopo

O CNT Gestor é um sistema para controle administrativo de estoque, movimentações, dispensações e acompanhamento das necessidades de pacientes que utilizam canetas aplicadoras reutilizáveis de insulina.

O sistema contempla:

- Cadastro e acompanhamento de pacientes.
- Cadastro de tipos de insulina e modelos de caneta.
- Associação entre modelos de caneta e tipos de insulina compatíveis.
- Histórico de tratamentos.
- Controle de estoque por lote.
- Registro de entradas, saídas e ajustes de estoque.
- Registro de dispensações realizadas pela UBS e por instituições externas.
- Controle da quantidade de canetas utilizáveis em posse dos pacientes.
- Registro de ocorrências que tornam quantidades não utilizáveis.
- Controle do prazo administrativo para substituição.
- Acompanhamento das necessidades e do atendimento dos pacientes.
- Histórico e rastreabilidade das operações.

O controle abrange exclusivamente as canetas aplicadoras reutilizáveis. Não fazem parte do escopo o estoque de insulinas, refis, agulhas ou outros materiais.

As canetas serão controladas por quantidade, sem identificação individual das unidades físicas.

### 1.1. Escopo da primeira versão

A primeira versão será utilizada por uma única UBS, que terá seu estoque local controlado pelo sistema.

Instituições externas poderão ser cadastradas para identificar origens de fornecimento ou destinos de saídas. Entretanto:

- Não haverá integração entre estoques de diferentes UBS.
- Uma saída destinada a outra instituição não gerará automaticamente uma entrada nessa instituição.
- Dispensações externas diretamente ao paciente serão registradas no histórico dele, sem movimentar o estoque local.
- O sistema não terá, nesta primeira versão, controle operacional independente de estoque de outras unidades.

## 2. Tipos de insulina e modelos de caneta

O sistema deverá permitir o cadastro de novos tipos de insulina e modelos de caneta, sem depender exclusivamente dos modelos inicialmente utilizados.

### 2.1. Modelos iniciais

| Modelo de caneta | Insulinas compatíveis |
|---|---|
| NPH/Regular | NPH e Regular |
| Glargina/Lantus | Glargina |

NPH e Regular utilizam o mesmo modelo físico de caneta. Quando ambas estiverem prescritas, serão necessárias duas unidades do modelo NPH/Regular.

### 2.2. Cálculo da necessidade

A quantidade necessária será calculada automaticamente com base nos tipos de insulina do tratamento vigente e nos modelos compatíveis.

| Tratamento prescrito | NPH/Regular | Glargina/Lantus |
|---|---:|---:|
| NPH | 1 | 0 |
| Regular | 1 | 0 |
| NPH + Regular | 2 | 0 |
| Glargina | 0 | 1 |
| Glargina + Regular | 1 | 1 |

A tabela representa a configuração inicial.

A necessidade atual deverá ser comparada com a quantidade de canetas utilizáveis que o paciente possui, considerando cada modelo separadamente.

A quantidade a dispensar será calculada pelo sistema. O operador não deverá definir livremente a necessidade do paciente.

O estoque disponível limita a quantidade que pode ser efetivamente entregue. Quando insuficiente, o sistema deverá permitir atendimento parcial e manter a quantidade restante como pendência.

## 3. Conceitos do domínio

### 3.1. Paciente

Pessoa cadastrada para controle das necessidades, posse e dispensações de canetas.

O cadastro deverá conter:

- Nome.
- Data de nascimento.
- CPF.
- CNS.

Pelo menos um entre CPF e CNS deverá ser informado. Os documentos deverão ser únicos quando presentes. A ausência de um documento será representada por valor nulo, nunca por texto vazio.

O cadastro da pessoa será único e independente da UBS de acompanhamento ou da instituição que realiza uma dispensação.

O sistema deverá distinguir:

- Situação cadastral.
- Acompanhamento territorial.
- Posse de canetas.
- Necessidade atual de canetas.

A situação cadastral poderá ser `active`, `inactive` ou `merged`.

Um paciente poderá estar ativo sem acompanhamento territorial vigente. Isso não apaga seu histórico nem sua posse.

### 3.2. Acompanhamento territorial

Representa o período em que o paciente está vinculado à área de uma UBS para fins de acompanhamento.

Cada período deverá registrar a UBS e as datas de início e término.

Regras:

- O paciente poderá ter, no máximo, um acompanhamento vigente.
- A mudança para outra UBS encerra o período anterior e inicia outro imediatamente.
- O encerramento do acompanhamento ocorre quando o paciente sai da área de cobertura da UBS.
- O retorno à mesma UBS cria um novo período; não reabre o anterior.
- O encerramento do acompanhamento não altera a posse nem o histórico de dispensações.
- Um paciente ativo poderá permanecer sem acompanhamento vigente.
- Pacientes sem acompanhamento não serão contabilizados como pendências de atendimento local.

O acompanhamento territorial não determina a instituição responsável por uma dispensação.

### 3.3. Tipo de insulina

Representa um tipo de insulina utilizado nos tratamentos registrados.

Os tipos serão cadastráveis e independentes dos modelos de caneta.

### 3.4. Modelo de caneta

Representa um modelo físico de caneta reutilizável.

O cadastro deverá contemplar identificação, marca, situação e associação com os tipos de insulina compatíveis.

A associação entre modelos e insulinas será utilizada no cálculo automático da necessidade.

### 3.5. Tratamento

Representa os tipos de insulina prescritos para o paciente durante determinado período.

Cada registro deverá conter:

- Paciente.
- Tipos de insulina prescritos.
- Data de início da vigência.
- Data de término, quando aplicável.
- Nome do médico prescritor.
- CRM e UF do prescritor.
- Operador responsável pelo registro.
- Data e hora do registro.
- Observação, quando necessária.

Toda alteração deverá ser realizada mediante apresentação de prescrição.

A data de início da vigência representa quando o tratamento passou a valer, independentemente da data do lançamento no sistema.

Os tratamentos anteriores deverão permanecer disponíveis para consulta.

O sistema registra informações administrativas da prescrição, mas não prescreve nem avalia a adequação clínica do tratamento.

### 3.6. Lote

Representa um lote de fabricação de determinado modelo de caneta.

Quando conhecido, deverá possuir código de identificação, modelo de caneta e validade do fabricante. A data de fabricação poderá ser registrada quando disponível.

Um mesmo lote poderá ser recebido em diferentes entregas.

A validade do fabricante é independente do prazo administrativo de três anos aplicado à posse do paciente.

### 3.7. Estoque e movimentação

O estoque local será controlado por modelo de caneta e lote.

Toda entrada, saída ou ajuste deverá gerar uma movimentação com:

- Tipo de operação.
- Lote.
- Quantidade.
- Data efetiva.
- Data e hora do registro.
- Operador responsável.
- Origem ou destino, quando aplicável.
- Justificativa, quando necessária.

As entradas poderão representar recebimentos de fornecedores, CAF, Estado ou outras instituições.

As saídas poderão representar dispensações a pacientes ou fornecimentos destinados a outras instituições.

Os ajustes poderão representar perdas, avarias, divergências de inventário ou correções.

Ajustes exigem justificativa e operador responsável. Não há exigência de aprovação por um segundo operador.

Correções não deverão apagar ou sobrescrever silenciosamente movimentações anteriores.

A quantidade disponível deverá refletir as movimentações registradas. Não será permitido concluir uma operação que resulte em estoque negativo.

### 3.8. Dispensação

Representa o recebimento de uma ou mais canetas por um paciente.

Uma dispensação poderá conter diferentes modelos e lotes.

O registro deverá identificar:

- Paciente.
- Instituição fornecedora.
- Data efetiva da dispensação ou recebimento, quando conhecida.
- Operador responsável pelo lançamento.
- Data e hora do lançamento.
- Itens, modelos, lotes quando conhecidos e quantidades.

As dispensações realizadas pela UBS:

- Deverão identificar o lote.
- Deverão movimentar o estoque local.
- Deverão registrar apenas as quantidades efetivamente entregues.

As dispensações realizadas por instituições externas:

- Deverão ser registradas no histórico do paciente.
- Deverão identificar a instituição fornecedora quando conhecida.
- Poderão registrar lote quando conhecido.
- Deverão permitir informar a data de recebimento.
- Não movimentarão o estoque local da UBS.

As origens poderão incluir a própria UBS, outras UBS, CAF, Estado, outro município ou outras instituições.

O sistema deverá permitir registros retroativos, preservando a diferença entre a data efetiva e a data do lançamento.

Quando a data efetiva for desconhecida, ela permanecerá nula. O sistema não deverá inventá-la.

### 3.9. Registros históricos incompletos

O sistema deverá permitir cadastrar quantidades recebidas anteriormente mesmo quando não houver informações completas.

Poderão ser registrados, no mínimo:

- Paciente.
- Modelo da caneta.
- Quantidade conhecida.
- Data, lote e instituição, quando conhecidos.

A ausência de informações deverá ser representada por valores nulos.

Quando houver apenas a informação de que o paciente possui determinada quantidade utilizável, essa quantidade deverá ser considerada no cálculo da posse.

Uma data desconhecida não poderá ser estimada pelo sistema. Consequentemente, o prazo administrativo daquela quantidade permanecerá indeterminado até que exista uma referência temporal confiável.

O registro histórico poderá ser complementado posteriormente, preservando a rastreabilidade da alteração.

### 3.10. Posse do paciente

A posse representa a quantidade de canetas atribuída ao paciente por dispensações internas, externas ou registros históricos.

A posse será calculada por modelo e, sempre que possível, por lote e dispensação de origem.

O sistema deverá distinguir:

- Quantidade historicamente recebida.
- Quantidade ainda utilizável.
- Quantidade afetada por ocorrências.
- Quantidade cujo prazo administrativo foi cumprido.
- Quantidade com elegibilidade temporal indeterminada.

Não haverá identificação individual das canetas.

O saldo utilizável será obtido a partir das quantidades recebidas, das ocorrências registradas e do prazo administrativo.

### 3.11. Ocorrência

Representa uma situação em que determinada quantidade de canetas deixa de ser utilizável pelo paciente.

O sistema não precisará distinguir operacionalmente canetas perdidas de canetas danificadas para o cálculo da posse. O que importa é se a quantidade continua utilizável.

O registro deverá conter:

- Paciente.
- Data da ocorrência, quando conhecida.
- Operador responsável.
- Data e hora do registro.
- Itens afetados e respectivas quantidades.
- Dispensação de origem de cada quantidade afetada.
- Observação ou referência documental, quando necessária.

Uma ocorrência poderá afetar quantidades de diferentes dispensações.

O operador deverá selecionar a dispensação de origem e informar a quantidade afetada. Não será necessário identificar cada caneta física.

A quantidade afetada não poderá superar o saldo utilizável daquela origem.

A ocorrência reduz a posse utilizável, mas não movimenta o estoque da UBS.

### 3.12. Reposição

Representa o recebimento de novas canetas após perda, dano ou cumprimento do prazo administrativo.

A ocorrência e a reposição serão registros independentes. Uma ocorrência não deverá gerar automaticamente uma dispensação.

A regra de fornecimento é:

| Situação | Responsável pelo fornecimento |
|---|---|
| Primeira dispensação | UBS |
| Substituição regular após três anos | UBS |
| Reposição antecipada por perda ou dano, com autorização exigida | Estado |

A reposição antecipada por perda ou dano deverá observar o procedimento de solicitação ao Estado e a documentação exigida, incluindo Boletim de Ocorrência conforme o procedimento operacional informado.

A autorização estadual deverá ser registrada e vinculada à ocorrência.

Quando o Estado fornecer a substituta:

- O recebimento será registrado como dispensação externa.
- A instituição fornecedora será identificada como Estado.
- A data de recebimento será registrada quando conhecida.
- Não haverá saída do estoque local da UBS.
- A nova quantidade terá seu próprio ciclo de elegibilidade.

A solicitação ou autorização não deverá ser confundida com o recebimento efetivo da reposição.

## 4. Regras de negócio

### 4.1. Necessidade e posse

A necessidade atual é calculada pelo tratamento vigente.

A posse utilizável é calculada a partir das dispensações e ocorrências, considerando o prazo administrativo.

A necessidade e a posse deverão ser comparadas separadamente por modelo de caneta.

A quantidade necessária para atendimento corresponde ao déficit entre a necessidade atual e a quantidade utilizável em posse.

A alteração do tratamento não apaga a posse anterior.

Canetas de modelos que deixaram de ser necessários permanecem no histórico e continuam sujeitas às regras de utilização e prazo.

Quando uma alteração de tratamento exigir um modelo diferente que o paciente não possua em quantidade suficiente, a necessidade desse novo modelo poderá ser atendida imediatamente, sem aguardar o ciclo de três anos do modelo anterior.

### 4.2. Prazo administrativo de três anos

O prazo administrativo de substituição é controlado por quantidade e por registro de dispensação, sem identificação individual das unidades físicas.

Cada quantidade dispensada terá sua própria referência temporal.

A data efetiva da dispensação ou do recebimento será utilizada como referência operacional para o cálculo do prazo.

Dispensações realizadas em datas diferentes terão ciclos independentes, mesmo quando referentes ao mesmo paciente e modelo.

Quando uma quantidade completar três anos:

- Deixará automaticamente de ser considerada utilizável.
- Deixará de compor a posse utilizável do paciente.
- Será considerada vencida para fins do controle administrativo.
- A necessidade de reposição será recalculada conforme o tratamento vigente.
- O registro histórico será preservado.

Essa regra representa o prazo administrativo de substituição, não uma afirmação sobre o estado físico da caneta.

Quando a data de recebimento for desconhecida, o sistema não poderá calcular o vencimento nem inventar uma referência temporal.

A elegibilidade não implica dispensação automática. A necessidade atual e a disponibilidade do estoque também deverão ser consideradas.

### 4.3. Ocorrências e reposições

Ocorrências reduzem a quantidade utilizável da dispensação de origem.

O prazo de três anos continuará associado à quantidade original e não será reiniciado por uma ocorrência.

Uma reposição efetivamente recebida será registrada como nova dispensação, com quantidade e referência temporal próprias.

A reposição antecipada por perda ou dano será fornecida pelo Estado mediante a autorização exigida. Não deverá ser registrada como saída do estoque da UBS.

### 4.4. Dispensações parciais

O sistema deverá calcular automaticamente a quantidade necessária.

Quando o estoque local não for suficiente para atender integralmente uma necessidade elegível, será permitida a dispensação parcial.

Somente a quantidade efetivamente entregue será registrada como dispensada.

A quantidade restante continuará pendente.

O prazo administrativo começará somente para a quantidade efetivamente recebida pelo paciente.

### 4.5. Controle de estoque

O estoque será calculado a partir das movimentações registradas por modelo e lote.

Uma movimentação deverá identificar operador responsável, data efetiva e data de registro.

Ajustes exigem justificativa obrigatória e preservação do histórico.

A saída destinada a outra instituição não gera automaticamente uma entrada em outro estoque.

A primeira versão não terá integração entre unidades.

A devolução de canetas por pacientes não será prevista como operação normal.

### 4.6. Classificação do atendimento

O sistema deverá permitir identificar, entre os pacientes acompanhados pela UBS:

- Pacientes com necessidade integralmente atendida.
- Pacientes com necessidade pendente e sem atendimento.
- Pacientes parcialmente atendidos.
- Pacientes sem necessidade pendente.

A classificação deverá considerar o tratamento vigente, a posse utilizável e as quantidades efetivamente dispensadas.

Pacientes sem acompanhamento vigente não serão contabilizados como pendências locais, embora seu histórico permaneça disponível.

Os indicadores deverão apresentar quantidades necessárias, dispensadas e pendentes por modelo.

### 4.7. Inativação cadastral

A inativação cadastral é independente do encerramento do acompanhamento territorial.

A inativação deverá registrar motivo controlado, operador, data efetiva e data/hora do registro. Quando o motivo for `other`, será obrigatória uma descrição.

A inativação deverá encerrar automaticamente o acompanhamento territorial vigente.

O paciente inativo não poderá receber novas dispensações nem realizar operações normais no sistema.

A inativação não apagará histórico nem gerará devolução automática de canetas ao estoque.

### 4.8. Falecimento

O falecimento deverá possuir procedimento próprio.

O registro deverá preservar:

- Data do óbito, quando conhecida.
- Data e hora do registro.
- Operador responsável.
- Motivo de alteração cadastral correspondente a falecimento.

O paciente passará à situação inativa, terá o acompanhamento vigente encerrado e ficará impedido de novas operações.

O falecimento não gera devolução automática de canetas ao estoque.

Um registro equivocado de falecimento exigirá correção formal e rastreável. Não deverá ser tratado como reativação cadastral comum.

### 4.9. Reativação cadastral

Somente pacientes inativos poderão ser reativados pelo procedimento normal.

A reativação deverá:

- Exigir justificativa controlada.
- Exigir descrição quando o motivo for `other`.
- Identificar o operador e o momento do registro.
- Exigir a indicação da UBS de acompanhamento.
- Criar um novo período de acompanhamento.
- Preservar os períodos anteriores.
- Ser executada de maneira atômica.

Cadastros incorporados por unificação não poderão ser reativados.

Pacientes inativados por falecimento não poderão ser reativados pelo fluxo normal.

### 4.10. Unificação de cadastros

A unificação será permitida somente entre cadastros ativos que tenham sido confirmados como pertencentes à mesma pessoa.

O procedimento deverá:

- Exigir confirmação explícita da identidade.
- Permitir escolher o cadastro principal.
- Apresentar resumo dos dados e históricos envolvidos antes da confirmação.
- Preservar a origem dos registros históricos.
- Ser executado de maneira atômica.
- Marcar o cadastro incorporado como `merged`.
- Fazer o cadastro incorporado apontar para o cadastro principal.
- Impedir novas operações no cadastro incorporado, mantendo-o consultável.

Cadastros inativos deverão ser avaliados e regularizados antes de uma eventual unificação. Um cadastro com falecimento registrado não poderá ser reativado para viabilizar a unificação.

## 5. Histórico e rastreabilidade

As operações deverão preservar a diferença entre a data efetiva do evento e a data em que ele foi registrado.

Toda movimentação de estoque deverá identificar o operador responsável.

O sistema deverá permitir consultar:

- Entradas, saídas e ajustes de estoque.
- Origem ou destino das movimentações.
- Dispensações por paciente, modelo, lote, instituição e período.
- Dispensações externas e registros históricos.
- Tratamentos e alterações.
- Médico prescritor e operador responsável pelo registro.
- Quantidades recebidas, utilizáveis, afetadas por ocorrências e vencidas.
- Ocorrências e autorizações de reposição.
- Reposições efetivamente recebidas.
- Acompanhamento territorial.
- Alterações de situação cadastral.
- Unificações de cadastro.
- Elegibilidade para nova dispensação.

Correções deverão preservar o registro original e permitir identificar o que foi corrigido, por quem e quando.

## 6. Limites do sistema

Não fazem parte do escopo:

- Controle de estoque de insulinas, refis ou agulhas.
- Identificação individual de cada caneta física.
- Controle do conteúdo ou utilização dos refis.
- Registro de aplicações de insulina.
- Prescrição ou decisão clínica sobre o tratamento.
- Avaliação da adequação clínica dos tratamentos.
- Substituição dos procedimentos e responsabilidades dos profissionais de saúde.
- Integração de estoques de múltiplas UBS na primeira versão.

## 7. Pontos de implementação que exigem detalhamento técnico

Os seguintes pontos não reabrem decisões de negócio já tomadas. São detalhes técnicos a serem definidos durante a implementação:

1. **Alocação de ocorrências sem identificação do lote:** quando houver mais de uma origem possível e não for possível identificar a dispensação exata, definir uma regra determinística de alocação entre os saldos disponíveis. O registro deverá preservar que a origem exata era desconhecida.
2. **Compatibilidade futura:** definir como o cadastro e o cálculo tratarão um tipo de insulina compatível com mais de um modelo de caneta. A configuração inicial permanece a descrita na seção 2.
3. **Classificação e indicadores:** transformar as categorias já definidas em consultas e critérios técnicos, sem alterar as regras de necessidade e posse.
4. **Correções de operações:** detalhar os mecanismos de estorno ou retificação que preservem os registros originais.
5. **Documentos:** avaliar armazenamento de referências ou arquivos de prescrições, Boletins de Ocorrência e autorizações estaduais.
6. **Restrições do SQLite:** implementar e testar integridade referencial, unicidade, transações e índices parciais necessários.

---

**Documento de referência:** este modelo descreve os conceitos e as regras de negócio do CNT Gestor. A estrutura de tabelas, atributos, chaves, restrições e relacionamentos será detalhada em `data-model.md`.