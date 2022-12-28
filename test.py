from bloxflip.client import Client

client = Client(auth_token="enter_token_here")
account = client.get_account_info()
print(f"Authenticated User: {account.username}")

for crash_round in client.get_crash_history():
    print(crash_round.id)
    print(crash_round.crash_point)

jackpot_game = client.get_jackpot_game()
for player in jackpot_game.players:
    print(player.username)
    print(player.amount)

game = client.create_mine_game(amount=5, mine_count=2)
for i in range(2):
    move_info = game.move(place=i)
    print(move_info.exploded)
    print(move_info.multiplier)

game.cashout()
