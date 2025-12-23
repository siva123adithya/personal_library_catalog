import json
import os
import csv
from colorama import Fore, Style, init

init(autoreset=True)

# ---------------- Book Class ----------------
class Book:
    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year
        }

    @staticmethod
    def from_dict(data):
        return Book(
            data.get("title", ""),
            data.get("author", ""),
            data.get("isbn", ""),
            data.get("year", "")
        )

    def __str__(self):
        return f"{Fore.CYAN}\"{self.title}\"{Style.RESET_ALL} by {self.author} | ISBN: {self.isbn} | Year: {self.year}"


# ---------------- Library Class ----------------
class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(b) for b in data]
            except json.JSONDecodeError:
                self.books = []

    def save_books(self):
        with open(self.filename, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    # ---------- ADD ----------
    def add_book(self, new_book):
        for book in self.books:
            if book.title.lower() == new_book.title.lower() and book.author.lower() == new_book.author.lower():
                print(Fore.RED + "\nDuplicate book. Not added.\n")
                return
        self.books.append(new_book)
        self.save_books()
        print(Fore.GREEN + "\nBook added successfully.\n")

    # ---------- LIST WITH PAGINATION ----------
    def list_books_paginated(self, page_size=5):
        if not self.books:
            print(Fore.YELLOW + "\nNo books available.\n")
            return

        total = len(self.books)
        page = 0

        while True:
            start = page * page_size
            end = start + page_size
            print(Fore.MAGENTA + f"\nShowing books {start + 1} to {min(end, total)} of {total}\n")

            for i, book in enumerate(self.books[start:end], start=start + 1):
                print(f"{i}. {book}")

            if end >= total and page == 0:
                break

            choice = input(Fore.YELLOW + "\n[N]ext  [P]revious  [Q]uit : ").lower()
            if choice == "n" and end < total:
                page += 1
            elif choice == "p" and page > 0:
                page -= 1
            elif choice == "q":
                break

    # ---------- SEARCH ----------
    def search_by_title(self, title):
        results = [b for b in self.books if title.lower() in b.title.lower()]
        self._print_search_results(results)

    def search_by_isbn(self, isbn):
        results = [b for b in self.books if b.isbn == isbn]
        self._print_search_results(results)

    def _print_search_results(self, results):
        if not results:
            print(Fore.RED + "\nNo matching books found.\n")
            return
        print(Fore.GREEN + "\nSearch Results:")
        for book in results:
            print(book)
        print()

    # ---------- SORT ----------
    def sort_books(self, key):
        if key == "title":
            self.books.sort(key=lambda b: b.title.lower())
        elif key == "author":
            self.books.sort(key=lambda b: b.author.lower())
        elif key == "year":
            self.books.sort(key=lambda b: b.year)
        self.save_books()
        print(Fore.GREEN + "\nBooks sorted successfully.\n")

    # ---------- EDIT ----------
    def edit_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                print(Fore.YELLOW + "\nLeave blank to keep existing value\n")
                title = input(f"New title ({book.title}): ").strip() or book.title
                author = input(f"New author ({book.author}): ").strip() or book.author
                year = input(f"New year ({book.year}): ").strip() or book.year

                book.title = title
                book.author = author
                book.year = year
                self.save_books()

                print(Fore.GREEN + "\nBook updated successfully.\n")
                return
        print(Fore.RED + "\nBook not found.\n")

    # ---------- EXPORT ----------
    def export_to_csv(self, filename="library.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Author", "ISBN", "Year"])
            for b in self.books:
                writer.writerow([b.title, b.author, b.isbn, b.year])
        print(Fore.GREEN + f"\nExported to {filename}\n")


# ---------------- MENU ----------------
def print_menu():
    print(Fore.BLUE + "\n===== Personal Library Catalog =====")
    print("1. Add Book")
    print("2. View Books (Paginated)")
    print("3. Search by Title")
    print("4. Search by ISBN")
    print("5. Sort Books")
    print("6. Edit Book")
    print("7. Export to CSV")
    print("8. Quit")


# ---------------- MAIN ----------------
def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Choose option (1-8): ").strip()

        if choice == "1":
            library.add_book(Book(
                input("Title: "),
                input("Author: "),
                input("ISBN: "),
                input("Year: ")
            ))

        elif choice == "2":
            library.list_books_paginated()

        elif choice == "3":
            library.search_by_title(input("Enter title keyword: "))

        elif choice == "4":
            library.search_by_isbn(input("Enter ISBN: "))

        elif choice == "5":
            print("Sort by: title / author / year")
            library.sort_books(input("Choice: ").strip().lower())

        elif choice == "6":
            library.edit_book(input("Enter ISBN of book to edit: "))

        elif choice == "7":
            library.export_to_csv()

        elif choice == "8":
            print(Fore.CYAN + "\nGoodbye 👋\n")
            break

        else:
            print(Fore.RED + "\nInvalid option.\n")


if __name__ == "__main__":
    main()
