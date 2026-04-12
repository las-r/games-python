import os
import random

# blackjack
# made by las-r on github

# constants
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALS = {r: (10 if r in ("J", "Q", "K", "10") else (11 if r == "A" else int(r))) for r in RANKS}

# helpers
def clear():
    os.system("cls" if os.name == "nt" else "clear")\
def score(hand):
    score = sum(VALS[card] for card in hand)
    aces = hand.count("A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# variables
deck = [rank for rank in RANKS * 4]
random.shuffle(deck)
plrhand = [deck.pop(), deck.pop()]
bothand = [deck.pop(), deck.pop()]

# blackjack
plrs = score(plrhand)
bots = score(bothand)
if plrs == 21 or bots == 21:
    clear()
    print(f"Your hand:", *plrhand, f"({score(plrhand)})")
    print(f"Bot's hand: X", *bothand[1:])
    print()
    if plrs == 21 and bots == 21:
        print("Both have Blackjack! It's a tie.")
    elif plrs == 21:
        print("Blackjack! You win instantly!")
    else:
        print("Bot has Blackjack! You lose.")
    exit()

# game loop
passes = 0
while passes != 2:
    clear()
    
    # rebuild deck if empty
    if not deck:
        deck = [rank for rank in RANKS * 4]
        random.shuffle(deck)
        
    # reset pass count
    passes = 0
        
    # output
    print(f"Your hand:", *plrhand, f"({score(plrhand)})")
    print(f"Bot's hand: X", *bothand[1:])
    print()
    
    # player move
    move = input("Do you `hit` or `pass`?: ")
    while move not in ("hit", "pass"):
        move = input("Do you `hit` or `pass`?: ")
    if move == "hit":
        plrhand.append(deck.pop())
    else:
        passes += 1
    
    # bot move
    if score(bothand) < 17:
        bothand.append(deck.pop())
    else:
        passes += 1

# final scores
plrs = score(plrhand)
bots = score(bothand)
print(f"\nYour score: {plrs} | Bot score: {bots}\n")
if plrs > 21:
    print("You busted! You lose.")
elif bots > 21:
    print("Bot busted! You win!")
elif plrs == bots:
    print("Push (Tie)!")
elif plrs > bots:
    print("You win!")
else:
    print("You lose!")
