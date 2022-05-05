import datetime
from unicodedata import decimal, name
from numpy import double
import requests
import pandas as pd
import re
import math
from pathlib import Path



queries_filepath = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/Horizons_queries.csv') 
queries = pd.read_csv(queries_filepath)

planets_filepath = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/planets.csv')

url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
spk_filename = 'spk_file.bsp'
file = 'documents/GitHib/SpaceLaser/input.txt'

example = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='499'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='2006-01-01'&STOP_TIME='2006-01-20'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"

request_base = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text"

pattern = "\$\$SOE([\s\S]+)\$\$EOE"

planet_df = pd.DataFrame(columns=["name", "centre_body", "a", "e", "i", "w", "Omega", "M_0", "dtInit"])


# Pulling latest planet data 

'''for i in range(len(queries.index)):
    query_df = queries.iloc[i]

    query_link = request_base
    query_link += "&COMMAND='" + str(query_df["COMMAND"]) + "'"
    query_link += "CENTER='500@10'"
    query_link += "&CSV_FORMAT='YES'"
    query_link += "&OBJ_DATA='NO'"
    query_link += "&STEP_SIZE='1d'"
    query_link += "&START_TIME='" + str(datetime.datetime.utcnow()) + "'"
    query_link += "&STOP_TIME='" + str(datetime.datetime.utcnow() +  datetime.timedelta(days=0.5)) + "'"
    query_link += "&OUT_UNITS='AU-D'"
    query_link += "&EPHEM_TYPE='ELEMENTS'"

    response = requests.get(query_link)
    text = response.text

    elements = re.search(pattern, text)
    elements = str(elements.group()).removeprefix("$$SOE\n").removesuffix("\n$$EOE")

    elements_ephem_df = pd.DataFrame(elements.split(","))

    planet_df.loc[i] = [query_df["name"], \
                        "Sun", \
                        elements_ephem_df.iloc[11][0], \
                        elements_ephem_df.iloc[2][0], \
                        elements_ephem_df.iloc[4][0], \
                        elements_ephem_df.iloc[6][0], \
                        elements_ephem_df.iloc[5][0], \
                        elements_ephem_df.iloc[9][0], \
                        pd.to_datetime(elements_ephem_df.iloc[1][0].removeprefix(" A.D. "))]
'''



# For other bodies (to be called for live script)
name = "599"

query_link = request_base
query_link += "&MAKE_EPHEM=YES"
query_link += "&COMMAND='" + name + "'"
query_link += "&EPHEM_TYPE=OBSERVER"
query_link += "&CENTER='coord@399'"
query_link += "&COORD_TYPE=GEODETIC"
query_link += "&SITE_COORD='+151.28330,-33.91660,0'"
query_link += "&STEP_SIZE='5 MINUTES'"
query_link += "&START_TIME='" + str(datetime.datetime.utcnow()) + "'"
query_link += "&STOP_TIME='" + str(datetime.datetime.utcnow() +  datetime.timedelta(hours=4)) + "'"
query_link += "&QUANTITIES='1,9,20,23,24,47,48'"
query_link += "&REF_SYSTEM='ICRF'"
query_link += "&ANG_FORMAT='HMS'"
query_link += "&CSV_FORMAT='YES'"
query_link += "&OBJ_DATA='YES'"''

response = requests.get(query_link)
text = response.text

results = re.search(pattern, text)
results = str(results.group()).removeprefix("$$SOE\n").removesuffix("\n$$EOE")

pattern_observer = "^\s?([^,]+),[^,]+,[^,]+, (\-*\d+) (\d+) (\d+\.\d+), (\-*\d+) (\d+) (\d+\.\d+)" #Finds Datetime, RA (H, m, s), DEC (H, m, s) - will need to be converted to height and azimuth
results = re.finditer(pattern_observer, results, flags=re.MULTILINE)




df = pd.DataFrame({
        "RA": [],
        "DEC": [],
        "obs_time": []
    })
i = 0

for match in results:
    print(match.groups())
    time = pd.to_datetime(match.group(1))
    RA = math.radians(int(match.group(2))*15 + int(match.group(3))*15/(60) + double(match.group(4))*15/(60*60))
    DEC = math.radians(int(match.group(5)) + int(match.group(6))/(60) + double(match.group(7))/(60*60))
    #RA and DEC in radians due to hidden function

    df2 = pd.DataFrame({
            "RA": [RA],
            "DEC": [DEC],
            "obs_time": [time]
        },
        index = [i])
    
    df = pd.concat([df, df2])
    i = i + 1

print(df)

# planet_df.to_csv(planets_filepath, mode='a', index=False, header=False)
