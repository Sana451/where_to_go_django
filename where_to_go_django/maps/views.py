import json

from django.http import Http404, JsonResponse
from django.shortcuts import render
from .models import Place


def index(request):
    places = Place.objects.all().prefetch_related('images')
    places_data = [place.to_dict() for place in places]

    context = {
        'places_data': json.dumps(places_data)
    }

    return render(request, template_name="maps/index.html", context=context)


def place_detail(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise Http404("Place not found")

    return JsonResponse(place.to_dict(), json_dumps_params={'ensure_ascii': False})
