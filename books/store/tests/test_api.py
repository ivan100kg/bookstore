import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_username')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='Author 1')
        self.book3 = Book.objects.create(name='Test book by Author 1', price=55, author='Author 2')
        self.url = reverse('book-list')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': 55})
        serializer_data = BooksSerializer([self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        response = self.client.get(self.url, data={'ordering': 'author'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        data = {
            'name': 'Programming in Python 3',
            'price': 260,
            'author': "Mark Summerfield",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        data = {
            'name': self.book1.name,
            'price': 306,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        self.url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.put(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book1 = Book.objects.get(id=self.book1.id)
        self.book1.refresh_from_db()
        self.assertEqual(306, self.book1.price)

    def test_delete(self):
        self.client.force_login(self.user)
        self.url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        try:
            self.book1 = Book.objects.get(id=self.book1.id)
        except Book.DoesNotExist:
            pass
