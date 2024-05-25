import jwt
from datetime import datetime, timedelta
from rest_framework import exceptions


def generate_access_token(id):
    return jwt.encode(
        {
            'id': id,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }, 'access_key', algorithm='HS256'
    )


def verify_access_token(token):
    try:
        data = jwt.decode(token, 'access_key', algorithms=['HS256'])
        return data['id']
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Access token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid access token')


def generate_refresh_token(id):
    return jwt.encode(
        {
            'id': id,
            'exp': datetime.utcnow() + timedelta(weeks=1),
            'iat': datetime.utcnow()
        }, 'refresh_key', algorithm='HS256'
    )


def verify_refresh_token(token):
    try:
        data = jwt.decode(token, 'refresh_key', algorithms=['HS256'])
        return data['id']
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Refresh token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid refresh token')
