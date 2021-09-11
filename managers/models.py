from django.db import models
from django.contrib.auth.models import User

from app.models import City


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)