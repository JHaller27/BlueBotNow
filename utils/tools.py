from utils import logging
from utils.logging import Logger

from typing import Optional
import os


class Secret:
    def __init__(self, val: Optional[str]):
        self._value = val or ''

    @property
    def value(self) -> str:
        return self._value

    @property
    def is_empty(self) -> bool:
        return len(self._value) == 0

    def __repr__(self) -> str:
        if len(self.value) < 3:
            return f'*** ({self.value})'

        return f'{self.value[0]}...{self.value[-1]} ({len(self.value)})'


def read_env(name: str, default: str = None) -> str:
    """
    Attempt to read a variable from the environment.
    :param name: Name of environment variable
    :param default: Default value to use if env var doesn't exist (default: raise ValueError)
    :param err_msg: Custom error message to use if ValueError is raised due to missing env var
                    Note: Can format with token name using '{0}'
    :param secret: Return a Secret string instead of a plaintext string (default: False)
    """
    Logger("read_env").debug(f"Reading '{name}'")

    value = os.environ.get(name)

    if value is None:
        if default is None:
            raise ValueError(f"No environment variable found named '{name}'")

        value = default
        Logger("read_env").debug(f"Using default value")

    else:
        Logger("read_env").debug(f"Found value")

    return value


def read_secret(*args, **kwargs) -> Secret:
    """
    Calls through to read_env(), but returns a Secret instead of a string.
    """

    value = read_env(*args, **kwargs)

    return Secret(value)