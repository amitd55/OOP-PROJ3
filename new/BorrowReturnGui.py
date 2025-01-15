import tkinter as tk
from tkinter import messagebox

class BorrowReturnGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Borrow & Return Books")
        self.root.geometry("400x300")
        self.mode = ""  # Mode will be "lend" or "return"

    def build_gui(self, mode):
        """Build the GUI with the specified mode (lend/return)."""
        self.mode = mode  # Store the mode (lend or return)

        tk.Label(self.root, text=f"{self.mode.capitalize()} a Book", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Title").pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        if self.mode == "lend":
            tk.Button(self.root, text="Lend Book", command=self.lend_book).pack(pady=10)
        elif self.mode == "return":
            tk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=10)

    def lend_book(self):
        title = self.title_entry.get()
        username = self.username_entry.get()

        if not (title and username):
            messagebox.showerror("Error", "Both Title and Username are required.")
            return

        # Add lending functionality (you can integrate with your borrowing manager here)
        messagebox.showinfo("Lend Book", f"Book '{title}' lent to {username}")

    def return_book(self):
        title = self.title_entry.get()
        username = self.username_entry.get()

        if not (title and username):
            messagebox.showerror("Error", "Both Title and Username are required.")
            return

        # Add returning functionality (you can integrate with your borrowing manager here)
        messagebox.showinfo("Return Book", f"Book '{title}' returned by {username}")

    def run(self, mode):
        """Run the GUI with the specified mode."""
        self.build_gui(mode)
        self.root.mainloop()
