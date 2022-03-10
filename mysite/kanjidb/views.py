from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View


class Search(View):
    def get(self, request):
        return HttpResponse(request)

def index(request):
    return HttpResponse("Hello, world. You're at the kanjidb index.")

def search(request):
    return HttpResponse("Not implemented")

def kanji(request, kanji_id):
    return HttpResponse("Should show details about a kanji.")
