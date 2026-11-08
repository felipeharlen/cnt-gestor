# CNT Gestor — Modelo de Domínio

## 1. Objetivo e Escopo

O CNT Gestor é um sistema destinado ao controle administrativo de canetas aplicadoras reutilizáveis de insulina, abrangendo o gerenciamento de estoque, lotes, movimentações, dispensações e acompanhamento da posse desses dispositivos pelos pacientes.

O sistema deverá permitir:

- Cadastrar e consultar pacientes.
- Registrar períodos de acompanhamento territorial.
- Registrar os tratamentos prescritos aos pacientes.
- Determinar a necessidade de canetas com base nos tipos de insulina prescritos.
- Controlar modelos de canetas e suas compatibilidades com os tipos de insulina.
- Controlar entradas, saídas e transferências de estoque por lote.
- Registrar dispensações realizadas por diferentes instituições.
- Acompanhar as quantidades de canetas em posse dos pacientes.
- Registrar perdas, danos e outras ocorrências.
- Controlar a elegibilidade administrativa para substituição de canetas.
- Preservar o histórico das operações e alterações realizadas.

### 1.1 Limites do escopo

O sistema controla exclusivamente as canetas aplicadoras reutilizáveis.

Não fazem parte do escopo:

- Controle de estoque de insulina.
- Controle de refis de insulina.
- Controle de agulhas.
- Controle de outros materiais ou insumos.

O sistema não deverá tomar decisões clínicas nem substituir a avaliação dos profissionais responsáveis pela prescrição.

Sua função é registrar e organizar informações administrativas necessárias ao controle das canetas.

## 2. Tipos de Insulina e Modelos de Caneta

O sistema deverá permitir o cadastro de diferentes tipos de insulina e modelos de caneta, mantendo uma relação de compatibilidade entre eles.

Essa relação será utilizada para determinar quais modelos de caneta atendem aos tratamentos prescritos.

### 2.1 Modelos iniciais

Os modelos inicialmente considerados são:

| Modelo de caneta | Tipos de insulina compatíveis |
|---|---|
| NPH/Regular | NPH e Regular |
| Glargina/Lantus | Glargina |

Os nomes representam modelos de caneta, não tipos de insulina.

### 2.2 Cálculo da necessidade de canetas

A necessidade será determinada com base nos tipos de insulina presentes no tratamento vigente.

As regras iniciais são:

| Tratamento prescrito | Necessidade de canetas |
|---|---|
| NPH | 1 NPH/Regular |
| Regular | 1 NPH/Regular |
| NPH + Regular | 2 NPH/Regular |
| Glargina | 1 Glargina/Lantus |
| Glargina + Regular | 1 Glargina/Lantus + 1 NPH/Regular |

O uso simultâneo de NPH e Glargina não faz parte das combinações consideradas válidas no modelo inicial.

O cadastro de novos tipos de insulina e modelos de caneta deverá ser possível sem exigir alterações estruturais nas regras gerais do sistema.

A associação entre tipos de insulina e modelos de caneta deverá ser cadastrável, permitindo ampliar as combinações compatíveis.

## 3. Conceitos do Domínio

### 3.1 Paciente

Representa a pessoa que utiliza ou utilizou canetas aplicadoras de insulina.

Cada pessoa deverá possuir um único cadastro no sistema, independentemente da UBS responsável pelo acompanhamento ou da instituição que realizou uma dispensação.

O cadastro deverá contemplar, no mínimo:

- Nome.
- Data de nascimento.
- CPF.
- CNS.

Pelo menos um dos documentos, CPF ou CNS, deverá estar informado. Ambos poderão ser cadastrados quando disponíveis.

Os documentos deverão identificar o paciente de forma única quando preenchidos. A inclusão posterior de um CPF, por exemplo, não deverá gerar um novo cadastro nem comprometer o histórico anteriormente associado ao CNS.

O cadastro do paciente deverá ser independente de seu acompanhamento territorial e de sua situação cadastral atual.

Um paciente poderá continuar cadastrado mesmo quando não estiver sendo acompanhado por uma UBS da rede, preservando seu histórico de tratamentos, dispensações, ocorrências e posse de canetas.

### 3.2 Situação cadastral do paciente

A situação cadastral representa a condição administrativa atual do registro do paciente.

O sistema deverá utilizar três situações:

