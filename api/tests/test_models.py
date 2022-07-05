from unittest import TestCase

from api.models import Offer


class OfferTestCase(TestCase):
    def test_model(self):
        self.offer_1 = Offer.objects.create(
            bank_name='bank test 1 Стандарт',
            term_min=5,
            term_max=10,
            rate_min=2.8,
            rate_max=13.97,
            payment_min=500000,
            payment_max=5000000
        )
        self.assertEqual(
            self.offer_1.__str__(),
            f'ID: {self.offer_1.id}: bank test 1 Стандарт. Ставка: 2.8'
        )
