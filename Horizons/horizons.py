import datetime
import requests
import pandas as pd
import re
from pathlib import Path



queries_filepath = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/Horizons_queries.csv') 
queries = pd.read_csv(queries_filepath)

planets_filepath = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/temp.csv')

url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
spk_filename = 'spk_file.bsp'
file = 'documents/GitHib/SpaceLaser/input.txt'

example = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='499'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='2006-01-01'&STOP_TIME='2006-01-20'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"

request_base = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text"

pattern = "\$\$SOE([\s\S]+)\$\$EOE"

#for i in range(len(queries.index)):
query_df = queries.iloc[0]

query_link = request_base
query_link += "&COMMAND='499'" #+ str(query_df["COMMAND"]) + "'"
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

planet_df = pd.DataFrame(columns=["name", "centre_body", "a", "e", "i", "w", "Omega", "M_0", "dtInit"])

planet_df.loc[0] = [query_df["name"], \
                    "Sun", \
                    elements_ephem_df.iloc[11][0], \
                    elements_ephem_df.iloc[2][0], \
                    elements_ephem_df.iloc[4][0], \
                    elements_ephem_df.iloc[6][0], \
                    elements_ephem_df.iloc[5][0], \
                    elements_ephem_df.iloc[9][0], \
                    pd.to_datetime(elements_ephem_df.iloc[1][0].removeprefix(" A.D. "))]

print(planet_df)
planet_df.to_csv(planets_filepath, mode='a', index=False, header=False)