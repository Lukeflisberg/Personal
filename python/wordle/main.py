import requests
import random

ANSWERS_URL = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/wordle-answers-alphabetical.txt"
GREEN = "\033[92m"
ORANGE = "\033[93m"

class Wordle:
    def __init__(self, word, max_attempts):
        self.word = word
        self.max_attempts = max_attempts
        self.attempt = 0

        self.guesses = []
        self.greens = set()

    def start(self):
        """ Starts the Wordle game loop, prompting the user for guesses and providing feedback in the form of colored letters"""
        print(self.grid())

        while self.attempt < self.max_attempts:
            guess = input("")[:5].upper()

            if guess == self.word:
                print(f"{GREEN}{self.word}")
                exit()
            else:
                self.adjust_colors(guess)
                self.guesses.append(self.format_guess(guess))
                print(self.grid())
                self.attempt += 1
        
        print(f"\nThe word was: {GREEN}{self.word}")
    
    def adjust_colors(self, guess):
        """ Adjusts the sets of greens and oranges based on the current guess """
        for i in range(len(self.word)):
            if guess[i] == self.word[i]:
                self.greens.add(guess[i])

    def format_guess(self, guess):
        """Applies the color formatting to the guess and returns a list of colored characters."""
        formatted_guess = []
        for i in range(len(self.word)):
            if guess[i] == self.word[i]:
                formatted_guess.append(f"{GREEN}{guess[i]}\033[0m")
            elif guess[i] in self.word and guess[i] not in self.greens:
                formatted_guess.append(f"{ORANGE}{guess[i]}\033[0m")
            else:
                formatted_guess.append(guess[i])
        return formatted_guess

    def grid(self):
        """Returns a formatted grid of guesses and remaining attempts"""
        print("\n" * 100)  # Clear the screen

        results = []

        # Join each colored character with a space
        results.extend([" ".join(guess) for guess in self.guesses])

        # Appends rows of _ for remaining attempts
        results.extend(["_ " * len(self.word) for _ in range(self.max_attempts - len(self.guesses))])

        return "\n".join(results)

class WordleGame:
    def __init__(self, word_list, max_attempts):
        self.word_list = word_list
        self.max_attempts = max_attempts
    
    def start_new_game(self):
        def generate_word():
            if word:=random.choice(self.word_list).upper().strip():
                return word
            raise ValueError("No word found in the word list.")

        if input("Press <ENTER> to start the game...") == "":
            word = generate_word()

            Wordle(word=word, max_attempts=self.max_attempts).start()

            self.start_new_game()
        
        print("Thanks for playing!")
        print("exit")

if __name__ == "__main__":
    print("Welcome to Wordle!")
    game = WordleGame(word_list=requests.get(ANSWERS_URL).text.splitlines(), max_attempts=6)
    game.start_new_game()