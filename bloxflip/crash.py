

class CrashRound:
    """Represents a round of the game-mode crash on bloxflip"""

    def __init__(self, info: dict) -> None:
        self.crash_point = info["crashPoint"]
        self.id = info["_id"]
        self.public_seed = info["publicSeed"]
        self.private_seed = info["privateSeed"]
        self.private_hash = info["privateHash"]
