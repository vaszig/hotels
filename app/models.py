from django.db import models


class City(models.Model):

    id = models.TextField(primary_key=True)
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Hotel(models.Model):

    id = models.TextField(primary_key=True)
    name = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name