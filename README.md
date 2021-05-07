# Desafio técnico mobile - Byebnk

Olá,

Estamos muito felizes que você deseja fazer parte do time da Byebnk. O teste abaixo é construido de
forma que você consiga demonstrar os seus conhecimentos em desenvolvimento de aplicativos mobile. Ele
consiste no desenvolvimento de um aplicativo simples para gestão de investimentos.

O aplicativo deve consumir uma API rest para mostrar os seus resultados e deve conter as três telas
especificadas abaixo. Você não precisa se preocupar com a formatação do layout (deixar bonito, etc).
O foco do desafio são as suas habilidade técnicas e as funcionalidades do aplicativo, não o design.

Você pode organizar o projeto da maneira que achar que faz mais sentido. Além disso, sinta-se a
vontade para adicionar ferramentas ou funcionalidades que ache relevante, porém não deixe que isso
impacte negativamente a qualidade dos requisitos obrigatórios.

Lembre-se: Existem diversas formas de se desenvolver um sistema. Não estamos procurando a resposta
certa, mas sim uma explicação racional por trás de cada decisão tomada.

## Requisitos obrigatórios
Desenvolva um aplicativo mobile para Android/iOS de gestão de investimentos.

## Telas
O aplicativo deve conter no mínimo as três telas abaixo. Você pode separar as funcionalidade em mais
telas caso acredite que faça mais sentido, porém não pode juntar funcionalidades de delas diferentes
em uma só (exemplo: criar apenas uma tela para ver as movimentações e fazer uma aplicação).

### 1. Login
O login é realizado utilizando o email e senha do usuário. Ao acessar o aplicativo pela primeira vez
o usuário deve ser forçado a realizar o login antes de acessar qualquer outra funcionalidade.

### 2. Movimentações e saldo
Esta é a tela inicial do app após o login, nela o usuário pode ver todas as movimentações que foram
feitas na sua conta (aplicações e resgate) e também o saldo da sua conta (saldo = aplicações - resgates).
A API não retorna o saldo da conta, ele deve ser calculado manuamente no app. Para facilitar a
visualização por parte do usuário é importante que as aplicações e resgates sejam visualmente
diferentes (uma sugestão pode ser utilizar uma cor para aplicação e outra para resgate, porém fica
ao seu critério como fazer). Por último, deve ser possível o usuário atualizar (no sentido de fazer
uma nova requisição para o servidor) o seu saldo/movimentações sem precisar fechar e abrir o aplicativo.

### 3. Realizar aplicação ou resgate
Nesta tela o usuário pode estipular um valor e fazer uma aplicação ou resgate na sua conta. Aplicação
é quando o usuário aporta dinheiro em sua conta. Resgate é quando o usuário retira dinheiro da sua
conta.

## API
O aplicativo deve ser configurado para utilizar a API abaixo. Todos os seus endpoints com os exemplos
de requisição estão documentados abaixo. Além disso há uma collection do Postman com exemplos de todos
os endpoints neste repositório. Caso tenha algum problema com a API você pode entrar em contato com
a gente.

Por ser um desafio, a API é stateless, isso significa que ela não possui banco de dados e sempre
retorna os mesmo resultados. Em outras palavras, não se preocupe se você fizer uma aplicação e ela
não aparecer nas movimentações, os dados retornados são sempre os mesmos. No entanto, você não pode
usar disso para simplificar o app. Ele precisa funcionar mesmo se a API fosse stateful. O código da
API também está incluso no repositório caso tenha curiosidade de ver.

Por último, a API as vezes encontra alguns problemas internos e retorna um erro 500. Para evitar uma
sobrecarga nos canais de suporte, é importante que a experiência do usuário não seja completamente
impactada caso erros como esse aconteçam. Você pode colocar uma mensagem de "Tente novamente mais
tarde" ou implementar a medida que achar necessário para que o usuário entenda que o erro é
temporário.

**NOTA**: Os erros 500 são implementados propositalmente na API do desafio. Em toda a requisição
existe uma chance da API retornar um erro 500. Você consegue diferenciar eles de erros reais pelo
conteúdo do retorno. Os erros descritos acima possuem uma mensagem avisando que eles são erros
propositais.


### Login

```
POST https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/login
Content-Type: application/json

{"username": "nome-de-usuario", "password": "senha"}


HTTP/2 200
{"token": "token-secreto"}
```

Para se autenticar nas outras chamadas você deve incluir o header `Authorization` com o valor do
token fornecido pela API no login.

| Usuário | Senha |
|---|---|
| jose@exemplo.com | jose |
| maria@exemplo.com | maria |

### Consultar movimentações
```
GET https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/movimentacoes
Authorization: token-secreto


HTTP/2 200
{"movimentacoes": [{"tipo": "aplicacao", "data": "2020-01-01", "valor": 111.11}, {"tipo": "resgate", "data": "2020-01-01", "valor": 111.11}]}
```

### Solicitar aplicação
```
PUT https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/aplicacao
Content-Type: application/json
Authorization: token-secreto

{"valor": 111.11}


HTTP/2 201
{"data": "2020-01-01", "valor": 111.11}
```

### Solicitar resgate
```
PUT https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/resgate
Content-Type: application/json
Authorization: token-secreto

{"valor": 111.11}


HTTP/2 201
{"data": "2020-01-01", "valor": 111.11}
```

## O que vamos avaliar (nesta ordem)
1. O cumprimento dos requisitos obrigatórios
2. A forma que o código está organizado
3. O domínio das funcionalidade do Framework
4. A simplicidade da solução
5. A implementação de requisitos opcionais
6. A implementação de funcionalidades extras
