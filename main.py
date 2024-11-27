import json
from typing import List, Optional

from const import DATA_FILE, Book


class Library:
    """Класс для управления библиотекой."""

    def __init__(self):
        self.books: List[Book] = self.load_data()

    @staticmethod
    def load_data() -> List[Book]:
        """Загружает данные из файла или возвращает пустой список, если файл отсутствует."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self) -> None:
        """Сохраняет данные в файл."""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

    def generate_id(self) -> int:
        """Генерирует уникальный ID для новой книги."""
        return max((book["id"] for book in self.books), default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет новую книгу в библиотеку."""

        if not isinstance(title, str) or not isinstance(author, str):
            raise TypeError("Название и автор книги должны быть строками")
        if not isinstance(year, int) or year <= 0:
            raise ValueError("Год издания должен быть положительным числом")

        new_book = {
            "id": self.generate_id(),
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии",
        }
        self.books.append(new_book)
        self.save_data()

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """Ищет книгу по ID."""
        return next((book for book in self.books if book["id"] == book_id), None)

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_data()
            return True
        return False

    def search_books(self, query: str) -> List[Book]:
        """Ищет книги по названию, автору или году."""
        return [
            book
            for book in self.books
            if query.lower() in book["title"].lower()
               or query.lower() in book["author"].lower()
               or query.isdigit() and int(query) == book["year"]
        ]

    def change_status(self, book_id: int, new_status: str) -> bool:
        """Изменяет статус книги."""
        book = self.find_book_by_id(book_id)
        if book and new_status in ["в наличии", "выдана"]:
            book["status"] = new_status
            self.save_data()
            return True
        return False


class LibraryApp:
    """Класс для работы с консольным приложением библиотеки."""

    def __init__(self):
        self.library = Library()

    def run(self):
        """Запускает приложение."""
        actions = {
            "1": self.add_book,
            "2": self.delete_book,
            "3": self.search_book,
            "4": self.display_books,
            "5": self.change_status,
            "0": self.exit_app,
        }

        while True:
            self.print_menu()
            choice = input("Выберите действие: ").strip()
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Ошибка: Некорректный выбор.")

    @staticmethod
    def print_menu():
        """Выводит меню действий."""
        print("\n--- Управление библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

    @staticmethod
    def get_int_input(prompt: str) -> Optional[int]:
        """Получает целочисленный ввод от пользователя."""
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: Введите корректное число.")
            return None

    def add_book(self):
        """Добавление книги."""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = self.get_int_input("Введите год издания: ")
        if year is None:
            return
        self.library.add_book(title, author, year)
        print("Книга успешно добавлена!")

    def delete_book(self):
        """Удаление книги."""
        book_id = self.get_int_input("Введите ID книги, которую нужно удалить: ")
        if book_id is None:
            return
        if self.library.delete_book(book_id):
            print("Книга успешно удалена")
        else:
            print("Ошибка: Книга с таким ID не найдена.")

    def search_book(self):
        """Поиск книги через ввод пользователя."""
        query = input("Введите название, автора или год для поиска: ")
        results = self.library.search_books(query)
        if results:
            print("Найденные книги:")
            self.print_books(results)
        else:
            print("Книги не найдены.")

    def display_books(self):
        """Отображает все книги."""
        if not self.library.books:
            print("Библиотека пуста.")
        else:
            print("Список книг:")
            self.print_books(self.library.books)

    @staticmethod
    def print_books(books: List[Book]):
        """Выводит список книг."""
        for book in books:
            print(
                f'id-{book["id"]}: название: {book["title"]}, автор: {book["author"]},год издания: {book["year"]}, статус: {book["status"]}'
            )

    def change_status(self):
        """Изменение статуса книги."""
        book_id = self.get_int_input("Введите ID книги: ")
        if book_id is None:
            return
        new_status = input("Введите новый статус (в наличии/выдана): ").strip().lower()
        if self.library.change_status(book_id, new_status):
            print("Статус книги успешно изменен!")
        else:
            print("Ошибка: Книга с таким ID не найдена или статус некорректный.")

    @staticmethod
    def exit_app(self):
        """Завершает работу приложения."""
        print("Выход из программы.")
        exit()


if __name__ == "__main__":
    app = LibraryApp()
    app.run()
