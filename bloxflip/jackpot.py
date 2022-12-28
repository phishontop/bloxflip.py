

class JackpotPlayer:
    """Represents a user who has joined a jackpot game."""

    def __init__(self, info: dict) -> None:
        self.roblox_id = info["_id"]
        self.username = info["username"]
        self.amount = info["betAmount"]
        self.winning_percentage = info["winningPercentage"]


class JackpotRound:
    """Represents the current round of the jackpot gamemode."""

    def __init__(self, round_info: dict) -> None:
        self.id = round_info["_id"]
        self.players = [
            JackpotPlayer(player)
            for player in round_info["players"]
        ]
        self.time_remaining = round_info["timeLeft"]
        self.winner = round_info["winner"]
