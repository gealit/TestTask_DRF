from rest_framework.serializers import ModelSerializer

from api.models import Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'id',
            'bank_name',
            'term_min',
            'term_max',
            'rate_min',
            'rate_max',
            'payment_min',
            'payment_max',
        ]

    def to_representation(self, data):
        serializer_data = super(OfferSerializer, self).to_representation(data)
        try:
            if bool(data.price):
                serializer_data.pop(key='id')
                serializer_data.pop(key='term_min')
                serializer_data.pop(key='term_max')
                serializer_data.pop(key='payment_min')
                serializer_data.pop(key='payment_max')
                serializer_data.update(
                    {
                        'payment_min': round(data.payment_low, 2),
                        'payment_max': round(data.payment_high, 2),
                        'price': data.price,
                        'deposit': data.deposit,
                        'term': data.term,
                    }
                )
        except AttributeError:
            print('данные не поступили')
        finally:
            return serializer_data
