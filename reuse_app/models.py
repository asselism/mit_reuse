from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django import forms

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
