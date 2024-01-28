import pytest

from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('book_name', [
        'В этой книге название состоит из 55 символов, что много', ''],
                             ids=['too long name', 'empty name'])
    def test_book_with_empty_name_or_more_than_41_chars_dont_add(self,
                                                                 book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)

        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize('book_name, genre, expected',
                             [('Гордость и предубеждение и зомби', 'Ужасы',
                               'Ужасы'),
                              ('Маша и медведь', 'Детектив', None),
                              (
                                      'Гордость и предубеждение и зомби',
                                      'Романтика', '')],
                             ids=['correct set genre', 'book name do not exist',
                                  'genre do not exist in list'])
    def test_set_book_genre(self, book_name, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre(book_name, genre)

        assert collector.get_book_genre(book_name) == expected

    @pytest.mark.parametrize('book_name, expected',
                             [('Гордость и предубеждение и зомби',
                               ''),
                              ('Маша и медведь', None)],
                             ids=['correct get gener',
                                  'book name do not exist, return None'])
    def test_get_book_genre(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')

        assert collector.get_book_genre(book_name) == expected

    @pytest.mark.parametrize('genre, expected_len',
                             [('Ужасы', 2), ('Комедии', 1), ('Драма', 0),
                              ('Мультфильмы', 0)],
                             ids=['correct 2 books', 'correct 1 book in list',
                                  'genre not in genre list',
                                  'no books with specific genre'])
    def test_get_books_with_specific_genre(self, genre, expected_len):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.add_new_book('Эта книга полна пауков')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить',
                                 'Ужасы')
        collector.set_book_genre('Эта книга полна пауков', 'Комедии')

        assert len(
            collector.get_books_with_specific_genre(genre)) == expected_len

    def test_get_books_with_specific_genre_if_books_genre_empty(self):
        collector = BooksCollector()

        assert collector.get_books_with_specific_genre('Ужасы') == []

    @pytest.mark.parametrize('empty_books_genre, expected',
                             [(True, {}), (False, {
                                 'Гордость и предубеждение и зомби': '',
                                 'Что делать, если ваш кот хочет вас убить': '',
                                 'Эта книга полна пауков': ''})],
                             ids=['empty book genre dict', '3 books in dict'])
    def test_get_books_genre(self, empty_books_genre, expected):
        collector = BooksCollector()
        if not empty_books_genre:
            collector.add_new_book('Гордость и предубеждение и зомби')
            collector.add_new_book('Что делать, если ваш кот хочет вас убить')
            collector.add_new_book('Эта книга полна пауков')

        assert collector.get_books_genre() == expected

    @pytest.mark.parametrize('book1_genre, book2_genre, book3_genre, expected',
                             [('Фантастика', 'Мультфильмы', 'Ужасы', 2),
                              ('Фантастика', 'Ужасы', 'Ужасы', 1),
                              ('Ужасы', 'Ужасы', 'Ужасы', 0),
                              ('Повесть', 'Драма', 'Стих', 0)],
                             ids=['2 books for children', '1 book for children',
                                  'no book for children', 'wrong genre'])
    def test_get_books_for_children(self, book1_genre, book2_genre,
                                    book3_genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.add_new_book('Эта книга полна пауков')

        collector.set_book_genre('Гордость и предубеждение и зомби',
                                 book1_genre)
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить',
                                 book2_genre)
        collector.set_book_genre('Эта книга полна пауков', book3_genre)

        assert len(collector.get_books_for_children()) == expected

    @pytest.mark.parametrize('name, expected', [(
            'Гордость и предубеждение и зомби',
            ['Эта книга полна пауков', 'Гордость и предубеждение и зомби']),
        ('Маща и медведи', ['Эта книга полна пауков']),
        ('Эта книга полна пауков', ['Эта книга полна пауков'])],
                             ids=['book added to favorites',
                                  'book do not added to favorites',
                                  'same book do not added to favorites'])
    def test_add_book_in_favorites(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Эта книга полна пауков')
        collector.add_book_in_favorites('Эта книга полна пауков')

        collector.add_book_in_favorites(name)

        assert collector.get_list_of_favorites_books() == expected

    @pytest.mark.parametrize('name, expected', [(
            'Гордость и предубеждение и зомби',
            ['Эта книга полна пауков']),
        ('Эта книга полна пауков', []), ],
                             ids=['book do not deleted from  favorites',
                                  'book deleted from  favorites', ])
    def test_delete_book_from_favorites(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Эта книга полна пауков')
        collector.add_book_in_favorites('Эта книга полна пауков')

        collector.delete_book_from_favorites(name)

        assert collector.get_list_of_favorites_books() == expected

    @pytest.mark.parametrize('name1,name2, expected', [(
            'Гордость и предубеждение и зомби', 'Эта книга полна пауков',
            ['Гордость и предубеждение и зомби', 'Эта книга полна пауков']),
        ('Маша и медведи', 'Маша и медведи2', []), (
                'Маша и медведи2', 'Гордость и предубеждение и зомби',
                ['Гордость и предубеждение и зомби'])],
                             ids=['get 2 books ', 'get 0 book ',
                                  'get 1 books ', ])
    def test_get_list_of_favorites_books(self, name1, name2, expected):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Эта книга полна пауков')
        collector.add_book_in_favorites(name1)
        collector.add_book_in_favorites(name2)

        assert collector.get_list_of_favorites_books() == expected
