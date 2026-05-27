import json
import os
import tempfile
from dataclasses import dataclass
from typing import List

F_NAME = "books.json"
AVAILABLE_STATUS = "available"
BORROWED_STATUS = "borrowed"

@dataclass
class Book:
    title: str
    isbn: str
    status: str

    @staticmethod
    def from_dict(data: dict) -> "Book":
        if not isinstance(data, dict):
            raise ValueError("Book data must be a dictionary")

        title = data.get("title")
        isbn = data.get("isbn")
        status = data.get("status")

        if not all(isinstance(field, str) for field in (title, isbn, status)):
            raise ValueError("Book fields must be strings")

        title = title.strip()
        isbn = isbn.strip()
        status = status.strip()

        if not title or not isbn or not status:
            raise ValueError("Book fields cannot be empty")

        return Book(title=title, isbn=isbn, status=status)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "isbn": self.isbn,
            "status": self.status,
        }


class Library:
    def __init__(self, filename: str = F_NAME):
        self.filename = filename
        self.books: List[Book] = []
        self.dirty: bool = False

    def load(self) -> None:
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as err:
            print(f"讀檔失敗: {err}")
            return

        if not isinstance(data, list):
            print("資料格式錯誤：JSON 應該為列表")
            return

        for item in data:
            if isinstance(item, dict):
                try:
                    self.books.append(Book.from_dict(item))
                except ValueError:
                    continue
        self.dirty = False

    def save(self) -> None:
        if not self.dirty:
            return

        temp_path = None
        try:
            directory = os.path.dirname(self.filename) or "."
            with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=directory) as tmp:
                json.dump([book.to_dict() for book in self.books], tmp, ensure_ascii=False, indent=2)
                temp_path = tmp.name
            os.replace(temp_path, self.filename)
            self.dirty = False
        except OSError as err:
            print(f"存檔失敗: {err}")
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def has_isbn(self, isbn: str) -> bool:
        return any(book.isbn == isbn for book in self.books)

    def add_book(self, title: str, isbn: str, status: str) -> bool:
        title = title.strip()
        isbn = isbn.strip()
        status = status.strip()

        if not title or not isbn or not status:
            raise ValueError("書名、ISBN 與狀態皆不可為空")

        if self.has_isbn(isbn):
            return False

        self.books.append(Book(title=title, isbn=isbn, status=status))
        self.dirty = True
        return True

    def borrow_book(self, isbn: str) -> str:
        isbn = isbn.strip()
        if not isbn:
            return "format_error"

        for book in self.books:
            if book.isbn == isbn:
                if book.status == BORROWED_STATUS:
                    return "already_borrowed"
                book.status = BORROWED_STATUS
                self.dirty = True
                return "updated"
        return "not_found"

    def list_books(self) -> List[Book]:
        return self.books


class CommandProcessor:
    def __init__(self, library: Library):
        self.library = library

    def run(self) -> None:
        self.library.load()
        print("=== 圖書管理系統 v0.1 (Legacy) ===")

        while True:
            try:
                command = input("> ").strip()
            except (EOFError, KeyboardInterrupt) as err:
                print(f"\n系統中止: {err}")
                self.library.save()
                break

            try:
                if command == "exit":
                    self.library.save()
                    print("系統關閉")
                    break
                if command.startswith("add "):
                    self.handle_add(command[4:])
                elif command == "show":
                    self.handle_show()
                elif command.startswith("borrow "):
                    self.handle_borrow(command[7:].strip())
                else:
                    print("Unknown Command")
            except Exception as err:
                print(f"命令執行失敗: {err}")

    def handle_add(self, payload: str) -> None:
        try:
            parts = payload.split("/", 2)
            if len(parts) != 3:
                print("Format Error")
                return

            title, isbn, status = (part.strip() for part in parts)
            if not title or not isbn or not status:
                print("Format Error")
                return

            if self.library.add_book(title, isbn, status):
                print("Success")
            else:
                print("ISBN Exist")
        except ValueError as err:
            print(f"Format Error: {err}")
        except Exception as err:
            print(f"新增書籍失敗: {err}")

    def handle_show(self) -> None:
        for book in self.library.list_books():
            print(f"書名: {book.title}, ISBN: {book.isbn}, 狀態: {book.status}")

    def handle_borrow(self, isbn: str) -> None:
        isbn = isbn.strip()
        if not isbn:
            print("Format Error")
            return

        result = self.library.borrow_book(isbn)
        if result == "updated":
            print("Updated")
        elif result == "already_borrowed":
            print("Already Borrowed")
        elif result == "format_error":
            print("Format Error")
        else:
            print("Book Not Found")


def main() -> None:
    library = Library()
    processor = CommandProcessor(library)
    processor.run()


if __name__ == "__main__":
    main()
