"""
Flashcard Quiz App
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json

class FlashcardQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("400x200")

        self.review_unknown_only = tk.BooleanVar()
        self.review_unknown_only.set(False)

        self.questions = []
        self.load_questions()

        self.current_question_index = -1
        self.showing_answer = False
        self.quiz_mode = False
        self.quiz_mode_click_count = 0

        self.question_label = tk.Label(root, text="", wraplength=400, font=("Helvetica", 16), justify="center")
        self.question_label.pack(expand=True)

        self.answer_entry = tk.Entry(root)

        self.flip_button = tk.Button(root, text="Flip", command=self.flip_card)
        self.flip_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_card)
        self.next_button.pack()

        self.previous_button = tk.Button(root, text="Previous", command=self.previous_card)
        self.previous_button.pack()

        self.shuffle_button = tk.Button(root, text="Shuffle", command=self.shuffle_cards)
        self.shuffle_button.pack()

        self.known_button = tk.Button(root, text="Known", command=self.mark_known)
        self.known_button.pack()

        self.unknown_button = tk.Button(root, text="Unknown", command=self.mark_unknown)
        self.unknown_button.pack()

        self.review_unknown_button = tk.Button(root, text="Review Unknown", command=self.review_unknown)
        self.review_unknown_button.pack()

        self.quiz_mode_button = tk.Button(root, text="Quiz Mode", command=self.toggle_quiz_mode)
        self.quiz_mode_button.pack()

        self.add_flashcard_button = tk.Button(root, text="Add Flashcard", command=self.add_flashcard)
        self.add_flashcard_button.pack()

        self.review_unknown_check = tk.Checkbutton(root, text="Review Unknown Only", variable=self.review_unknown_only, command=self.filter_questions)
        self.review_unknown_check.pack()

        self.add_edit_button = tk.Button(root, text="Add/Edit Flashcards", command=self.open_add_edit_window)
        self.add_edit_button.pack()

    def load_questions(self):
        with open("flashcards.json") as file:
            self.all_questions = json.load(file)
        self.filter_questions()

    def shuffle_cards(self):
        random.shuffle(self.questions)
        self.current_question_index = -1

    def next_card(self):
        if not hasattr(self, 'question_label'):
            return
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
        question = self.questions[self.current_question_index]["question"]
        self.question_label.config(text=question)
        self.answer_entry.delete(0, tk.END)

    def flip_card(self):
        if self.quiz_mode:
            user_answer = self.answer_entry.get()
            correct_answer = self.questions[self.current_question_index]["answer"]
            if user_answer.lower() == correct_answer.lower():
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", f"The correct answer is: {correct_answer}")
        else:
            if self.showing_answer:
                self.question_label.config(text=self.questions[self.current_question_index]["question"])
            else:
                self.question_label.config(text=self.questions[self.current_question_index]["answer"])
            self.showing_answer = not self.showing_answer

    def mark_known(self):
        self.questions[self.current_question_index]["status"] = "known"
        self.next_card()

    def mark_unknown(self):
        self.questions[self.current_question_index]["status"] = "unknown"
        self.next_card()

    def review_unknown(self):
        self.questions = [q for q in self.all_questions if q["status"] == "unknown"]
        self.current_question_index = -1
        self.next_card()

    def toggle_quiz_mode(self):
        self.quiz_mode_click_count += 1
        if self.quiz_mode_click_count % 2 == 1:
            self.quiz_mode = True
            self.answer_entry.pack()
        else:
            self.quiz_mode = False
            self.answer_entry.pack_forget()
        self.next_card()

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        answer = simpledialog.askstring("Input", "Enter the answer:")
        if question and answer:
            self.all_questions.append({"question": question, "answer": answer, "status": "unknown"})
            with open("flashcards.json", "w") as file:
                json.dump(self.all_questions, file)
            self.filter_questions()

    def filter_questions(self):
        if self.review_unknown_only.get():
            self.questions = [q for q in self.all_questions if q["status"] == "unknown"]
        else:
            self.questions = self.all_questions
        self.current_question_index = -1

    def open_add_edit_window(self):
        # Implement add/edit flashcards logic
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardQuizApp(root)
    root.mainloop()
