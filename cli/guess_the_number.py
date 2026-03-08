import random

# random number guessing game
# made by las-r on github

# settings
rmin, rmax = 1, 1000

# game variables
rand = random.randint(rmin, rmax)
guess = rmax + 1
guesses = 0

# game loop
while guess != rand:
    guess = int(input("Enter a guess: "))
    guesses += 1
    
    if guess > rand:
        print("Lower!")
    elif guess < rand:
        print("Higher!")
    else:
        break

# results
print(f"Guessed in {guesses} tries.")
