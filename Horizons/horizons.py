import datetime
import julian
import requests
import pandas as pd
import re
import math
from pathlib import Path

#sb_filepath_input = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/smallbodies.csv')
#sb_filepath_output = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/smallbodies_transformed.csv')

url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
file = 'documents/GitHib/SpaceLaser/input.txt'

sb_filepath_input = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/smallbodies.csv')
sb_filepath_output = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/smallbodies_transformed.csv')

url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
file = 'documents/GitHib/SpaceLaser/input.txt'

request_base = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text"

pattern_marker = "\$\$SOE([\s\S]+)\$\$EOE"

request_base = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text"

pattern_marker = "\$\$SOE([\s\S]+)\$\$EOE"


def sb_query():
    sb_df = pd.DataFrame(columns=["name", "centre_body", "a", "e", "i", "w", "Omega", "M_0", "dtInit"])

    df = pd.read_csv(sb_filepath_input)

    for i in range(20):
        elements_ephem_df = df.iloc[i]

        sb_df.loc[i] = [elements_ephem_df.iloc[0], \
            "Sun", \
            elements_ephem_df.iloc[1], \
            elements_ephem_df.iloc[2], \
            elements_ephem_df.iloc[3], \
            elements_ephem_df.iloc[4], \
            elements_ephem_df.iloc[5], \
            elements_ephem_df.iloc[6], \
            pd.to_datetime(julian.from_jd(elements_ephem_df.iloc[7], fmt='mjd'))]

    sb_df.to_csv(sb_filepath_output, mode='a', index=False, header=False)

path_output = 'planets.csv'
path_queries = 'Horizons_queries.csv'
# Pulling latest planet data 

def planet_query(path_queries, path_output):
    queries_filepath = Path(path_queries) 
    planets_filepath = Path(path_output)
    queries = pd.read_csv(queries_filepath)

    planet_df = pd.DataFrame(columns=["name", "centre_body", "a", "e", "i", "w", "Omega", "M_0", "dtInit"])

    for i in range(len(queries.index)):
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

        elements = re.search(pattern_marker, text)
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

    planet_df.to_csv(planets_filepath, mode='a', index=False, header=False)

path_RA_DEC = 'RA_DEC.csv'

# For other bodies (to be called for live script)
def jpl_request(name, jpl_id, path_RA_DEC):

    path_RA_DEC = Path(path_RA_DEC)
    
    name = name #INSERT NAME OF OBJECT HERE
    query_link = request_base
    query_link += "&MAKE_EPHEM=YES"
    query_link += "&COMMAND='" + jpl_id + "'" #INSERT JPL ID HERE as a STRING
    query_link += "&EPHEM_TYPE=OBSERVER"
    query_link += "&CENTER='coord@399'"
    query_link += "&COORD_TYPE=GEODETIC"
    query_link += "&SITE_COORD='+151.28330,-33.91660,0'"
    query_link += "&STEP_SIZE='5 MINUTES'"
    query_link += "&START_TIME='" + str(datetime.datetime.utcnow()) + "'"
    query_link += "&STOP_TIME='" + str(datetime.datetime.utcnow() +  datetime.timedelta(hours=24)) + "'"
    query_link += "&QUANTITIES='1,9,20,23,24,47,48'"
    query_link += "&REF_SYSTEM='ICRF'"
    query_link += "&ANG_FORMAT='HMS'"
    query_link += "&CSV_FORMAT='YES'"
    query_link += "&OBJ_DATA='YES'"''

    response = requests.get(query_link)
    text = response.text

    results = re.search(pattern_marker, text)
    results = str(results.group()).removeprefix("$$SOE\n").removesuffix("\n$$EOE")

    pattern_observer = "^\s?([^,]+),[^,]+,[^,]+, (\-*\d+) (\d+) (\d+\.\d+), (\-*\d+) (\d+) (\d+\.\d+)"
    #Finds Datetime, RA (H, m, s), DEC (H, m, s) - will need to be converted to height and azimuth
    results = re.finditer(pattern_observer, results, flags=re.MULTILINE)

    df = pd.DataFrame()
    i = 0

    for match in results:
        #print(match.groups())
        time = pd.to_datetime(match.group(1))
        RA = math.radians(int(match.group(2))*15 + int(match.group(3))*15/(60) + float(match.group(4))*15/(60*60))
        DEC = math.radians(int(match.group(5)) + int(match.group(6))/(60) + float(match.group(7))/(60*60))
        #RA and DEC in radians due to hidden function

        df2 = pd.DataFrame({
                "RA": [RA],
                "DEC": [DEC],
                "obs_time": [time]
            },
            index = [i])
        
        df = pd.concat([df, df2])
        i = i + 1
        
        df.to_csv(path_RA_DEC, mode='w', index=False, header=True)
