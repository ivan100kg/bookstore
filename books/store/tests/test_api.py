import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_username')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1', owner=self.user)
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='Author 1', owner=self.user)
        self.book3 = Book.objects.create(name='Test book by Author 1', price=55, author='Author 2', owner=self.user)
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
        self.assertEqual(self.user, Book.objects.last().owner)

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

    def test_update_not_owner(self):
        self.user2 = User.objects.create_user(username='enemy_user')
        data = {
            'name': self.book1.name,
            'price': 306,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        self.url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.put(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(25, self.book1.price)

    def test_update_not_owner_but_staff(self):
        self.user3 = User.objects.create_user(username='admin', is_staff=True)
        data = {
            'name': self.book1.name,
            'price': 306,
            'author': self.book1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        self.url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.put(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(306, self.book1.price)

    def test_delete(self):
        self.client.force_login(self.user)
        self.url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        # self.assertRaisesMessage(Book.objects.get(id=self.book1.id), Book.DoesNotExist)
        # try:
        #     self.book1 = Book.objects.get(id=self.book1.id)
        # except Book.DoesNotExist:
        #     pass


class BooksRelationsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test_username1')
        self.user2 = User.objects.create_user(username='test_username2')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='Author 1', owner=self.user1)
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='Author 1', owner=self.user1)
        self.book3 = Book.objects.create(name='Test book by Author 1', price=55, author='Author 2', owner=self.user2)
        self.url = reverse('userbookrelation-detail', args=(self.book1.id,))

    def test_like(self):
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertTrue(relation.like)

        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
