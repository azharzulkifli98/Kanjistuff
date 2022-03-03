from django.db import models

# Create your models here.
class Tag(models.Model):
    tag_id = models.CharField(max_length=20)
    tag_name = models.CharField(max_length=20)
    tag_description = models.CharField(max_length=70)
