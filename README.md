# foobartory

Challenge foobartory for Alma

## Set up

- Have Python 3 installed (developed with Python 3.9.9)
- (Optional) In the project folder, create a python virtual env and source it
  - `python -m venv venv`
  - `source venv/bin/activate` (or `source venv/Scripts/activate` on Windows)
- `pip install -r requirements.txt`

## Run

`python main.py`

The game will run and you will be able to see it progress through logs until 30 robots are present. You should see the end of actions with their results and the beginning of new actions from the robots.

## Run the tests

`pytest tests/`

## Explanations

The major part of this project is to model the game universe (found in the model folder).

The game execution is in the engine.py file where we have the game execution loop (`run_game`) and the function to impact the game state with the result of the finished actions (`evaluate_action_result`).

The game is done in turns, each being 0.5s. To simplify, the "mine bar" action take between 1 and 4 turns.

In the game execution, when a robot has finished its action, we must have a step which will set the new action of the robot. The project implements an agent with such a method, and calls it at the needed step of the loop. That is where we would replace the call with a method from another agent (for instance, one which would ask for user inputs).

The implemented agent has its own way of organizing its workforce, and has a strategy worked through with trial and error on my part.
