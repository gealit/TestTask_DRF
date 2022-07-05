import json
from collections import OrderedDict
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Offer
from api.serializers import OfferSerializer


class OfferApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1', is_staff=True)
        self.user2 = User.objects.create(username='test_user2')
        self.offer_1 = Offer.objects.create(
            bank_name='bank test 1 Стандарт',
            term_min=5,
            term_max=10,
            rate_min=2.8,
            rate_max=13.97,
            payment_min=500000,
            payment_max=50000000
        )
        self.offer_2 = Offer.objects.create(
            bank_name='bank test 2',
            term_min=1,
            term_max=20,
            rate_min=1.8,
            rate_max=23.98,
            payment_min=100000,
            payment_max=10000000
        )
        self.offer_3 = Offer.objects.create(
            bank_name='bank test 3',
            term_min=10,
            term_max=30,
            rate_min=5,
            rate_max=15,
            payment_min=600000,
            payment_max=60000000
        )
        self.offer_4 = Offer.objects.create(
            bank_name='bank test 4 Стандарт',
            term_min=1,
            term_max=20,
            rate_min=1.7,
            rate_max=23.98,
            payment_min=200000,
            payment_max=20000000
        )

    def test_get(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        serializer_data = OfferSerializer(
            [self.offer_4, self.offer_2, self.offer_1, self.offer_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one(self):
        url = reverse('offer-detail', args=(self.offer_1.id,))
        response = self.client.get(url)
        serializer_data = OfferSerializer(self.offer_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('offer-list')
        response = self.client.get(url, data={'search': 'Стандарт'})
        serializer_data = OfferSerializer(
            [self.offer_4, self.offer_1], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('offer-list')
        response = self.client.get(url, data={'ordering': 'payment_min'})
        serializer_data = OfferSerializer(
            [self.offer_2, self.offer_4, self.offer_1, self.offer_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(4, Offer.objects.all().count())
        url = reverse('offer-list')
        data = {
            'bank_name': 'creation test',
            'term_min': 1,
            'term_max': 1,
            'rate_min': 1,
            'rate_max': 1,
            'payment_min': 1,
            'payment_max': 1
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Offer.objects.all().count())

    def test_update(self):
        url = reverse('offer-detail', args=(self.offer_1.id,))
        data = {
            'bank_name': 'test 1 update',
            'term_min': self.offer_1.term_min,
            'term_max': self.offer_1.term_max,
            'rate_min': '0.01',
            'rate_max': self.offer_1.rate_max,
            'payment_min': 5,
            'payment_max': 50
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.offer_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('test 1 update', self.offer_1.bank_name)
        self.assertEqual(Decimal('0.01'), self.offer_1.rate_min)
        self.assertEqual(5, self.offer_1.payment_min)
        self.assertEqual(50, self.offer_1.payment_max)

    def test_delete(self):
        self.assertEqual(4, Offer.objects.all().count())
        url = reverse('offer-detail', args=(self.offer_4.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, Offer.objects.all().count())

    def test_get_offers(self):
        url = '/api/offer/?price=10000000&deposit=10&term=10'
        response = self.client.get(url)
        data = [
            OrderedDict(
                {
                    "bank_name": "bank test 4 Стандарт",
                    "rate_min": "1.70",
                    "rate_max": "23.98",
                    "payment_min": Decimal('76062.50'),
                    "payment_max": Decimal('89987.50'),
                    "price": 10000000,
                    "deposit": Decimal('10'),
                    "term": 10
                }),
            OrderedDict(
                {
                    "bank_name": "bank test 2",
                    "rate_min": "1.80",
                    "rate_max": "23.98",
                    "payment_min": Decimal('76125.00'),
                    "payment_max": Decimal('89987.50'),
                    "price": 10000000,
                    "deposit": Decimal('10'),
                    "term": 10
                }),
            OrderedDict(
                {
                    "bank_name": "bank test 1 Стандарт",
                    "rate_min": "2.80",
                    "rate_max": "13.97",
                    "payment_min": Decimal('76750.00'),
                    "payment_max": Decimal('83731.25'),
                    "price": 10000000,
                    "deposit": Decimal('10'),
                    "term": 10
                }),
            OrderedDict(
                {
                    "bank_name": "bank test 3",
                    "rate_min": "5.00",
                    "rate_max": "15.00",
                    "payment_min": Decimal('78125.00'),
                    "payment_max": Decimal('84375.00'),
                    "price": 10000000,
                    "deposit": Decimal('10'),
                    "term": 10
                })
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, data)

    def test_get_valid_by_price_offers(self):
        url = '/api/offer/?price=30000000&deposit=10&term=10'
        response = self.client.get(url)
        data = [
            OrderedDict(
                {
                    "bank_name": "bank test 1 Стандарт",
                    "rate_min": "2.80",
                    "rate_max": "13.97",
                    "payment_min": Decimal('230250.00'),
                    "payment_max": Decimal('251193.75'),
                    "price": 30000000,
                    "deposit": Decimal('10'),
                    "term": 10
                }),
            OrderedDict(
                {
                    "bank_name": "bank test 3",
                    "rate_min": "5.00",
                    "rate_max": "15.00",
                    "payment_min": Decimal('234375.00'),
                    "payment_max": Decimal('253125.00'),
                    "price": 30000000,
                    "deposit": Decimal('10'),
                    "term": 10
                })
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, data)

    def test_get_valid_by_term_offers(self):
        url = '/api/offer/?price=10000000&deposit=10&term=30'
        response = self.client.get(url)
        data = [
            OrderedDict(
                {
                    "bank_name": "bank test 3",
                    "rate_min": "5.00",
                    "rate_max": "15.00",
                    "payment_min": Decimal('28125.00'),
                    "payment_max": Decimal('34375.00'),
                    "price": 10000000,
                    "deposit": Decimal('10'),
                    "term": 30
                })
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, data)

    def test_wrong_value(self):
        url = '/api/offer/?price=10000000&deposit=0.222&term=a'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
