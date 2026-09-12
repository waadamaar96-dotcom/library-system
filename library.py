import json
from pathlib import Path


DATA_FILE = Path("books.json")


class Book:
    def __init__(self, title, author, pages, year, available=True):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year
        self.available = available

    def show_info(self):
        status = "Available" if self.available else "Borrowed"

        print("Title:", self.title)
        print("Author:", self.author)
        print("Pages:", self.pages)
        print("Year:", self.year)
        print("Status:", status)

    def borrow(self):
        if self.available:
            self.available = False
            print("Book borrowed successfully.")
        else:
            print("Book is not available.")

    def return_book(self):
        if not self.available:
            self.available = True
            print("Book returned successfully.")
        else:
            print("Book is already available.")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print("Book added successfully.")

    def show_books(self):
        if not self.books:
            print("No books in the library.")
            return

        for number, book in enumerate(self.books, start=1):
            print(f"\nBook {number}")
            book.show_info()
            print("-" * 25)

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.show_info()
                return book

        print("Book not found.")
        return None

    def search_without_printing(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book

        return None

    def borrow_book(self, title):
        book = self.search_without_printing(title)

        if book:
            book.borrow()
        else:
            print("Book not found.")

    def return_book(self, title):
        book = self.search_without_printing(title)

        if book:
            book.return_book()
        else:
            print("Book not found.")

    def save_books(self):
        data = []

        for book in self.books:
            data.append({
                "title": book.title,
                "author": book.author,
                "pages": book.pages,
                "year": book.year,
                "available": book.available
            })

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("Books saved successfully.")

        except OSError:
            print("Could not save books.")

    def load_books(self):
        if not DATA_FILE.exists():
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("Invalid books file.")
                return

            for item in data:
                if not isinstance(item, dict):
                    continue

                book = Book(
                    item["title"],
                    item["author"],
                    item["pages"],
                    item["year"],
                    item.get("available", True)
                )

                self.books.append(book)

        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("Could not load saved books.")


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print("Please enter a valid number.")


library = Library()
library.load_books()


while True:
    print("\n===== Library System =====")
    print("1. Add book")
    print("2. Show books")
    print("3. Search book")
    print("4. Borrow book")
    print("5. Return book")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author: ")
        pages = get_integer("Enter pages: ")
        year = get_integer("Enter year: ")

        book = Book(title, author, pages, year)

        library.add_book(book)
        library.save_books()

    elif choice == "2":
        library.show_books()

    elif choice == "3":
        title = input("Enter book title: ")
        library.search_book(title)

    elif choice == "4":
        title = input("Enter book title: ")

        library.borrow_book(title)
        library.save_books()

    elif choice == "5":
        title = input("Enter book title: ")

        library.return_book(title)
        library.save_books()

    elif choice == "6":
        library.save_books()
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please choose from 1 to 6.")