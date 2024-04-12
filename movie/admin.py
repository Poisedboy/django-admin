from django.contrib import admin

from .models import Movie, Director
from utils.export_csv_file import export_selected_objects_as_csv

class MovieInline (admin.TabularInline):
    model = Movie

class MovieAdmin (admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'director', 'release_date']})
    ]
    list_display = ('name', 'director', 'release_date')
    action = [export_selected_objects_as_csv] 

class DirectorInline (admin.TabularInline):
    model = Director

class DirectorAdmin (admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'age']})
    ]
    list_display = ('name', 'age')
    actions = [export_selected_objects_as_csv]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
