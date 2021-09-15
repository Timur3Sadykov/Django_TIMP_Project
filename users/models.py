from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
import uuid

class GreenHouse(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('house-detail', kwargs={'pk': self.pk})

class TController(models.Model):
    UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(GreenHouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    vstart = models.DecimalField(max_digits=3, decimal_places=1, default=35.0)
    vstop = models.DecimalField(max_digits=3, decimal_places=1, default=25.0)
    hstart = models.DecimalField(max_digits=3, decimal_places=1, default=15.0)
    hstop = models.DecimalField(max_digits=3, decimal_places=1, default=25.0)
    tmin = models.DecimalField(max_digits=3, decimal_places=1, default=10.0)
    tmax = models.DecimalField(max_digits=3, decimal_places=1, default=38.0)
    refresh = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(300)])
    t = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    status = models.BooleanField(default=False)
    old = models.TextField(default="")

    def get_absolute_url(self):
        return reverse('house-detail', kwargs={'pk': self.house.pk})

class LController(models.Model):
    UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(GreenHouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    LightDayStart = models.TimeField(auto_now=False, auto_now_add=False, default='8:00')
    LightDayStop = models.TimeField(auto_now=False, auto_now_add=False, default='20:00')
    refresh = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(300)])
    light = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.BooleanField(default=False)
    old = models.TextField(default="")

    def get_absolute_url(self):
        return reverse('house-detail', kwargs={'pk': self.house.pk})

class WController(models.Model):
    UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(GreenHouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    WaterStart = models.PositiveIntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(100)])
    WaterStop = models.PositiveIntegerField(default=70, validators=[MinValueValidator(0), MaxValueValidator(100)])
    refresh = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(300)])
    water = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.BooleanField(default=False)
    old = models.TextField(default="")

    def get_absolute_url(self):
        return reverse('house-detail', kwargs={'pk': self.house.pk})
