import datetime
import math
from operator import mod
import pandas as pd
from pathlib import Path
import horizons

class planet:
    def __init__(self, name, planets_filepath):
        planetsdf = pd.read_csv(Path(planets_filepath))
        planetsdf = planetsdf.set_index("name")


        planet = planetsdf.loc[name]
        
        self.a = planet["a"]
        self.e = planet["e"]
        self.i = planet["i"]
        self.w = planet["w"]
        self.Omega = planet["Omega"]
        self.M_0 = planet["M_0"]
        self.dtInit = pd.to_datetime(planet["dtInit"])

        # Intitialise keplarian elements
        # All variables defined in degrees
    
    def meanAnomaly(self, dtLCL, tzdiff):
        n = 0.9856076686/(self.a**(3/2))
        
        dtLCLutc = dtLCL + tzdiff
        diff  = dtLCLutc - self.dtInit
        
        
        # CONVERT DIF TO A DECIMAL POINT
        diff_float = diff.total_seconds()/(60*60*24) # In Days
        M = self.M_0 + n*diff_float
        M = M % 360
        return math.radians(M)

        # Output M in radians for simplicity

    def keplerEq(self, M):
        E_0 = M + self.e  * math.sin(M) * (1 + self.e * math.cos(M))
        E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))

        while (math.fabs(E_0 - E) > 0.0000001):
            E_0 = E
            E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))
        
        return E
        # Note that E is in radians
    
    def trueAnomaly(self, E, M):
        tau_e = math.tan(E/2)
        v = 2*math.atan(math.sqrt((1+self.e) / (1-self.e))* tau_e )
        v = math.degrees(v)
        
        v = v % 360
        if (v < 0):
            v = v+360
        
        return math.radians(v)
        # Note v is returned in radians for future calculations
    
    def distFromSun(self, v):
        r = self.a * (1 - self.e**2)/(1+self.e * math.cos(v))
        return r

    def rectangularHelioCoords(self, v, r, tzdiff):
        Omegatemp = math.radians(self.Omega)
        wtemp = math.radians(self.w)
        itemp = math.radians(self.i)

        xp = r * (math.cos(Omegatemp) * math.cos(wtemp + v) - math.sin(Omegatemp) * math.cos(itemp) * math.sin(wtemp+v))
        yp = r * (math.sin(Omegatemp) * math.cos(wtemp + v) + math.cos(Omegatemp) * math.cos(itemp) * math.sin(wtemp+v))
        zp = r * math.sin(itemp) * math.sin (wtemp + v)
        return xp, yp, zp

    def sidrealTime(self, M, longlitude, dtLCL, tzdiff):
        Pi = math.radians(self.Omega) + math.radians(self.w)
        Pi = math.radians(math.degrees(Pi) % 360) 

        time = dtLCL.time()
        time  = (time.hour*60*60 + time.minute*60 + time.second)/(60*60) # Time in hours 

        tzdiff = tzdiff.total_seconds()/(60*60)

        Theta = math.degrees(M) + math.degrees(Pi) + 15 * (time + tzdiff)
        Theta = math.radians(Theta % 360)

        theta = Theta - math.radians(longlitude) 
        theta = math.radians(math.degrees(theta) % 360)
        return theta

def plantet2Planet(xp, yp, zp, xe, ye, ze):
    x = xp - xe
    y = yp - ye
    z = zp - ze
    return x, y, z

def geoElipLongLat(x, y, z):
    # this function should take the output from the planet2Planet function
    Delta = math.sqrt(x**2 + y**2 + z**2)
    beta = math.asin(z/Delta)
    lambdaVal = math.atan2(y, x)
    while lambdaVal < 0:
        lambdaVal = math.radians(math.degrees(lambdaVal) + 360)
    return lambdaVal, beta
    # Note that the output from the function is in radians
def equatorialCoords(lambdaVal, beta, epsilon):
    # epsilon given in radians
    delta  = math.asin(math.sin(beta) * math.cos(epsilon) + math.cos(beta) * math.sin(epsilon) * math.sin(lambdaVal))
    alpha = math.atan2(math.sin(lambdaVal) * math.cos(epsilon) - math.tan(beta) * math.sin(epsilon), math.cos(lambdaVal))

    while alpha < 0:
        alpha = math.radians(math.degrees(alpha) + 360)
    return alpha, delta
def hourAngle(theta, alpha, delta, latitude):
    H = theta - alpha

    A = math.atan2(math.sin(H), (math.cos(H) * math.sin(math.radians(latitude)) - math.tan(delta) * math.cos(math.radians(latitude)))) 
    A = math.degrees(A) + 180

    h = math.asin(math.sin(math.radians(latitude)) * math.sin(delta) + math.cos(math.radians(latitude)) * math.cos(delta) * math.cos(H))
    h = math.degrees(h)

    while A < 0:
        A = A + 360
    return A, h
    # Output returned in degrees for embedded team
def tzDiff():
    tzdiff = (datetime.datetime.now() - datetime.datetime.utcnow())
    return tzdiff
