from django.contrib import admin

from .models import AwardBanner, AwardCategory, AwardEntry, AwardJury, Region, AwardResult, AwardShows, AwardSponsor, AwardMedia, CategoryMediumRegion, CountryForJuryAllotment, Side, TaggedCompanies
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

class AwardJuryInline (admin.TabularInline):
    model = AwardJury

class AwardJuryAdmin (admin.ModelAdmin):
        list_display = ('name', 'job_title', 'award_show', 'user_id', 'is_super', 'hide_from_final_judging')
        list_filter = ('award_show', 'is_super', 'hide_from_final_judging')
        search_fields = ('name', 'job_title', 'award_show')

class AwardRegionInline (admin.TabularInline):
    model = Region

class AwardRegionAdmin (admin.ModelAdmin):
    list_display = ('id', 'name',)

class AwardResultInline (admin.TabularInline):
    model = AwardResult

class AwardResultAdmin (admin.ModelAdmin):
    list_display = ('id', 'award_name', 'min_score', 'max_score', 'award_show')

class AwardShowsInline (admin.TabularInline):
    model = AwardShows

class AwardShowsAdmin (admin.ModelAdmin):
    list_display = ('id', 'name', 'office',)

class AwardSponsorInline (admin.TabularInline):
    model = AwardSponsor

class AwardSponsorAdmin (admin.ModelAdmin):
    list_display = ('id', 'title', 'url',)

class AwardMediaAdmin (admin.ModelAdmin):
    list_display = ('id', 'name')

class CategoryMediumRegionAdmin (admin.ModelAdmin):
    list_display = ('id', 'category', 'medium')

class CountryForJuryAllotmentAdmin (admin.ModelAdmin):
    list_display = ('id', 'name', 'region')

class SideAdmin (admin.ModelAdmin):
    list_display = ('id', 'title', 'clicks', 'order')

class TaggedCompaniesAdmin (admin.ModelAdmin):
    list_display = ('id', 'entry', 'company', 'score')

admin.site.register(AwardBanner, AwardBannerAdmin)
admin.site.register(AwardCategory, AwardCategoriesAdmin)
admin.site.register(AwardEntry, AwardEntryAdmin)
admin.site.register(AwardJury, AwardJuryAdmin)
admin.site.register(Region, AwardRegionAdmin)
admin.site.register(AwardResult, AwardResultAdmin)
admin.site.register(AwardShows, AwardShowsAdmin)
admin.site.register(AwardSponsor, AwardSponsorAdmin)
admin.site.register(AwardMedia, AwardMediaAdmin)
admin.site.register(CategoryMediumRegion, CategoryMediumRegionAdmin)
admin.site.register(CountryForJuryAllotment, CountryForJuryAllotmentAdmin)
admin.site.register(Side, SideAdmin)
admin.site.register(TaggedCompanies, TaggedCompaniesAdmin)
