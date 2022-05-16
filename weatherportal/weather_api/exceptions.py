class ServerResponseError(Exception):
    pass


class ValidationWeatherError(Exception):
    pass


def exception_check(exception):
    if isinstance(exception, ServerResponseError):
        msg = 'Server response error'
        return f'<h1>{msg}</h1><br>{exception}'

    if isinstance(exception, ValidationWeatherError):
        msg = 'Validation error'
        return f'<h1>{msg}</h1><br>{exception}'

    if isinstance(exception, ValueError):
        msg = 'ValueError'
        return f'<h1>{msg}</h1><br>{exception}'
