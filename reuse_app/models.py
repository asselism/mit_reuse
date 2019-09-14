from django.db import models
from django.core import validators
from django.contrib.auth.models import User

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField('Title', max_length=32, validators = (
        validators.MinLengthValidator(5),)
    )
    loc_text = models.CharField('Where?', max_length=32, blank = True)
    description = models.TextField('Description', max_length = 1024)
