from django.db import models

from django.db import models


class Collections(models.Model):
    public = models.BooleanField(default=False)
    # user = models.ForeignKey('auth.User', related_name='collections_user')
    # collection_place=models.ForeignKey('companies.CompanyOffice',related_name='collections_place',null=True, blank=True)
    collection_name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    # items=models.ManyToManyField('collection.CollectionItem')
    def __str__(self):
        return self.collection_name

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"


class CollectionItem(models.Model):

    sort_number = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=120, null=False, blank=False)
    # item_type = models.ForeignKey(ContentType, limit_choices_to=models.Q(app_label='immortalawards', model='AwardEntry') | models.Q(app_label='news', model='News') | models.Q(app_label='work', model='Work') | models.Q(app_label='collection', model='Quote'))
    item_id = models.PositiveIntegerField()
    # item = generic.GenericForeignKey('item_type', 'item_id')
    # news=models.ForeignKey('news.News',null=True)
    # award = models.ForeignKey('immortalawards.AwardEntry', null=True)
    # work = models.ForeignKey('work.Work', null=True)
    # quote = models.ForeignKey('collection.Quote', null=True)

    class Meta:
        verbose_name = "Collection Item"
        verbose_name_plural = "Collection Items"

    def __str__(self):
        return self.type
