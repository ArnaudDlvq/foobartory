from random import randint


class Action:
    def __init__(
        self,
        start: int,
        action_type: str,
        destination: str = None,
        quantity: int = None,
    ) -> None:
        self.type = action_type
        self.start = start
        self.duration = Action.get_duration(action_type)
        self.destination = destination
        self.quantity = quantity

    @staticmethod
    def get_duration(action_type: str) -> int:
        if action_type == "move":
            return 10
        if action_type == "mine_foo":
            return 2
        if action_type == "mine_bar":
            return randint(1, 4)
        if action_type == "assemble":
            return 4
        if action_type == "sell":
            return 20
        if action_type == "buy":
            return 0
