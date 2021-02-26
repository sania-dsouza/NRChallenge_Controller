import datetime
from time import time

from django.db import models


class ControllerReadings(models.Model):
    cumulative_CO2 = models.FloatField()
    minute_heat_rate_avg = models.FloatField()
    plant_efficiency = models.FloatField()
    co2_reserve = models.PositiveBigIntegerField()
    measured_date = models.DateField()
    measured_at_minute = models.PositiveSmallIntegerField(default=1)   # Minute of the emission

    def __str__(self):
        return str(self.measured_date) + ", " + str(self.measured_at_minute)