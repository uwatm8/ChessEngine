import berserk
client = berserk.Client()

upgradeToBot = False
if upgradeToBot:
    client.account.upgrade_to_bot()

token = ""

with open('.apitoken') as f:
    token = f.read().replace("\n", "")

session = berserk.TokenSession("" + token)
client = berserk.Client(session)

def should_accept(arg):
    return True




is_polite = True
for event in client.bots.stream_incoming_events():
    if event['type'] == 'challenge':
        if should_accept(event):
            client.bots.accept_challenge(event['challenge']['id'])
        elif is_polite:
            client.bots.decline_challenge(event['challenge']['id'])
        elif event['type'] == 'gameStart':
            game = Game(event['id'])
            game.start()
