import os
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta

class Auth():
    hasher = CryptContext(schemes=['bcrypt'])
    #secret = os.getenv("APP_SECRET_STRING")
    secret = "1b0b1cd761525c45be721743ce1a0cf9b3d053e04f7976ffdc4ff8e2e3279634"

    def encode_password(self, password):
        return self.hasher.hash(password)
    
    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)
    
    def encode_token(self, username):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'scope' : 'access_token',
            'sub' : username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm = 'HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(status_code=401, detail = 'Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail = 'Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Token expired')
    
    def encode_refresh_token(self, username):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'scope' : 'refrsh_token',
            'sub' : username
        }
        print(payload)
        return jwt.encode(
            payload,
            self.secret,
            algorithm = 'HS256'
        )
    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'refrsh_token'):
                username = payload['sub']
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')