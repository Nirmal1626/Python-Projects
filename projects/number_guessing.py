import tkinter as tk
from tkinter import messagebox
import random


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x400")
        self.root.config(bg="#101820")

        self.target = random.randint(1, 100)
        self.attempts = 0

        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self.root,
            text="🎯 Number Guessing Game",
            font=("Helvetica", 20, "bold"),
            bg="#101820",
            fg="#FEE715"
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Guess a number between 1 and 100",
            font=("Arial", 12),
            bg="#101820",
            fg="white"
        ).pack(pady=5)

        # Input Field
        self.entry = tk.Entry(self.root, font=("Arial", 14), justify="center", width=10)
        self.entry.pack(pady=10)

        # Guess Button
        tk.Button(
            self.root,
            text="Submit Guess",
            bg="#007BFF",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.check_guess
        ).pack(pady=10)

        # Feedback Label
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#101820",
            fg="white"
        )
        self.feedback_label.pack(pady=10)

        # Attempts Label
        self.attempts_label = tk.Label(
            self.root,
            text=f"Attempts: {self.attempts}",
            font=("Arial", 12),
            bg="#101820",
            fg="white"
        )
        self.attempts_label.pack(pady=5)

        # Restart Button
        tk.Button(
            self.root,
            text="Restart Game",
            bg="#28A745",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.restart_game
        ).pack(pady=10)

    def check_guess(self):
        guess = self.entry.get().strip()

        if not guess.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return

        guess = int(guess)
        if not (1 <= guess <= 100):
            messagebox.showwarning("Out of Range", "Your guess must be between 1 and 100!")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess == self.target:
            self.feedback_label.config(fg="#00FF00", text=f"🎉 Correct! You guessed it in {self.attempts} attempts.")
            messagebox.showinfo("Winner!", f"Congratulations! You found the number {self.target} in {self.attempts} attempts!")
            self.entry.config(state="disabled")
        elif guess < self.target:
            self.feedback_label.config(fg="#FFD700", text="Too low! Try a higher number.")
        else:
            self.feedback_label.config(fg="#FF6347", text="Too high! Try a lower number.")

    def restart_game(self):
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.feedback_label.config(text="", fg="white")
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
