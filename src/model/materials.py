from dataclasses import dataclass


@dataclass
class Foo:
    serial: int


@dataclass
class Bar:
    serial: int


@dataclass
class Foobar:
    foo_serial: int
    bar_serial: int
