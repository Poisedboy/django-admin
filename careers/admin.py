from django.contrib import admin

from .models import Craft, Skill, CraftCategory, JobApplicant, Jobs, Resume

class CareersCraftInline (admin.TabularInline):
    model = Craft

class CareersCraftAdmin (admin.ModelAdmin):
    list_display = ('id', 'description', 'skill')

class CareersSkill (admin.TabularInline):
    model = Skill

class CareersSkillAdmin (admin.ModelAdmin):
    list_display = ('id', 'skill', 'category')

class CareersCategoryInline (admin.TabularInline):
    model = CraftCategory

class CareersCategoryAdmin (admin.ModelAdmin):
    list_display = ['id', 'name']

class CareersJobInline(admin.TabularInline):
    model = Jobs

class CareersJobsAdmin(admin.ModelAdmin):
    list_display = ['id', 'employer', 'category']

class CareersJobsApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']

admin.site.register(Craft, CareersCraftAdmin)
admin.site.register(Skill, CareersSkillAdmin)
admin.site.register(CraftCategory, CareersCategoryAdmin)
admin.site.register(Jobs, CareersJobsAdmin)
admin.site.register(JobApplicant, CareersJobsApplicantAdmin)
admin.site.register(Resume)
