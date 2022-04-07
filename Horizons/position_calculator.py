import datetime
import math

# Intialise location
latitude = 0
longlitude = 0

# Intitialise keplarian elements
class planet:
    def __init__(self, a, e, i, w, Omega, M_0, datetimeInitial):
        self.a = a
        self.e = e
        self.i = i       
        self.w = w
        self.Omega = Omega
        self.M_0 = Omega
        self.datetimeInitial = datetimeInitial
    
    def meanAnomaly(datetimeObservation):
        n = 0.9856076686/(a**(3/2))
        diff  = self.datetimeObservation - self.datetimeInitial
        M = self.M_0 + n*diff
        M = M % 360
        return math.radian(M)
        # Output M in radians for simplicity

    def keplerEq(M):
        E_0 = M + self.e  * math.sin(M) * (1 + self.e * math.cos(M))
        E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))

        while (math.fabs(E_0 - E) > 0.00001):
            E_0 = E
            E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))
        return E
        # Note that E is in radians
    
    def trueAnomaly(E, M):
        v = math.atan2(self.a * math.sqrt(1 - self.e**2) * math.sin(E), self.a * math.cos(E) - self.e)
        
        v = math.degrees(v)
        
        v = v % 360
        if (v < 0):
            v = v+360
        v = math.radians(v)
        return v
        # Note v is returned in radians for future calculations
    
    def distFromSun(v):
        r = self.a * (1 - self.e**2)/(1+self.e * math.cos(v))
        return r

    def rectangularHelioCoords(v, r):
        Omega = math.radians(self.Omega)
        w = math.radians(self.w)
        i = math.radians(self.i)
        x = r * (math.cos(Omega) * math.cos(w + v) - math.sin(Omega) * math.cos(i) * math.sin(w+v))
        y = r * (math.sin(Omega) * math.cos(w + v) + math.cos(Omega) * math.cos(i) * math.sin(w+v))
        z = r * math.sin(i) * math.sin (w + v)
        return x, y, z

    def sidrealTime(M, longlitude, datetimeObservation):
        Pi = math.radians(self.Omega) + math.radians(self.w)
        Pi = math.radians(math.degrees(Pi) % 360) 

        time = time(datetimeObservation)
        # MAGIC BOX FIX LATER

        Theta = M + Pi + 15 * time
        Theta = math.radians(math.degrees(Theta) % 360)

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
    return lambdaVal, beta
    # Note that the output from the function is in radians

def equatorialCoords(lambdaVal, beta, epsilon):
    delta  = math.asin(math.sin(beta) * math.cos(epsilon) + math.cos(beta) * math.sin(epsilon) * math.sin(lambdaVal))
    alpha = math.atan2(math.sin(lambdaVal) * math.cos(epsilon) + math.tan(beta) * math.sin(epsilon), math.cos(lambdaVal))
    return alpha, delta

def hourAngle(theta, alpha, delta, latitude):
    H = theta - alpha

    A = math.atan2(math.sin(H), math.cos(H) * math.sin(latitude) - math.tan(delta) * math.cos(latitude)) 
    A = math.degrees(A)

    h = math.asin(math.sin(latitude) * math.sin(delta) + math.cos(lat) * math.cos(delta) * math.cos(H))
    h = math.degrees(h)

    return A, h


### MAIN SCRIPT
a = 5.20260
e = 0.04849
i = 1.303
w = 273.867
Omega = 100.464
M_0 = 20.020

jupiter = planet(a, e, i, w, Omega, M_0, )
