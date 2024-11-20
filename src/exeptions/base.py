class BaseError(Exception):
    message: str = 'Unknown error'
    code: int = 0
    http_code: int = 500
