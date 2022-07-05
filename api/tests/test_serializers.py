from django.test import TestCase

from api.models import Offer
from api.serializers import OfferSerializer


class OfferSerializerTestCase(TestCase):
    def test_ok(self):
        offer_1 = Offer.objects.create(
            bank_name='bank test 1',
            term_min=5,
            term_max=10,
            rate_min=2.8,
            rate_max=13.97,
            payment_min=500000,
            payment_max=5000000
        )
        offer_2 = Offer.objects.create(
            bank_name='bank test 2',
            term_min=1,
            term_max=20,
            rate_min=1,
            rate_max=23,
            payment_min=100000,
            payment_max=1000000
        )
        data = OfferSerializer([offer_1, offer_2], many=True).data
        expected_data = [
            {
                'id': offer_1.id,
                'bank_name': 'bank test 1',
                'term_min': 5,
                'term_max': 10,
                'rate_min': '2.80',
                'rate_max': '13.97',
                'payment_min': 500000,
                'payment_max': 5000000,
            },
            {
                'id': offer_2.id,
                'bank_name': 'bank test 2',
                'term_min': 1,
                'term_max': 20,
                'rate_min': '1.00',
                'rate_max': '23.00',
                'payment_min': 100000,
                'payment_max': 1000000,
            },
        ]
        self.assertEqual(expected_data, data)
