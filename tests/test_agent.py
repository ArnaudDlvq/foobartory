from random import randint

import pytest
from src.model.action import ActionType
from src.agent import Agent
from src.model.robot import Location, Robot
from src.model.state import State


def test_put_robot_in_ok_case():
    agent = Agent()
    robot = Robot(1)
    agent.mining_bar = [robot]
    agent.mining_foo = []
    agent.put_robot_in(robot, "mining_foo")
    assert robot in agent.mining_foo
    assert len(agent.mining_bar) == 0


def test_put_robot_in_error_case():
    agent = Agent()
    robot = Robot(1)
    agent.mining_bar = [robot]
    with pytest.raises(ValueError):
        agent.put_robot_in(robot, "unknown_activity")


def test_choose_action_for_robot():
    agent = Agent()
    robot = Robot(1)
    state = State()
    state.current_turn = randint(1, 20)
    state.robot_list = [robot]
    agent.choose_action_for_robot(robot, state)
    assert robot.action is not None
    assert robot.action.start == state.current_turn


def test_get_associated_location():
    assert Agent.get_associated_location("mining_foo") == Location.FOO
    with pytest.raises(ValueError):
        Agent.get_associated_location("unknown_activity")


def test_get_associated_action():
    assert Agent.get_associated_action("mining_foo") == ActionType.MINE_FOO
    with pytest.raises(ValueError):
        Agent.get_associated_action("unknown_activity")


def test_make_robot_do_ok_case():
    agent = Agent()
    robot = Robot(1)
    state = State()
    state.current_turn = randint(2, 15)
    agent.make_robot_do(robot, state, "mining_foo")
    assert robot in agent.mining_foo
    assert robot.action.start == state.current_turn
    assert robot.action.type == ActionType.MOVE
    assert robot.action.destination == Location.FOO
    state.current_turn = randint(16, 25)
    robot.location = Location.FOO
    agent.make_robot_do(robot, state, "mining_foo")
    assert robot in agent.mining_foo
    assert robot.action.start == state.current_turn
    assert robot.action.type == ActionType.MINE_FOO


def test_make_robot_do_error_case():
    agent = Agent()
    robot = Robot(1)
    state = State()
    state.current_turn = randint(2, 15)
    with pytest.raises(ValueError):
        agent.make_robot_do(robot, state, "macarena")
