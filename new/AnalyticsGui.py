import tkinter as tk
from tkinter import messagebox
from AnalyticsManager import AnalyticsManager

class AnalyticsGui:
    def __init__(self):
        self.analytics_manager = AnalyticsManager()
        self.root = tk.Tk()
        self.root.title("Analytics")
        self.root.geometry("400x300")
        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Top 10 Most Popular Books", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="Show Top 10 Books", command=self.show_top_books).pack(pady=10)

    def show_top_books(self):
        top_books = self.analytics_manager.get_top_books(top_n=10)

        if not top_books:
            messagebox.showinfo("Top Books", "No books to display.")
            return

        books_info = "\n".join(
            [f"{i+1}. {book.title} by {book.author} - Genre: {book.genre}, Popularity Score: {book.loaned_count + len(book.waiting_list)}"
             for i, book in enumerate(top_books)]
        )
        messagebox.showinfo("Top Books", books_info)

    def run(self):
        self.root.mainloop()