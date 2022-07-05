from django.db import models


class Offer(models.Model):
    bank_name = models.CharField(max_length=100)
    term_min = models.IntegerField()
    term_max = models.IntegerField()
    rate_min = models.DecimalField(max_digits=4, decimal_places=2)
    rate_max = models.DecimalField(max_digits=4, decimal_places=2)
    payment_min = models.IntegerField()
    payment_max = models.IntegerField()

    def __str__(self):
        return f'ID: {self.id}: {self.bank_name}. ' \
               f'Ставка: {self.rate_min}'
