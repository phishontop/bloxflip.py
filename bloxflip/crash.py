from typing import Union
import requests


class Round:
    """Represents a round of the game-mode crash on bloxflip"""

    def __init__(self, info: dict) -> None:
        self.crash_point = info["crashPoint"]
        self.id = info["_id"]
        self.public_seed = info["publicSeed"]
        self.private_seed = info["privateSeed"]
        self.private_hash = info["privateHash"]


class Crash:

    def __init__(self, headers) -> None:
        self.headers = headers

    @property
    def history(self) -> Union[list[Round]]:
        rounds = []
        response = requests.get("https://rest-bf.blox.land/games/crash", headers=self.headers)
        for round_info in response.json()["history"]:
            rounds.append(Round(round_info))

        return rounds
