from bloxflip.client import Client

client = Client(auth_token='secret-token-auth-token-here')

account = client.get_account_info()
print(f"Authenticated User: {account.username}")
print(f"Games Played: {account.game.played}")

history = client.get_crash_history()
for crash_round in history:
    print(crash_round.id)
    print(crash_round.crash_point)
