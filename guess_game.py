import random

def play_game():
    print("====================================")
    print("🎲 WELCOME TO THE NUMBER GUESSING GAME 🎲")
    print("====================================")
    
    # 1. Generate a random secret number
    secret_number = random.randint(1, 20)
    print("I am thinking of a number between 1 and 20.")
    
    # 2. Set up game tracking variables
    allowed_attempts = 5
    attempts_taken = 0
    
    # 3. The Core Game Loop
    while attempts_taken < allowed_attempts:
        try:
            # Get the user's guess and convert it to an integer
            guess = int(input(f"\n[Attempt {attempts_taken + 1}/{allowed_attempts}] Take a guess: "))
        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")
            continue
        
        attempts_taken += 1
        
        # 4. Check the win/loss conditions (Game Logic)
        if guess < secret_number:
            print("🔼 Too low! Try a higher number.")
        elif guess > secret_number:
            print("🔽 Too high! Try a lower number.")
        else:
            print(f"\n🎉 CONGRATULATIONS! You guessed it in {attempts_taken} attempts!")
            return # Exits the function because they won!
            
    # If the loop finishes without guessing correctly
    print(f"\n💥 Game Over! You ran out of guesses. The number was {secret_number}.")

# Run the game
if __name__ == "__main__":
    play_game()
