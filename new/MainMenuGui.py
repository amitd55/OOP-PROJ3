import tkinter as tk
from BookManagmentGui import BookManagementGui
from SearchManagerGui import SearchDisplayGui
from BorrowReturnGui import BorrowReturnGui
from AuthGui import AuthGui
from AnalyticsGui import AnalyticsGui
from BookManager import BookManager

class MainMenuGui:
    def __init__(self, user=None):
        self.user = user  # Store the current logged-in user
        self.book_manager = BookManager()  # Initialize BookManager once
        self.root = tk.Tk()  # Main application root (Tk root for the main window)
        self.root.title("Library Management System")
        self.root.geometry("400x600")
        self.root.configure(bg="pink")  # Set background color to pink
        self.build_gui()

    def build_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear previous widgets (useful for rebuilding GUI)

        tk.Label(self.root, text=f"Welcome {self.user}!", font=("Arial", 14), bg="pink", fg="white").pack(pady=10)
        tk.Label(self.root, text="Library Management System", font=("Arial", 16, "bold"), bg="pink", fg="white").pack(pady=20)

        button_style = {"width": 20, "bg": "white", "fg": "black", "font": ("Arial", 10, "bold"), "relief": "raised"}

        tk.Button(self.root, text="Add Book", command=self.open_add_book_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="Remove Book", command=self.open_remove_book_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="Search Book", command=self.open_search_book_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="View Books", command=self.open_view_books_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="Lend Book", command=self.open_lend_book_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=self.open_return_book_gui, **button_style).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.open_logout, **button_style).pack(pady=10)

    def open_add_book_gui(self):
        self.root.withdraw()
        try:
            app = BookManagementGui(self.book_manager, mode="add", return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()  # Ensure the main menu is visible if there's an error
            tk.messagebox.showerror("Error", f"Failed to open Add Book window: {e}")

    def open_remove_book_gui(self):
        self.root.withdraw()
        try:
            app = BookManagementGui(self.book_manager, mode="remove", return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to open Remove Book window: {e}")

    def open_search_book_gui(self):
        self.root.withdraw()
        try:
            app = SearchDisplayGui(return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to open Search Book window: {e}")

    def open_view_books_gui(self):
        self.root.withdraw()
        try:
            app = BookManagementGui(self.book_manager, mode="view", return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to open View Books window: {e}")

    def open_lend_book_gui(self):
        self.root.withdraw()
        try:
            app = BorrowReturnGui(self.book_manager, mode="lend", return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to open Lend Book window: {e}")

    def open_return_book_gui(self):
        self.root.withdraw()
        try:
            app = BorrowReturnGui(self.book_manager, mode="return", return_callback=self.return_to_main_menu)
            app.run()
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to open Return Book window: {e}")

    def open_logout(self):
        """Handle logout and redirect to authentication."""
        self.root.withdraw()  # Hide the current window instead of destroying it
        try:
            auth_app = AuthGui(on_success=self.open_main_menu)
            auth_app.run("login")
        except Exception as e:
            self.root.deiconify()
            tk.messagebox.showerror("Error", f"Failed to logout: {e}")

    def open_main_menu(self, user):
        """This function is triggered after successful authentication."""
        self.user = user
        self.root.deiconify()  # Show the main menu window
        self.build_gui()  # Rebuild the GUI for the new user

    def return_to_main_menu(self):
        self.root.deiconify()  # Show the main menu window

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Start with the authentication GUI
    try:
        auth_app = AuthGui(on_success=MainMenuGui)
        auth_app.run("login")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Application failed to start: {e}")