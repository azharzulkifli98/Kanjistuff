from django.db import models
from datetime import date

# need many to many relationship
class Tag(models.Model):
    tag_id = models.CharField(max_length=20)
    tag_name = models.CharField(max_length=30)
    tag_description = models.CharField(max_length=255)
    num_kanji_included = models.PositiveIntegerField(default=0)

    date_created = models.DateTimeField(default=date.today)
    last_updated = models.DateTimeField(default=date.today)

    def __str__(self):
        return self.tag_name

class Kanji(models.Model):
    kanji_id = models.CharField(max_length=20)
    kanji_name = models.CharField(max_length=30)
    kanji_description = models.CharField(max_length=255)
    kanji_api_info = models.URLField()
    num_tags_included = models.PositiveIntegerField(default=1)
    list_tags_included = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(default=date.today)
    last_updated = models.DateTimeField(default=date.today)

    def __str__(self):
        return self.kanji_name
