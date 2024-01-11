import random
import sys
from collections import deque

class Main:

    def __init__(self):
        self.complex = 2
        self.first = True
        self.play = 0
        self.papergl = 0
        self.rockgl = 0
        self.scissorgl = 0
        self.actions = ["Rock", "Scissor", "Paper"]
        self.last = deque(maxlen=self.complex)

    def vs(self, myself, rules):
        enemy = self.bias(myself)
        result = rules[myself][enemy]
        if self.play > 1:
            print(self.last[0])
            print(self.last[1])
        print(result)

    def print_score(self, paperpoints, rockpoints, scissorpoints):
        if self.first:
            print(f"Rock     Paper     Scissor\n")
        self.first = False
        print(f" {rockpoints}         {paperpoints}          {scissorpoints}\n")

    def bias(self, myself):
        enemy = ""
        move_counts = {move: self.last.count(move) for move in self.actions}

        if self.play < 1:
            enemy = random.choice(self.actions)
            print(f"The opponent chose {enemy}")
        else:
            if self.play > 1 and self.last[0] == self.last[1]:
                move_counts[self.last[1]] -= 1
            
            enemy = max(move_counts, key=move_counts.get)
            print(f"The opponent chose {enemy}")

            self.print_score(move_counts["Paper"], move_counts["Rock"], move_counts["Scissor"])

            

        self.first = True
        return enemy

    def menu(self):
        print("Welcome to the Rock-Paper-Scissors game!")
        print("Here are the rules:")
        print("You have to beat the opponent with a winning move")
        print("Scissor > Paper\nPaper > Rock\nRock > Scissor")
        print("You can always go back to the menu to see the rules by typing 'menu'\n")
        
        while True:
            user_response = input("Are you ready to play? Type 'Yes' to continue: ").title()
            
            if user_response == "Yes":
                self.logic()
                break  # Exit the loop if the user responds with 'Yes'
            
            print("Please type 'Yes' to continue.")

    def logic(self):
        while True:
            myself = input("Choose your move: Rock, Scissor, Paper \n").title()

            if myself == "Menu":
                self.menu()
                continue 

            if myself in self.actions:
                break
            else:
                print("Invalid input. Please choose Rock, Scissor, or Paper.")

        print(f"You chose {myself}")
        
        if myself in self.actions:
            setattr(self, f"{myself.lower()}gl", getattr(self, f"{myself.lower()}gl") + 1)

        rules = {
            "Rock": {"Rock": "Draw!", "Paper": "You lose!", "Scissor": "You win!"},
            "Paper": {"Rock": "You win!", "Paper": "Draw!", "Scissor": "You lose!"},
            "Scissor": {"Rock": "You lose!", "Paper": "You win!", "Scissor": "Draw!"}
        }
        
        self.last.append(myself)
        self.vs(myself, rules)
        
        if len(self.last) > self.complex:
            self.last.popleft()
        
        self.play += 1

        while True:
            play_again = input("Do you want to play again? Type 'Yes' or 'No': ").title()

            if play_again == "No":
                sys.exit() 
            elif play_again == "Yes":
                self.logic()

            print("Invalid input. Please type 'Yes' or 'No'.")

main_game = Main()
main_game.menu()
