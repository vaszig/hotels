from django.http import response
from django.urls import reverse
from django.test import TestCase, Client

from app.models import Hotel, City


class ListSearchHotelsView(TestCase):
    

    def setUp(self):
        self.client = Client()
        
        # Add some cities and hotels in database for testing purposes
        City.objects.bulk_create(
            [
                City(id='AMS', name='Amsterdam'),
                City(id='ANT', name='Antwerpen'),
                City(id='BER', name='Berlin'),
                City(id='BAR', name='Barcelona')
            ]
        )
        Hotel.objects.bulk_create(
            [
                Hotel(id='AMS909', city=City.objects.get(id='AMS'), name='Amsterdam Hotel'),
                Hotel(id='ANT77', city=City.objects.get(id='ANT'), name='Hotel Ant'),
                Hotel(id='ANT888', city=City.objects.get(id='ANT'), name='Second Hotel Ant'),
                Hotel(id='BAR8', city=City.objects.get(id='BAR'), name='Barcelona Hotel'),
                Hotel(id='BER22', city=City.objects.get(id='BER'), name='Berlin Hotel')
            ]
        )

    def test_list_hotels_fetches_all_rows_from_db(self):
        self.client.get(reverse('list_hotels'))
        cities_qs = City.objects.prefetch_related('hotel_set')
        
        cities = [city.id for city in cities_qs]
        hotels = [hotel.id for city in cities_qs for hotel in city.hotel_set.all()]
        
        self.assertEquals(cities, ['AMS', 'ANT', 'BER', 'BAR'])
        self.assertEquals(hotels, ['AMS909', 'ANT77', 'ANT888', 'BER22', 'BAR8'])


    def test_search_hotels_view_returns_right_hotels_of_one_matching_city(self):
        chosen_city = {'city': 'antw'}
        response = self.client.get(reverse('search_hotels'), chosen_city)

        cities = [city['city'] for city in response.json()['data']]
        hotels = [hotel for city in response.json()['data'] for hotel in city['hotels']]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(cities, ['Antwerpen'])
        self.assertEquals(hotels, ['Hotel Ant', 'Second Hotel Ant'])

    def test_search_hotels_view_returns_hotels_of_multiple_matching_cities(self):
        chosen_cities = {'city': 'b'}
        response = self.client.get(reverse('search_hotels'), chosen_cities)
        cities = [city['city'] for city in response.json()['data']]
        hotels = [hotel for city in response.json()['data'] for hotel in city['hotels']]
        self.assertEquals(response.status_code, 200)
        self.assertEquals(cities, ['Berlin','Barcelona'])
        self.assertEquals(hotels, ['Berlin Hotel', 'Barcelona Hotel'])
