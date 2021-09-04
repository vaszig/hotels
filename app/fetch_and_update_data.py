import csv
import os
from io import StringIO

import requests
from django.core.exceptions import ObjectDoesNotExist
from requests.auth import HTTPBasicAuth

from .models import City, Hotel


def fetch_csv_data(url):
    """Downloads new csv data from server."""
    response = requests.get(
        url, 
        auth=HTTPBasicAuth(os.environ.get('M_USERNAME'), os.environ.get('M_PASSWORD'))
    )
    
    content = ''
    if response.status_code == 200:
        content= response.content.decode()

    return content


def read_csv(content, length): 
    """Reads new csv data and passes the expected rows (list) for update."""     
    csv_list = [item for item in csv.reader(StringIO(content), delimiter=';') if len(item) == length]
    return csv_list


def update_cities(csv_cities):
    """Updates db with the new or updated cities."""
    csv_cities = ({'id':id_, 'name':name} for id_, name in csv_cities)
    db_cities = {id_: name for id_, name in City.objects.values_list('id', 'name')}

    cities_to_create = []
    cities_to_update = []
    
    for city in csv_cities:
        if city['id'] not in db_cities:
            cities_to_create.append(
                City(id=city['id'], name=city['name'])
            )
        elif city['name'] != db_cities[city['id']]:
            city_obj = City.objects.get(id=city['id'])
            city_obj.name = city['name']
            cities_to_update.append(city_obj)
    
    if cities_to_create:
        City.objects.bulk_create(cities_to_create)    
    if cities_to_update:
        City.objects.bulk_update(cities_to_update, ['name'])    


def update_hotels(csv_hotels):
    """Updates db with the new or updated hotels."""
    csv_hotels = ({'city_id':c_id, 'hotel_id':h_id, 'name':name} for c_id, h_id, name in csv_hotels)
    db_hotels = {id_:name for id_, name in Hotel.objects.values_list('id', 'name')}
    
    hotels_to_create = []
    hotels_to_update = []
    
    for hotel in csv_hotels:
        try:
            city_obj = City.objects.get(id=hotel['city_id'])
        except ObjectDoesNotExist:
            continue

        if hotel['hotel_id'] not in db_hotels:
            hotels_to_create.append(
                Hotel(id=hotel['hotel_id'], city=city_obj, name=hotel['name'])
            )
        elif hotel['name'] != db_hotels[hotel['hotel_id']]:
            hotel_obj = Hotel.objects.get(id=hotel['hotel_id'])
            hotel_obj.name = hotel['name']
            hotels_to_update.append(hotel_obj)
    
    if hotels_to_create:
        Hotel.objects.bulk_create(hotels_to_create)    
    if hotels_to_update:
        Hotel.objects.bulk_update(hotels_to_update, ['name'])  
