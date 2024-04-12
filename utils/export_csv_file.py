from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str

def export_selected_objects_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="selected_objects.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in queryset.model._meta.fields]
    writer.writerow(fields)

    for obj in queryset:
        row = [smart_str(getattr(obj, field)) for field in fields]
        writer.writerow(row)

    return response

export_selected_objects_as_csv.short_description = "Export selected objects as CSV"
