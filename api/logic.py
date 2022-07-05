from django.db.models import F


def logic(summa, term, field):
    return (summa + summa * term * ((F(field)) / 12) / 100) / (term * 12)

