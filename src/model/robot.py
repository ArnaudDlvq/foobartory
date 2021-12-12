from src.model.action import Action


class Location:
    HOME = "home"
    FOO = "foo"
    BAR = "bar"
    ASSEMBLY = "assembly"
    SELL = "sell"
    BUY = "buy"


class Robot:
    def __init__(self, serial: str, action: Action = None) -> None:
        self.serial = serial
        self.action = action
        self.location = Location.HOME
