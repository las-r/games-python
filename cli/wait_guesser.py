import random
import time

# wait guesser
# made by las-r on github

# settings
accu = 3
maxwait = 5

# wait
wait = round(random.random() * maxwait, accu)
print("Starting the wait in 1 second...\n")
time.sleep(1)
print("Start!")
time.sleep(wait)
print("Finish!")

# user guess
guess = float(input("\nEnter the amount of seconds you waited: "))

# results
print(f"\nYou waited for {wait} second(s).")
print(f"You were {round(abs(wait - guess), accu)} second(s) off.")
