# CNT Gestor — Modelo de Domínio

## 1. Objetivo e escopo

O CNT Gestor é um sistema para controle administrativo de estoque, movimentações, dispensações e acompanhamento de pacientes que utilizam canetas reutilizáveis de insulina.

O sistema contempla:

- Cadastro e acompanhamento de pacientes.
- Cadastro de tipos de insulina e canetas reutilizáveis.
- Associação entre canetas e tipos de insulina compatíveis.
- Histórico de tratamentos dos pacientes.
- Controle de estoque por lote.
- Registro de entradas, saídas, transferências e ajustes de estoque.
- Registro de dispensações realizadas pela UBS e por outras instituições.
- Controle da quantidade de canetas em posse dos pacientes.
- Registro de perdas, danos e substituições.
- Controle do prazo administrativo para nova dispensação.
- Acompanhamento contínuo das necessidades e do atendimento dos pacientes.
- Histórico das operações e alterações realizadas.

O controle abrange exclusivamente as canetas aplicadoras reutilizáveis. O estoque de insulinas, refis, agulhas e outros materiais não faz parte do escopo.

As canetas serão controladas por quantidade, sem identificação individual das unidades físicas.

## 2. Tipos de insulina e canetas

O sistema deverá permitir o cadastro de diferentes tipos de insulina e modelos de caneta, possibilitando a inclusão de novos registros sem depender exclusivamente dos modelos inicialmente utilizados.

### 2.1. Modelos iniciais

Existem inicialmente dois modelos físicos:

| Modelo de caneta | Insulinas compatíveis |
|---|---|
| NPH/Regular | NPH e Regular |
| Glargina/Lantus | Glargina |

NPH e Regular utilizam o mesmo modelo físico de caneta. Quando ambas estiverem registradas para um paciente, serão necessárias duas unidades desse modelo.

### 2.2. Cálculo da quantidade necessária

A quantidade necessária de cada modelo será calculada conforme os tipos de insulina registrados no tratamento vigente do paciente e suas respectivas associações com as canetas compatíveis.

| Insulinas utilizadas | NPH/Regular | Glargina/Lantus |
|---|---:|---:|
| NPH | 1 | 0 |
| Regular | 1 | 0 |
| NPH + Regular | 2 | 0 |
| Glargina | 0 | 1 |
| Glargina + Regular | 1 | 1 |

A tabela representa a configuração inicial do sistema. A estrutura deverá permitir o cadastro de novos tipos de insulina e canetas.

## 3. Conceitos do domínio

### 3.1. Paciente

Pessoa cadastrada no sistema para acompanhamento das necessidades e controle das dispensações de canetas.

O cadastro deverá conter:

- Nome.
- Data de nascimento.
- CPF.
- CNS.

O paciente possui histórico de tratamentos, dispensações, ocorrências e movimentações de posse.

O sistema deverá distinguir a situação cadastral do paciente de seu vínculo de acompanhamento pela unidade.

**Situação cadastral:**
- Ativo.
- Inativo.

**Vínculo de acompanhamento:**
- Acompanhado pela unidade.
- Não acompanhado pela unidade.

O encerramento do acompanhamento não implica a exclusão do paciente nem de seu histórico. O paciente poderá continuar possuindo canetas mesmo após deixar de ser acompanhado pela UBS ou pelo município.

Caso retorne ao acompanhamento, seu vínculo poderá ser reativado sem perda das informações anteriores.

O sistema deverá registrar as datas e os motivos de encerramento e retomada do acompanhamento.

### 3.2. Tipo de insulina

Representa um tipo de insulina utilizado nos tratamentos registrados no sistema.

Os tipos de insulina serão cadastrados independentemente das canetas, permitindo que novas opções sejam adicionadas futuramente.

### 3.3. Caneta

Representa um produto ou modelo de caneta reutilizável controlado pelo sistema.

O cadastro deverá contemplar:

