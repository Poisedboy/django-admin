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
    product_categories = models.TextField()
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
    
class AwardJury(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    award_show = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='jury_images/')
    user_id = models.IntegerField()
    is_super = models.BooleanField(default=False)
    hide_from_final_judging = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AwardResult(models.Model):
    AWARD_SHOW_CHOICES = [
        ('New Creators Showcase', 'The New Creators Showcase'),
        ('Immortal Awards', 'The Immortal Awards')
    ]

    award_name = models.CharField(max_length=100)
    min_score = models.IntegerField(default=1)
    max_score = models.IntegerField(default=500)
    award_show = models.CharField(max_length=100, choices=AWARD_SHOW_CHOICES)

    def __str__(self):
        return f"{self.award_name}"
    
class AwardShows(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    submissions_start_date = models.DateTimeField()
    submissions_deadline = models.DateTimeField()
    online_judging_start_date = models.DateTimeField()
    global_shortlist_date = models.DateTimeField()
    final_judging_start_date = models.DateTimeField()
    winners_announced_date = models.DateTimeField()
    launch_date_from = models.DateTimeField()
    launch_date_to = models.DateTimeField()
    announce_results_till = models.DateTimeField()
    office = models.CharField(max_length=200)
    stop_submissions = models.BooleanField(default=False)
    show_league_table = models.BooleanField(default=False)

class AwardSponsor(models.Model):
    TYPES = [
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
        ('Global', 'Global'),
        ('White Paper', 'White Paper'),
        ('North America', 'North America'),
        ('Europe', 'Europe'),
        ('Latin America', 'Latin America'),
        ('Middle East & Africa', 'Middle East & Africa'),
        ('Asia Pacific', 'Asia Pacific'),
    ]
    title = models.CharField(max_length=100)
    url = models.URLField()
    logo = models.ImageField(upload_to='logo/')
    isGlobal = models.BooleanField(default=False)
    immortal = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    type = models.CharField(max_length=30, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class AwardMedia(models.Model):
    EXISTS_IN = [
        ('Campaign & Single', 'Campaign & Single'),
        ('Single', 'Single'),
        ('Campaign', 'Campaign'),
    ]

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    # parent = models.CharField(max_length=30, null=True, blank=True)
    from_entry_id = models.CharField(max_length=50)
    to_entry_id = models.CharField(max_length=50)
    show_in_frontend = models.BooleanField(default=False)
    exists_in = models.CharField(max_length=100, choices=EXISTS_IN)

    def __str__(self):
        return self.name
    
class CategoryMediumRegion(models.Model):
    category = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    region = models.ManyToManyField(Region)
    country = models.CharField(max_length=100)
    from_entry_id = models.IntegerField()
    to_entry_id = models.IntegerField()

    def __str__(self):
        return f"{self.category} - {self.medium} - {self.region} - {self.country}"
    
class CountryForJuryAllotment(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    online_judging = models.BooleanField(default=False)
    live_judging = models.BooleanField(default=False)

class Side(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    logo = models.ImageField(upload_to='logo/')
    ribbon_title = models.CharField(max_length=100, blank=True, null=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    award_show = models.CharField(max_length=100, choices=[
        ('The Immortal Awards', 'The Immortal Awards'),
        ('The New Creators Showcase', 'The New Creators Showcase'),
    ], blank=True, null=True)
    order = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class TaggedCompanies(models.Model):
    entry = models.ForeignKey(AwardEntry, on_delete=models.PROTECT)
    company = models.CharField(max_length=30)
    score = models.ImageField(default=1)