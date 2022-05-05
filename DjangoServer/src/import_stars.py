# This file imports a CSV file into the Django database.
# It finds the star's parameters and corresponds them into each one of the Django database fields.
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
file_name = "./hygfull.csv"

with open(file_name, 'r') as planets:
    csv_reader = csv.reader(planets, delimiter=',')
    target_count = 0
    #entries = []
    for target in csv_reader:
        if target_count != 0:
            # Star must be named to be added to the entry list.
            title = ""
            if target[6] != "":
                title = target[6]
            elif target[5] != "":
                title = target[5]
            elif target[4] != "":
                title = target[4]
            else:
                continue

            print(title)
            s = models.DeepSpaceTarget()
            s.title = title
            s.right_ascension = target[7]
            s.declination = target[8]
            s.bayer = target[5]
            s.magnitude = target[10]
            s.type = "DSO"
            s.save()
        target_count += 1