

class AuthenticationError(Exception):
    """Raises an error when authentication is denied, normally means the auth_token or cookie is invalid"""
    pass


class MineGameError(Exception):
    """Raises an error when the MineGame class is misused."""
    pass
