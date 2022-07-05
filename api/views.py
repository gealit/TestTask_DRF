from django.db.models import Sum, Value, DecimalField, IntegerField, Q

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import GenericViewSet

from api.logic import logic
from api.models import Offer
from api.permissions import IsStaffOrReadOnly
from api.serializers import OfferSerializer


class OfferViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_queryset(self):
        queryset = Offer.objects.all().order_by('rate_min')
        request = self.request.GET
        if request.get('price', False) and request.get('deposit', False) \
                and request.get('term', False):

            try:
                price = int(request['price'])
                deposit = float(request['deposit'])
                term = int(request['term'])
            except MultiValueDictKeyError and ValueError:
                print("Введены неверные данные")
                return queryset

            if price > 0 and term > 0 and 0 <= deposit < 100:
                summa = (price - price * deposit / 100)
                queryset = queryset.filter(
                    Q(payment_min__lte=summa) & Q(payment_max__gte=summa)
                )
                queryset = queryset.filter(
                    Q(term_min__lte=term) & Q(term_max__gte=term)
                )
                result = queryset.annotate(
                    payment_low=Sum(logic(summa, term, field='rate_min'))
                )
                result = result.annotate(
                    payment_high=Sum(logic(summa, term, field='rate_max'))
                )
                result = result.annotate(
                    price=Value(price, output_field=IntegerField())
                )
                result = result.annotate(
                    deposit=Value(deposit, output_field=DecimalField(
                        max_digits=4, decimal_places=2
                    ))
                )
                result = result.annotate(
                    term=Value(term, output_field=IntegerField())
                )
                return result
        return queryset

    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['bank_name']
    ordering_fields = ['rate_min', 'term_min', 'payment_min']