- Identificação.
- Marca.
- Tipos de insulina compatíveis.
- Situação ativa ou inativa.

Uma caneta poderá ser compatível com mais de um tipo de insulina.

A associação entre tipos de insulina e canetas será utilizada no cálculo da quantidade necessária para cada paciente.

### 3.4. Tratamento

Representa os tipos de insulina prescritos para um paciente durante determinado período.

O sistema deverá preservar o histórico das alterações de tratamento.

Cada registro deverá conter:

- Paciente.
- Tipos de insulina prescritos.
- Data de início da vigência.
- Data de término da vigência, quando aplicável.
- Médico responsável pela prescrição.
- Identificação do médico: nome, CRM e UF.
- Operador responsável pelo registro.
- Data e hora do registro no sistema.
- Observação, quando necessária.

O tratamento vigente será utilizado para calcular a necessidade atual de canetas.

Toda alteração deverá ocorrer mediante apresentação de receita que identifique o médico prescritor.

A data de início da vigência deverá representar quando o tratamento passou a valer, independentemente da data em que a alteração foi cadastrada no sistema.

Os tratamentos anteriores deverão permanecer disponíveis para consulta.

O armazenamento de imagens ou arquivos das receitas poderá ser avaliado em uma etapa futura.

### 3.5. Lote

Representa um lote de fabricação de determinado modelo de caneta.

Cada lote está associado a uma caneta e possui:

- Código de identificação.
- Data de fabricação, quando disponível.
- Validade do fabricante, quando aplicável.

Um mesmo lote poderá ser recebido em diferentes entregas pela UBS.

A quantidade recebida não deverá ser armazenada como atributo definitivo do lote, pois cada recebimento representa uma operação independente.

### 3.6. Movimentação de estoque

Representa uma alteração na quantidade de canetas disponíveis no estoque da UBS.

O controle será realizado por caneta e lote.

As movimentações deverão contemplar:

**Entradas:**
- Recebimento de fornecedor, CAF ou Estado.
- Recebimento por transferência de outra instituição.

**Saídas:**
- Dispensação ao paciente.
- Transferência para outra UBS ou instituição.

**Ajustes:**
- Perdas.
- Avarias.
- Divergências de inventário.
- Correções de registros.

Cada movimentação deverá preservar a identificação do lote, a quantidade, a data, o tipo de operação e o operador responsável.

Nas transferências, deverá ser identificada a instituição de origem ou destino, conforme a operação.

Os ajustes de estoque exigirão justificativa obrigatória e identificação do operador responsável. Não haverá exigência de aprovação por um segundo responsável.

Correções não deverão apagar ou sobrescrever silenciosamente movimentações anteriores.

### 3.7. Entrada de estoque

Representa o recebimento de determinada quantidade de canetas de um lote.

Cada entrada deverá possuir registro próprio, contendo:

- Lote.
- Quantidade recebida.
- Data de entrada.
- Origem ou fornecedor.
- Responsável pelo registro.

Um mesmo lote poderá possuir várias entradas independentes.

### 3.8. Dispensação

Representa a entrega de uma ou mais canetas a um paciente.

Uma dispensação poderá conter diferentes modelos de caneta e diferentes lotes.

O registro principal deverá conter:

- Paciente.
- Data efetiva da dispensação.
- Origem da dispensação.
- Responsável pelo registro.
- Motivo, quando aplicável.
- Data e hora do registro no sistema.

Cada item da dispensação deverá conter:

- Modelo de caneta.
- Lote, quando identificado.
- Quantidade dispensada.

As dispensações realizadas pela UBS deverão obrigatoriamente identificar o lote e movimentar o estoque local.

As dispensações realizadas por outras instituições deverão ser registradas no histórico do paciente, sem alterar o estoque da UBS.

Quando disponível, o lote das dispensações externas também poderá ser informado.

A origem deverá permitir identificar a instituição responsável, incluindo a própria UBS, outras UBS, CAF, Estado, outro município ou outras instituições pertinentes.

