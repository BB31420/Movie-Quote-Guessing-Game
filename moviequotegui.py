import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class MovieGuessingGame:
    def __init__(self):
        self.quotes = []
        self.correct_guesses = 0
        self.incorrect_guesses = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if not os.path.exists("high_score.txt"):
            with open("high_score.txt", "w") as file:
                file.write("0")
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_quotes(self, filename):
        self.quotes.clear()
        current_quote = ""
        movie_title = ""
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if line.startswith('§'):
                    if movie_title and current_quote:
                        self.quotes.append((movie_title, current_quote.strip()))
                    parts = line[1:].split(' ¤ ', 1)
                    movie_title = parts[0]
                    current_quote = parts[1] if len(parts) > 1 else ""
                
                elif line.startswith('¤'):
                    current_quote += " " + line[1:].strip()
            
            if movie_title and current_quote:
                self.quotes.append((movie_title, current_quote.strip()))
                    
        return self.quotes

    def check_selection(self, correct_answer, selected_answer, score_label, quote_text):
        if selected_answer == correct_answer:
            messagebox.showinfo("Result", "Correct!")
            self.correct_guesses += 1
            score_label["text"] = f"Score: {self.correct_guesses}  |  Lives: {5 - self.incorrect_guesses}  |  High Score: {self.high_score}"
            self.ask_question(quote_text)
        else:
            messagebox.showinfo("Result", f"Wrong! The correct answer is {correct_answer}.")
            self.incorrect_guesses += 1
            score_label["text"] = f"Score: {self.correct_guesses}  |  Lives: {5 - self.incorrect_guesses}  |  High Score: {self.high_score}"
            
            if self.incorrect_guesses >= 5:
                # Check and update high score when the game is over
                if self.correct_guesses > self.high_score:
                    self.high_score = self.correct_guesses
                    self.save_high_score()
                
                messagebox.showinfo("Game Over", f"Game Over! You scored {self.correct_guesses}.")
                self.correct_guesses = 0
                self.incorrect_guesses = 0
                score_label["text"] = f"Score: {self.correct_guesses}  |  Lives: {5 - self.incorrect_guesses}  |  High Score: {self.high_score}"
            else:
                self.ask_question(quote_text)

    def ask_question(self, quote_text):
        if not self.quotes:
            messagebox.showerror("Error", "No quotes loaded from the file. Please check the file and try again.")
            return
        
        movie_title, full_quote = random.choice(self.quotes)
        quote_text.delete(1.0, tk.END)
        quote_text.insert(tk.END, full_quote)
        
        all_titles = [quote[0] for quote in self.quotes]
        incorrect_answers = random.sample([title for title in all_titles if title != movie_title], 3)
        
        answer_options = [movie_title] + incorrect_answers
        random.shuffle(answer_options)
        
        for i in range(4):
            answer_buttons[i]["text"] = answer_options[i]
            answer_buttons[i]["command"] = lambda ans=answer_options[i]: self.check_selection(movie_title, ans, score_label, quote_text)


    def start_game(self, quote_text, score_label):
        filename = 'movie_quotes.txt'
        if not self.quotes:
            self.load_quotes(filename)
        
        self.correct_guesses = 0
        self.incorrect_guesses = 0
        
        self.ask_question(quote_text)

# Create the main application window
root = tk.Tk()
root.title("Movie Title Guessing Game")
root.configure(background='#1e1e1e')  # Set background color

# Initialize the game
game = MovieGuessingGame()

# Create and configure the style
style = ttk.Style()
style.configure('TLabel', foreground='#FFD700', background='#1e1e1e', font=('Arial', 14))
style.configure('TButton', foreground='#ffffff', background='#FF4500', font=('Arial', 12))
style.configure('TScrolledText', foreground='#000000', background='#F5F5F5', font=('Arial', 12))

# Create widgets for the GUI
ttk.Label(root, text="Guess the movie title based on the given quote!", style='TLabel').pack(pady=20)

quote_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
quote_text.pack(pady=20)
quote_text.configure(background='#F5F5F5', foreground='#1e1e1e', font=('Arial', 12))  # Set background and font properties

answer_buttons = []
for i in range(4):
    btn = ttk.Button(root, text="", command=lambda: None, style='TButton')
    btn.pack(pady=5)
    answer_buttons.append(btn)

ttk.Button(root, text="Start Game", command=lambda: game.start_game(quote_text, score_label), style='TButton').pack(pady=20)

score_label = ttk.Label(root, text="Score: 0  |  Lives: 0  |  High Score: 0", style='TLabel')
score_label.pack(pady=20)

root.mainloop()
