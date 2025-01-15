import tkinter as tk
from tkinter import messagebox
from SearchStrategy import SearchManager, TitleSearchStrategy, AuthorSearchStrategy, GenreSearchStrategy

class SearchDisplayGui:
    def __init__(self):
        self.search_manager = SearchManager()
        self.root = tk.Tk()
        self.root.title("Search and Display Books")
        self.root.geometry("500x400")
        self.build_gui()

    def build_gui(self):
        # Search Section
        search_frame = tk.Frame(self.root)
        tk.Label(search_frame, text="Search Books", font=("Arial", 14)).pack(pady=10)

        tk.Label(search_frame, text="Search By").pack()
        self.search_type_var = tk.StringVar(value="title")
        tk.Radiobutton(search_frame, text="Title", variable=self.search_type_var, value="title").pack()
        tk.Radiobutton(search_frame, text="Author", variable=self.search_type_var, value="author").pack()
        tk.Radiobutton(search_frame, text="Genre", variable=self.search_type_var, value="genre").pack()

        tk.Label(search_frame, text="Query").pack()
        self.search_query_entry = tk.Entry(search_frame)
        self.search_query_entry.pack()

        tk.Button(search_frame, text="Search", command=self.search_books).pack(pady=10)
        search_frame.pack(pady=20)

        # Display Section
        display_frame = tk.Frame(self.root)
        tk.Label(display_frame, text="Display Books", font=("Arial", 14)).pack(pady=10)

        tk.Button(display_frame, text="All Books", command=lambda: self.display_books("all")).pack(pady=5)
        tk.Button(display_frame, text="Available Books", command=lambda: self.display_books("available")).pack(pady=5)
        tk.Button(display_frame, text="Loaned Books", command=lambda: self.display_books("loaned")).pack(pady=5)
        display_frame.pack(pady=20)

    def search_books(self):
        search_type = self.search_type_var.get()
        query = self.search_query_entry.get()

        if not query:
            messagebox.showerror("Error", "Please enter a query.")
            return

        try:
            if search_type == "title":
                self.search_manager.set_strategy(TitleSearchStrategy())
            elif search_type == "author":
                self.search_manager.set_strategy(AuthorSearchStrategy())
            elif search_type == "genre":
                self.search_manager.set_strategy(GenreSearchStrategy())

            results = self.search_manager.search(query)
            if not results:
                self.search_manager.logger.log(f"Search for {search_type} '{query}' failed: No results.")
                messagebox.showinfo("Search Results", "No books found.")
            else:
                results_info = "\n".join([str(book) for book in results])
                self.search_manager.logger.log(f"Search for {search_type} '{query}' succeeded with results.")
                messagebox.showinfo("Search Results", results_info)
        except Exception as e:
            self.search_manager.logger.log(f"Search for {search_type} '{query}' failed: {e}")
            messagebox.showerror("Error", f"Search failed: {e}")

    def display_books(self, status):
        try:
            books = self.search_manager.display_books(status)
            if not books:
                self.search_manager.logger.log(f"Displaying {status} books failed: No books found.")
                messagebox.showinfo("Books", f"No {status} books available.")
            else:
                books_info = "\n".join([str(book) for book in books])
                self.search_manager.logger.log(f"Displayed {status} books successfully.")
                messagebox.showinfo("Books", books_info)
        except Exception as e:
            self.search_manager.logger.log(f"Displaying {status} books failed: {e}")
            messagebox.showerror("Error", f"Displaying {status} books failed: {e}")

    def run(self):
        self.root.mainloop()