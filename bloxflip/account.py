

class GameStats:
    """Represents the games the authenticated user has played"""
    def __init__(self, info: dict):
        self.won = info["gamesWon"]
        self.lost = info["gamesLost"]
        self.played = info["gamesPlayed"]


class Account:
    """Represents the authenticated user"""
    def __init__(self, info: dict) -> None:
        self.balance = info["wallet"]
        self.username = info["robloxUsername"]
        self.game = GameStats(info=info)
