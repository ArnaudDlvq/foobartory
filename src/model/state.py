import logging
from typing import List
from src.model.robot import Robot
from src.model.materials import Foo, Bar, Foobar


class State:
    def __init__(self) -> None:
        self.current_turn = 0
        self.robot_list: List[Robot] = []
        self.foo_number = 0
        self.foo_inventory: List[Foo] = []
        self.bar_number = 0
        self.bar_inventory: List[Bar] = []
        self.foobar_inventory: List[Foobar] = []
        self.money = 0

    def __str__(self):
        return f"{self.foo_number=} {self.bar_number=} {self.foobar_inventory=} {self.money=}"

    def add_robot(self):
        new_serial = f"robot_{len(self.robot_list) +1}"
        self.robot_list.append(Robot(new_serial))
        logging.info(f"Robot {new_serial} added")

    def add_foo(self):
        new_serial = len(self.foo_inventory) + 1
        self.foo_inventory.append(Foo(new_serial))

    def lose_foo(self):
        if len(self.foo_inventory) == 0:
            logging.error("Tried to lose foo but foo_inventory is empty")
            return
        self.foo_inventory.pop(0)

    def add_bar(self):
        new_serial = len(self.bar_inventory) + 1
        self.bar_inventory.append(Bar(new_serial))

    def add_foobar(self):
        if len(self.foo_inventory) == 0:
            logging.error("Tried to add foobar but foo_inventory is empty")
            return
        if len(self.bar_inventory) == 0:
            logging.error("Tried to add foobar but bar_inventory is empty")
            return
        foo = self.foo_inventory.pop(0)
        bar = self.bar_inventory.pop(0)
        self.foobar_inventory.append(Foobar(foo.serial, bar.serial))

    def sell_foobars(self) -> int:
        if len(self.foobar_inventory) == 0:
            logging.error("Tried to sell foobar but foobar_inventory is empty")
            return 0
        sell_quantity = min(5, len(self.foobar_inventory))
        for _ in range(sell_quantity):
            self.foobar_inventory.pop(0)
            self.money = self.money + 1
        return sell_quantity

    def buy_robots(self) -> int:
        if len(self.foo_inventory) < 6:
            logging.error(
                "Tried to buy robot but foo_inventory has less than 6 elements"
            )
            return 0
        if self.money < 3:
            logging.error("Tried to buy robot but money is lower than 3")
            return 0
        bought_quantity = min(len(self.foo_inventory) // 6, self.money // 3)
        for _ in range(bought_quantity):
            self.money = self.money - 3
            for _ in range(6):
                self.lose_foo()
            self.add_robot()


GAME_STATE = State()