- **Ativo (`active`):** cadastro válido e habilitado para operações compatíveis com as demais regras do sistema.
- **Inativo (`inactive`):** cadastro temporariamente ou definitivamente inabilitado para novas operações.
- **Incorporado (`merged`):** cadastro duplicado que foi incorporado a outro cadastro pertencente à mesma pessoa.

A situação cadastral não deverá ser confundida com o acompanhamento territorial.

Um paciente ativo poderá estar sem acompanhamento territorial vigente, por exemplo, quando mudar para fora da área de cobertura da rede.

Um paciente inativo não poderá possuir acompanhamento territorial vigente.

Um cadastro incorporado não poderá ser utilizado para novas operações. Ele deverá permanecer consultável e direcionar consultas futuras ao cadastro principal.

### 3.3 Acompanhamento territorial

Representa o vínculo de um paciente com a UBS responsável por seu acompanhamento territorial durante determinado período.

O acompanhamento territorial deverá ser registrado por períodos históricos.

Um paciente residente na área de cobertura de determinada UBS deverá permanecer acompanhado por ela enquanto residir naquela área.

Quando o paciente mudar para fora da área de cobertura da UBS, o acompanhamento vigente deverá ser encerrado.

Se a mudança ocorrer para a área de outra UBS, deverá ser criado um novo período de acompanhamento para essa instituição, mesmo que ainda não tenha ocorrido atendimento ou dispensação.

Se o paciente retornar posteriormente à área de uma UBS com a qual já teve vínculo, deverá ser criado um novo período de acompanhamento. Períodos encerrados não deverão ser reabertos.

O encerramento do acompanhamento territorial não implica inativação do cadastro do paciente.

O acompanhamento territorial também não determina qual instituição poderá realizar uma dispensação. Uma instituição diferente da UBS responsável pelo acompanhamento poderá realizar a entrega de canetas.

### 3.4 Tipo de insulina

Representa cada tipo de insulina utilizado nos tratamentos dos pacientes.

O sistema deverá permitir o cadastro e a manutenção de diferentes tipos de insulina, sem limitar sua estrutura aos tipos inicialmente considerados.

A compatibilidade com os modelos de caneta deverá ser definida por uma associação cadastrável.

### 3.5 Modelo de caneta

Representa o modelo de caneta aplicadora reutilizável.

O controle será realizado por modelo, lote e quantidade, não por identificação individual de cada unidade física.

Um modelo poderá ser compatível com um ou mais tipos de insulina.

O sistema deverá permitir o cadastro de novos modelos e suas respectivas compatibilidades.

### 3.6 Tratamento

Representa o conjunto de tipos de insulina prescritos a um paciente durante determinado período.

O tratamento deverá manter seu histórico, permitindo identificar quais tipos de insulina foram prescritos em cada período.

Cada alteração deverá ser fundamentada em uma nova prescrição.

O registro deverá contemplar:

- Tipos de insulina prescritos.
- Data de início da vigência.
- Data de encerramento, quando aplicável.
- Identificação do médico prescritor, incluindo nome, CRM e UF.
- Operador responsável pelo registro.
- Data e horário do registro.

O sistema não deverá decidir qual tratamento é clinicamente adequado. Sua responsabilidade será registrar a prescrição e utilizar os tipos de insulina informados para calcular a necessidade administrativa de canetas.

### 3.7 Lote

Representa o lote de fabricação de determinado modelo de caneta.

O controle de estoque deverá identificar o modelo, o lote e a quantidade disponível.

O lote deverá permitir rastrear as entradas e saídas de estoque e as dispensações realizadas.

A identificação individual de cada caneta não será necessária.

### 3.8 Estoque

Representa a quantidade disponível de canetas por modelo e lote em determinada instituição.

O estoque deverá ser controlado por movimentações registradas, incluindo entradas, saídas, transferências e ajustes autorizados.

O saldo deverá ser obtido a partir do histórico dessas movimentações, preservando a rastreabilidade de sua formação.

O sistema deverá permitir que diferentes instituições possuam estoques próprios.

### 3.9 Movimentação de estoque

Representa qualquer operação que altere a quantidade de canetas disponível no estoque de uma instituição.

As movimentações poderão incluir:

- Entrada de estoque.
- Saída de estoque.
- Transferência entre instituições.
- Ajuste de estoque.