O sistema deverá permitir registros retroativos, preservando a diferença entre a data efetiva da dispensação e a data de lançamento no sistema.

Quando a data efetiva for desconhecida, não deverá ser inventada uma data para cálculo do prazo administrativo.

### 3.9. Ocorrência

Representa uma perda ou dano de canetas em posse de um paciente.

O registro deverá conter:

- Paciente.
- Modelo de caneta.
- Quantidade afetada.
- Tipo de ocorrência.
- Data da ocorrência.
- Lote, quando identificado.
- Informações pertinentes à documentação apresentada.
- Operador responsável.
- Data e hora do registro.

Conforme o procedimento operacional adotado pela UBS, perdas ou danos ocorridos antes do término do prazo administrativo de três anos exigem apresentação de Boletim de Ocorrência (BO) para solicitação de reposição ao Estado.

O sistema deverá apresentar, durante o registro da ocorrência, os lotes que possuem saldo atribuído ao paciente para o modelo selecionado.

O operador poderá selecionar um ou mais lotes e informar a quantidade afetada em cada um.

A quantidade informada não poderá ultrapassar o saldo disponível do lote para aquele paciente.

Quando não for possível identificar o lote, a ocorrência poderá ser registrada sem essa informação. Nessa situação, deverá ser utilizada uma regra de alocação alternativa, ainda a ser detalhada.

As ocorrências reduzem a quantidade de canetas utilizáveis em posse do paciente e permanecem no histórico.

### 3.10. Reposição

Representa o recebimento de novas canetas pelo paciente em decorrência de perda, dano ou outra situação que exija substituição.

A ocorrência e a reposição serão registros independentes.

A ocorrência não deverá gerar automaticamente uma reposição.

Quando o Estado fornecer uma nova caneta, ela será registrada como uma nova dispensação, com origem identificada como Estado.

A reposição não movimentará o estoque da UBS.

Cada nova dispensação terá sua própria data de referência para cálculo do prazo administrativo.

## 4. Regras de negócio

### 4.1. Necessidade e posse do paciente

O sistema deverá manter separadas as seguintes informações:

**Necessidade atual:**

Quantidade de canetas exigida pelo tratamento vigente, calculada conforme os tipos de insulina utilizados e suas associações com os modelos de caneta.

**Posse registrada:**

Quantidade de canetas atribuída ao paciente, considerando as dispensações e ocorrências registradas.

**Posse ativa:**

Quantidade que permanece atribuída ao paciente e ainda é considerada utilizável para fins de controle administrativo.

**Quantidade elegível:**

Quantidade que cumpriu o prazo administrativo de três anos e pode ser considerada para nova dispensação, conforme a necessidade atual.

Essas informações deverão ser calculadas separadamente.

A necessidade não deverá ser armazenada como um valor fixo no cadastro do paciente, pois depende do tratamento vigente e das associações entre insulinas e canetas.

### 4.2. Alterações de tratamento

Uma alteração no tratamento deverá atualizar a necessidade calculada do paciente.

As dispensações anteriores e a posse histórica deverão ser preservadas.

A alteração do tratamento não deverá apagar, devolver ou modificar automaticamente as canetas anteriormente dispensadas.

Canetas de modelos que deixaram de ser necessários permanecerão registradas na posse do paciente, respeitando seu prazo administrativo e eventuais ocorrências.

### 4.3. Controle da posse por lote e dispensação

O saldo de posse será calculado a partir das dispensações e ocorrências.

Sempre que possível, a quantidade em posse deverá permanecer associada ao lote e à dispensação de origem.

Isso permitirá identificar quais quantidades foram recebidas, quando foram dispensadas e quais foram afetadas por perdas, danos ou pelo término do prazo administrativo.

Quando o lote não estiver identificado, o sistema deverá utilizar uma regra alternativa de alocação cronológica entre as dispensações com saldo disponível.

