from src.exeptions.base import BaseError


class AuthError(BaseError):
    message = 'Auth error'
    code = 403000
    http_code = 403


class AuthHeaderRequired(AuthError):
    message = 'Auth header required'
    code = 403001


class WrongCredential(AuthError):
    message = 'Wrong username or password'
    code = 403002


class AuthenticationError(AuthError):
    message = 'Wrong username or password, or you have no permission to access this resource'
    code = 403003
