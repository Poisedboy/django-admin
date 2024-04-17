from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User

class CraftCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Jobs Categories"

    def __str__(self):
        return self.name

class Skill(models.Model):
    skill = models.CharField(max_length=100)
    category = models.ForeignKey(CraftCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.skill

class Craft(models.Model):
    description = models.CharField(max_length=100)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.description} - {self.skill.skill}'
    
class Jobs(models.Model):
    city = models.CharField(max_length=100)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    meta_description = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=100)
    meta_keywords = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    office = models.CharField(max_length=100)
    category = models.ForeignKey(CraftCategory, on_delete=models.PROTECT)
    employer = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    contract = models.CharField(max_length=100)
    office_type = models.CharField(max_length=100, choices=[
        ('On-site', 'On-site'),
        ('Remote', 'Remote'),
        ('Hybrid(On-site & Remote)', 'Hybrid(On-site & Remote)'),
    ])
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField()
    skill_set = models.CharField(max_length=255)
    job_expire = models.DateField()
    editions_shared_to = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.position

class JobApplicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    job = models.ForeignKey(Jobs, on_delete=models.PROTECT)
    comment = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Job Applicants"

    def __str__(self):
        return f"{self.user} - {self.job}"
    
class Resume(models.Model):
    name = models.ForeignKey(User, on_delete=models.PROTECT)
    email = models.EmailField()
    category = models.ForeignKey(CraftCategory, on_delete=models.PROTECT)
    skill_set = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    last_job = models.CharField(max_length=100)
    past_jobs = models.TextField()
    education = models.CharField(max_length=100)
    links = models.URLField()
    summary = models.TextField()
    skills = models.ForeignKey(Skill, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Resumes"

    def __str__(self):
        return self.email