Cada movimentação deverá identificar, conforme sua natureza:

- Modelo e lote envolvidos.
- Quantidade movimentada.
- Instituição de origem e/ou destino.
- Data da operação.
- Operador responsável.
- Justificativa, quando necessária.

As movimentações deverão preservar seu histórico e não poderão ser removidas fisicamente para corrigir erros.

### 3.10 Entrada de estoque

Representa o recebimento de canetas por uma instituição.

A entrada deverá identificar o modelo, o lote e a quantidade recebida.

Quando aplicável, deverá permitir identificar a instituição ou entidade de origem do recebimento.

Uma entrada poderá corresponder ao recebimento de uma transferência, ao abastecimento por uma entidade externa ou a outra operação de recebimento reconhecida pelo sistema.

### 3.11 Dispensação

Representa a entrega de uma ou mais canetas a um paciente.

Cada operação deverá registrar:

- Paciente.
- Instituição responsável pela dispensação.
- Modelo de caneta.
- Lote, quando conhecido.
- Quantidade entregue.
- Data da dispensação.
- Operador responsável.
- Tratamento considerado na operação, quando disponível.

A instituição responsável pela dispensação não precisa ser a mesma UBS responsável pelo acompanhamento territorial.

O sistema deverá permitir o registro de dispensações realizadas por:

- UBS responsável pelo acompanhamento.
- Outra UBS.
- CAF.
- Estado.
- Instituição de outro município.
- Outra instituição reconhecida pelo sistema.

O histórico de dispensações deverá ser preservado, inclusive quando o paciente mudar de UBS, alterar seu tratamento ou deixar de ser acompanhado pela rede.

### 3.12 Posse de canetas

Representa as quantidades de canetas que permanecem sob posse do paciente.

A posse deverá ser acompanhada por modelo e, quando conhecido, por lote.

O histórico de posse deverá considerar:

- Dispensações realizadas.
- Perdas.
- Danos.
- Reposições.
- Outras movimentações que alterem a quantidade em posse.

A necessidade atual do paciente deverá ser calculada a partir do tratamento vigente.

A posse, entretanto, deverá preservar as canetas recebidas anteriormente, mesmo quando o tratamento for alterado.

Assim, a mudança de tratamento não deverá apagar nem desconsiderar automaticamente as canetas anteriormente dispensadas.

Uma caneta de modelo compatível poderá continuar sendo considerada na disponibilidade do paciente, desde que permaneça utilizável e atenda às regras administrativas de validade e substituição.

O sistema deverá distinguir a necessidade atual da quantidade efetivamente em posse do paciente.

### 3.13 Ocorrência

Representa uma situação relacionada às canetas que estão ou estiveram em posse do paciente.

As ocorrências poderão incluir:

- Perda.
- Dano.
- Outras situações que comprometam a disponibilidade ou utilização da caneta.

O registro deverá identificar o paciente, a natureza da ocorrência, a data, a descrição e o operador responsável.

Quando possível, a ocorrência deverá identificar os modelos, lotes e quantidades envolvidos.

Uma ocorrência não deverá provocar automaticamente uma movimentação de entrada no estoque da UBS.

### 3.14 Reposição

Representa a entrega de uma nova caneta para substituir uma unidade perdida, danificada ou indisponível.

A reposição deverá estar relacionada à ocorrência que a motivou.

A reposição regular deverá respeitar o prazo administrativo estabelecido para substituição.

Uma reposição excepcional antes desse prazo dependerá de autorização do Estado, conforme o procedimento aplicável.

O registro da ocorrência, isoladamente, não autoriza uma reposição excepcional.

A reposição deverá ser registrada como operação própria, preservando a relação com a ocorrência e a autorização correspondente, quando exigida.

## 4. Regras de Negócio

### 4.1 Necessidade e posse

A necessidade de canetas deverá ser calculada a partir dos tipos de insulina prescritos no tratamento vigente.

A quantidade necessária deverá respeitar as regras de compatibilidade e as combinações definidas para os modelos de caneta.

A quantidade em posse do paciente deverá ser controlada independentemente da necessidade atual.

A alteração do tratamento não deverá apagar o histórico de posse nem remover automaticamente as canetas anteriormente dispensadas.

O sistema deverá permitir identificar:

