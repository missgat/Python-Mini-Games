import random

def play_rpsls():
    # 1. Define the rulebook
    RULES = {
        "rock": ["lizard", "scissors"],
        "paper": ["rock", "spock"],
        "scissors": ["paper", "lizard"],
        "lizard": ["spock", "paper"],
        "spock": ["scissors", "rock"]
    }
    
    options = list(RULES.keys())
    
    print("=========================================")
    print("🖖 ROCK, PAPER, SCISSORS, LIZARD, SPOCK 🦎")
    print("=========================================")
    print(f"Choices: {', '.join([o.capitalize() for o in options])}")
    
    while True:
        # 2. Get Player Input
        player_choice = input("\nMake your choice (or type 'quit' to exit): ").lower().strip()
        
        if player_choice == 'quit':
            print("Thanks for playing!")
            break
            
        if player_choice not in options:
            print("❌ Invalid choice. Check your spelling and try again!")
            continue
            
        # 3. Get Computer Input
        computer_choice = random.choice(options)
        print(f"🤖 Computer chose: {computer_choice.capitalize()}")
        
        # 4. Evaluate Game Logic using the Dictionary
        if player_choice == computer_choice:
            print("👔 It's a tie!")
        elif computer_choice in RULES[player_choice]:
            print(f"🎉 You win! {player_choice.capitalize()} beats {computer_choice.capitalize()}.")
        else:
            print(f"😢 You lose! {computer_choice.capitalize()} beats {player_choice.capitalize()}.")

if __name__ == "__main__":
    play_rpsls()
