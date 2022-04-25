# This file imports a CSV file into the Django database.
# It finds the orbital parameters and corresponds them into each one of the Django database fields.

from django.db import models
from targets.models import target
import csv

file_name = "./Horizons/planets.csv"

with open(file_name, 'r') as planets:
    csv_reader = csv.reader(planets, delimiter=',')
    target_count = 0
    for target in csv_reader:
        if target_count != 0:
            #Insert data into field.

            print(target)
        target_count += 1



    