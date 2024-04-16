from django import forms
from django.conf import settings

# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.forms.widgets import TextInput
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings


class M2MFilterSelect(forms.Select):

    def __init__(
        self, filter_field_id, filter_model, filter_model_field, attrs=None, choices=()
    ):
        super(M2MFilterSelect, self).__init__(attrs, choices)
        self.filter_field_id = filter_field_id
        self.filter_model = filter_model
        self.filter_model_name = filter_model.__name__
        self.filter_app_name = filter_model._meta.app_label
        self.filter_model_field = filter_model_field

    def render(self, name, value, attrs=None, choices=()):
        output = super(M2MFilterSelect, self).render(
            name, value, attrs=attrs, choices=choices
        )

        url = reverse(
            "filter_model",
            kwargs={
                "app": self.filter_app_name,
                "model": self.filter_model_name,
                "field": self.filter_model_field,
                "value": 0,
            },
        )[:-3]

        js = """
            <script type="text/javascript">
            //<![CDATA[
                $(function (){
                    $('#%(id)s').change(function (){
                        if ($(this).val() == ''){
                            $("#%(filter_field_id)s").html('');
                            return;
                        }
                        $.getJSON("%(url)s/"+$(this).val()+"/", function(j){
                            var options = '';
                            for (var i = 0; i < j.objects.length; i++) {
                                options += '<option value="' + j.objects[i].value + '">' + j.objects[i].label + '<'+'/option>';
                            }
                            $("#%(filter_field_id)s").html(options);

                        })

                    })
                    //$("#%(id)s").change();

                });



            //]]>
            </script>

            """ % {
            "url": url,
            "id": attrs["id"],
            "filter_field_id": self.filter_field_id,
            "value": value,
        }

        return mark_safe(output + js)

    class Media:
        js = [
            "%s%s" % (settings.STATIC_URL, i)
            for i in ("js/jquery.min.js", "js/jquery.init.js")
        ]


class M2MFilterSelectMultiple(forms.Select):

    def __init__(
        self, filter_field_id, filter_model, filter_model_field, attrs=None, choices=()
    ):
        super(M2MFilterSelectMultiple, self).__init__(attrs, choices)
        self.filter_field_id = filter_field_id
        self.filter_model = filter_model
        self.filter_model_name = filter_model.__name__
        self.filter_app_name = filter_model._meta.app_label
        self.filter_model_field = filter_model_field

    def render(self, name, value, attrs=None, choices=()):
        output = super(M2MFilterSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )

        url = reverse(
            "filter_model",
            kwargs={
                "app": self.filter_app_name,
                "model": self.filter_model_name,
                "field": self.filter_model_field,
                "value": 0,
            },
        )[:-3]

        js = """
            <script type="text/javascript">
                $(function (){
                    if ($('#%(id)s').val() == ''){
                        $("#%(filter_field_id)s").html('');
                        $("#%(filter_field_id)s").selectpicker('refresh');
                    }
                    $('#%(id)s').change(function (){
                        if ($(this).val() == ''){
                            $("#%(filter_field_id)s").html('');
                            $("#%(filter_field_id)s").selectpicker('refresh');
                            return;
                        }
                        $.getJSON("%(url)s/"+$(this).val()+"/", function(j){
                            var options = '';
                            for (var i = 0; i < j.objects.length; i++) {
                                options += '<option value="' + j.objects[i].value + '">' + j.objects[i].label + '<'+'/option>';
                            }
                            $("#%(filter_field_id)s").html(options);
                            $("#%(filter_field_id)s").selectpicker('refresh');

                        })

                    })
                    //$("#%(id)s").change();

                });



            </script>

            """ % {
            "url": url,
            "id": attrs["id"],
            "filter_field_id": self.filter_field_id,
            "value": value,
        }

        return mark_safe(output + js)


