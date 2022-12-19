import requests
from .account import Account
from .crash import Crash
from .utilities.errors import AuthenticationError


class Client:

    def __init__(self, auth_token):
        self.headers = {
            "x-auth-token": auth_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
        }

        self.crash = Crash(self.headers)

    @classmethod
    def login(cls, cookie):
        """
        TODO: Login with cookie which gets the auth_token to then create a Client object
        :param: the roblox security cookie which allows the program to authenticate as a user
        :return: Client object.

        """
        return cls(auth_token=cookie)

    def get_account_info(self):
        """Factory Pattern for creating an Account object of the authenticated user
        :return: Account Object.
        """
        response = requests.get("https://rest-bf.blox.land/user", headers=self.headers)
        response_json = response.json()

        if response_json["success"]:
            user_info = response_json["user"]
            return Account(info=user_info)

        else:
            raise AuthenticationError("auth_token is invalid")

    def get_crash_history(self):
        """Factory Pattern for getting the crash games' history (limit: last 30)
        :return: List of the past 30 rounds
        """
        return self.crash.history


