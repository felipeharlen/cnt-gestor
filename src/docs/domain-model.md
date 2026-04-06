# Modelo de Domínio — CNT Gestor

Este documento descreve os principais conceitos do domínio do CNT Gestor, bem como suas responsabilidades e relações, servindo como base para a modelagem do banco de dados e das regras de negócio do sistema.

---

## Conceitos Centrais

### Paciente
Indivíduo insulino-dependente cadastrado no sistema com o objetivo de registrar sua demanda por canetas aplicadoras de insulina.

Um paciente pode estar apenas registrado (aguardando atendimento) ou possuir uma ou mais dispensações registradas.

**Atributos principais:**
- Nome
- CNS
- CPF
- Unidade de Saúde de referência
- Quantidade de canetas necessárias

---

### Dispensação
Evento que representa a entrega de uma caneta aplicadora de insulina a um paciente, em uma data específica.

Uma dispensação pode ocorrer diretamente ao paciente ou a um responsável autorizado, mediante apresentação de receita médica.

**Atributos principais:**
- Data da dispensação
- Paciente associado
- Responsável pela retirada
- Servidor que realizou a dispensação

---

### Unidade de Saúde
Entidade responsável pelo cadastro do paciente e pela realização das dispensações.

**Atributos principais:**
- Nome da unidade

---

### Servidor
Funcionário da unidade de saúde responsável por realizar a dispensação de canetas.

**Atributos principais:**
- Nome do servidor