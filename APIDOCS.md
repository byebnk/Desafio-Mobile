# Documentação da API
O aplicativo deve ser configurado para utilizar a API abaixo. Todos os seus endpoints com os exemplos
de requisição estão documentados abaixo. Além disso há uma [collection do Postman](https://gitlab.com/byebnk/desafio-mobile/-/blob/master/desafio-mobile.postman_collection.json) com exemplos de todos
os endpoints neste repositório. Caso tenha algum problema com a API você pode entrar em contato com
a gente.

Por ser um desafio, a API é stateless, isso significa que ela não possui banco de dados e sempre
retorna os mesmo resultados. Em outras palavras, não se preocupe se você fizer uma aplicação e ela
não aparecer nas movimentações, os dados retornados são sempre os mesmos. No entanto, você não pode
usar disso para simplificar o app. Ele precisa funcionar mesmo se a API fosse stateful. O [código da
API](https://gitlab.com/byebnk/desafio-mobile/-/blob/master/api.py) também está incluso no repositório caso tenha curiosidade de ver.

## Tratamento de erros da API
Por último, a API as vezes encontra alguns problemas internos e retorna um erro 500. Para evitar uma
sobrecarga nos canais de suporte, é importante que a experiência do usuário não seja completamente
impactada caso erros como esse aconteçam. Você pode colocar uma mensagem de "Tente novamente mais
tarde" ou implementar a medida que achar necessário para que o usuário entenda que o erro é
temporário.

**NOTA**: Os erros 500 são implementados propositalmente na API do desafio. Em toda a requisição
existe uma chance da API retornar um erro 500. Você consegue diferenciar eles de erros reais pelo
conteúdo do retorno. Os erros descritos acima possuem uma mensagem avisando que eles são erros
propositais.

```
Fake error to test how your application can handle unexpected events
```


## 1. Login

```
POST https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/login
Content-Type: application/json

{"username": "nome-de-usuario", "password": "senha"}


HTTP/2 200
{"token": "token-secreto"}
```

Para se autenticar nas outras chamadas você deve incluir o header `Authorization` com o valor do
token fornecido pela API no login.

### Usuários disponíveis

| Usuário | Senha |
|---|---|
| jose@exemplo.com | jose |
| maria@exemplo.com | maria |

## 2. Consultar movimentações
```
GET https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/movimentacoes
Authorization: token-secreto


HTTP/2 200
{"movimentacoes": [{"tipo": "aplicacao", "data": "2020-01-01", "valor": 111.11}, {"tipo": "resgate", "data": "2020-01-01", "valor": 111.11}]}
```

## 3. Solicitar aplicação
```
PUT https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/aplicacao
Content-Type: application/json
Authorization: token-secreto

{"valor": 111.11}


HTTP/2 201
{"data": "2020-01-01", "valor": 111.11}
```

## 4. Solicitar resgate
```
PUT https://mrwffgnpgf.execute-api.sa-east-1.amazonaws.com/prod/resgate
Content-Type: application/json
Authorization: token-secreto

{"valor": 111.11}


HTTP/2 201
{"data": "2020-01-01", "valor": 111.11}
```
