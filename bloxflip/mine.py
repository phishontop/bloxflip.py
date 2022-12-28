from .utilities.errors import MineGameError
from dataclasses import dataclass


@dataclass
class Movement:
    """Represents the response from undiscovering a spot on the grid"""
    multiplier: float
    exploded: bool


class MineGame:
    """Represents a game of the Mines gamemode on bloxflip"""

    def __init__(self, session, info: dict) -> None:
        self.session = session
        self.game_id = info["uuid"]
        self.bet_amount = info["betAmount"]
        self.mines_amount = info["minesAmount"]
        self.multiplier = None
        self.exploded = False
        self.cashed_out = False

    def get_multiplier(self, response_info: dict) -> float:
        """
        Gets the multiplier from the move action.

        :argument: the json response from the move
        :return: Multiplier returns 0 if exploded.
        """
        if response_info["success"]:
            if response_info["exploded"]:
                self.exploded = True
                return 0

            else:
                return response_info["multiplier"]

    def raise_errors(self) -> None:
        """
        Raises errors if each condition is met.
        """
        if self.exploded:
            raise MineGameError("Game is over, create a new game. The bomb has been found")

        if self.cashed_out:
            raise MineGameError("You have already cashed out, create a new game")

    def move(self, place: int) -> Movement:
        """
        Undiscovers a location on the grid.
        :argument: place or grid location must be between 0 - 24.
        :return: Movement dataclass object holding the multiplier and if exploded.
        """
        self.raise_errors()

        if -1 < place < 25:
            response = self.session.post(
                url="https://api.bloxflip.com/games/mines/action",
                json={"cashout": False, "mine": place}
            )
            response_json = response.json()

            self.multiplier = self.get_multiplier(response_info=response_json)
            return Movement(multiplier=self.multiplier, exploded=response_json["exploded"])

        else:
            raise MineGameError("Invalid place, must be between 0 - 24")

    def cashout(self):
        """
        Cashes out the current game.
        :return: if the multiplier is more than 1x returns True else False
        """
        self.raise_errors()

        if self.multiplier > 1:
            self.session.post(
                url="https://api.bloxflip.com/games/mines/action",
                json={"cashout": True}
            )

            self.cashed_out = True
            return self.cashed_out

        else:
            return False
