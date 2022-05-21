from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord_points = models.ManyToManyField('CoordPoints')


class CoordPoints(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    state = models.CharField(max_length=100)

    def __str__(self):
        return f'state: {self.state} - ({self.lat}, {self.lon})'