- Quantidade necessária pelo tratamento atual.
- Quantidade em posse do paciente.
- Quantidade considerada disponível para utilização.
- Eventual diferença entre necessidade e disponibilidade.

### 4.2 Alterações de tratamento

Toda alteração de tratamento deverá ser registrada com base em uma nova prescrição.

O tratamento anterior deverá ter sua vigência encerrada, e um novo período deverá ser registrado.

Os registros históricos deverão permanecer preservados.

A alteração do tratamento deverá atualizar o cálculo da necessidade de canetas, sem modificar automaticamente as quantidades anteriormente dispensadas ou em posse do paciente.

O sistema não deverá exigir que as canetas anteriormente entregues sejam devolvidas à UBS quando houver mudança de tratamento.

### 4.3 Posse por modelo e lote

O controle de posse deverá considerar as dispensações e demais ocorrências que alterem as quantidades em posse do paciente.

Quando o lote for conhecido, deverá ser preservado para rastreabilidade.

Quando o lote de uma dispensação histórica ou externa for desconhecido, o sistema deverá permitir registrar essa ausência de informação sem inventar um lote.

A quantidade em posse deverá ser calculada a partir dos registros disponíveis, respeitando as ocorrências que reduzam ou alterem a disponibilidade.

### 4.4 Estoque

O estoque deverá ser controlado por instituição, modelo de caneta e lote.

Toda entrada ou saída deverá gerar um registro de movimentação.

Uma saída não poderá resultar em saldo negativo.

Transferências entre instituições deverão preservar a identificação da origem e do destino.

O histórico de movimentações deverá ser suficiente para reconstruir a evolução do estoque.

Correções de movimentações não deverão apagar registros anteriores. Deverão ocorrer por meio de operações de ajuste ou correção rastreáveis.

### 4.5 Prazo administrativo de substituição

O prazo administrativo regular para substituição de uma caneta será de três anos.

A regra do fabricante considera o primeiro uso da caneta. Entretanto, como a data efetiva do primeiro uso pode não estar disponível, o sistema utilizará a data da dispensação como referência administrativa para o cálculo.

O prazo deverá ser controlado por quantidade dispensada, modelo e lote, respeitando cada ciclo de dispensação.

A data da dispensação será uma referência operacional, não uma afirmação de que a caneta foi efetivamente utilizada pela primeira vez naquele dia.

Quando a data de uma dispensação anterior for desconhecida, o sistema deverá registrar essa ausência de informação.

Nesses casos, não deverá inventar uma data nem calcular a elegibilidade como se a data fosse conhecida.

A reposição antes do prazo de três anos somente poderá ocorrer em caráter excepcional, mediante autorização do Estado após a ocorrência correspondente, como perda ou dano.

### 4.6 Perda, dano e substituição

Perdas e danos deverão ser registrados como ocorrências.

Sempre que possível, o registro deverá identificar o modelo, o lote e a quantidade afetada.

A ocorrência deverá ser associada à posse do paciente, permitindo atualizar a quantidade considerada disponível.

A substituição deverá respeitar o prazo administrativo regular ou possuir autorização excepcional válida.

A ocorrência não deverá gerar devolução fictícia ao estoque.

Quando houver recebimento físico posterior de uma caneta, essa operação deverá ser registrada separadamente.

### 4.7 Dispensações parciais

O sistema deverá permitir dispensações parciais quando a instituição não possuir quantidade suficiente para atender à necessidade calculada.

Deverá ser possível identificar a quantidade necessária, a quantidade já entregue e a quantidade ainda pendente.

O sistema deverá permitir que o atendimento seja concluído por mais de uma operação de dispensação, preservando as datas, os lotes e os operadores envolvidos.

A necessidade não atendida deverá permanecer identificável até sua resolução ou alteração por uma nova prescrição.

### 4.8 Acompanhamento contínuo e indicadores

O sistema deverá permitir identificar pacientes:

- Com necessidade de canetas.
- Com atendimento integral.
- Com atendimento parcial.
- Sem atendimento registrado.
- Sem acompanhamento territorial vigente.

Os indicadores deverão considerar a necessidade calculada a partir do tratamento vigente e as quantidades efetivamente dispensadas.

A ausência de acompanhamento territorial não deverá apagar o histórico nem impedir consultas administrativas sobre o paciente.

