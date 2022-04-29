from django.db import models
from django.core.validators import MinValueValidator


class Currency(models.Model):
    title = models.CharField(max_length=100)
    code = models.SlugField(unique=True)
    ratio = models.FloatField()


class Wallet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='Main')
    amount = models.FloatField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['owner']
