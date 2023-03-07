class ValidationError(Exception):
    def __init__(self, message = "", errors = None):
        super().__init__(message)
        self.errors = errors


class ConversionError(Exception):
    def __init__(self, message = "", errors = None):
        super().__init__(message)
        self.errors = errors


class NotFoundError(Exception):
    def __init__(self, message = "", errors = None):
        super().__init__(message)
        self.errors = errors