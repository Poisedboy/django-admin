from django.contrib import admin
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'collection_name']

admin.site.register(Collection, CollectionAdmin)
