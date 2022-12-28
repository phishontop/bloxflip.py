import requests
from typing import Optional, Union

from .account import Account
from .crash import CrashRound
from .jackpot import JackpotRound
from .mine import MineGame
from .utilities.errors import AuthenticationError, MineGameError


class Client:

    def __init__(self, auth_token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "x-auth-token": auth_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
        })

    @classmethod
    def login(cls, cookie: str, code: Optional[str] = None):
        """
        Login with cookie which gets the auth_token to then create a Client object
        :params:
            cookie: the roblox security cookie which allows the program to authenticate as a user
            code: bloxflip affiliate code (doesn't force affiliate like original bloxflip.py)

        :return: Client object.
        """
        response = requests.post(
            url="https://api.bloxflip.com/user/login",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"},
            json={
                "cookie": cookie,
                "affiliateCode": code
            }
        )

        response_json = response.json()
        if response_json["success"]:
            return cls(auth_token=response_json["jwt"])

        else:
            raise AuthenticationError("cookie is invalid")

    def get_account_info(self):
        """
        Factory Pattern for creating an Account object of the authenticated user
        :return: Account Object.
        """
        response = self.session.get("https://rest-bf.blox.land/user")
        response_json = response.json()

        if response_json["success"]:
            user_info = response_json["user"]
            return Account(info=user_info)

        else:
            raise AuthenticationError("auth_token is invalid")

    def get_jackpot_game(self) -> JackpotRound:
        """
        Factory method for creating a JackpotRound object of the current jackpot game

        :return: JackpotRound object
        """
        response = self.session.get("https://api.bloxflip.com/games/jackpot")
        return JackpotRound(response.json()["current"])

    def get_crash_history(self) -> Union[list[CrashRound]]:
        """
        Factory method for creating a list of past CrashRound objects for the previous crash games.

        :return: list: CrashRound objects
        """
        response = self.session.get("https://rest-bf.blox.land/games/crash")
        return [
            CrashRound(round_info)
            for round_info in response.json()["history"]
        ]

    def create_mine_game(self, amount: float, mine_count: int):
        """
        Factory method for creating a mine game object.

        :Arugments:
            amount: The amount of robux you want to play the game with.

        :return: MineGame object.
        """

        if not 0 < mine_count < 25:
            raise MineGameError(f"mine_count must be inbetween 1 - 24 not {mine_count}")

        if amount < 5:
            raise MineGameError(f"amount must be more then 5 not {amount}")

        response = self.session.post(
            url="https://api.bloxflip.com/games/mines/create",
            json={"mines": str(mine_count), "betAmount": amount}
        )

        return MineGame(session=self.session, info=response.json()["game"])


