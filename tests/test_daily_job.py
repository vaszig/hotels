import os
from unittest import mock

import requests
from django.test import TestCase

from app.models import Hotel, City


class MockedResponse:

    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code


def mock_csv_data(cities=b'', hotels=b'', status_code=200):

    def get(url, *args, **kwargs):
        if url.endswith('city.csv'):
            return MockedResponse(cities, status_code)
        elif url.endswith('hotel.csv'):
            return MockedResponse(hotels, status_code)
        else:
            raise RuntimeError(f'Unexpected url to mock: {url}')
        
    requests.get = get


def mock_daily_job():
    with mock.patch.dict(os.environ, {
        'M_USERNAME': 'user', 
        'M_PASSWORD': 'pass', 
        'MC_URL': 'urlcity.csv', 
        'MH_URL': 'urlhotel.csv'
        }):
        from app.tasks import daily_job
        daily_job()


class TestCronjob(TestCase):        


    def test_cronjob_saves_new_data(self):        
        mock_csv_data(cities=b'"AMS";"Amsterdam"', hotels=b'"AMS";"AMS777";"Hotel"')
        mock_daily_job()

        city_results = City.objects.all().first()
        hotel_results = Hotel.objects.all().first()

        self.assertEquals(city_results.id, 'AMS')
        self.assertEquals(city_results.name, 'Amsterdam')
        
        self.assertEquals(hotel_results.id, 'AMS777')
        self.assertEquals(hotel_results.name, 'Hotel')
        self.assertEquals(hotel_results.city_id, 'AMS')

    def test_cronjob_does_not_save_invalid_data(self):
        mock_csv_data(cities=b'"WR"', hotels=b'"UU88","Wrong hotel"')
        mock_daily_job()
        
        city_results = City.objects.all()
        hotel_results = Hotel.objects.all()

        self.assertEquals(city_results.count(), 0)
        self.assertEquals(hotel_results.count(), 0)

    def test_cronjob_updates_name_of_existing_hotels_and_cities(self):
        mock_csv_data(cities=b'"AMS";"Amsterdam"', hotels=b'"AMS";"AMS777";"Hotel"')
        mock_daily_job()
        mock_csv_data(b'"AMS";"Amsterdam1"', hotels=b'"AMS";"AMS777";"Modified hotel"')
        mock_daily_job()

        city_results = City.objects.all().first()
        hotel_results = Hotel.objects.all().first()

        self.assertEquals(city_results.id, 'AMS')
        self.assertEquals(city_results.name, 'Amsterdam1')
        self.assertEquals(hotel_results.id, 'AMS777')
        self.assertEquals(hotel_results.name, 'Modified hotel')
        self.assertEquals(hotel_results.city_id, 'AMS')

    def test_csv_import_response_is_not_200(self):
        mock_csv_data(cities=b'"AMS";"Amsterdam"', hotels=b'"AMS";"AMS777";"Hotel"', status_code=405)
        mock_daily_job()

        cities = City.objects.all()
        hotels = Hotel.objects.all()

        self.assertEquals(cities.count(), 0)
        self.assertEquals(hotels.count(), 0)