### 4.9 Encerramento e retomada do acompanhamento territorial

O acompanhamento territorial será encerrado quando o paciente mudar para fora da área de cobertura da UBS responsável.

O encerramento deverá registrar a data em que o paciente deixou a área de cobertura.

Não será necessário registrar um motivo variável de encerramento, pois a mudança para fora da área de cobertura é a razão prevista para essa operação.

Quando o paciente passar a residir na área de outra UBS, deverá ser criado imediatamente um novo período de acompanhamento, mesmo que ainda não tenha ocorrido atendimento ou dispensação.

Quando retornar à área de uma UBS anteriormente responsável, deverá ser criado outro período, sem reabrir o registro encerrado.

Um paciente ativo poderá permanecer sem acompanhamento territorial vigente quando estiver fora da área de cobertura da rede.

### 4.10 Inativação cadastral

A inativação representa a suspensão administrativa do cadastro do paciente.

A operação deverá exigir uma justificativa selecionada a partir de uma lista controlada de motivos.

Deverá existir a opção `other`, que exigirá uma descrição manual obrigatória.

O sistema deverá registrar:

- Situação anterior.
- Nova situação.
- Motivo da alteração.
- Descrição complementar, quando aplicável.
- Operador responsável.
- Data e horário do registro.

A inativação deverá encerrar automaticamente qualquer acompanhamento territorial vigente.

A operação deverá preservar os históricos de acompanhamento, tratamento, dispensações, ocorrências e posse de canetas.

Um paciente inativo não poderá receber novas dispensações nem realizar operações incompatíveis com essa situação.

A inativação não deverá gerar devolução automática de canetas ao estoque.

### 4.11 Falecimento

O falecimento deverá possuir um procedimento próprio de registro no cadastro do paciente.

Após a confirmação, o sistema deverá:

- Registrar a data do falecimento, quando conhecida.
- Registrar a data e o horário em que a informação foi inserida no sistema.
- Identificar o operador responsável pelo registro.
- Alterar a situação cadastral para `inactive`.
- Registrar o motivo de inativação como `death`.
- Encerrar o acompanhamento territorial vigente.
- Bloquear novas dispensações e operações incompatíveis.

A data do falecimento e a data de registro deverão ser informações distintas.

O falecimento não deverá apagar o histórico do paciente nem provocar devolução automática das canetas ao estoque.

Caso ocorra recebimento físico posterior de canetas, deverá ser registrada uma operação independente.

Se o falecimento tiver sido registrado equivocadamente, não deverá ser permitida uma reativação administrativa simples. A correção deverá seguir procedimento formal, preservando a rastreabilidade do registro original e de sua correção.

### 4.12 Reativação cadastral

A reativação será permitida somente para cadastros com situação `inactive`.

Cadastros com situação `merged` não poderão ser reativados.

A operação deverá exigir justificativa selecionada a partir de uma lista controlada de motivos.

Deverá existir a opção `other`, com descrição manual obrigatória.

A reativação deverá registrar o operador responsável, a data e o horário da operação.

A reativação deverá exigir a identificação da UBS responsável pelo novo acompanhamento territorial.

A operação deverá criar um novo período de acompanhamento, sem reabrir períodos anteriores.

A reativação cadastral e a criação do novo acompanhamento deverão ocorrer como uma única operação: ambas serão concluídas ou nenhuma será aplicada.

Cadastros inativados por falecimento não poderão ser reativados por esse procedimento. Eventuais erros no registro de falecimento deverão ser tratados por correção formal.

### 4.13 Unificação de cadastros

A unificação deverá ser utilizada quando for identificado que dois ou mais cadastros pertencem à mesma pessoa.

A operação dependerá de confirmação explícita do operador de que os registros representam o mesmo indivíduo.

O operador deverá selecionar qual cadastro permanecerá como principal.

Antes da confirmação, o sistema deverá apresentar os dados e históricos envolvidos, além de um resumo das informações que serão associadas ao cadastro principal.

A operação deverá ser atômica, impedindo que apenas parte dos registros seja incorporada.

Somente cadastros com situação `active` poderão participar diretamente de uma unificação.

Cadastros inativos deverão passar por avaliação e eventual reativação administrativa antes da unificação.

Cadastros com registro de falecimento não poderão ser reativados apenas para viabilizar uma unificação. Se o falecimento tiver sido registrado equivocadamente, será necessária correção formal.

