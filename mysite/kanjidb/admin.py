from django.contrib import admin

# Register your models here.
from .models import Tag, Kanji

admin.site.register(Tag)
admin.site.register(Kanji)