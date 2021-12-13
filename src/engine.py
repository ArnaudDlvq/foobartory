import logging
from random import randint
from src.agent import GAME_AGENT
from src.model.action import ActionType
from src.model.robot import Location, Robot
from src.model.state import GAME_STATE

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


def run_game():
    while len(GAME_STATE.robot_list) < 30:
        logging.info(f"We are at {GAME_STATE.current_turn / 2}s")
        for robot in GAME_STATE.robot_list:
            current_action = robot.action
            if (
                current_action is not None
                and current_action.start + current_action.duration
                > GAME_STATE.current_turn
            ):
                continue
            if (
                current_action is not None
                and current_action.start + current_action.duration
                == GAME_STATE.current_turn
            ):
                evaluate_action_result(robot)
            GAME_AGENT.choose_action_for_robot(robot, GAME_STATE)
            logging.info(f"{robot.serial} will {robot.action}")
            if robot.action.type == ActionType.BUY:
                evaluate_action_result(robot)
        GAME_STATE.current_turn += 1
    logging.info(f"Game finished in {(GAME_STATE.current_turn-1)/2}s")


def evaluate_action_result(robot: Robot) -> None:
    if robot.action.type == ActionType.MOVE:
        robot.location = robot.action.destination
        logging.info(f"{robot.serial} has arrived to {robot.location}")
        return
    if robot.action.type == ActionType.MINE_FOO and robot.location == Location.FOO:
        GAME_STATE.add_foo()
        logging.info(
            f"{robot.serial} mined 1 foo ({len(GAME_STATE.foo_inventory)} in inventory)"
        )
        return
    if robot.action.type == ActionType.MINE_BAR and robot.location == Location.BAR:
        GAME_STATE.add_bar()
        logging.info(
            f"{robot.serial} mined 1 bar ({len(GAME_STATE.bar_inventory)} in inventory)"
        )
        return
    if (
        robot.action.type == ActionType.ASSEMBLE
        and robot.location == Location.ASSEMBLY
        and len(GAME_STATE.foo_inventory) > 0
        and len(GAME_STATE.bar_inventory) > 0
    ):
        roll = randint(1, 100)
        if roll <= 60:
            GAME_STATE.add_foobar()
            logging.info(
                f"{robot.serial} successfully assembled 1 foobar ({roll=}) "
                f"({len(GAME_STATE.foobar_inventory)} in inventory)"
            )
        else:
            logging.info(
                f"{robot.serial} tried to assemble a foobar but failed ({roll=})"
            )
            GAME_STATE.lose_foo()
        return
    if (
        robot.action.type == ActionType.SELL
        and robot.location == Location.SELL
        and len(GAME_STATE.foobar_inventory) > 0
    ):
        number_sold = GAME_STATE.sell_foobars()
        logging.info(
            f"{robot.serial} sold {number_sold} foobars"
            f"({len(GAME_STATE.foobar_inventory)} in inventory)"
        )
        return
    if (
        robot.action.type == ActionType.BUY
        and robot.location == Location.BUY
        and len(GAME_STATE.foo_inventory) >= 6
        and GAME_STATE.money >= 3
    ):
        number_bought = GAME_STATE.buy_robots()
        logging.info(
            f"{robot.serial} bought {number_bought} robots "
            f"({len(GAME_STATE.robot_list)} working robots)"
        )
        return
    logging.error(
        f"{robot.serial} tried to do {robot.action} at {robot.location} while "
        f"{GAME_STATE} which was not supported"
    )
