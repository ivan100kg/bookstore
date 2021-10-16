from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create_user(username='user1')
        user2 = User.objects.create_user(username='user2')
        user3 = User.objects.create_user(username='user3')

        book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        book2 = Book.objects.create(name='Test book 2', price=55, author='Author 2')
        book3 = Book.objects.create(name='Test book 3', price=15, author='Author 1')

        UserBookRelation.objects.create(user=user1, book=book1, like=True)
        UserBookRelation.objects.create(user=user2, book=book1, like=True)
        UserBookRelation.objects.create(user=user3, book=book1, like=True)

        UserBookRelation.objects.create(user=user1, book=book2, like=True)
        UserBookRelation.objects.create(user=user2, book=book2, like=False)
        UserBookRelation.objects.create(user=user3, book=book2, like=True)

        UserBookRelation.objects.create(user=user1, book=book3, like=False)
        UserBookRelation.objects.create(user=user2, book=book3, like=False)
        UserBookRelation.objects.create(user=user3, book=book3, like=False)

        data = BooksSerializer([book1, book2, book3], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': 25,
                'author': 'Author 1',
                'likes_count': 3,

            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': 55,
                'author': 'Author 2',
                'likes_count': 2,

            },
            {
                'id': book3.id,
                'name': 'Test book 3',
                'price': 15,
                'author': 'Author 1',
                'likes_count': 0,

            },
        ]
        # print(data)

        self.assertEqual(expected_data, data)
