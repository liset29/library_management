import pytest
from main import Library
from const import DATA_FILE
@pytest.fixture
def test_library():
    """Создает экземпляр библиотеки для тестов."""
    library = Library()
    library.books = []
    return library

@pytest.fixture
def sample_books():
    """Возвращает пример списка книг."""
    return [
        {"title": "Маленькая жизнь", "author": "Ханья Янагихара", "year": 2023},
        {"title": "Воин без меча", "author": "Неизвестен", "year": 2022},
    ]

@pytest.mark.parametrize("title, author, year", [
    ("Маленькая жизнь", "Ханья Янагихара", 2023),
    ("Воин без меча", "Неизвестен ", 2022),
])
def test_add_book(test_library, title, author, year):
    """Тест добавления книги."""
    test_library.add_book(title, author, year)
    assert len(test_library.books) == 1, "Книга не была добавлена"
    assert test_library.books[0]["title"] == title, "Название книги не совпадает"
    assert test_library.books[0]["status"] == "в наличии", "Статус книги неверный"

def test_delete_book(test_library):
    """Тест удаления книги."""
    test_library.add_book("Маленькая жизнь", "Ханья Янагихара", 2023)
    book_id = test_library.books[0]["id"]
    test_library.delete_book(book_id)
    assert len(test_library.books) == 0, "Книга не была удалена"
    assert test_library.delete_book(book_id) is False, "Удаление несуществующей книги вернуло True"

def test_search_books(test_library, sample_books):
    """Тест поиска книг."""
    for book in sample_books:
        test_library.add_book(book["title"], book["author"], book["year"])
    results = test_library.search_books("Маленькая жизнь")
    assert len(results) == 1, "Неправильное количество найденных книг"
    assert results[0]["title"] == "Маленькая жизнь", "Название найденной книги не совпадает"

    results = test_library.search_books("2022")
    assert len(results) == 1, "Поиск по году не работает"
    assert results[0]["year"] == 2022, "Год книги не совпадает"

    results = test_library.search_books("Несуществующая книга")
    assert len(results) == 0, "Поиск несуществующей книги вернул результаты"

def test_change_status(test_library):
    """Тест изменения статуса книги."""
    test_library.add_book("Маленькая жизнь", "Ханья Янагихара", 2023)
    book_id = test_library.books[0]["id"]
    assert test_library.change_status(book_id, "выдана") is True, "Изменение статуса не выполнено"
    assert test_library.books[0]["status"] == "выдана", "Статус книги неверный"
    assert test_library.change_status(book_id, "в наличии") is True, "Изменение статуса не выполнено"
    assert test_library.books[0]["status"] == "в наличии", "Статус книги неверный"
    assert test_library.change_status(book_id, "неизвестный статус") is False, "Изменение на некорректный статус прошло успешно"

def test_add_book_with_invalid_data(test_library):
    """Тест добавления книги с некорректными данными."""
    with pytest.raises(TypeError):
        test_library.add_book(None, "Автор", 2023)
    with pytest.raises(ValueError):
        test_library.add_book("Книга", "Автор", -1)


def test_unique_ids(test_library):
    """Тест уникальности ID."""
    test_library.add_book("Маленькая жизнь", "Ханья Янагихара", 2023)
    test_library.add_book("Воин без меча", "Неизвестен", 2022)
    ids = [book["id"] for book in test_library.books]
    assert len(ids) == len(set(ids)), "ID книг не уникальны"
