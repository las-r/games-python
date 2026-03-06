from itertools import zip_longest
import random

# doublets
# made by las-r on github

# THIS REQUIRES A WORD LIST AT "/words.txt"
# ONE CAN BE FOUND HERE: 
# https://docs.google.com/document/d/1tuuCZaK_xeULAprobjxAHfJU8u2sKiR2fC6P0x5c_vU/edit?tab=t.0

# helper functions
def rchoice(l, x):
    choice = random.choice(l)
    while choice == x:
        choice = random.choice(l)
    return choice

def ctry(c, l):
    c = c.upper()
    d = [(i, j) for i, j in zip_longest(c, l, fillvalue="") if i != j]
    if c not in words or len(d) != 1 or c == l:
        print("Invalid guess.")
        return ctry(input(), l)
    return c
  
# words list
with open("words.txt") as wf:
    words = [word.strip() for word in wf.readlines()]

# game vars
target = rchoice(words, "")
current = rchoice(words, target)
last = ""
guesses = 0

# game loop
while current != target:
    print(f"{guesses + 1}: {current} - {target}")
    
    l = current
    current = ctry(input(), l)
    guesses += 1
    
    print()

# results
if guesses == 1:
    print(f"Won in {guesses} guess.")
else:
    print(f"Won in {guesses} guesses.")
