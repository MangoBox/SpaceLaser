from django.db import models
"""import serial
import datetime
import math
import pandas as pd
from pathlib import Path"""

# Create your models here.
class Telescope(models.Model):
    port = models.CharField(max_length=10)
    baud_rate = models.IntegerField()

    cur_alt = models.DecimalField(max_digits=10, decimal_places=5)
    cur_az  = models.DecimalField(max_digits=10, decimal_places=5)


   # connected = models.BooleanField(default=False)