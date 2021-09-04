from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from celery.schedules import crontab

from hotels.celery import app
from .fetch_and_update_data import fetch_csv_data, read_csv, update_cities, update_hotels


@shared_task
def daily_job():
    """Main daily task for downloading csv data and updating the database."""
    city_content = fetch_csv_data(os.environ.get('MC_URL'))
    hotel_content = fetch_csv_data(os.environ.get('MH_URL'))
    cities = read_csv(city_content, 2)
    hotels = read_csv(hotel_content, 3)
    update_cities(cities)
    update_hotels(hotels)

# Settings for the scheduled crontab
app.conf.beat_schedule = {
    'fetching-csv-data-and-update-db-every-day_at_06:00(UTC)': {
        'task':'app.tasks.daily_job',
        'schedule': crontab(minute=0, hour=6),
    },
}
