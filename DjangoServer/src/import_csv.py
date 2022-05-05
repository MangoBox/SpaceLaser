# This file imports a CSV file into the Django database.
# It finds the orbital parameters and corresponds them into each one of the Django database fields.

import os
from re import A
import sys
import django
from datetime import datetime
sys.path.append('./try_django')
#from django_project import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'try_django.settings')
django.setup()

import csv
from targets import models


print(os.getcwd())
file_name = "./planets.csv"

with open(file_name, 'r') as planets:
    csv_reader = csv.reader(planets, delimiter=',')
    target_count = 0
    for target in csv_reader:
        if target_count != 0:
            #Insert data into field.
            p = models.SolarTarget()
            p.title = target[0]
            p.centre_body = target[1].upper()
            p.type = "PL"
            p.semimajor_axis = target[2]
            p.eccentricity = target[3]
            p.inclination = target[4]
            p.perihelion = target[5]
            p.longitude = target[6]
            p.mean_anomaly = target[7]
            input_date = target[8]
            time_result = datetime.strptime(input_date, "%d/%m/%y %H:%M")
            #Note: check in future month-day order is okay. could cause issues for non 2000 epochs.
            #print( time_result.strftime("%Y-%m-%d %H:%M"))
            p.init_date = time_result.strftime("%Y-%m-%d %H:%M")
            p.save()
            print(target)
        target_count += 1