### 4.4. Controle de estoque

O estoque será controlado por caneta e lote.

Toda entrada, saída ou ajuste deverá gerar uma movimentação correspondente.

A quantidade disponível de cada lote deverá refletir as movimentações registradas.

As operações de transferência deverão permitir registrar entradas e saídas entre instituições.

A devolução de canetas por pacientes não será prevista como operação normal, pois uma vez dispensadas, as canetas não retornam ao estoque da unidade.

A validade do fabricante é independente do prazo administrativo de dispensação ao paciente.

### 4.5. Prazo administrativo de dispensação

A regra operacional da UBS estabelece um intervalo de três anos para a substituição regular de canetas.

O prazo será contado a partir da data efetiva da dispensação.

O cálculo deverá ocorrer individualmente para cada quantidade dispensada, considerando seu respectivo registro de origem.

Dispensações realizadas em datas diferentes deverão manter seus prazos independentes, mesmo quando referentes ao mesmo paciente e modelo.

A ocorrência de perda ou dano deverá reduzir a quantidade ainda atribuída à dispensação correspondente.

Quando uma quantidade completar três anos, passará a ser considerada não utilizável para fins do controle administrativo e deixará de compor a posse ativa do paciente.

O registro histórico deverá permanecer preservado.

A nova dispensação, quando realizada, iniciará seu próprio prazo de três anos.

O sistema deverá atualizar automaticamente a elegibilidade de cada quantidade e apresentar alertas aos operadores sobre pacientes com quantidades elegíveis.

A elegibilidade não implica dispensação automática. A necessidade atual do tratamento também deverá ser considerada.

Quando a data efetiva de uma dispensação anterior não estiver disponível, o prazo correspondente não poderá ser determinado até que a informação seja obtida.

A alteração das insulinas registradas poderá gerar necessidade de outro modelo de caneta, cujo controle deverá considerar o histórico de dispensações daquele modelo.

### 4.6. Perda, dano e substituição

Perdas e danos reduzem a posse ativa do paciente.

A solicitação de reposição ao Estado não deverá ser confundida com a reposição efetivamente recebida.

Quando uma reposição acontecer, deverá ser registrada como nova dispensação, preservando a ocorrência original.

A substituição de quantidades que cumpriram o prazo administrativo também deverá ser registrada como nova dispensação, mantendo o histórico da quantidade anterior como não utilizável.

### 4.7. Dispensações parciais e atendimento

O sistema deverá permitir dispensações parciais quando o estoque disponível for inferior à quantidade necessária e elegível para atendimento.

Deverão ser registradas apenas as quantidades efetivamente dispensadas.

O sistema deverá atualizar o estoque e a posse do paciente conforme a quantidade entregue.

A quantidade restante deverá continuar identificada como necessidade pendente de atendimento.

O prazo administrativo de três anos será iniciado somente para as quantidades efetivamente dispensadas.

### 4.8. Acompanhamento contínuo dos pacientes

O sistema deverá manter acompanhamento contínuo das necessidades e do atendimento dos pacientes, sem depender de fechamentos mensais.

Os indicadores deverão ser atualizados conforme ocorram alterações de tratamento, dispensações, ocorrências, vencimentos administrativos e mudanças no vínculo de acompanhamento.

O sistema deverá permitir identificar, entre os pacientes acompanhados pela unidade:

- Pacientes com necessidade integralmente atendida.
- Pacientes que precisam receber canetas, mas ainda não receberam nenhuma quantidade elegível.
- Pacientes parcialmente atendidos.
- Pacientes sem necessidade pendente de atendimento.

A classificação deverá considerar a necessidade atual, a posse ativa e a quantidade elegível, evitando confundir pacientes que possuem canetas dentro do prazo administrativo com pacientes que precisam receber novas unidades.

Também deverão ser disponibilizados indicadores de quantidade de canetas necessárias, dispensadas e pendentes, separados por modelo.

