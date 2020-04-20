import random

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def gen_code():
	symbols = 'ab1cd2ef3gh4ij5kl6mn7op8qr9stuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_'
	code = ''.join([random.choice(symbols) for i in range(8)])
	return code


class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True, default=gen_code)
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	active = models.BooleanField()

	def __str__(self):
		return self.code
