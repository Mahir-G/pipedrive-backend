from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pipeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    deal_probability = models.BooleanField(default=True)
    

class Board(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=64)
    probability = models.IntegerField(blank=True)
    rotting_in = models.IntegerField(blank=True)


class Lead(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=64, blank=True)
    organization = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=64)
    value = models.IntegerField(blank=True)
    currency = models.CharField(max_length=10, blank=True)
    expected_close_date = models.DateField(blank=True)

