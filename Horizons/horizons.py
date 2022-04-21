import sys
import base64
import requests
import pandas as pd
import re
from pathlib import Path



queries_filepath = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/Horizons_queries.csv') 

queries = pd.read_csv(queries_filepath)

url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
spk_filename = 'spk_file.bsp'
file = 'documents/GitHib/SpaceLaser/input.txt'

example = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='499'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='2006-01-01'&STOP_TIME='2006-01-20'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"

request_base = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text"

pattern = "\$\$SOE([\s\S]+)\$\$EOE"

for i in range(len(queries.index)):
  query_df = queries.iloc[i]

  query_link = request_base
  query_link += "&COMMAND='" + query_df["COMMAND"]+"'"
  query_link += "&COMMAND='" + query_df["COMMAND"]+"'"
  query_link += "&COMMAND='" + query_df["COMMAND"]+"'"
  query_link += "&COMMAND='" + query_df["COMMAND"]+"'"
 
  response = requests.get(query_link)
  text = response.text

  elements = re.search(pattern, text)
  elements = str(elements.group()).removeprefix("$$SOE\n").removesuffix("\n$$EOE")
print(elements)