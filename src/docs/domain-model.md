# CNT Gestor — Modelo de Domínio

## 1. Objetivo e escopo

O CNT Gestor é um sistema para controle de estoque, movimentações e dispensação de canetas reutilizáveis de insulina em uma Unidade Básica de Saúde (UBS).

O sistema contempla:

- Cadastro de pacientes.
- Cadastro de modelos de caneta.
- Controle de estoque por lote.
- Registro de dispensações.
- Controle da quantidade de canetas em posse dos pacientes.
- Registro de perdas, danos e reposições.
- Histórico de movimentações.

O controle abrange exclusivamente as canetas aplicadoras reutilizáveis. O estoque de insulina, refis, agulhas e outros materiais não faz parte do escopo.

As canetas serão controladas por quantidade, sem identificação individual das unidades físicas.

## 2. Modelos de caneta

Existem inicialmente dois modelos físicos:

| Modelo | Insulinas compatíveis |
|---|---|
| NPH/Regular | NPH e Regular |
| Glargina/Lantus | Glargina |

NPH e Regular utilizam o mesmo modelo físico de caneta. Quando ambas estiverem registradas para um paciente, serão necessárias duas unidades desse modelo.

### 2.1. Quantidade necessária por tratamento

A quantidade necessária de cada modelo será calculada conforme as insulinas registradas para o paciente.

| Insulinas utilizadas | NPH/Regular | Glargina/Lantus |
|---|---:|---:|
| NPH | 1 | 0 |
| Regular | 1 | 0 |
| NPH + Regular | 2 | 0 |
| Glargina | 0 | 1 |
| Glargina + Regular | 1 | 1 |

## 3. Conceitos do domínio

### 3.1. Paciente

Pessoa cadastrada no sistema para controle das dispensações.

O paciente possui um histórico de dispensações e movimentações, além de um saldo atual de canetas por modelo físico.

### 3.2. Modelo de caneta

Representa um tipo de caneta reutilizável controlado pelo sistema.

Cada modelo possui sua identificação e as insulinas correspondentes para cálculo da quantidade necessária.

### 3.3. Lote

Representa um conjunto de canetas recebido pela UBS.

Cada lote está associado a um modelo de caneta e possui:

- Código de identificação.
- Quantidade recebida.
- Data de entrada.
- Validade do fabricante, quando aplicável.
- Origem ou fornecedor, quando disponível.

O estoque é controlado pela quantidade disponível em cada lote.

### 3.4. Movimentação de estoque

Representa uma alteração na quantidade de canetas disponíveis na UBS.

As movimentações incluem entradas e saídas, com identificação do lote, quantidade, data, tipo de operação e responsável pelo registro.

### 3.5. Dispensação

Representa a entrega de uma ou mais canetas a um paciente.

Cada registro deve conter:

- Paciente.
- Modelo de caneta.
- Quantidade.
- Data da dispensação.
- Origem (UBS ou Estado).
- Motivo.
- Lote de origem, quando fornecido pela UBS.
- Responsável pelo registro.

As dispensações realizadas pela UBS movimentam o estoque. As fornecidas pelo Estado são registradas no histórico do paciente, sem alterar o estoque da UBS.

### 3.6. Ocorrência

Representa uma perda ou dano de canetas em posse de um paciente.

O registro deve conter o paciente, o modelo, a quantidade afetada, o tipo de ocorrência, a data e as informações pertinentes à documentação apresentada.

As ocorrências alteram a quantidade de canetas utilizáveis em posse do paciente e devem permanecer no histórico.

## 4. Regras de negócio

### 4.1. Controle de quantidade

A quantidade atual em posse do paciente é controlada por modelo de caneta e resulta das dispensações e ocorrências registradas.

A quantidade necessária é calculada conforme as insulinas registradas e a tabela de modelos e quantidades definida neste documento.

A necessidade de dispensação corresponde à diferença entre a quantidade necessária e a quantidade utilizável em posse do paciente, quando esta for inferior àquela.

Canetas excedentes após uma alteração das insulinas registradas permanecem em posse do paciente e não retornam automaticamente ao estoque da UBS.

### 4.2. Controle de estoque

O estoque é controlado por modelo e lote.

Toda entrada ou saída deve gerar uma movimentação correspondente. A quantidade disponível de um lote deve refletir as movimentações registradas.

A validade do fabricante é independente do prazo administrativo de dispensação ao paciente.

### 4.3. Prazo administrativo de dispensação

A regra operacional da UBS estabelece um intervalo de três anos para a dispensação regular de novas canetas.

O prazo é contado a partir da data efetiva da dispensação e deve ser acompanhado por modelo, quantidade e registro de origem.

Dispensações realizadas em datas diferentes devem manter registros separados, mesmo quando forem referentes ao mesmo paciente e modelo.

Quando a data de uma dispensação anterior não estiver disponível, o prazo correspondente não poderá ser determinado até que a informação seja obtida.

A alteração das insulinas registradas pode gerar necessidade de outro modelo de caneta, cujo controle deve considerar o histórico de dispensações daquele modelo.

### 4.4. Perda, dano e reposição

Conforme o procedimento operacional adotado pela UBS, perdas ou danos ocorridos antes do término do prazo administrativo de três anos exigem apresentação de Boletim de Ocorrência (BO) para solicitação de reposição ao Estado.

A ocorrência deve registrar a quantidade afetada e reduzir o saldo de canetas utilizáveis em posse do paciente.

A reposição fornecida pelo Estado deve ser registrada como uma nova dispensação, com sua respectiva data e quantidade. Essa operação não movimenta o estoque da UBS.

## 5. Histórico e rastreabilidade

As movimentações devem preservar o histórico das operações realizadas.

O sistema deve permitir consultar:

- Entradas e saídas de estoque.
- Dispensações por paciente, modelo, lote e período.
- Quantidades atualmente em posse de cada paciente.
- Ocorrências de perda ou dano.
- Reposições fornecidas pelo Estado.

Os registros históricos não devem ser apagados ou sobrescritos de maneira que comprometa a rastreabilidade.

Correções devem preservar o registro da operação original e permitir identificar a alteração realizada.

## 6. Limites do sistema

O CNT Gestor é destinado ao controle administrativo de estoque, movimentações e dispensações de canetas reutilizáveis.

Não fazem parte do escopo:

- Controle de estoque de insulinas, refis ou agulhas.
- Identificação individual de cada caneta física.
- Controle do conteúdo ou utilização dos refis.
- Registro de aplicações de insulina.
- Prescrição ou acompanhamento clínico do tratamento.