import tkinter as tk
from tkinter import messagebox
from BorrowingManager import BorrowingManager

class BorrowReturnGui:
    def __init__(self):
        self.borrowing_manager = BorrowingManager()
        self.root = tk.Tk()
        self.root.title("Borrow and Return Books")
        self.root.geometry("500x400")
        self.build_gui()

    def build_gui(self):
        # Borrow Book Section
        borrow_frame = tk.Frame(self.root)
        tk.Label(borrow_frame, text="Borrow a Book", font=("Arial", 14)).pack(pady=10)

        tk.Label(borrow_frame, text="Title").pack()
        self.borrow_title_entry = tk.Entry(borrow_frame)
        self.borrow_title_entry.pack()

        tk.Label(borrow_frame, text="Username").pack()
        self.borrow_user_entry = tk.Entry(borrow_frame)
        self.borrow_user_entry.pack()

        tk.Button(borrow_frame, text="Borrow Book", command=self.borrow_book).pack(pady=10)
        borrow_frame.pack(pady=20)

        # Return Book Section
        return_frame = tk.Frame(self.root)
        tk.Label(return_frame, text="Return a Book", font=("Arial", 14)).pack(pady=10)

        tk.Label(return_frame, text="Title").pack()
        self.return_title_entry = tk.Entry(return_frame)
        self.return_title_entry.pack()

        tk.Label(return_frame, text="Username").pack()
        self.return_user_entry = tk.Entry(return_frame)
        self.return_user_entry.pack()

        tk.Button(return_frame, text="Return Book", command=self.return_book).pack(pady=10)
        return_frame.pack(pady=20)

        # Waiting List Section
        tk.Button(self.root, text="View Waiting List", command=self.view_waiting_list).pack(pady=10)

    def borrow_book(self):
        title = self.borrow_title_entry.get()
        username = self.borrow_user_entry.get()

        if not (title and username):
            messagebox.showerror("Error", "Both Title and Username are required.")
            return

        result = self.borrowing_manager.borrow_book(title, username)
        messagebox.showinfo("Borrow Book", result)

    def return_book(self):
        title = self.return_title_entry.get()
        username = self.return_user_entry.get()

        if not (title and username):
            messagebox.showerror("Error", "Both Title and Username are required.")
            return

        result = self.borrowing_manager.return_book(title, username)
        messagebox.showinfo("Return Book", result)

    def view_waiting_list(self):
        title = self.borrow_title_entry.get()

        if not title:
            messagebox.showerror("Error", "Enter the title to view its waiting list.")
            return

        book = self.borrowing_manager.get_book_by_title(title)
        if not book:
            messagebox.showinfo("Waiting List", f"Book '{title}' not found.")
            return

        waiting_list = book.waiting_list
        if not waiting_list:
            messagebox.showinfo("Waiting List", f"No users in the waiting list for '{title}'.")
        else:
            waiting_list_str = "\n".join(waiting_list)
            messagebox.showinfo("Waiting List", f"Waiting List for '{title}':\n{waiting_list_str}")

    def run(self):
        self.root.mainloop()

