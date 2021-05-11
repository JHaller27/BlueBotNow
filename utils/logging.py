from typing import Optional, Union
from utils.time import iso_now
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
        if name not in cls._instances:
            instance = super().__call__(name)
            cls._instances[name] = instance
        return cls._instances[name]


class Logger(metaclass=SingletonMeta):
    _name: str
    _level: str
    _fmt: str

    NAME_MAX_WIDTH = 8

    def __init__(self, name: Optional[str]) -> None:
        self._name = name

        if self._name is not None and len(self._name) > 0:
            self._fmt = '{now} {name:%d} {level_name:>8} - {msg}' % Logger.NAME_MAX_WIDTH
        else:
            self._fmt = '{now} {level_name:>8} {msg}'

        if len(self._name) > Logger.NAME_MAX_WIDTH:
            new_name = self._name[:Logger.NAME_MAX_WIDTH]
            self.warn(f"Logger name too long: will show as {new_name}")
            self._name = new_name

    @property
    def _level(self) -> Level:
        return level

    def set_level(self, level: int):
        self._level = level

    def info(self, *msg: str) -> None:
        self.log(*msg, level=Level.INFO)

    def debug(self, *msg: str) -> None:
        self.log(*msg, level=Level.DEBUG)

    def warn(self, *msg: str) -> None:
        self.log(*msg, level=Level.WARNING)

    def error(self, *msg: str) -> None:
        self.log(*msg, level=Level.ERROR)

    def critical(self, *msg: str) -> None:
        self.log(*msg, level=Level.CRITICAL)

    def log(self, *parts: str, level: int = Level.INFO) -> None:
        now = iso_now()

        if level < self._level:
            return

        try:
            level_name = Level(level).name
        except ValueError:
            level_name = f"LOG:{level}"

        msg = ' '.join([str(p) for p in parts])
        print(self._fmt.format(now=now, name=self._name, level_name=level_name, msg=msg))


level: Level = Level.WARNING


def set_level(new_level: Union[Level, int, str]):
    global level

    if isinstance(new_level, int):
        new_level = Level(new_level)
    elif isinstance(new_level, str):
        new_level = Level[new_level.upper()]

    level = new_level


if __name__ == "__main__":
    def log():
        Logger("foo").warn("Warning!")
        Logger("foo").info("This is some", "info")
        Logger("foo").log("Custom message", level=23)
        Logger("foo").critical("Apocalypse!!!")

    log()
    set_level('debug')
    log()
