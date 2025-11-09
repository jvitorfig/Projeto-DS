# Fluxo de Colaboração no Repositório
## 1. Abrir uma issue
* Verificar se não existe uma issue relacionada antes de abrir uma nova;
* Caso não exista, abrir uma nova issue com título claro e objetivo, descrição do que será implementado, corrigido, melhorado ou documentado, e adicionar rótulo (label) adequado à issue.

## 2. Criar uma branch
* Criar uma branch específica para o trabalho a ser realizado a partir da develop.

## 3. Desenvolver e commitar
* Fazer commits frequentes e significativos;
* Garantir que o código seja testado localmente antes de enviar para o Github.

## 4. Abrir uma pull request
* Criar uma pull request vinculada ao issue correspondente;
* Incluir descrição das mudanças realizadas;
* Solicitar revisão de pelo menos um colega do time antes de realizar o merge.

<br>
<br>

# Convenções de nomes de branch e mensagens de commit
## Nomes de branch
O Formato utilizado será: "tipo/descricao-curta"

São os principais tipos:
* feat - nova funcionalidade
* fix - correção de bug
* docs - documentação
* refactor - refatoração de código sem alterar funcionalidade
* test - testes automatizados
* chore - tarefas de manutenção

## Mensagens de commit
Mensagens curtas, descritivas e no imperativo, no seguinte formato: "tipo: descrição breve"
Os principais tipos de commit se assemelham aos de branches, então deve ser usada a mesma nomenclatura.

<br>
<br>

# Checklist antes de submeter o código para integração
* Verificar se a branch develop está atualizada com o repositório remoto;
* Testar o código localmente e garantir que não há erro;
* Garantir que o código segue os padrões definidos para o projeto;
* Confirmar que a issue correspondente foi atualizada e está vinculada ao PR;
* Manter a documentação atualizada;
* Quando aplicável, escrever testes automatizados.

<br>
<br>

# Como configurar o projeto localmente