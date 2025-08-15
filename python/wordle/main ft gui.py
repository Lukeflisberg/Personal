import tkinter as tk
import requests
import random

ANSWERS_URL = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/wordle-answers-alphabetical.txt"
GREEN = "#6aaa64"
ORANGE = "#c9b458"
BLACK = "#212121"
GREY = "#787c7e"
WHITE = "#d3d6da"

class WordleUI:
    def __init__(self, master, word, max_attempts):
        self.master = master
        self.word = word
        self.max_attempts = max_attempts
        self.word_length = len(word)
        self.attempt = 0
        self.current_guess = ""
        self.guesses = []
        self.keyboard_state = {}  # letter: color

        self.grid_labels = []
        self.keyboard_buttons = {}

        self.setup_ui()
        self.master.bind("<Key>", self.on_key)

    def setup_ui(self):
        self.master.title("Wordle")
        self.frame = tk.Frame(self.master, bg=BLACK)
        self.frame.pack(padx=20, pady=20)

        # Grid
        for row in range(self.max_attempts):
            row_labels = []
            for col in range(self.word_length):
                lbl = tk.Label(self.frame, text=" ", width=4, height=2, font=("Consolas", 24, "bold"),
                               bg=WHITE, fg=BLACK, relief="groove", borderwidth=2)
                lbl.grid(row=row, column=col, padx=2, pady=2)
                row_labels.append(lbl)
            self.grid_labels.append(row_labels)

        # Keyboard
        kb_frame = tk.Frame(self.master, bg=BLACK)
        kb_frame.pack(pady=(20,0))
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for r, keys in enumerate(rows):
            row_frame = tk.Frame(kb_frame, bg=BLACK)
            row_frame.pack()
            for k in keys:
                btn = tk.Label(row_frame, text=k, width=4, height=2, font=("Consolas", 14, "bold"),
                               bg=GREY, fg=WHITE, relief="raised", borderwidth=2)
                btn.pack(side="left", padx=2, pady=2)
                self.keyboard_buttons[k] = btn

    def on_key(self, event):
        if self.attempt >= self.max_attempts:
            return
        if event.keysym == "BackSpace":
            if len(self.current_guess) > 0:
                self.current_guess = self.current_guess[:-1]
                self.update_grid()
        elif event.keysym == "Return":
            if len(self.current_guess) == self.word_length:
                self.submit_guess()
        elif event.char and event.char.isalpha():
            if len(self.current_guess) < self.word_length:
                self.current_guess += event.char.upper()
                self.update_grid()

    def update_grid(self):
        # Show current guess in the current row
        for i in range(self.word_length):
            char = self.current_guess[i] if i < len(self.current_guess) else " "
            self.grid_labels[self.attempt][i].config(text=char, bg=WHITE, fg=BLACK)

    def submit_guess(self):
        guess = self.current_guess.upper()
        colors = [WHITE] * self.word_length
        word_chars = list(self.word)
        guess_chars = list(guess)

        # First pass: green
        for i in range(self.word_length):
            if guess_chars[i] == word_chars[i]:
                colors[i] = GREEN
                word_chars[i] = None  # Mark as used

        # Second pass: orange
        for i in range(self.word_length):
            if colors[i] == WHITE and guess_chars[i] in word_chars:
                colors[i] = ORANGE
                word_chars[word_chars.index(guess_chars[i])] = None

        # Update grid colors
        for i in range(self.word_length):
            self.grid_labels[self.attempt][i].config(
                text=guess[i],
                bg=colors[i],
                fg=WHITE if colors[i] != WHITE else BLACK
            )

        # Update keyboard colors
        for i in range(self.word_length):
            letter = guess[i]
            btn = self.keyboard_buttons.get(letter)
            if btn:
                if colors[i] == GREEN:
                    btn.config(bg=GREEN, fg=WHITE)
                    self.keyboard_state[letter] = GREEN
                elif colors[i] == ORANGE and self.keyboard_state.get(letter) != GREEN:
                    btn.config(bg=ORANGE, fg=WHITE)
                    self.keyboard_state[letter] = ORANGE
                elif colors[i] == WHITE and self.keyboard_state.get(letter) not in (GREEN, ORANGE):
                    btn.config(bg=BLACK, fg=WHITE)
                    self.keyboard_state[letter] = BLACK

        self.guesses.append(guess)
        self.attempt += 1
        self.current_guess = ""

        if guess == self.word:
            self.show_end_message("Congratulations! You guessed the word!")
        elif self.attempt == self.max_attempts:
            self.show_end_message(f"Game Over! The word was: {self.word}")

    def show_end_message(self, msg):
        popup = tk.Toplevel(self.master)
        popup.title("Game Over")
        tk.Label(popup, text=msg, font=("Consolas", 16)).pack(padx=20, pady=20)
        tk.Button(popup, text="Exit", command=self.master.destroy).pack(pady=(0,20))

def main():
    root = tk.Tk()
    word_list = requests.get(ANSWERS_URL).text.splitlines()
    word = random.choice(word_list).upper().strip()
    app = WordleUI(root, word, max_attempts=6)
    root.mainloop()

if __name__ == "__main__":
    main()