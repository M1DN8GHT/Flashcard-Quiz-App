import tkinter as tk
from tkinter import simpledialog
import json

class AddEditFlashcards:
    def __init__(self, root, flashcards_file):
        self.root = root
        self.flashcards_file = flashcards_file
        self.load_flashcards()

        self.add_button = tk.Button(root, text="Add Flashcard", command=self.add_flashcard)
        self.add_button.pack()

        self.edit_button = tk.Button(root, text="Edit Flashcard", command=self.edit_flashcard)
        self.edit_button.pack()

    def load_flashcards(self):
        with open(self.flashcards_file) as file:
            self.flashcards = json.load(file)

    def save_flashcards(self):
        with open(self.flashcards_file, 'w') as file:
            json.dump(self.flashcards, file, indent=4)

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        answer = simpledialog.askstring("Input", "Enter the answer:")
        if question and answer:
            self.flashcards.append({"question": question, "answer": answer, "status": "unknown"})
            self.save_flashcards()

    def edit_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question to edit:")
        for flashcard in self.flashcards:
            if flashcard["question"] == question:
                new_question = simpledialog.askstring("Input", "Enter the new question:", initialvalue=flashcard["question"])
                new_answer = simpledialog.askstring("Input", "Enter the new answer:", initialvalue=flashcard["answer"])
                if new_question and new_answer:
                    flashcard["question"] = new_question
                    flashcard["answer"] = new_answer
                    self.save_flashcards()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = AddEditFlashcards(root, "flashcards.json")
    root.mainloop()
