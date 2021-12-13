import pytest
from src.model.materials import Bar, Foo, Foobar
from src.model.state import BuyError, SellError, State


def test_add_robot():
    state = State()
    current_robot_number = len(state.robot_list)
    state.add_robot()
    assert len(state.robot_list) == current_robot_number + 1
    state.add_robot()
    state.add_robot()
    assert len(state.robot_list) == current_robot_number + 3


def test_add_foo():
    state = State()
    current_foo_quantity = len(state.foo_inventory)
    current_foo_number = state.foo_number
    state.add_foo()
    assert len(state.foo_inventory) == current_foo_quantity + 1
    assert state.foo_number == current_foo_number + 1


def test_lose_foo_ok_case():
    state = State()
    state.foo_inventory = [Foo(1), Foo(2)]
    current_foo_quantity = len(state.foo_inventory)
    current_foo_number = state.foo_number
    state.lose_foo()
    assert len(state.foo_inventory) == current_foo_quantity - 1
    assert state.foo_number == current_foo_number


def test_lose_foo_error_case():
    state = State()
    state.foo_inventory = []
    with pytest.raises(IndexError):
        state.lose_foo()


def test_add_bar():
    state = State()
    current_bar_quantity = len(state.bar_inventory)
    current_bar_number = state.bar_number
    state.add_bar()
    assert len(state.bar_inventory) == current_bar_quantity + 1
    assert state.bar_number == current_bar_number + 1


def test_add_foobar_ok_case():
    state = State()
    state.foo_inventory = [Foo(1)]
    state.bar_inventory = [Bar(1)]
    current_foo_quantity = len(state.foo_inventory)
    oldest_foo_serial = state.foo_inventory[0].serial
    current_bar_quantity = len(state.bar_inventory)
    oldest_bar_serial = state.bar_inventory[0].serial
    current_foobar_quantity = len(state.foobar_inventory)
    state.add_foobar()
    assert len(state.foo_inventory) == current_foo_quantity - 1
    assert len(state.bar_inventory) == current_bar_quantity - 1
    assert len(state.foobar_inventory) == current_foobar_quantity + 1
    last_foobar = state.foobar_inventory[-1]
    assert last_foobar.foo_serial == oldest_foo_serial
    assert last_foobar.bar_serial == oldest_bar_serial


def test_add_foobar_error_case():
    state = State()
    state.foo_inventory = []
    state.add_bar()
    with pytest.raises(IndexError):
        state.add_foobar()
    state.bar_inventory = []
    state.add_foo()
    with pytest.raises(IndexError):
        state.add_foobar()


def test_sell_foobars_ok_case():
    state = State()
    state.foobar_inventory = [
        Foobar(1, 1),
        Foobar(2, 2),
        Foobar(3, 3),
        Foobar(4, 4),
        Foobar(5, 5),
        Foobar(6, 6),
    ]
    state.money = 0
    number_sold = state.sell_foobars()
    assert number_sold == 5
    assert len(state.foobar_inventory) == 1
    assert state.money == 5
    number_sold = state.sell_foobars()
    assert number_sold == 1
    assert len(state.foobar_inventory) == 0
    assert state.money == 6


def test_sell_foobars_error_case():
    state = State()
    state.foobar_inventory = []
    with pytest.raises(SellError):
        state.sell_foobars()


def test_buy_robots_ok_case():
    state = State()
    # Have enough foo and money to buy 1
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6), Foo(7)]
    state.money = 4
    state.robot_list = []
    number_bought = state.buy_robots()
    assert number_bought == 1
    assert len(state.robot_list) == 1
    assert len(state.foo_inventory) == 1
    assert state.money == 1
    # Have enough foo to buy 2 and money to buy 1
    state.foo_inventory = [
        Foo(1),
        Foo(2),
        Foo(3),
        Foo(4),
        Foo(5),
        Foo(6),
        Foo(7),
        Foo(8),
        Foo(9),
        Foo(10),
        Foo(11),
        Foo(12),
        Foo(13),
    ]
    state.money = 4
    state.robot_list = []
    number_bought = state.buy_robots()
    assert number_bought == 1
    assert len(state.robot_list) == 1
    assert len(state.foo_inventory) == 7
    assert state.money == 1
    # Have enough foo to buy 1 and money to buy 2
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6), Foo(7)]
    state.money = 7
    state.robot_list = []
    number_bought = state.buy_robots()
    assert number_bought == 1
    assert len(state.robot_list) == 1
    assert len(state.foo_inventory) == 1
    assert state.money == 4
    # Have enough foo and money to buy 2
    state.foo_inventory = [
        Foo(1),
        Foo(2),
        Foo(3),
        Foo(4),
        Foo(5),
        Foo(6),
        Foo(7),
        Foo(8),
        Foo(9),
        Foo(10),
        Foo(11),
        Foo(12),
        Foo(13),
    ]
    state.money = 7
    state.robot_list = []
    number_bought = state.buy_robots()
    assert number_bought == 2
    assert len(state.robot_list) == 2
    assert len(state.foo_inventory) == 1
    assert state.money == 1


def test_buy_robots_error_case():
    state = State()
    # Have not enough foo and money to buy
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4)]
    state.money = 1
    with pytest.raises(BuyError):
        state.buy_robots()
    # Have enough foo to buy 1 but not enough money
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4), Foo(5), Foo(6), Foo(7)]
    state.money = 2
    with pytest.raises(BuyError):
        state.buy_robots()
    # Have enough money to buy 1 but not enough foo
    state.foo_inventory = [Foo(1), Foo(2), Foo(3), Foo(4)]
    state.money = 5
    with pytest.raises(BuyError):
        state.buy_robots()