class M2MFilterCheckboxSelectMultiple(forms.Select):

    def __init__(
        self, filter_field_id, filter_model, filter_model_field, attrs=None, choices=()
    ):
        super(M2MFilterCheckboxSelectMultiple, self).__init__(attrs, choices)
        self.filter_field_id = filter_field_id
        self.filter_model = filter_model
        self.filter_model_name = filter_model.__name__
        self.filter_app_name = filter_model._meta.app_label
        self.filter_model_field = filter_model_field

    def render(self, name, value, attrs=None, choices=()):
        output = super(M2MFilterCheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )

        url = reverse(
            "filter_model",
            kwargs={
                "app": self.filter_app_name,
                "model": self.filter_model_name,
                "field": self.filter_model_field,
                "value": 0,
            },
        )[:-3]

        js = """
            <script type="text/javascript">
            //<![CDATA[
                $(function (){
                    $('#%(id)s').change(function (){
                        if ($(this).val() == ''){
                            $("label[for=%(filter_field_id)s]").next('ul').html('');
                            return;
                        }
                        $.getJSON("%(url)s/"+$(this).val()+"/", function(j){
                            var ul = $("label[for=%(filter_field_id)s]").next('ul').html('');
                            $.each(j.objects, function(key, value){
                                ul.append($('<li><label><input type="checkbox" class="checkboxselectmultiple" name="skills" value="'+ value.value +'"> ' + value.label + '</label></li>'));
                            });
                        })

                    })
                    //$("#%(id)s").change();

                });



            //]]>
            </script>

            """ % {
            "url": url,
            "id": attrs["id"],
            "filter_field_id": self.filter_field_id,
            "value": value,
        }

        return mark_safe(output + js)

    class Media:
        js = [
            "%s%s" % (settings.STATIC_URL, i)
            for i in ("js/jquery.min.js", "js/jquery.init.js")
        ]


class AddressWithMapWidget(TextInput):
    choices = []

    def render(self, name, value, attrs=None):
        default_html = super(AddressWithMapWidget, self).render(name, value, attrs)
        if not value:
            value = "London, United Kingdom"
        map_template = Template(
            "{% load easy_maps_tags %}{% easy_map address 400 200 14 using 'easy_maps/map_widget.html' %}"
        )
        context = Context(
            {
                "address": value,
                "input_id": attrs["id"],
                "easy_key": settings.EASY_MAPS_GOOGLE_KEY,
            }
        )
        try:
            map_rendered = map_template.render(context)
        except Exception as e:
            context["address"] = "London, United Kingdom"
            map_rendered = map_template.render(context)
        return default_html + map_rendered


class InlineLocationAutocompleteWidget(TextInput):
    choices = []

    def __init__(self, attrs=None):
        super(InlineLocationAutocompleteWidget, self).__init__(attrs)
        self.attrs["autocomplete"] = "off"

    def render(self, name, value, attrs=None):
        default_html = super(InlineLocationAutocompleteWidget, self).render(
            name, value, attrs
        )
        autocomplete = """
            <script type="text/javascript">
                $(function() {
                    var input = document.getElementById('%s');
                    console.log($('#%s').closest("div").find("ul").remove());
                    var autocomplete = new google.maps.places.Autocomplete(input, {types: ['(cities)']});
                });
            </script>
        """ % (
            attrs["id"],
            attrs["id"],
        )
        return mark_safe(default_html + autocomplete)


class LocationAutocompleteWidget(TextInput):
    choices = []

    def __init__(self, attrs=None):
        super(LocationAutocompleteWidget, self).__init__(attrs)
        self.attrs["autocomplete"] = "off"

    def render(self, name, value, attrs=None):
        default_html = super(LocationAutocompleteWidget, self).render(
            name, value, attrs
        )
        autocomplete = """
            <script type="text/javascript">
                $(function() {
                    var input = document.getElementById('%s');
                    
                    var autocomplete = new google.maps.places.Autocomplete(input, {types: ['(cities)']});
                });
            </script>
        """ % (
            attrs["id"]
        )
        return mark_safe(default_html + autocomplete)


