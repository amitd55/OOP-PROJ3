import tkinter as tk
from tkinter import messagebox
from BookManager import BookManager

class BookManagementGui:
    def __init__(self, book_manager, mode="add", return_callback=None):
        self.book_manager = book_manager
        self.mode = mode
        self.return_callback = return_callback

        if return_callback:
            self.root = tk.Toplevel()
        else:
            self.root = tk.Tk()

        self.root.title("Book Management")
        self.root.geometry("500x400")
        self.build_gui()

    def build_gui(self):
        if self.mode == "add":
            self.build_add_gui()
        elif self.mode == "remove":
            self.build_remove_gui()
        elif self.mode == "view":
            self.build_view_gui()
        else:
            messagebox.showerror("Error", f"Unknown mode: {self.mode}")

        # Add Back button
        tk.Button(
            self.root,
            text="Back to Main Menu",
            command=self.return_to_main_menu,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
        ).pack(pady=20)

    def build_add_gui(self):
        add_frame = tk.Frame(self.root)
        tk.Label(add_frame, text="Add a New Book", font=("Arial", 14)).pack(pady=10)

        tk.Label(add_frame, text="Title").pack()
        self.title_entry = tk.Entry(add_frame)
        self.title_entry.pack()

        tk.Label(add_frame, text="Author").pack()
        self.author_entry = tk.Entry(add_frame)
        self.author_entry.pack()

        tk.Label(add_frame, text="Genre").pack()
        self.genre_entry = tk.Entry(add_frame)
        self.genre_entry.pack()

        tk.Label(add_frame, text="Year").pack()
        self.year_entry = tk.Entry(add_frame)
        self.year_entry.pack()

        tk.Label(add_frame, text="Copies").pack()
        self.copies_entry = tk.Entry(add_frame)
        self.copies_entry.pack()

        tk.Button(add_frame, text="Add Book", command=self.add_book).pack(pady=10)
        add_frame.pack(pady=20)

    def build_remove_gui(self):
        remove_frame = tk.Frame(self.root)
        tk.Label(remove_frame, text="Remove a Book", font=("Arial", 14)).pack(pady=10)

        tk.Label(remove_frame, text="Title").pack()
        self.remove_title_entry = tk.Entry(remove_frame)
        self.remove_title_entry.pack()

        tk.Button(
            remove_frame,
            text="Remove Book",
            command=self.remove_book,
            bg="red",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=10)

        remove_frame.pack(pady=20)

    def build_view_gui(self):
        view_frame = tk.Frame(self.root)
        tk.Label(view_frame, text="View All Books", font=("Arial", 14)).pack(pady=10)

        # Add a Text widget to display books
        self.books_display = tk.Text(view_frame, wrap=tk.WORD, width=60, height=20)
        self.books_display.pack()

        # Populate books
        self.display_books()

        view_frame.pack(pady=20)

    def display_books(self):
        self.books_display.delete(1.0, tk.END)  # Clear previous content
        books = self.book_manager.books

        if not books:
            self.books_display.insert(tk.END, "No books available.")
        else:
            for book in books:
                self.books_display.insert(tk.END, f"Title: {book.title}, Author: {book.author}, Copies: {book.copies}, Genre: {book.genre}, Year: {book.year}\n")

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        copies = self.copies_entry.get()

        if not (title and author and genre and year and copies):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            year = int(year)
            copies = int(copies)
        except ValueError:
            messagebox.showerror("Error", "Year and Copies must be integers.")
            return

        try:
            self.book_manager.add_book(title, author, genre, year, copies)
            messagebox.showinfo("Success", "Book added successfully!")
            self.display_books()
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def remove_book(self):
        title = self.remove_title_entry.get()

        if not title:
            messagebox.showerror("Error", "Please enter the title of the book to remove.")
            return

        try:
            self.book_manager.remove_book(title)
            messagebox.showinfo("Success", "Book removed successfully!")
            self.display_books()
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def return_to_main_menu(self):
        self.root.destroy()
        if self.return_callback:
            self.return_callback()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # For standalone testing
    book_manager = BookManager()
    gui = BookManagementGui(book_manager)
    gui.run()
