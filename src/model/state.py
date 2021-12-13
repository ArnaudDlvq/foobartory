import logging
from typing import List
from src.model.robot import Robot
from src.model.materials import Foo, Bar, Foobar


class SellError(Exception):
    """Exception to raise when we try to sell something we don't have"""


class BuyError(Exception):
    """Exception to raise when we try to buy without sufficent funds"""


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
        return (
            f"{len(self.foo_inventory)=} {len(self.bar_inventory)=} "
            f"{len(self.foobar_inventory)=} {self.money=}"
        )

    def add_robot(self):
        new_serial = f"robot_{len(self.robot_list) +1}"
        self.robot_list.append(Robot(new_serial))
        logging.info(f"Robot {new_serial} added")

    def add_foo(self):
        new_serial = self.foo_number + 1
        self.foo_inventory.append(Foo(new_serial))
        self.foo_number += 1

    def lose_foo(self):
        self.foo_inventory.pop(0)

    def add_bar(self):
        new_serial = self.bar_number + 1
        self.bar_inventory.append(Bar(new_serial))
        self.bar_number += 1

    def add_foobar(self):
        used_foo = self.foo_inventory.pop(0)
        used_bar = self.bar_inventory.pop(0)
        self.foobar_inventory.append(Foobar(used_foo.serial, used_bar.serial))

    def sell_foobars(self) -> int:
        if len(self.foobar_inventory) == 0:
            raise SellError("Tried to sell foobar but foobar_inventory is empty")
        sell_quantity = min(5, len(self.foobar_inventory))
        for _ in range(sell_quantity):
            self.foobar_inventory.pop(0)
            self.money += 1
        return sell_quantity

    def buy_robots(self) -> int:
        if len(self.foo_inventory) < 6:
            raise BuyError(
                "Tried to buy robot but foo_inventory has less than 6 elements"
            )
        if self.money < 3:
            raise BuyError("Tried to buy robot but money is lower than 3")
        bought_quantity = min(len(self.foo_inventory) // 6, self.money // 3)
        for _ in range(bought_quantity):
            self.money -= 3
            for _ in range(6):
                self.lose_foo()
            self.add_robot()
        return bought_quantity


GAME_STATE = State()
