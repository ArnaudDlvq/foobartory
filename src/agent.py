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
        agent_lists = ["mining_foo", "mining_bar", "assembling", "selling", "buying"]
        agent_lists.remove(list_name)
        for old_list in agent_lists:
            try:
                getattr(self, old_list).remove(robot)
            except ValueError:
                pass
        getattr(self, list_name).append(robot)

    def choose_action_for_robot(self, robot: Robot, state: State):
        logging.debug(f"Need to choose action for robot {robot.serial}")
        if (
            len(state.foo_inventory) >= 6
            and state.money >= 3
            and (len(self.buying) == 0 or robot in self.buying)
        ):
            if robot not in self.buying:
                self.put_robot_in(robot, "buying")
            if robot.location != Location.BUY:
                robot.action = Action(state.current_turn, ActionType.MOVE, Location.BUY)
                logging.info(f"Robot {robot.serial} move to BUY")
                return
            else:
                robot.action = Action(state.current_turn, ActionType.BUY)
                logging.info(f"Robot {robot.serial} will BUY")
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

    def make_robot_sell(self, robot: Robot, state: State):
        if robot not in self.selling:
            self.put_robot_in(robot, "selling")
        if robot.location != Location.SELL:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.SELL)
            logging.info(f"Robot {robot.serial} move to SELL")
        else:
            robot.action = Action(state.current_turn, ActionType.SELL)
            logging.info(f"Robot {robot.serial} will SELL")

    def make_robot_assemble(self, robot: Robot, state: State):
        if robot not in self.assembling:
            self.put_robot_in(robot, "assembling")
        if robot.location != Location.ASSEMBLY:
            robot.action = Action(
                state.current_turn, ActionType.MOVE, Location.ASSEMBLY
            )
            logging.info(f"Robot {robot.serial} move to ASSEMBLY")
            return
        else:
            robot.action = Action(state.current_turn, ActionType.ASSEMBLE)
            logging.info(f"Robot {robot.serial} will ASSEMBLE")
            return

    def make_robot_mine_foo(self, robot: Robot, state: State):
        if robot not in self.mining_foo:
            self.put_robot_in(robot, "mining_foo")
        if robot.location != Location.FOO:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.FOO)
            logging.info(f"Robot {robot.serial} move to FOO")
        else:
            robot.action = Action(state.current_turn, ActionType.MINE_FOO)
            logging.info(f"Robot {robot.serial} will MINE_FOO")

    def make_robot_mine_bar(self, robot: Robot, state: State):
        if robot not in self.mining_bar:
            self.put_robot_in(robot, "mining_bar")
        if robot.location != Location.BAR:
            robot.action = Action(state.current_turn, ActionType.MOVE, Location.BAR)
            logging.info(f"Robot {robot.serial} move to BAR")
            return
        else:
            robot.action = Action(state.current_turn, ActionType.MINE_BAR)
            logging.info(f"Robot {robot.serial} will MINE_BAR")
            return


GAME_AGENT = Agent()
