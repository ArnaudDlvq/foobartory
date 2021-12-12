from src.engine import run_game
from src.model.state import GAME_STATE


if __name__ == "__main__":
    GAME_STATE.add_robot()
    GAME_STATE.add_robot()
    run_game()
