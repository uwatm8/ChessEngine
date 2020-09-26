import berserk
import time
import itertools
client = berserk.Client()

upgradeToBot = False
if upgradeToBot:
    client.account.upgrade_to_bot()

token = ""

with open('.apitoken') as f:
    token = f.read().replace("\n", "")

session = berserk.TokenSession("" + token)
client = berserk.Client(session)

gameRunning = False






def should_accept(arg):
    return not gameRunning



should_decline_if_in_game = True
for event in client.bots.stream_incoming_events():
    print("asdasd")
    if event['type'] == 'challenge':
        print("event--------------------------------")
        print(event)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if should_accept(event):
            client.bots.accept_challenge(event['challenge']['id'])
            gameID = event['challenge']['id']
            print("starting challange")
            gameRunning = True
            break
        elif should_decline_if_in_game:
            client.bots.decline_challenge(event['challenge']['id'])
            print("declining challange")
        #elif event['type'] == 'gameStart':
        #    game = Game(event['id'])
        #    game.start()
        #    gameRunning = True
        #    print("starting broken game")

print("done with loop")
client.bots.make_move(gameID, 'e2e3')

if not gameRunning:
    print("setting custom id @@@@@@@@@@@@@@@@@@@@@@")
    gameID = "vztNjpfq"
            
print("gameid: ", gameID)

for i in range(10):
    print("looping 2")
    print("looping 3")
    

    gen = client.bots.stream_game_state(gameID)
    print("looping 4")

    for element in gen:
        print("looping in gen")    
        if(list(element)):
            print("looping if")
            print("element: ",element)
        else:
            print("no board")

    
    print("looping 5")
print("done with loop2")

    