class TagsInputWidget(TextInput):
    def _media(self):
        return forms.Media(
            css={"all": ("css/bootstrap-tag.css",)},
            js=("js/bootstrap/bootstrap-tag.js",),
        )

    media = property(_media)

    def __init__(self, model, attrs=None):
        self.model = model
        self.url = model.__name__.lower()
        super(TagsInputWidget, self).__init__(attrs)

    def _format_value(self, value):
        tags = self.model.objects.filter(pk__in=value)
        return ", ".join([tag.name for tag in tags])

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != "":
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs["value"] = force_str(self._format_value(value))
        final_attrs["autocomplete_url"] = "/api/lbb/%s/" % (self.url)
        return mark_safe(render_to_string("lbb/widgets/tags_input.html", final_attrs))


class CategoryInputWidget(forms.SelectMultiple):
    def value_from_datadict(self, data, files, name):
        value = data.getlist(name, None)
        if len(value) == 2 and value[0] and value[1]:
            return value
        return None

    def render(self, name, value, attrs=None, choices=()):
        from lbb.models import Category

        categories = Category.objects.filter(parent__isnull=True)
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        try:
            parent = categories.filter(pk__in=value)[0]
            parent_value = parent.pk

            child_value = (
                int(value[1]) if str(value[0]) == str(parent_value) else int(value[0])
            )
        except Exception as e:
            parent_value = None
            child_value = None

        return mark_safe(
            render_to_string(
                "lbb/widgets/category_input.html",
                {
                    "final_attrs": final_attrs,
                    "value": value,
                    "categories": categories,
                    "subcategories": (
                        Category.objects.filter(parent=parent_value)
                        if parent_value
                        else None
                    ),
                    "parent_value": parent_value,
                    "child_value": child_value,
                    "child_check_url": "/api/lbb/categories/",
                },
            )
        )


class AwardCategoryInputWidget(forms.SelectMultiple):

    def value_from_datadict(self, data, files, name):
        value = data.getlist(name, None)
        if len(value) == 2 and value[0] is not None and value[1] is not None:
            return [value[0]]
        elif len(value) == 1:
            return [value[0]]
        return None

    def render(self, name, value, attrs=None, choices=()):
        from immortalawards.models import AwardsCategory

        categories = AwardsCategory.objects.filter(parent__isnull=True)
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        try:
            parent = categories.filter(pk__in=value).first()
            parent_value = parent.pk
            child_value = None
        except Exception as e:
            parent_value = None
            child_value = None
        return mark_safe(
            render_to_string(
                "lbb/widgets/awards_category_input.html",
                {
                    "final_attrs": final_attrs,
                    "value": value,
                    "categories": categories,
                    "subcategories": (
                        AwardsCategory.objects.filter(parent=parent_value)
                        if parent_value
                        else None
                    ),
                    "parent_value": parent_value,
                    "child_value": child_value,
                    "child_check_url": "/api/immortals/awards_categories/",
                },
            )
        )


class AwardMediumInputWidget(forms.SelectMultiple):

    def value_from_datadict(self, data, files, name):
        value = data.getlist(name, None)
        if len(value) == 2 and value[0] and value[1]:
            return value
        return None

    def render(self, name, value, attrs=None, choices=()):
        from immortalawards.models import AwardsMedium

        categories = AwardsMedium.objects.filter(parent__isnull=True)
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        try:
            parent = categories.filter(pk__in=value)[0]
            parent_value = parent.pk

            child_value = (
                int(value[1]) if str(value[0]) == str(parent_value) else int(value[0])
            )
        except Exception as e:
            parent_value = None
            child_value = None

        return mark_safe(
            render_to_string(
                "lbb/widgets/awards_category_input.html",
                {
                    "final_attrs": final_attrs,
                    "value": value,
                    "categories": categories,
                    "subcategories": (
                        AwardsMedium.objects.filter(parent=parent_value)
                        if parent_value
                        else None
                    ),
                    "parent_value": parent_value,
                    "child_value": child_value,
                    "child_check_url": "/api/immortals/awards_medium/",
                },
            )
        )


class SummernoteWidget(forms.Textarea):
    pass
