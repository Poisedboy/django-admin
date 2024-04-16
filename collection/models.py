from django.db import models

class Collection (models.Model):
    meta_description = models.CharField()
    meta_title = models.CharField()
    meta_keywords = models.CharField()
    item_type = models.CharField()
    public = models.BooleanField(default=False)
    collection_place = models.CharField(null=True)
    collection_name = models.CharField(max_length=100)
    description = models.CharField()

    class Meta:
        verbose_name_plural = 'Collection'

    def __str__(self):
        return self.collection_name
    
