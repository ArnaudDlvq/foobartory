from unittest.mock import patch
from src.model.materials import Bar, Foo, Foobar
from src.model.state import State
from src.model.action import Action, ActionType
from src.model.robot import Location, Robot
from src.engine import evaluate_action_result, evaluate_foobar_assembly


def test_evaluate_move_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    robot.action = Action(0, ActionType.MOVE, Location.FOO)
    evaluate_action_result(robot, state)
    assert robot.location == Location.FOO


def test_evaluate_mining_foo_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    state.foo_inventory = []
    state.foo_number = 0
    robot.location = Location.FOO
    robot.action = Action(0, ActionType.MINE_FOO)
    with patch("src.model.state.State.add_foo") as mock_add_foo:
        evaluate_action_result(robot, state)
        mock_add_foo.assert_any_call()
    robot.location = Location.HOME
    with patch("src.model.state.State.add_foo") as mock_add_foo:
        evaluate_action_result(robot, state)
        mock_add_foo.assert_not_called()


def test_evaluate_mining_bar_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    state.bar_inventory = []
    state.bar_number = 0
    robot.location = Location.BAR
    robot.action = Action(0, ActionType.MINE_BAR)
    with patch("src.model.state.State.add_bar") as mock_add_bar:
        evaluate_action_result(robot, state)
        mock_add_bar.assert_any_call()
    robot.location = Location.HOME
    with patch("src.model.state.State.add_bar") as mock_add_bar:
        evaluate_action_result(robot, state)
        mock_add_bar.assert_not_called()


def test_evaluate_foobar_assembly():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    with patch("src.model.state.State.add_foobar") as mock_add_foobar:
        evaluate_foobar_assembly(robot, state, 60)
        mock_add_foobar.assert_any_call()
    with patch("src.model.state.State.add_foobar") as mock_add_foobar:
        with patch("src.model.state.State.lose_foo") as mock_lose_foo:
            evaluate_foobar_assembly(robot, state, 61)
            mock_lose_foo.assert_any_call()
            mock_add_foobar.assert_not_called()


def test_evaluate_foobar_assemble_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    state.foo_inventory = [Foo(1)]
    state.bar_inventory = [Bar(1)]
    robot.location = Location.ASSEMBLY
    robot.action = Action(0, ActionType.ASSEMBLE)
    evaluate_action_result(robot, state)
    assert len(state.foo_inventory) == 0
    robot.location = Location.HOME
    state.foo_inventory = [Foo(1)]
    state.bar_inventory = [Bar(1)]
    evaluate_action_result(robot, state)
    assert len(state.foo_inventory) == 1
    robot.location = Location.ASSEMBLY
    state.bar_inventory = []
    evaluate_action_result(robot, state)
    assert len(state.foo_inventory) == 1


def test_evaluate_sell_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    state.foobar_inventory = [Foobar(1, 1)]
    robot.location = Location.SELL
    robot.action = Action(0, ActionType.SELL)
    with patch("src.model.state.State.sell_foobars") as mock_sell:
        evaluate_action_result(robot, state)
        mock_sell.assert_any_call()
    robot.location = Location.HOME
    state.foobar_inventory = [Foobar(1, 1)]
    with patch("src.model.state.State.sell_foobars") as mock_sell:
        evaluate_action_result(robot, state)
        mock_sell.assert_not_called()
    robot.location = Location.SELL
    state.foobar_inventory = []
    with patch("src.model.state.State.sell_foobars") as mock_sell:
        evaluate_action_result(robot, state)
        mock_sell.assert_not_called()


def test_evaluate_buy_result():
    state = State()
    robot = Robot(1)
    state.robot_list = [robot]
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6)]
    state.money = 3
    robot.location = Location.BUY
    robot.action = Action(0, ActionType.BUY)
    with patch("src.model.state.State.buy_robots") as mock_buy:
        evaluate_action_result(robot, state)
        mock_buy.assert_any_call()
    robot.location = Location.HOME
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6)]
    state.money = 3
    with patch("src.model.state.State.buy_robots") as mock_buy:
        evaluate_action_result(robot, state)
        mock_buy.assert_not_called()
    robot.location = Location.BUY
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5)]
    state.money = 3
    with patch("src.model.state.State.buy_robots") as mock_buy:
        evaluate_action_result(robot, state)
        mock_buy.assert_not_called()
    robot.location = Location.BUY
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6)]
    state.money = 2
    with patch("src.model.state.State.buy_robots") as mock_buy:
        evaluate_action_result(robot, state)
        mock_buy.assert_not_called()
