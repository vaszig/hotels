from django.shortcuts import render
from django.http import JsonResponse

from .models import City


def list_hotels(request):
    """Lists all cities and hotels."""
    cities = City.objects.prefetch_related('hotel_set')
    return render(request, "hotel_search/list_hotels.html", {'cities':cities})
    

def search_hotels(request):
    """Lists all hotels according to the city the user searches for."""
    results = []
    city = request.GET.get('city')
    cities_qs = City.objects.prefetch_related('hotel_set').filter(name__icontains=city)
    if cities_qs.count() > 0 and len(city) > 0:
        for city in cities_qs:
            item = {'city':city.name, 'hotels':[]}
            for hotel in city.hotel_set.all():
                item['hotels'].append(hotel.name)
            results.append(item)
    return JsonResponse({'data': results})
