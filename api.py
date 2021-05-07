"""
API desafio mobile

Este é o código da API para o desafio mobile. Ele está incluso no
repositório apenas para comodidade caso tenha alguma dúvida sobre o
funcionamento. Você não precisa entender python (nem mesmo utilizar
este arquivo), pois ela já está hospedada em um servidor e a
documentação de todos os endpoints está disponível no README.
"""
import json
import random
import re
from datetime import date


USERS = [
    {'username': 'jose@exemplo.com', 'password': 'jose', 'token': '3cfLwoXYdBblURcbSfjS'},
    {'username': 'maria@exemplo.com', 'password': 'maria', 'token': '9psohKwHcxahFV4O3V89'},
]


def lambda_handler(event, context):
    """AWS Lambda entrypoint"""
    request = {
        'id': event['requestContext']['requestId'],
        'method': event['httpMethod'],
        'path': event['path'],
        'body': event['body'],
        'headers': {k.lower(): v for k, v in event['headers'].items()},
    }

    print(f'starting request {request["id"]}: {request["method"]} {request["path"]}')
    response = dispatcher(request)
    print(f'ending request {request["id"]}: {response["statusCode"]} {response["body"]}')
    return response


def dispatcher(request):
    """Route request to the correct handler"""
    if random.randint(0, 100) <= 5:  # There's a 5% chance that the API will return a 500 error
        return {'statusCode': 500, 'body': 'Fake error to test how your application can handle unexpected events'}

    if request['body']:
        if request['headers'].get('content-type') != 'application/json':
            return {'statusCode': 415, 'body': 'Invalid Content-Type: This server only supports application/json'}
        try:
            request['body'] = json.loads(request['body'])
        except json.errors.JSONDecodeError:
            return {'statusCode': 400, 'body': 'Unable to parse application/json data'}
    else:
        request['body'] = {}

    if re.match(r'^/login/?$', request['path']):
        return handler_login(request)
    elif re.match(r'^/movimentacoes/?$', request['path']):
        return handler_movimentacoes(request)
    elif re.match(r'^/aplicacao/?$', request['path']):
        return handler_aplicacao_resgate(request)
    elif re.match(r'^/resgate/?$', request['path']):
        return handler_aplicacao_resgate(request)
    return {'statusCode': 404, 'body': 'Not Found'}


def allow_methods(methods):
    """Restrict handler to a list of methods"""
    def wrapper(func):
        def inner_wrapper(request, *args, **kwargs):
            if request['method'].upper() not in methods:
                return {'statusCode': 405, 'body': 'Method Not Allowed'}
            return func(request, *args, **kwargs)
        return inner_wrapper
    return wrapper


def authenticated(func):
    """Restrict handler to authenticated users"""
    def wrapper(request, *args, **kwargs):
        token = request['headers'].get('authorization')
        if token is None:
            return {'statusCode': 401, 'body': 'Unauthorized'}

        for user in USERS:
            if token == user['token']:
                return func(request, user, *args, **kwargs)
        return {'statusCode': 403, 'body': 'Forbidden'}
    return wrapper


@allow_methods(['POST'])
def handler_login(request):
    username, password = request['body'].get('username'), request['body'].get('password')
    if username is None:
        return {'statusCode': 400, 'body': json.dumps({'errors': 'missing \'username\''})}
    elif password is None:
        return {'statusCode': 400, 'body': json.dumps({'errors': 'missing \'password\''})}

    for user in USERS:
        if username == user['username'] and password == user['password']:
            return {'statusCode': 200, 'body': json.dumps({'token': user['token']})}
    return {'statusCode': 400, 'body': json.dumps({'errors': 'invalid username or password'})}


@allow_methods(['GET'])
@authenticated
def handler_movimentacoes(request, user):
    if user['username'] == 'jose@exemplo.com':
        return {'statusCode': 200, 'body': json.dumps({
            'movimentacoes': [
                {'tipo': 'aplicacao', 'data': '2020-03-21', 'valor': 400.25},
                {'tipo': 'aplicacao', 'data': '2020-04-12', 'valor': 100.00},
                {'tipo': 'resgate', 'data': '2020-01-13', 'valor': 300.10},
                {'tipo': 'aplicacao', 'data': '2020-03-21', 'valor': 39.44},
            ]
        })}
    elif user['username'] == 'maria@exemplo.com':
        return {'statusCode': 200, 'body': json.dumps({
            'movimentacoes': [
                {'tipo': 'aplicacao', 'data': '2020-01-14', 'valor': 823.15},
                {'tipo': 'aplicacao', 'data': '2020-03-12', 'valor': 300.00},
                {'tipo': 'resgate', 'data': '2020-05-13', 'valor': 100.00},
                {'tipo': 'aplicacao', 'data': '2020-05-13', 'valor': 45.12},
                {'tipo': 'aplicacao', 'data': '2020-05-15', 'valor': 88.12},
                {'tipo': 'aplicacao', 'data': '2020-08-03', 'valor': 10.00},
                {'tipo': 'resgate', 'data': '2020-11-22', 'valor': 1000.00},
                {'tipo': 'resgate', 'data': '2020-11-23', 'valor': 100.00},
                {'tipo': 'aplicacao', 'data': '2020-12-01', 'valor': 4000.20},
                {'tipo': 'resgate', 'data': '2021-03-18', 'valor': 3000.00},
                {'tipo': 'aplicacao', 'data': '2020-03-28', 'valor': 40.00},
                {'tipo': 'aplicacao', 'data': '2020-04-07', 'valor': 80.00},
            ]
        })}
    return {'statusCode': 200, 'body': json.dumps({'movimentacoes': []})}


@allow_methods(['PUT'])
@authenticated
def handler_aplicacao_resgate(request, user):
    amount = request['body'].get('valor')
    if amount is None:
        return {'statusCode': 400, 'body': json.dumps({'errors': 'missing \'valor\''})}
    elif not isinstance(amount, (int, float)):
        return {'statusCode': 400, 'body': json.dumps({'errors': '\'valor\' must be a number'})}
    elif amount <= 0:
        return {'statusCode': 400, 'body': json.dumps({'errors': '\'valor\' must be greater than zero'})}

    return {'statusCode': 201, 'body': json.dumps({
        'valor': float(amount),
        'data': date.today().strftime('%Y-%m-%d'),
    })}


if __name__ == '__main__':
    import uuid

    lambda_handler(
        event={
            # "httpMethod": "POST", "path": "/login",
            "httpMethod": "GET", "path": "/movimentacoes",
            # "httpMethod": "PUT", "path": "/aplicacao",
            # "httpMethod": "PUT", "path": "/resgate",
            "requestContext": {
              "requestId": str(uuid.uuid4()),
            },
            "headers": {
                'Content-Type': 'application/json',

                # Authorization
                # 'Authorization': 'invalid',
                # 'Authorization': '3cfLwoXYdBblURcbSfjS',  # jose@exemplo.com
                'Authorization': '9psohKwHcxahFV4O3V89',  # maria@exemplo.com
            },
            "body": json.dumps({
                # Login
                # 'username': 'jose@exemplo.com',
                # 'password': 'jose',

                # Aplicação / Resgate
                # 'valor': 100.25
            }),
        },
        context=None
    )
