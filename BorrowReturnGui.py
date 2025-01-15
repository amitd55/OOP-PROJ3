import tkinter as tk
from tkinter import messagebox
from classes.BorrowingManager import BorrowingManager

class BorrowReturnGui:
    def __init__(self, borrowing_manager, return_callback=None):
        self.borrowing_manager = borrowing_manager
        self.return_callback = return_callback

        if return_callback:
            self.root = tk.Toplevel()
        else:
            self.root = tk.Tk()

        self.root.title("Borrow & Return Books")
        self.root.geometry("500x400")
        self.root.configure(bg="pink")
        self.current_frame = None

    def build_gui(self, mode):
        self.mode = mode
        if self.current_frame:
            self.current_frame.destroy()

        frame = tk.Frame(self.root, bg="pink")
        tk.Label(frame, text=f"{self.mode.capitalize()} a Book", font=("Arial", 16), bg="pink").pack(pady=20)

        tk.Label(frame, text="Title", bg="pink").pack()
        self.title_entry = tk.Entry(frame, width=40)
        self.title_entry.pack()

        if self.mode == "borrow":
            tk.Button(frame, text="Borrow Book", command=self.lend_book, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)
        elif self.mode == "return":
            tk.Button(frame, text="Return Book", command=self.return_book, bg="blue", fg="white", font=("Arial", 12)).pack(pady=20)

        tk.Button(
            frame,
            text="Back",
            command=self.return_to_main_menu,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
        ).pack(pady=20)

        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def lend_book(self):
        title = self.title_entry.get()

        if not title:
            messagebox.showerror("Error", "The Title field is required.")
            return

        try:
            success = self.borrowing_manager.borrow_book(title)
            if success:
                messagebox.showinfo("Success", f"Book '{title}' borrowed successfully.")
            else:
                messagebox.showerror("Error", f"Failed to borrow the book '{title}'. It may not be available.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def return_book(self):
        title = self.title_entry.get()

        if not title:
            messagebox.showerror("Error", "The Title field is required.")
            return

        try:
            success = self.borrowing_manager.return_book(title)
            if success:
                messagebox.showinfo("Success", f"Book '{title}' returned successfully.")
            else:
                messagebox.showerror("Error", f"Failed to return the book '{title}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def return_to_main_menu(self):
        self.root.destroy()
        if self.return_callback:
            self.return_callback()

    def run(self, mode):
        self.build_gui(mode)
        self.root.mainloop()

if __name__ == "__main__":
    borrowing_manager = BorrowingManager()
    gui = BorrowReturnGui(borrowing_manager)
    gui.run("borrow")
