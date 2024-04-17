from django.db import models
from location_field.models.plain import PlainLocationField
from lbb.fields import InlineLocationField


class Company(models.Model):
    # city = models.CharField(max_length=100)
    # location = PlainLocationField(based_fields=["city"], zoom=7)
    # company_group = models.
    city = InlineLocationField(verbose_name=_("City"), null=True, blank=True)
