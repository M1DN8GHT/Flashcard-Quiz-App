"""
Flashcard Quiz App
"""

import tkinter as tk
from tkinter import messagebox
import random
import json

class FlashcardQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("400x200")

        self.questions = []
        self.load_questions()

        self.current_question_index = -1
        self.showing_answer = False

        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack()

        self.flip_button = tk.Button(root, text="Flip", command=self.flip_card)
        self.flip_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_card)
        self.next_button.pack()

        self.previous_button = tk.Button(root, text="Previous", command=self.previous_card)
        self.previous_button.pack()

        self.shuffle_button = tk.Button(root, text="Shuffle", command=self.shuffle_cards)
        self.shuffle_button.pack()

    def load_questions(self):
        with open("flashcards.json") as file:
            self.questions = json.load(file)

    def shuffle_cards(self):
        random.shuffle(self.questions)
        self.current_question_index = -1
        self.next_card()

    def next_card(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            self.current_question_index = 0
        self.showing_answer = False
        self.display_question()

    def previous_card(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
        else:
            self.current_question_index = len(self.questions) - 1
        self.showing_answer = False
        self.display_question()

    def display_question(self):
        self.question_label.config(text=self.questions[self.current_question_index]["question"])

    def flip_card(self):
        if self.showing_answer:
            self.question_label.config(text=self.questions[self.current_question_index]["question"])
        else:
            self.question_label.config(text=self.questions[self.current_question_index]["answer"])
        self.showing_answer = not self.showing_answer

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardQuizApp(root)
    root.mainloop()
