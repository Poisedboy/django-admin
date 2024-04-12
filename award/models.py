from django.db import models
from django.utils.html import mark_safe

class AwardBanner(models.Model):
    description = models.CharField(max_length=100)
    home = models.CharField(max_length=100)
    link = models.URLField()
    sort = models.CharField(max_length=50)
    get_cities = models.BooleanField(default=True)
    get_countries = models.BooleanField(default=True)
    image_exists = models.BooleanField(default=True)
    clicks = models.IntegerField()

    def __str__(self):
        return self.description

class AwardCategory(models.Model):
    name = models.CharField(max_length=100)
    # Change relation to according model
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    award_show = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AwardEntry(models.Model):
    MEDIUM_CHOICES = [
        ('Digital', 'Digital'),
        ('Other', 'Other'),
    ]
    GENRE_CHOICES = [
        ('Horror', 'Horror'),
        ('Animation', 'Animation'),
        ('Choreography', 'Choreography'),
    ]
    CATEGORY_CHOICES = [
        ('Creative', 'Creative'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    medium_type = models.CharField(max_length=20, choices=MEDIUM_CHOICES)
    office = models.CharField(max_length=100)
    entrant_company = models.CharField(max_length=100)
    brand_client = models.CharField(max_length=100)
    commissioning_client = models.CharField(max_length=100)
    product_categories = models.TextField()  # You might want to use a different field type depending on the data
    # genres = models.ManyToManyField('Genre')
    image = models.ImageField(upload_to='award_entries/', null=True, blank=True)
    commissioning_client_contact = models.CharField(max_length=100)
    commissioning_client_email = models.EmailField()
    year_of_participation = models.PositiveIntegerField()
    award_show = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    url = models.URLField()
    country_for_jury = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=200)
    placements = models.CharField(max_length=100)
    case_study_description = models.TextField()
    entry_type = models.CharField(max_length=20)
    categories = models.ManyToManyField(AwardCategory)
    # lbb_credits = models.ManyToManyField('Credit', related_name='lbb_entries')
    # old_credits = models.ManyToManyField('Credit', related_name='old_entries')
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    entry_region = models.CharField(max_length=100)
    immortal_score = models.FloatField()
    total_score = models.FloatField()
    moderation_status = models.CharField(max_length=20)
    lbb_admin_email = models.EmailField()
    # works = models.ManyToManyField('Work')
    # case_studies = models.ManyToManyField('CaseStudy')
    # award_scores = models.ManyToManyField('AwardScore')
    # tagged_companies = models.ManyToManyField('TaggedCompany')
    # award_entry_links = models.ManyToManyField('AwardEntryLink')

    def __str__(self):
        return self.title

    def image_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')
    
