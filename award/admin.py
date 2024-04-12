from django.contrib import admin

from .models import AwardBanner, AwardCategory, AwardEntry
from utils.export_csv_file import export_selected_objects_as_csv

class AwardBannerInline (admin.TabularInline):
    model = AwardBanner

class AwardBannerAdmin (admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description', 'home', 'link', 'sort', 'get_cities', 'get_countries', 'image_exists', 'clicks']})
    ]
    list_display = ('description', 'home', 'link', 'sort', 'get_cities', 'get_countries', 'image_exists', 'clicks')
    actions = [export_selected_objects_as_csv]

class AwardBannerInline (admin.TabularInline):
    model = AwardCategory

class AwardCategoriesAdmin (admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'parent', 'award_show']})
    ]
    list_display = ('name', 'parent', 'award_show')
    actions = [export_selected_objects_as_csv]

class AwardEntryInline (admin.TabularInline):
    model = AwardEntry

class AwardEntryAdmin (admin.ModelAdmin):
    readonly_fields = ['image_preview']
    list_display = ['title', 'medium_type', 'office', 'entrant_company', 'brand_client']
    search_fields = ['title', 'office', 'entrant_company', 'brand_client']
    list_per_page = 10

    list_filter = ['medium_type', 'title']

    fieldsets = (
        ('General Information', {
            'fields': ('title', 'medium_type', 'office', 'entrant_company', 'brand_client')
        }),
        ('Client Information', {
            'fields': ('commissioning_client', 'product_categories', 'commissioning_client_contact', 'commissioning_client_email')
        }),
        ('Entry Details', {
            'fields': ('year_of_participation', 'award_show', 'channel', 'url', 'country_for_jury', 'start_date', 'end_date')
        }),
        ('Additional Information', {
            'fields': ('address', 'placements', 'case_study_description', 'entry_type', 'categories')
        }),
        ('Scores and Status', {
            'fields': ('immortal_score', 'total_score', 'moderation_status', 'lbb_admin_email', 'status')
        }),
        ('Location Information', {
            'fields': ('location', 'entry_region')
        }),
        ('Image', {
            'fields': ('image_preview', 'image')
        }),
    )
    actions = [export_selected_objects_as_csv]

admin.site.register(AwardBanner, AwardBannerAdmin)
admin.site.register(AwardCategory, AwardCategoriesAdmin)
admin.site.register(AwardEntry, AwardEntryAdmin)
