import logging
from typing import List
from src.model.state import State
from src.model.action import Action, ActionType
from src.model.robot import Location, Robot


class Agent:
    def __init__(self) -> None:
        self.mining_foo: List[Robot] = []
        self.mining_bar: List[Robot] = []
        self.assembling: List[Robot] = []
        self.selling: List[Robot] = []
        self.buying: List[Robot] = []

    def __str__(self):
        return (
            f"{self.mining_foo=} {self.mining_bar=} {self.assembling=} {self.selling=}"
            f" {self.buying=}"
        )

    def put_robot_in(self, robot: Robot, list_name: str):
        """Put a robot in the designated list and try to remove it from all others"""
        agent_lists = ["mining_foo", "mining_bar", "assembling", "selling", "buying"]
        agent_lists.remove(list_name)
        for old_list in agent_lists:
            try:
                getattr(self, old_list).remove(robot)
            except ValueError:
                pass
        getattr(self, list_name).append(robot)

    def choose_action_for_robot(self, robot: Robot, state: State):
        """Place where we make decisions.
        The strategy is to prioritize buying, over selling, over assembling, over
        mining foo, over mining bar
        When we have available task covered by at least one robot, we put it in an
        already covered task"""
        logging.debug(f"Choosing action for robot {robot.serial}")
        if (
            len(state.foo_inventory) >= 6
            and state.money >= 3
            and (len(self.buying) == 0 or robot in self.buying)
        ):
            self.make_robot_do_(robot, state, "buying")
            return
        if len(state.foobar_inventory) >= 5 and (
            len(self.selling) == 0 or robot in self.selling
        ):
            self.make_robot_do_(robot, state, "selling")
            return
        if (
            len(state.foo_inventory) > 6
            and len(state.bar_inventory) >= 1
            and (len(self.assembling) == 0 or robot in self.assembling)
        ):
            self.make_robot_do_(robot, state, "assembling")
            return
        if len(self.mining_foo) == 0 or robot in self.mining_foo:
            self.make_robot_do_(robot, state, "mining_foo")
            return
        if len(self.mining_bar) == 0 or robot in self.mining_bar:
            self.make_robot_do_(robot, state, "mining_bar")
            return
        # All available tasks are covered
        if len(self.selling) <= len(self.assembling):
            self.make_robot_do_(robot, state, "selling")
            return
        if len(self.assembling) <= len(self.mining_foo):
            self.make_robot_do_(robot, state, "assembling")
            return
        if len(self.mining_foo) <= 2 * len(self.mining_bar):
            self.make_robot_do_(robot, state, "mining_foo")
            return
        self.make_robot_do_(robot, state, "mining_bar")

    @staticmethod
    def get_associated_location(action_str: str) -> str:
        if action_str == "mining_foo":
            return Location.FOO
        if action_str == "mining_bar":
            return Location.BAR
        if action_str == "assembling":
            return Location.ASSEMBLY
        if action_str == "selling":
            return Location.SELL
        if action_str == "buying":
            return Location.BUY
        raise ValueError("Unknown activity")

    @staticmethod
    def get_associated_action(action_str: str) -> str:
        if action_str == "mining_foo":
            return ActionType.MINE_FOO
        if action_str == "mining_bar":
            return ActionType.MINE_BAR
        if action_str == "assembling":
            return ActionType.ASSEMBLE
        if action_str == "selling":
            return ActionType.SELL
        if action_str == "buying":
            return ActionType.BUY
        raise ValueError("Unknown activity")

    def make_robot_do_(self, robot: Robot, state: State, action_str: str):
        if action_str not in [
            "mining_foo",
            "mining_bar",
            "assembling",
            "selling",
            "buying",
        ]:
            raise ValueError("Unknown activity")
        if robot not in getattr(self, action_str):
            self.put_robot_in(robot, action_str)
        location = Agent.get_associated_location(action_str)
        if robot.location != location:
            robot.action = Action(state.current_turn, ActionType.MOVE, location)
        else:
            robot.action = Action(
                state.current_turn, Agent.get_associated_action(action_str)
            )


GAME_AGENT = Agent()
