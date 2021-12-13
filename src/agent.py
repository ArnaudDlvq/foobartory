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

    def _put_robot_in(self, robot: Robot, list_name: str):
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
            self.make_robot_buy(robot, state)
            return
        if len(state.foobar_inventory) >= 5 and (
            len(self.selling) == 0 or robot in self.selling
        ):
            self.make_robot_sell(robot, state)
            return
        if (
            len(state.foo_inventory) > 6
            and len(state.bar_inventory) >= 1
            and (len(self.assembling) == 0 or robot in self.assembling)
        ):
            self.make_robot_assemble(robot, state)
            return
        if len(self.mining_foo) == 0 or robot in self.mining_foo:
            self.make_robot_mine_foo(robot, state)
            return
        if len(self.mining_bar) == 0 or robot in self.mining_bar:
            self.make_robot_mine_bar(robot, state)
            return
        # All available tasks are covered
        if len(self.selling) <= len(self.assembling):
            self.make_robot_sell(robot, state)
            return
        if len(self.assembling) <= len(self.mining_foo):
            self.make_robot_assemble(robot, state)
            return
        if len(self.mining_foo) <= 2 * len(self.mining_bar):
            self.make_robot_mine_foo(robot, state)
            return
        self.make_robot_mine_bar(robot, state)

    def make_robot_buy(self, robot: Robot, state: State):
        if robot not in self.buying:
            self._put_robot_in(robot, "buying")
        if robot.location != Location.BUY:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.BUY)
        else:
            robot.action = Action(state.current_turn, ActionType.BUY)

    def make_robot_sell(self, robot: Robot, state: State):
        if robot not in self.selling:
            self._put_robot_in(robot, "selling")
        if robot.location != Location.SELL:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.SELL)
        else:
            robot.action = Action(state.current_turn, ActionType.SELL)

    def make_robot_assemble(self, robot: Robot, state: State):
        if robot not in self.assembling:
            self._put_robot_in(robot, "assembling")
        if robot.location != Location.ASSEMBLY:
            robot.action = Action(
                state.current_turn, ActionType.MOVE, Location.ASSEMBLY
            )
            return
        else:
            robot.action = Action(state.current_turn, ActionType.ASSEMBLE)
            return

    def make_robot_mine_foo(self, robot: Robot, state: State):
        if robot not in self.mining_foo:
            self._put_robot_in(robot, "mining_foo")
        if robot.location != Location.FOO:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.FOO)
        else:
            robot.action = Action(state.current_turn, ActionType.MINE_FOO)

    def make_robot_mine_bar(self, robot: Robot, state: State):
        if robot not in self.mining_bar:
            self._put_robot_in(robot, "mining_bar")
        if robot.location != Location.BAR:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.BAR)
            return
        else:
            robot.action = Action(state.current_turn, ActionType.MINE_BAR)
            return


GAME_AGENT = Agent()
