import tkinter as tk
from tkinter import ttk, messagebox
from classes.SearchManager import SearchManager
from classes.BookManager import BookManager
from classes.Logger import Logger

class DisplayBooksGui:
    def __init__(self, return_callback=None):
        self.return_callback = return_callback  # Store the return callback
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

        # Dropdown for filter type
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
                messagebox.showinfo("Books", "No books available.")
            else:
                for book in books:
                    self.tree.insert("", tk.END, values=(
                        getattr(book, 'title', 'N/A'),
                        getattr(book, 'author', 'N/A'),
                        getattr(book, 'genre', 'N/A'),
                        getattr(book, 'year', 'N/A'),
                        getattr(book, 'copies_available', 'N/A')
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def return_to_main_menu(self):
        self.root.withdraw()  # Hide the current window
        if self.return_callback:
            self.return_callback()  # Call the callback function to return to the main menu

    def run(self):
        self.root.mainloop()


class SearchBooksGui:
    def __init__(self):
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

        # Treeview widget for displaying results
        columns = ("Title", "Author", "Genre", "Year", "Available Copies")
        self.tree = ttk.Treeview(search_frame, columns=columns, show="headings")
        self.tree.pack(expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(search_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        tk.Button(search_frame, text="Search", command=self.perform_search, width=15).pack(pady=20)
        tk.Button(search_frame, text="Return", command=self.return_to_main_menu, width=15).pack(pady=10)
        tk.Button(search_frame, text="Close", command=self.close_window, width=15).pack(pady=10)

        search_frame.pack(expand=True, fill="both")

    def perform_search(self):
        query = self.search_query_entry.get()
        search_type = self.search_type_var.get()

        if not query:
            messagebox.showerror("Error", "Please enter a query.")
            return

        # Validate search type
        valid_search_types = ["title", "author", "genre", "year"]
        if search_type not in valid_search_types:
            messagebox.showerror("Error", f"Search failed: Invalid search type: {search_type}")
            return

        try:
            # Clear previous Treeview entries
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
                        getattr(book, 'copies_available', 'N/A')
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def return_to_main_menu(self):
        """Handle return to main menu."""
        print("Returning to main menu...")  # You can add logic for the main menu here
        # Example of returning to the main menu
        # If you have a MainMenuGui class, call it here:
        # main_menu = MainMenuGui()
        # main_menu.run()

        # For now, reset the search window without destroying it
        self.search_query_entry.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.search_type_var.set("title")  # Reset the filter to the default

    def close_window(self):
        """Close the current window."""
        self.root.destroy()

    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()




if __name__ == "__main__":
    # Uncomment the desired GUI to test it
    # DisplayBooksGui().run()
    SearchBooksGui().run()
