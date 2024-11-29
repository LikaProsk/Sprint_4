import pytest

from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("book_name", ['A', 'Что делать, если ваш кот хочет вас убить'])
    def test_add_new_book_book_name_positive_boundary_values_check(self, book_name):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        collector.add_new_book(book_name)

        # проверяем, что книги добавились
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize("book_name", ['', 'Что делать, если ваш кот хочет вас убить?'])
    def test_add_new_book_book_name_negative_boundary_values_check(self, book_name):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        collector.add_new_book(book_name)

        # проверяем, что книги не добавились
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_add_existing_book_name(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книгу в первый раз
        collector.add_new_book('Гордость и предубеждение и зомби')

        # добавляем книгу во второй раз
        collector.add_new_book('Гордость и предубеждение и зомби')

        # проверяем, что книга повторно не добавилась
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_positive_genre_positive_result(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем  книгу
        book_name = 'Гордость и предубеждение и зомби'
        collector.add_new_book(book_name)

        # устанавливаем жанр добавленной книге
        genre = 'Комедии'
        collector.set_book_genre(book_name, genre)

        # проверяем, что жанр установлен
        assert collector.books_genre.get(book_name) == genre

    def test_get_book_genre_existing_book_genre_positive_result(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем  книгу
        book_name = 'Война миров'
        collector.add_new_book(book_name)

        # устанавливаем жанр добавленной книге
        genre = 'Фантастика'
        collector.set_book_genre(book_name, genre)

        # проверяем, что жанр соответствует установленному
        assert collector.get_book_genre(book_name) == genre

    def test_get_books_with_specific_genre_positive_result(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем  книги
        books_and_genres = {
            'Призрак дома на холме': 'Ужасы',
            'Астрал': 'Ужасы',
            'Зеркала': 'Ужасы',
            'Война миров': 'Фантастика'
        }

        for book, genre in books_and_genres.items():
            collector.add_new_book(book)

            # устанавливаем жанры добавленным книгам
            collector.set_book_genre(book, genre)

        # проверяем книги жанра ужасы
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        assert len(horror_books) == 3 and 'Астрал' in horror_books

    @pytest.mark.parametrize('books', [['Призрак дома на холме', 'Астрал'], []])
    def test_get_books_genre_positive_result(self, books):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        for book in books:
            collector.add_new_book(book)

        # проверяем список книг
        assert len(collector.get_books_genre()) == len(books)

    @pytest.mark.parametrize('books', [{'Призрак дома на холме': 'Ужасы', 'Том и Джерри': 'Мультфильмы'},
                                       {'Книга без жанра': ''}, {'Лило и Стич': 'Мультфильмы'}])
    def test_get_books_for_children_positive_result(self, books):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книги
        for book, genre in books.items():
            collector.add_new_book(book)

            # устанавливаем жанры добавленным книгам
            collector.set_book_genre(book, genre)

        # Ожидаемый результат
        result = [book for book, genre in books.items() if
                  genre not in collector.genre_age_rating and genre in collector.genre]

        # проверяем книги разрешенные для детей
        assert len(collector.get_books_for_children()) == len(result)

    @pytest.mark.parametrize('cases',
                             [{'Призрак дома на холме': True,
                               'Том и Джерри': True,
                               'Великий Гетсби': False}
                                 , {}, {'Великий Гетсби': True}])
    def test_add_book_in_favorites_positive_result(self, cases):

        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()
        result = []
        # добавляем книги
        for book, is_favourite in cases.items():
            collector.add_new_book(book)
            if is_favourite:
                collector.add_book_in_favorites(book)
                result.append(book)

        # проверяем список Избранных книг
        assert len(collector.favorites) == len(result)

    def test_delete_book_from_favorites_positive_result(self):

        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем книгу
        book_name = 'Гордость и предубеждение и зомби'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        # удаляем книгу из Избранных
        collector.delete_book_from_favorites(book_name)

        assert len(collector.favorites) == 0

    @pytest.mark.parametrize('cases',
                             [{'Призрак дома на холме': True,
                               'Том и Джерри': True,
                               'Великий Гетсби': False}
                                 , {}, {'Великий Гетсби': True}])
    def test_get_list_of_favorites_books_positive_result(self, cases):

        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()
        result = []
        # добавляем книги
        for book, is_favourite in cases.items():
            collector.add_new_book(book)
            if is_favourite:
                collector.add_book_in_favorites(book)
                result.append(book)

        # проверяем список Избранных книг
        assert len(collector.get_list_of_favorites_books()) == len(result)