def findCoords(planet, earth, dtLCL, tzdiff, latitude, longlitude):
    epsilon = math.radians(23.4397)
    Mp = planet.meanAnomaly(dtLCL, tzdiff)

    Ep = planet.keplerEq(Mp)
    vp = planet.trueAnomaly(Ep, Mp)

    rp = planet.distFromSun(vp)
    xp, yp, zp = planet.rectangularHelioCoords(vp, rp, tzdiff)

    Me = earth.meanAnomaly(dtLCL, tzdiff)
    Ee = earth.keplerEq(Me)
    ve = earth.trueAnomaly(Ee, Me)
    re = earth.distFromSun(ve)
    xe, ye, ze = earth.rectangularHelioCoords(ve, re, tzdiff)

    x, y, z = plantet2Planet(xp, yp, zp, xe, ye, ze)

    theta = earth.sidrealTime(Me, longlitude, dtLCL, tzdiff) 
    lambdaVal, beta = geoElipLongLat(x, y, z)
    alpha, delta = equatorialCoords(lambdaVal, beta, epsilon)

    A, h =  hourAngle(theta, alpha, delta, latitude)
    return A, h

def findCoords_short(RA, DEC, obs_time, tzdiff, earth, latitude, longlitude):
    Me = earth.meanAnomaly(obs_time, tzdiff)
    theta = earth.sidrealTime(Me, longlitude, obs_time, tzdiff) 
    alpha = RA
    delta = DEC
    A, h =  hourAngle(theta, alpha, delta, latitude)
    return A, h
    # Finds A and h from Right Ascenion and Declination

# MAIN FUNCTIONS
def main_calc_planet(planet_name, filepath_planets, filepath_results):
    latitude = -34
    longlitude = 151
    dtLCL = datetime.datetime.now()
    tzdiff = tzDiff()

    filepath_planets = Path(filepath_planets)

    planet_selected = planet(planet_name, filepath_planets)
    earth = planet('Earth', filepath_planets)

    df = pd.DataFrame()

    for j in range(288):
        dtLCL = datetime.datetime.now() + j * datetime.timedelta(minutes = 5) # Local time
        A, h = findCoords(planet_selected, earth, dtLCL, tzdiff, latitude, longlitude)
        df2 = pd.DataFrame({
            "A": [A],
            "h": [h],
            "time": [dtLCL]
        },
        index = [j])

        df = pd.concat([df, df2])

    df.to_csv(filepath_results)

def main_calc_RA_DEC(path_RA_DEC, filepath_planets, filepath_results):#
    latitude = -34
    longlitude = 151
    dtLCL = datetime.datetime.now()
    tzdiff = tzDiff()

    path_RA_DEC = Path(path_RA_DEC)
    filepath_results = Path(filepath_results)

    earth = planet('Earth', filepath_planets)

    df_RA_DEC = pd.read_csv(path_RA_DEC)

    df = pd.DataFrame()

    for i in range(len(df)):
        df2_RA_DEC = df_RA_DEC.iloc[i]
        
        obs_time = pd.to_datetime(df2_RA_DEC.loc["obs_time"]) # Local time
        RA = df2_RA_DEC.loc["RA"]
        DEC = df2_RA_DEC.loc["DEC"]

        A, h = findCoords_short(RA, DEC, obs_time, tzdiff, earth, latitude, longlitude)
        df2 = pd.DataFrame({
            "A": [A],
            "h": [h],
            "time": [obs_time]
        },
        index = [i])
    
        df = pd.concat([df, df2])

    df.to_csv(filepath_results, mode="w", index=False, header=True)

def main_calc_stars(RA, DEC, filepath_planets, filepath_results):
    latitude = -34
    longlitude = 151
    dtLCL = datetime.datetime.now()
    tzdiff = tzDiff()

    earth = planet('Earth', filepath_planets)

    df = pd.DataFrame()
    
    for i in range(288):
        dtLCL = datetime.datetime.now() + i * datetime.timedelta(minutes = 5) # Local time # Local time

        A, h = findCoords_short(RA, DEC, dtLCL, tzdiff, earth, latitude, longlitude)
        df2 = pd.DataFrame({
            "A": [A],
            "h": [h],
            "time": [dtLCL]
        },
        index = [i])

        df = pd.concat([df, df2])

    df.to_csv(filepath_results, mode="w", index=False, header=True)

    


path_RA_DEC = 'RA_DEC.csv'

#filepath_init = Path(r'C:\Users\chess\OneDrive\Documents\GK_Clone_Place\SpaceLaser\Horizons\planets.csv')  
#filepath_results = Path(r'C:\Users\chess\OneDrive\Documents\GK_Clone_Place\SpaceLaser\Horizons\temp.csv')
filepath_planets = 'planets.csv'
filepath_results = 'temp.csv'

#main_calc_RA_DEC(path_RA_DEC, filepath_results)
#earth = planet('Earth', filepath_planets)

#main_calc_planet("Mars", filepath_planets, filepath_results)

#main_calc_stars(6.75, -16.75, filepath_planets, filepath_results)


selection = input("1. planet \n2. star \n3. jpl query\n")
if (selection ==  "1"):
    planet_selected = input("name of planet: ")
    main_calc_planet(planet_selected, filepath_planets, filepath_results)
elif (selection == "2"):
    RA = input("RA: ")
    RA = math.radians(float(RA)*15)
    DEC = input("DEC: ")
    DEC = math.radians(float(DEC))
    main_calc_stars(RA, DEC, filepath_planets, filepath_results)
elif (selection == "3"):
    jpl_id = input("jpl id: ")
    horizons.jpl_request("Name", jpl_id, path_RA_DEC)
    main_calc_RA_DEC(path_RA_DEC, filepath_planets, filepath_results)
else:
    print("None")
