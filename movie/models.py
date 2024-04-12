from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=200)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    release_date = models.DateField()

    def __str__(self):
        return self.name