Após a unificação:

- O cadastro principal permanecerá ativo.
- O cadastro incorporado receberá a situação `merged`.
- O cadastro incorporado deverá apontar para o cadastro principal.
- O cadastro incorporado permanecerá consultável.
- O cadastro incorporado não poderá receber novas operações.
- Consultas futuras pelos documentos associados ao cadastro incorporado deverão direcionar ao cadastro principal.
- Os históricos dos cadastros envolvidos deverão ser preservados.
- A origem dos registros deverá continuar identificável.

A unificação não deverá apagar o cadastro incorporado nem eliminar a rastreabilidade dos registros históricos.

## 5. Histórico e Rastreabilidade

O sistema deverá preservar o histórico das operações administrativas realizadas.

Deverão ser rastreáveis:

- Cadastro e alterações cadastrais de pacientes.
- Inativações e reativações.
- Registros e correções de falecimento.
- Unificações de cadastros.
- Períodos de acompanhamento territorial.
- Alterações de tratamento.
- Prescrições associadas aos tratamentos.
- Entradas e saídas de estoque.
- Transferências entre instituições.
- Dispensações e respectivos itens.
- Lotes envolvidos nas operações.
- Ocorrências de perda e dano.
- Reposições e autorizações excepcionais.
- Operadores responsáveis pelas operações.

Os registros históricos e transacionais deverão permanecer consultáveis, mesmo quando o paciente ou outra entidade cadastral deixar de estar ativa.

A rastreabilidade deverá permitir compreender não apenas a situação atual, mas também os eventos que levaram a ela.

## 6. Limites do Sistema

O CNT Gestor terá natureza administrativa e operacional.

O sistema não deverá:

- Prescrever tratamentos.
- Determinar alterações clínicas.
- Substituir a avaliação médica.
- Presumir datas de primeiro uso ou dispensações desconhecidas.
- Inventar lotes para registros históricos incompletos.
- Considerar uma ocorrência como autorização automática de reposição.
- Gerar devoluções fictícias de canetas ao estoque.
- Apagar históricos para simplificar cadastros ou corrigir operações.

As informações clínicas serão utilizadas somente na medida necessária para calcular a necessidade administrativa de canetas e preservar o histórico dos tratamentos prescritos.

## 7. Decisões Pendentes de Detalhamento

Os seguintes pontos ainda dependem de definições mais específicas antes da implementação:

### 7.1 Compatibilidade múltipla

Definir como o sistema tratará novos modelos de caneta e combinações de compatibilidade que não estejam previstas nas regras iniciais.

### 7.2 Ocorrências sem identificação de lote

Definir quais informações mínimas serão exigidas quando o paciente não souber informar o lote da caneta envolvida.

### 7.3 Lotes de dispensações externas

Definir como serão registrados os lotes desconhecidos em dispensações realizadas por outras instituições.

### 7.4 Classificação dos atendimentos

Detalhar os critérios operacionais para classificar pacientes como atendidos, parcialmente atendidos ou ainda não atendidos.

### 7.5 Dispensações antigas sem data conhecida

Definir como serão importados e apresentados registros históricos incompletos, sem atribuir datas artificiais.

### 7.6 Transferências entre instituições

Detalhar o fluxo operacional e as informações necessárias para registrar transferências de estoque entre instituições.

### 7.7 Ajustes de estoque

Definir os tipos de ajuste permitidos, as justificativas obrigatórias e os níveis de autorização necessários.

### 7.8 Situação das canetas em posse

Detalhar como serão representadas as condições de utilização, indisponibilidade, perda e dano, distinguindo a posse física da disponibilidade para uso.

### 7.9 Motivos de inativação e reativação

Definir as opções específicas das listas controladas de motivos, incluindo os critérios para utilização da opção `other`.

### 7.10 Correção de falecimento

Detalhar o procedimento formal para corrigir um registro de falecimento realizado equivocadamente, incluindo as autorizações e os registros necessários.

### 7.11 Armazenamento de prescrições

Definir como os documentos de prescrição serão armazenados, consultados e associados aos respectivos tratamentos.

### 7.12 Autorização de reposição excepcional

Detalhar as informações documentais necessárias para registrar e validar uma autorização estadual de reposição antecipada.