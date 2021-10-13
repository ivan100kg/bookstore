from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        book2 = Book.objects.create(name='Test book 2', price=55, author='Author 2')
        book3 = Book.objects.create(name='Test book 3', price=15, author='Author 1')
        data = BooksSerializer([book1, book2, book3], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': 25,
                'author': 'Author 1',
                'owner': None,
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': 55,
                'author': 'Author 2',
                'owner': None,

            },
            {
                'id': book3.id,
                'name': 'Test book 3',
                'price': 15,
                'author': 'Author 1',
                'owner': None,

            },
        ]
        self.assertEqual(expected_data, data)
