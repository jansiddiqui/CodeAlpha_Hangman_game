import random
from words import word_list
import tkinter as tk
from tkinter import messagebox


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    stages = [
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / \\
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |     / 
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|/
        |      |
        |      
        -
        """,
        """
        --------
        |      |
        |      O
        |     \\|
        |      |
        |     
        -
        """,
        """
        --------
        |      |
        |      O
        |      |
        |      |
        |     
        -
        """,
        """
        --------
        |      |
        |      O
        |    
        |      
        |     
        -
        """,
        """
        --------
        |      |
        |      
        |    
        |      
        |     
        -
        """
    ]
    return stages[tries]


def play(word):
    global word_completion, guessed, guessed_letters, guessed_words, tries

    word_completion = list("_" * len(word))
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    # Prefill two letters
    indices = random.sample(range(len(word)), 2)
    for index in indices:
        word_completion[index] = word[index]
        guessed_letters.append(word[index])

    word_completion = "".join(word_completion)

    word_label.config(text=word_completion, fg="blue")
    tries_label.config(text=f"Tries left: {tries}", fg="red")
    hangman_label.config(text=display_hangman(tries), fg="green")
    guess_entry.delete(0, tk.END)


def check_guess():
    global word_completion, guessed, tries

    guess = guess_entry.get().upper()
    guess_entry.delete(0, tk.END)

    if len(guess) == 1 and guess.isalpha():
        if guess in guessed_letters:
            messagebox.showinfo("Info", f"You already guessed the letter {guess}")
        elif guess not in word:
            tries -= 1
            guessed_letters.append(guess)
            tries_label.config(text=f"Tries left: {tries}", fg="red")
            hangman_label.config(text=display_hangman(tries), fg="green")
        else:
            guessed_letters.append(guess)
            word_as_list = list(word_completion)
            indices = [i for i, letter in enumerate(word) if letter == guess]
            for index in indices:
                word_as_list[index] = guess
            word_completion = "".join(word_as_list)
            word_label.config(text=word_completion, fg="blue")
            if "_" not in word_completion:
                guessed = True
    elif len(guess) == len(word) and guess.isalpha():
        if guess in guessed_words:
            messagebox.showinfo("Info", f"You already guessed the word {guess}")
        elif guess != word:
            tries -= 1
            guessed_words.append(guess)
            tries_label.config(text=f"Tries left: {tries}", fg="red")
            hangman_label.config(text=display_hangman(tries), fg="green")
        else:
            guessed = True
            word_completion = word
            word_label.config(text=word_completion, fg="blue")
    else:
        messagebox.showinfo("Info", "Not a valid guess.")

    if guessed:
        messagebox.showinfo("Info", "Congrats, you guessed the word! You win!")
        play(get_word())
    elif tries == 0:
        messagebox.showinfo("Info", f"Sorry, you ran out of tries. The word was {word}. Maybe next time!")
        play(get_word())


def main():
    global word, word_label, tries_label, hangman_label, guess_entry

    word = get_word()

    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("400x500")
    root.configure(bg="turquoise")  # Setting background color
    root.resizable(False, False)

    main_frame = tk.Frame(root, bg="turquoise")
    main_frame.pack(expand=True, fill="both")

    word_label = tk.Label(root, text="_" * len(word), font=("Helvetica", 18), bg="turquoise")
    word_label.pack(pady=10)

    tries_label = tk.Label(root, text=f"Tries left: {6}", font=("Univers", 14), bg="turquoise")
    tries_label.pack(pady=10)

    hangman_label = tk.Label(root, text=display_hangman(6), font=("Helvetica", 14), bg="turquoise")
    hangman_label.pack(pady=10)

    guess_entry = tk.Entry(root, font=("Helvetica", 14), justify='center')
    guess_entry.pack(pady=10)

    guess_button = tk.Button(root, text="Guess", command=check_guess, font=("Helvetica", 14), bg="lightblue")
    guess_button.pack(pady=10)

    reset_button = tk.Button(root, text="Reset Game", command=lambda: play(get_word()), font=("Helvetica", 14), bg="lightcoral")
    reset_button.pack(pady=10)

    root.bind('<Return>', lambda event: check_guess())

    play(word)

    root.mainloop()


if __name__ == "__main__":
    main()
