from utils.logging import Logger

from typing import Optional, Any
import ctypes
import os


class CacheCalls:
    def __init__(self, ignore: list[str] = []) -> None:
        self._cache = {}
        self._ignore_list = ignore

    def __call__(self, func) -> Any:
        def _do(*args, **kwargs):
            key = self._key(*args, **kwargs)
            if key not in self._cache:
                self._cache[key] = func(*args, **kwargs)
            return self._cache[key]

        return _do

    def _key(self, *args: Any, **kwargs: Any) -> str:
        allowed_kwargs = filter(lambda kvp: kvp[0] not in self._ignore_list, kwargs.items())
        return '::'.join(map(str, args)) + '|' + '::'.join(map(str, sorted(allowed_kwargs, key=lambda kvp: kvp[0])))


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


@CacheCalls(ignore=['logger'])
def read_env(name: str, default: str = None, *, logger: Logger = None) -> str:
    """
    Attempt to read a variable from the environment.
    :param name: Name of environment variable
    :param default: Default value to use if env var doesn't exist (default: raise ValueError)
    :param err_msg: Custom error message to use if ValueError is raised due to missing env var
                    Note: Can format with token name using '{0}'
    :param secret: Return a Secret string instead of a plaintext string (default: False)
    """
    if logger is None:
        logger = Logger("read_env")

    logger.debug(f"Reading '{name}'")

    value = os.environ.get(name)

    if value is None:
        if default is None:
            raise ValueError(f"No environment variable found named '{name}'")

        value = default
        logger.debug(f"Using default value")

    else:
        logger.debug(f"Found value")

    return value


def read_secret(*args, **kwargs) -> Secret:
    """
    Calls through to read_env(), but returns a Secret instead of a string.
    """

    value = read_env(*args, **kwargs)

    return Secret(value)


def short_hash(*parts, N: int = 4):
    hashu=lambda word: ctypes.c_uint64(hash(word)).value
    hashn=lambda word: (hashu(word)%(2**(N*8))).to_bytes(N,"big").hex()

    uid = ''.join([str(p) for p in parts])

    return hashn(uid)
