from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import Offer


@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    pass
