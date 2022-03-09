from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path(r'kanji/?P<kanji_id>', views.kanji, name='kanji'),
]