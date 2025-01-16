import tkinter as tk
from tkinter import ttk, messagebox
from classes.SearchManager import SearchManager
from classes.BookManager import BookManager
from classes.Logger import Logger

class DisplayBooksGui:
    def __init__(self, main_menu=None):
        self.main_menu = main_menu  # Store the main menu window
        self.logger = Logger()
        self.book_manager = BookManager()
        self.search_manager = SearchManager(self.book_manager, self.logger)

        if not hasattr(self.book_manager, 'books') or not self.book_manager.books:
            messagebox.showinfo("Warning", "No books found in the BookManager.")

        self.root = tk.Tk()
        self.root.title("Display Books")
        self.root.geometry("800x600")
        self.root.configure(bg="pink")

        self.build_display_frame()

    def build_display_frame(self):
        display_frame = tk.Frame(self.root, bg="pink")
        tk.Label(display_frame, text="Display Books", font=("Arial", 16), bg="pink").pack(pady=20)

        tk.Label(display_frame, text="Filter By", bg="pink").pack()
        self.filter_type_var = tk.StringVar(value="all")
        filter_dropdown = ttk.Combobox(display_frame, textvariable=self.filter_type_var, state="readonly")
        filter_dropdown['values'] = ("all", "popular", "available", "loaned")
        filter_dropdown.pack(pady=10)

        columns = ("Title", "Author", "Genre", "Year", "Available Copies")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.tree.pack(expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        tk.Button(display_frame, text="Load Books", command=self.load_books, width=20).pack(pady=10)
        tk.Button(display_frame, text="Return", command=self.return_to_main_menu, width=20).pack(pady=10)
        tk.Button(display_frame, text="Close", command=self.root.destroy, width=20).pack(pady=10)

        display_frame.pack(expand=True, fill="both")

    def load_books(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing rows
        filter_type = self.filter_type_var.get()
        try:
            books_iterator = self.search_manager.display_books(filter_type)
            books = list(books_iterator)

            if not books:
                messagebox.showinfo("Books", f"No books found for filter: {filter_type.capitalize()}.")
            else:
                for book in books:
                    self.tree.insert("", tk.END, values=(
                        getattr(book, 'title', 'N/A'),
                        getattr(book, 'author', 'N/A'),
                        getattr(book, 'genre', 'N/A'),
                        getattr(book, 'year', 'N/A'),
                        getattr(book, 'copies', 'N/A')
                    ))

                messagebox.showinfo("Books", f"{len(books)} books found for filter: {filter_type.capitalize()}.")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid filter type: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def return_to_main_menu(self):
        self.root.destroy()  # Close the current window
        if self.main_menu:
            self.main_menu.deiconify()  # Show the main menu again

    def run(self):
        self.root.mainloop()


class SearchBooksGui:
    def __init__(self, main_menu=None):
        self.main_menu = main_menu  # Store the main menu window
        self.logger = Logger()
        self.book_manager = BookManager()
        self.search_manager = SearchManager(self.book_manager, self.logger)

        if not hasattr(self.book_manager, 'books') or not self.book_manager.books:
            messagebox.showinfo("Warning", "No books found in the BookManager.")

        self.root = tk.Tk()
        self.root.title("Search Books")
        self.root.geometry("800x600")
        self.root.configure(bg="pink")

        self.build_search_frame()

    def build_search_frame(self):
        search_frame = tk.Frame(self.root, bg="pink")
        tk.Label(search_frame, text="Search Books", font=("Arial", 16), bg="pink").pack(pady=20)

        tk.Label(search_frame, text="Search By", bg="pink").pack()
        self.search_type_var = tk.StringVar(value="title")
        search_options = [("Title", "title"), ("Author", "author"), ("Genre", "genre"), ("Year", "year")]
        for text, value in search_options:
            tk.Radiobutton(search_frame, text=text, variable=self.search_type_var, value=value, bg="pink").pack()

        tk.Label(search_frame, text="Query", bg="pink").pack()
        self.search_query_entry = tk.Entry(search_frame, width=30)
        self.search_query_entry.pack()

        columns = ("Title", "Author", "Genre", "Year", "Available Copies")
        self.tree = ttk.Treeview(search_frame, columns=columns, show="headings")
        self.tree.pack(expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(search_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        tk.Button(search_frame, text="Search", command=self.perform_search, width=15).pack(pady=20)
        tk.Button(search_frame, text="Return", command=self.return_to_main_menu, width=15).pack(pady=10)
        tk.Button(search_frame, text="Close", command=self.root.destroy, width=15).pack(pady=10)

        search_frame.pack(expand=True, fill="both")

    def perform_search(self):
        query = self.search_query_entry.get()
        search_type = self.search_type_var.get()

        if not query:
            messagebox.showerror("Error", "Please enter a query.")
            return

        valid_search_types = ["title", "author", "genre", "year"]
        if search_type not in valid_search_types:
            messagebox.showerror("Error", f"Search failed: Invalid search type: {search_type}")
            return

        try:
            self.tree.delete(*self.tree.get_children())
            results_iterator = self.search_manager.perform_search(query, search_type)
            results = list(results_iterator)

            if not results:
                messagebox.showinfo("Search Results", "No books found.")
            else:
                for book in results:
                    self.tree.insert("", tk.END, values=(
                        getattr(book, 'title', 'N/A'),
                        getattr(book, 'author', 'N/A'),
                        getattr(book, 'genre', 'N/A'),
                        getattr(book, 'year', 'N/A'),
                        getattr(book, 'copies', 'N/A')
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def return_to_main_menu(self):
        self.root.destroy()
        if self.main_menu:
            self.main_menu.deiconify()

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = DisplayBooksGui()
    gui.run()
