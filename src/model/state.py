from src.model.robot import Robot


class State:
    def __init__(self) -> None:
        self.current_turn = 0
        self.robot_list = []
        self.foo_number = 0
        self.foo_inventory = []
        self.bar_number = 0
        self.bar_inventory = []
        self.money = 0

    def add_robot(self):
        new_serial = f"robot_{len(self.robot_list) +1}"
        self.robot_list.append(Robot(new_serial))


GAME_STATE = State()
