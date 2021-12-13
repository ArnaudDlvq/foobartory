import logging
from random import randint


class UnsupportedActionType(Exception):
    """Exception to raise when a given action type was not handled by a function"""


class ActionType:
    MOVE = "MOVE"
    MINE_FOO = "MINE_FOO"
    MINE_BAR = "MINE_BAR"
    ASSEMBLE = "ASSEMBLE"
    SELL = "SELL"
    BUY = "BUY"


class Action:
    def __init__(
        self,
        start: int,
        action_type: str,
        destination: str = None,
    ) -> None:
        self.type = action_type
        self.start = start
        self.duration = Action.get_duration(action_type)
        self.destination = destination

    def __str__(self):
        if self.type == ActionType.MOVE:
            return f"{ActionType.MOVE} to {self.destination}"
        return f"{self.type}"

    @staticmethod
    def get_duration(action_type: str) -> int:
        if action_type == ActionType.MOVE:
            return 10
        if action_type == ActionType.MINE_FOO:
            return 2
        if action_type == ActionType.MINE_BAR:
            return randint(1, 4)
        if action_type == ActionType.ASSEMBLE:
            return 4
        if action_type == ActionType.SELL:
            return 20
        if action_type == ActionType.BUY:
            return 0
        logging.error(f"Unsupported action type: {action_type}")
        raise UnsupportedActionType(f"Unsupported action type: {action_type}")
