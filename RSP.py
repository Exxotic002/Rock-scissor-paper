import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import random
from datetime import datetime
import sys

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock-Paper-Scissors Game")

        self.complex = 2
        self.first = True
        self.play = 0
        self.papergl = 0
        self.rockgl = 0
        self.scissorgl = 0
        self.actions = ["Rock", "Scissor", "Paper"]
        self.last = deque(maxlen=self.complex)

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Welcome to the Rock-Paper-Scissors game!\nHere are the rules:\nYou have to beat the opponent with a winning move\nScissor > Paper\nPaper > Rock\nRock > Scissor")
        self.label.pack(padx=10, pady=10)

        self.start_button = ttk.Button(self, text="Start", command=self.logic)
        self.start_button.pack(padx=10, pady=10)

    def logic(self):
        self.label.config(text="Choose your move: Rock, Scissor, Paper")
        self.start_button.config(state=tk.DISABLED)

        self.move_var = tk.StringVar()
        self.move_entry = ttk.Entry(self, textvariable=self.move_var)
        self.move_entry.pack(padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.process_move)
        self.submit_button.pack(padx=10, pady=10)

    def process_move(self):
        move = self.move_var.get().title()

        if move in self.actions:
            self.move_entry.destroy()
            self.submit_button.destroy()

            self.label.config(text=f"You chose {move}")

            if move in self.actions:
                setattr(self, f"{move.lower()}gl", getattr(self, f"{move.lower()}gl") + 1)

            rules = {
                "Rock": {"Rock": "Draw!", "Paper": "You lose!", "Scissor": "You win!"},
                "Paper": {"Rock": "You win!", "Paper": "Draw!", "Scissor": "You lose!"},
                "Scissor": {"Rock": "You lose!", "Paper": "You win!", "Scissor": "Draw!"}
            }

            self.last.append(move)
            self.vs(move, rules)

            if len(self.last) > self.complex:
                self.last.popleft()

            self.play += 1

            play_again = ttk.Button(self, text="Play Again", command=self.reset)
            play_again.pack(padx=10, pady=10)

        else:
            self.label.config(text="Invalid input. Please choose Rock, Scissor, or Paper.")

    def reset(self):
        self.label.config(text="Welcome to the Rock-Paper-Scissors game!\nHere are the rules:\nYou have to beat the opponent with a winning move\nScissor > Paper\nPaper > Rock\nRock > Scissor")
        self.start_button.config(state=tk.NORMAL)
        self.play = 0
        self.first = True
        self.last.clear()
        self.destroy_widgets()

    def destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def vs(self, myself, rules):
        enemy = self.bias(myself)
        result = rules[myself][enemy]
        if self.play > 1:
            print(self.last[0])
            print(self.last[1])
        print(result)

    def bias(self, myself):
        enemy = ""
        move_counts = {move: self.last.count(move) for move in self.actions}
        enemy = random.choice(self.actions)

        if self.play < 1:
            print(f"The opponent chose {enemy}")
        else:
            if self.last[0] == self.last[1]:
                move_counts[self.last[1]] -= 1
                move_counts[enemy] += 1.1

            enemy = max(move_counts, key=move_counts.get)
            print(f"The opponent chose {enemy}")

            self.print_score(move_counts["Paper"], move_counts["Rock"], move_counts["Scissor"])

        self.first = True
        return enemy

    def print_score(self, paperpoints, rockpoints, scissorpoints, output_file=None):
        if self.first:
            if output_file:
                formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(output_file, 'a') as f:
                    f.write(f"{formatted_datetime}\n\nRock     Paper     Scissor\n")

        self.first = False

        output = f" {rockpoints}         {paperpoints}          {scissorpoints}\n"
        if output_file:
            with open(output_file, 'a') as f:
                f.write(output)
        else:
            print(output)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    