from django.utils.deconstruct import deconstructible
from datetime import date
from django.core.validators import BaseValidator


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@deconstructible
class MinAgeValidator(BaseValidator):
    message = ("Age must be at least 18.")
    code = 'min_age'

    def compare(self, a):
        return calculate_age(a) < 18