from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from datetime import datetime, timedelta

class CoordinateField(models.DecimalField):
    def __init__(self, **kwargs):
        kwargs['max_digits'] = 9
        kwargs['decimal_places'] = 6
        super().__init__(**kwargs)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField('Title', max_length=32, validators = (
        validators.MinLengthValidator(5),)
    )
    loc_text = models.CharField('Where?', max_length = 32, blank = True)
    loc_lat = CoordinateField(default = 42.3598)
    loc_lng = CoordinateField(default = -71.0921)
    description = models.TextField('Description', max_length = 1024)

    updated_at = models.DateTimeField(auto_now = True)
    marked_taken = models.BooleanField(default = False)

    def is_archived(self):
        return self.updated_at < Listing.get_archived_t()

    @staticmethod
    def get_archived_t():
        return timezone.now() - timedelta(hours=8)
