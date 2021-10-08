from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        book2 = Book.objects.create(name='Test book 2', price=55, author='Author 2')
        book3 = Book.objects.create(name='Test book 3', price=15, author='Author 1')
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([book1, book2, book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
