__all__ = [
    'AllConfError',
    'AllConfFileNotFoundError',
    'AllConfFileAlreadyExistsError',
    'AllConfParsingError',

    'AllConfSyntaxError',
    'AllConfExpressionResolvingError',
    'AllConfFideliusError',
    'AllConfFideliusNotInstalledError',
    'AllConfFideliusSyntaxError',

    'AllConfUnknownFileTypeError',
    'AllConfStubberError',
    'AllConfStubberSyntaxError',
    'AllConfStubberInvalidTypeName',
]


class AllConfError(Exception):
    pass


class AllConfFileNotFoundError(AllConfError, FileNotFoundError):
    def __init__(self, message: str, file_name: str = '?'):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f'{super().__str__()} (file_name="{self.file_name}")'


class AllConfFileAlreadyExistsError(AllConfError, FileExistsError):
    def __init__(self, message: str, file_name: str = '?'):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f'{super().__str__()} (file_name="{self.file_name}")'


class AllConfParsingError(AllConfError, ValueError):
    pass


class AllConfSyntaxError(AllConfParsingError):
    pass


class AllConfExpressionResolvingError(AllConfParsingError):
    pass


class AllConfFideliusError(AllConfExpressionResolvingError):
    pass


class AllConfFideliusNotInstalledError(AllConfExpressionResolvingError, ImportError):
    pass


class AllConfFideliusSyntaxError(AllConfExpressionResolvingError, AllConfSyntaxError):
    pass


class AllConfUnknownFileTypeError(AllConfParsingError, NotImplementedError):
    def __init__(self, message: str, file_name: str = '?'):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f'{super().__str__()} (file_name="{self.file_name}")'


class AllConfStubberError(AllConfError):
    pass


class AllConfStubberSyntaxError(AllConfStubberError, ValueError):
    def __init__(self, message: str, field_name: str = '?'):
        super().__init__(message)
        self.field_name = field_name

    def __str__(self):
        return f'{super().__str__()} (field_name="{self.field_name}")'


class AllConfStubberInvalidTypeName(AllConfStubberSyntaxError, TypeError):
    def __init__(self, message: str, field_name: str = '?', type_name: str = '?'):
        super().__init__(message, field_name)
        self.type_name = type_name

    def __str__(self):
        return f'{super().__str__()} (type_name="{self.type_name}", field_name="{self.field_name}")'
