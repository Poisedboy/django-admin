from urllib.error import HTTPError
import logging

from django.conf import settings
from django.db.models.fields.related import ForeignKey, ManyToOneRel
from django.utils.encoding import smart_str
from geopy.exc import GeopyError
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django import forms
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from lbb.geocoders import GoogleGeocoder, GoogleGeocoderDirect
from lbb.widgets import LocationAutocompleteWidget, InlineLocationAutocompleteWidget
import requests

logger = logging.getLogger("geocode")


def validate_location(value):

    q = GoogleGeocoderDirect()
    try:
        geo_data = q.getData(value)

    except Exception as e:
        raise ValidationError(_("Invalid city"))


#    if not city:
#        raise ValidationError(_("Invalid city"))


class LocationFormField(forms.Field):
    widget = LocationAutocompleteWidget

    def __init__(self, *args, **kwargs):
        kwargs.pop("queryset", 1)
        super(LocationFormField, self).__init__(*args, **kwargs)
        self.q = GoogleGeocoderDirect()

    def prepare_value(self, value):
        from lbb.models import City

        if isinstance(value, int):
            return str(City.objects.get(pk=value))
        return value

    def to_python(self, value):
        from lbb.models import Country, City

        try:
            geo_data = self.q.getData(value)
            print("from to_python feilds")
            print(value)
            if geo_data is None:
                raise ValidationError(_("Invalid location"))

            if not geo_data.get("city"):
                raise ValidationError(_("Invalid city"))

            if not geo_data.get("country"):
                raise ValidationError(_("Invalid country"))

            country, created = Country.objects.get_or_create(
                location=geo_data["country_short"],
                defaults={"title": geo_data["country"]},
            )
            location = "%s, %s" % (geo_data["city"], geo_data["country"])
            value, created = City.objects.get_or_create(
                location=location, country=country, defaults={"title": geo_data["city"]}
            )

            return value
        except GeopyError as e:
            logger.warning(e, exc_info=True)
            raise ValidationError(_("Invalid location"))
        except HTTPError as e:
            logger.warning(e, exc_info=True)
            raise ValidationError(
                _("Google geocoding service failed. Please try again later")
            )


class LocationFormFieldInline(LocationFormField):
    widget = InlineLocationAutocompleteWidget

    def to_python(self, value):
        from lbb.models import Country, City

        if not value or value == "":
            return value
        try:
            geo_data = self.q.getData(value)
            print("from to_python feilds")
            print(value)
            if geo_data is None:
                raise ValidationError(_("Invalid location"))

            if not geo_data.get("city"):
                raise ValidationError(_("Invalid city"))

            if not geo_data.get("country"):
                raise ValidationError(_("Invalid country"))

            country, created = Country.objects.get_or_create(
                location=geo_data["country_short"],
                defaults={"title": geo_data["country"]},
            )
            location = "%s, %s" % (geo_data["city"], geo_data["country"])
            value, created = City.objects.get_or_create(
                location=location, country=country, defaults={"title": geo_data["city"]}
            )

            return value
        except GeopyError as e:
            logger.warning(e, exc_info=True)
            raise ValidationError(_("Invalid location"))
        except HTTPError as e:
            logger.warning(e, exc_info=True)
            raise ValidationError(
                _("Google geocoding service failed. Please try again later")
            )


class LocationField(ForeignKey):

    def __init__(self, rel_class=ManyToOneRel, **kwargs):
        kwargs.pop("to", 1)
        super().__init__("lbb.City", rel_class=rel_class, **kwargs)

    def formfield(self, **kwargs):
        # Passing max_length to forms.CharField means that the value's length
        # will be validated twice. This is considered acceptable since we want
        # the value in the form field (to pass into widget for example).
        defaults = {"label": "City"}
        defaults.update(kwargs)
        return LocationFormField(**defaults)


class InlineLocationField(LocationField):

    def formfield(self, **kwargs):
        # Passing max_length to forms.CharField means that the value's length
        # will be validated twice. This is considered acceptable since we want
        # the value in the form field (to pass into widget for example).
        defaults = {"label": "City"}
        defaults.update(kwargs)
        return LocationFormFieldInline(**defaults)


class CommaSeparatedTagField(forms.CharField):
    def __init__(self, model, max=None, min=None, default_kwargs={}, *args, **kwargs):
        self.model = model
        self.max, self.min = max, min
        self.default_kwargs = default_kwargs
        super(CommaSeparatedTagField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Normalize data to an unordered list of distinct, non empty, whitespace-stripped strings."""
        value = super(CommaSeparatedTagField, self).to_python(value)
        if value in EMPTY_VALUES:  # Return an empty list if no useful input was given.
            return []
        return list(
            set(
                [
                    name.strip()
                    for name in value.split(",")
                    if name and not name.isspace()
                ]
            )
        )

    def validate(self, value):
        """Check the limits."""
        super(CommaSeparatedTagField, self).validate(value)
        if value in EMPTY_VALUES:
            return
        count = len(value)
        if self.max and count > self.max:
            raise ValidationError(
                self.error_messages["max"].format(
                    limit_value=self.max, show_value=count
                )
            )
        if self.min and count < self.min:
            raise ValidationError(
                self.error_messages["min"].format(
                    limit_value=self.min, show_value=count
                )
            )

    def clean(self, value):
        """Check names are valid and filter them."""
        names = super(CommaSeparatedTagField, self).clean(value)
        if not names:
            return []
        tags = []
        for tag_name in names:
            if len(tag_name) > 50:
                raise ValidationError(_("Maximum keyword length is 50 chars."))
            try:
                tag = self.model.objects.get(name__iexact=tag_name)
            except self.model.DoesNotExist:
                tag = self.model.objects.create(
                    name=capfirst(tag_name), **self.default_kwargs
                )

            tags.append(tag)

        return tags


class CategoryField(models.ManyToManyField):
    pass
    # def south_field_triple(self):
    #     "Returns a suitable description of this field for South."
    #     # We'll just introspect ourselves, since we inherit.
    #     from south.modelsinspector import introspector
    #     field_class = "django.db.models.fields.related.ManyToManyField"
    #     args, kwargs = introspector(self)
    #     # That's our definition!
    #     return (field_class, args, kwargs)


class NormalCategoryField(models.ManyToManyField):
    pass
    # def south_field_triple(self):
    #     "Returns a suitable description of this field for South."
    #     # We'll just introspect ourselves, since we inherit.
    #     from south.modelsinspector import introspector
    #     field_class = "django.db.models.fields.related.ManyToManyField"
    #     args, kwargs = introspector(self)
    #     # That's our definition!
    #     return (field_class, args, kwargs)


class MediumField(models.ManyToManyField):
    pass
    # def south_field_triple(self):
    #     "Returns a suitable description of this field for South."
    #     # We'll just introspect ourselves, since we inherit.
    #     from south.modelsinspector import introspector
    #     field_class = "django.db.models.fields.related.ManyToManyField"
    #     args, kwargs = introspector(self)
    #     # That's our definition!
    #     return (field_class, args, kwargs)


class AwardCategoryField(models.ManyToManyField):
    pass
    # def south_field_triple(self):
    #     "Returns a suitable description of this field for South."
    #     # We'll just introspect ourselves, since we inherit.
    #     from south.modelsinspector import introspector
    #     field_class = "django.db.models.fields.related.ManyToManyField"
    #     args, kwargs = introspector(self)
    #     # That's our definition!
    #     return (field_class, args, kwargs)
