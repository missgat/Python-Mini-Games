import random

def play_hangman():
    # 1. Setup a word bank
    word_bank = ["arkansas", "california", "jamaica", "montego bay", "reggae", "sunshine"]
    secret_word = random.choice(word_bank)
    
    # 2. Track game state
    hidden_word = ["_"] * len(secret_word)
    guessed_letters = []
    lives = 6
    
    print("====================================")
    print("🪓 WELCOME TO TERMINAL HANGMAN 🪓")
    print("====================================")
    
    # 3. Main Game Loop
    while lives > 0 and "_" in hidden_word:
        print(f"\nWord: {" ".join(hidden_word)}")
        print(f"Lives remaining: {lives}")
        print(f"Guessed letters: {', '.join(guessed_letters) if guessed_letters else 'None'}")
        
        guess = input("Guess a letter: ").lower().strip()
        
        # Validation checks
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single, valid alphabetical letter.")
            continue
        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'! Try a different one.")
            continue
            
        # Add to tracking list
        guessed_letters.append(guess)
        
        # 4. Check if the guess is in the secret word
        if guess in secret_word:
            print(f"✅ Nice! '{guess}' is in the word.")
            # Swap out underscores with the correct letter at the exact right position
            for index, letter in enumerate(secret_word):
                if letter == guess:
                    hidden_word[index] = guess
        else:
            print(f"❌ Oops! '{guess}' is not in the word.")
            lives -= 1
            
    # 5. Game Over conditions
    if "_" not in hidden_word:
        print(f"\n🎉 CONGRATULATIONS! You saved them! The word was: {secret_word.upper()}")
    else:
        print(f"\n💥 GAME OVER! You ran out of lives. The word was: {secret_word.upper()}")

if __name__ == "__main__":
    play_hangman()