Os pacientes não acompanhados pela unidade não deverão ser contabilizados como pendências de atendimento local, embora seu histórico e sua posse continuem registrados.

### 4.9. Encerramento e retomada do acompanhamento

O paciente poderá deixar de ser acompanhado pela unidade sem que seu cadastro seja excluído ou seu saldo de canetas seja zerado.

O encerramento do acompanhamento deverá registrar data e motivo.

A posse e o histórico de dispensações continuarão preservados, inclusive quando houver dispensações realizadas por outras instituições.

O acompanhamento poderá ser retomado posteriormente, sem perda do histórico.

A inativação cadastral será independente do encerramento do acompanhamento. Pacientes que deixarem de utilizar insulina, falecerem ou tiverem outra situação que justifique a inativação poderão permanecer registrados para fins históricos.

## 5. Histórico e rastreabilidade

As operações deverão preservar o histórico de movimentações e alterações realizadas.

O sistema deverá permitir consultar:

- Entradas e saídas de estoque.
- Transferências entre instituições.
- Ajustes de estoque e respectivas justificativas.
- Dispensações por paciente, modelo, lote, origem e período.
- Histórico de tratamentos e suas alterações.
- Médico prescritor e operador responsável pelas alterações de tratamento.
- Quantidades historicamente recebidas por paciente.
- Quantidades em posse ativa.
- Quantidades não utilizáveis por prazo administrativo cumprido.
- Ocorrências de perda ou dano.
- Reposições realizadas.
- Situação de acompanhamento dos pacientes.
- Elegibilidade para nova dispensação.

Os registros históricos não deverão ser apagados ou sobrescritos de maneira que comprometa a rastreabilidade.

Correções deverão preservar o registro da operação original e permitir identificar a alteração realizada.

O sistema deverá distinguir a data em que uma operação efetivamente ocorreu da data em que foi registrada.

## 6. Limites do sistema

O CNT Gestor é destinado ao controle administrativo de estoque, movimentações, dispensações e acompanhamento da posse e das necessidades de canetas reutilizáveis.

Não fazem parte do escopo:

- Controle de estoque de insulinas, refis ou agulhas.
- Identificação individual de cada caneta física.
- Controle do conteúdo ou utilização dos refis.
- Registro de aplicações de insulina.
- Prescrição ou decisão clínica sobre o tratamento.
- Avaliação da adequação clínica de tratamentos.
- Substituição dos procedimentos e responsabilidades dos profissionais de saúde.

## 7. Decisões pendentes de detalhamento

Os seguintes pontos ainda precisam ser definidos antes da consolidação do modelo de dados:

1. **Compatibilidade entre insulinas e canetas:** definir a regra de cálculo caso um mesmo tipo de insulina seja compatível com mais de um modelo de caneta.
2. **Ocorrências sem identificação de lote:** detalhar a regra de alocação cronológica das quantidades afetadas quando o paciente não souber informar o lote.
3. **Lotes de dispensações externas:** definir como registrar a identificação de lotes que não pertencem ao estoque local da UBS.
4. **Classificação de atendimento:** detalhar os critérios de classificação e os indicadores do painel, inclusive para pacientes sem necessidade pendente.
5. **Registros de dispensações antigas:** definir como tratar quantidades históricas cuja data de dispensação ou lote não estejam disponíveis.
6. **Transferências:** detalhar os dados e procedimentos de registro das instituições de origem e destino.
7. **Ajustes de estoque:** detalhar as categorias, os motivos e os procedimentos específicos para cada tipo de ajuste.

Esses pontos não impedem a definição conceitual das entidades principais, mas deverão ser resolvidos antes ou durante a elaboração do modelo relacional.

---

**Documento de referência:** este modelo descreve os conceitos e as regras de negócio do CNT Gestor. A estrutura de tabelas, atributos técnicos, chaves, restrições e relacionamentos do banco de dados será detalhada posteriormente no documento `data-model.md`.