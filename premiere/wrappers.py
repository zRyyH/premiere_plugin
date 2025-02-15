from functools import wraps
from logger import critical, warning


def error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            critical("Erro ao executar função: %s" % e)
            return None

    return wrapper


def safe_project(func):
    @wraps(func)
    @error_handler
    def wrapper(self, *args, **kwargs):
        if not self.project:
            warning("Projeto não carregado.")
            return None
        return func(self, *args, **kwargs)

    return wrapper


def safe_sequence(func):
    @wraps(func)
    @error_handler
    def wrapper(self, *args, **kwargs):
        if not self.activeSequence:
            warning("Nenhuma sequência ativa encontrada.")
            return None
        return func(self, *args, **kwargs)

    return wrapper


def safe_premiere(func):
    @wraps(func)
    @error_handler
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper