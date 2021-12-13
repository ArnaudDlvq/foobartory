from src.model.action import Action, ActionType


def test_get_duration():
    assert Action.get_duration(ActionType.MINE_BAR) <= 4
    assert Action.get_duration(ActionType.MINE_BAR) >= 1
