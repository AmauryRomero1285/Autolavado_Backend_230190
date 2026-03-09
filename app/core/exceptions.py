# app/core/exceptions.py

class DuplicatePhoneError(Exception):
    """Excepción lanzada cuando un número de teléfono ya existe en la DB."""
    def __init__(self, message="Este número de teléfono ya está registrado"):
        self.message = message
        super().__init__(self.message)
