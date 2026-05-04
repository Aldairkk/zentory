from fastapi import HTTPException, status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class NotFoundException(AppException):
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationException(AppException):
    def __init__(self, message: str = "Validación fallida"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class InventoryException(AppException):
    def __init__(self, message: str = "Error de inventario"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class DuplicateException(AppException):
    def __init__(self, message: str = "Recurso duplicado"):
        super().__init__(message, status.HTTP_409_CONFLICT)


def exception_handler(request, exc: AppException):
    return HTTPException(status_code=exc.status_code, detail=exc.message)