import random
import requests

HANGMAN_ART = {0: ("   ",
                                   "   ",
                                   "   "),
                             1: (" o ",
                                   "   ",
                                   "   "),
                             2: (" o ",
                                   " | ",
                                   "   "),
                             3: (" o ",
                                   "/| ",
                                   "   "),
                             4: (" o ",
                                  "/|\\",
                                   "   "),
                              5: (" o ",
                                   "/|\\",
                                   "/  "),
                              6: (" o ",
                                   "/|\\",
                                   "/ \\")}      

class Hangman():
      def __init__(self, word_list, max_attempts):
            self.word_list = word_list
            self.max_attempts = max_attempts

      def generate_word(self):
            return random.choice(self.word_list).strip()
      
      def start(self):
            if input("Press <ENTER> to start") == "":
                  selected_word = self.generate_word().upper()

                  while len(selected_word) > 8 or len(selected_word) < 3:
                        selected_word = self.generate_word().upper()

                  user_inputs = set()
                  won = False
                  attempt = 0

                  self.display_hangman(0)
                  self.display_word(selected_word, [])

                  while attempt < self.max_attempts:
                        guess = input("Guess a letter: ").upper()[:1]
                        user_inputs.add(guess)

                        if self.same_word(selected_word, user_inputs):
                              won = True
                              break
                        
                        attempt += 1 if guess not in selected_word else 0

                        self.display_hangman(attempt)
                        self.display_word(selected_word, user_inputs)
                  
                  if won:
                        self.display_word(selected_word, user_inputs)
                        print("Congratulations! You won!")
                  else:
                        print("You lost...")
                        print("The word was: ", selected_word)

                  self.start()
            else:
                  print("Thanks for playing!")
                  exit()

      def same_word(self, selected_word, user_inputs):
            return all(c in user_inputs for c in selected_word)

      def display_word(self, selected_word, user_inputs):
            print(" ".join([selected_word[i] if selected_word[i] in user_inputs else "_" for i in range(len(selected_word))]))
      
      def display_hangman(self, attempt):
            for line in HANGMAN_ART[attempt//2]:
                  print(line)

if __name__ == "__main__":
      print("Welcome to Hangman!")
      word_list = requests.get("https://github.com/dwyl/english-words/blob/master/words.txt").text.splitlines()
      Hangman(word_list=word_list, max_attempts=12).start()
