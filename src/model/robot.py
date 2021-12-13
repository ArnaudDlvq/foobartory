from src.model.action import Action


class Location:
    HOME = "HOME"
    FOO = "FOO_LOCATION"
    BAR = "BAR_LOCATION"
    ASSEMBLY = "ASSEMBLY"
    SELL = "SELL_LOCATION"
    BUY = "BUY_LOCATION"


class Robot:
    def __init__(self, serial: str, action: Action = None) -> None:
        self.serial = serial
        self.action = action
        self.location = Location.HOME
