from typing import Optional
from datetime import datetime
from enum import Enum


class Level(int, Enum):
    DEBUG=0,
    INFO=10,
    WARNING=20,
    ERROR=30,
    CRITICAL=40,


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, name: str = None):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(name)
            cls._instances[name] = instance
        return cls._instances[name]


class Logger(metaclass=SingletonMeta):
    _name: str
    _level: str
    _fmt: str

    def __init__(self, name: Optional[str]) -> None:
        self._name = name

        if self._name is not None and len(self._name) > 0:
            self._fmt = '[{now} {name}:{level_name}] {msg}'
        else:
            self._fmt = '[{now} {level_name}] {msg}'

    @property
    def _level(self) -> Level:
        return level

    def set_level(self, level: int):
        self._level = level

    def info(self, msg: str) -> None:
        self.log(msg, Level.INFO)

    def debug(self, msg: str) -> None:
        self.log(msg, Level.DEBUG)

    def warn(self, msg: str) -> None:
        self.log(msg, Level.WARNING)

    def error(self, msg: str) -> None:
        self.log(msg, Level.ERROR)

    def critical(self, msg: str) -> None:
        self.log(msg, Level.CRITICAL)

    def log(self, msg: str, level: int) -> None:
        if level >= self._level:
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            try:
                level_name = Level(level).name
            except ValueError:
                level_name = f"LOG:{level}"

            print(self._fmt.format(now=now, name=self._name, level_name=level_name, msg=msg))


level: Level = Level.WARNING


if __name__ == "__main__":
    level = Level.DEBUG

    Logger("foo").warn("Warning!")
    Logger("foo").info("This is some info")
    Logger("foo").log("Custom message", 23)
