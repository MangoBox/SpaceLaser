import datetime
import math
import pytz

# Intitialise keplarian elements
class planet:
    def __init__(self, a, e, i, w, Omega, M_0, dtInit):
        self.a = a
        self.e = e
        self.i = i       
        self.w = w
        self.Omega = Omega
        self.M_0 = M_0
        self.dtInit = dtInit
    
    def meanAnomaly(self, dtLCL):
        n = 0.9856076686/(self.a**(3/2))
        #tzdiff = tzDiff()
        # FIX
        
        datetime.timedelta(hours = -69891)
        dtLCLutc = dtLCL + tzdiff
        diff  = dtLCLutc - self.dtInit
        diff  = dtLCLutc - self.dtInit
        # CONVERT DIF TO A DECIMAL POINT
        diff_float = diff.total_seconds()/(60*60*24) # In Days
        M = self.M_0 + n*diff_float# CHECK THIS
        M = M % 360
        print("M: " + str(math.degrees(M) % 360))
        print("M_0: " + str(math.degrees(M_0) % 360))
        return math.radians(M)

        # Output M in radians for simplicity

    def keplerEq(self, M):
        E_0 = M + self.e  * math.sin(M) * (1 + self.e * math.cos(M))
        E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))

        while (math.fabs(E_0 - E) > 0.000001):
            E_0 = E
            E = E_0 - (E_0 - self.e * math.sin(E_0) - M)/(1 - self.e * math.cos(E_0))
        return E
        # Note that E is in radians
    
    def trueAnomaly(self, E, M):
        v = math.atan2(self.a * math.sqrt(1 - self.e**2) * math.sin(E), self.a * math.cos(E) - self.e)
        
        v = math.degrees(v)
        
        v = v % 360
        if (v < 0):
            v = v+360
        v = math.radians(v)
        return v
        # Note v is returned in radians for future calculations
    
    def distFromSun(self, v):
        r = self.a * (1 - self.e**2)/(1+self.e * math.cos(v))
        return r

    def rectangularHelioCoords(self, v, r):
        Omega = math.radians(self.Omega)
        w = math.radians(self.w)
        i = math.radians(self.i)
        x = r * (math.cos(Omega) * math.cos(w + v) - math.sin(Omega) * math.cos(i) * math.sin(w+v))
        y = r * (math.sin(Omega) * math.cos(w + v) + math.cos(Omega) * math.cos(i) * math.sin(w+v))
        z = r * math.sin(i) * math.sin (w + v)
        return x, y, z

    def sidrealTime(self, M, longlitude, dtLCL):
        Pi = math.radians(self.Omega) + math.radians(self.w)
        Pi = math.radians(math.degrees(Pi) % 360) 

        time = dtLCL.time()
        time  = (time.hour*60*60 + time.minute*60 + time.second)/(60*60) # Time in hours 

        #tzdiff = tzDiff()
        tzdiff = - 1

        Theta = math.degrees(M) + math.degrees(Pi) + 15 * (time + tzdiff)
        print("Theta: " + str(Theta % 360))
        print("M: " + str(math.degrees(M) % 360))
        print("Theta: " + str(Theta % 360))
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

    h = math.asin(math.sin(latitude) * math.sin(delta) + math.cos(latitude) * math.cos(delta) * math.cos(H))
    h = math.degrees(h)

    return A, h
    # Output returned in degrees for embedded team

def tzDiff():
    tzdiff = (datetime.datetime.now() - datetime.datetime.utcnow())
    return tzdiff

### MAIN SCRIPT
a = 5.20260
e = 0.04849
i = 1.303
w = 273.867
Omega = 100.464
M_0 = 20.020


#datetimeInitial = datetime.datetime(2000, 1, 1, 0, 0, 0)
#datetimeObervation = datetime.datetime(2004, 1, 1, 0, 0, 0)
tzdiff = tzDiff() # Time zone difference between LCL and UTC

dtInit = datetime.datetime(2000, 1, 1, 0, 0, 0) # Initial time (UTC)
#dtLCL = datetime.datetime.now() # Local time
dtLCL = datetime.datetime(2004, 1, 1, 1, 0, 0)

# Intialise location
latitude = 52
longlitude = -5

jupiter = planet(a, e, i, w, Omega, M_0, dtInit)
earth  =  planet(1.00000, 0.01671, 0.000, 288.064, 174.873, 357.529, dtInit)
epsilon = 23.4397

Mj = jupiter.meanAnomaly(dtLCL)
print(math.degrees(Mj))

Ej = jupiter.keplerEq(Mj)
vj = jupiter.trueAnomaly(Ej, Mj)
print(math.degrees(vj))

rj = jupiter.distFromSun(vj)
print((rj))

xj, yj, zj = jupiter.rectangularHelioCoords(vj, rj)
print(str(xj) +","+ str(yj) +","+ str(zj))


print("SIDREAL")
Me = earth.meanAnomaly(dtLCL)
Ee = earth.keplerEq(Me)
ve = earth.trueAnomaly(Ee, Me)
re = earth.distFromSun(ve)
xe, ye, ze = earth.rectangularHelioCoords(ve, re)


theta = earth.sidrealTime(Me, longlitude, dtLCL) # FIX
print(math.degrees(theta))

x, y, z = plantet2Planet(xj, yj, zj, xe, ye, ze)
lambdaVal, beta = geoElipLongLat(x, y, z)
alpha, delta = equatorialCoords(lambdaVal, beta, epsilon)
A, h =  hourAngle(theta, alpha, delta, latitude)

print(str(A) + ',' + str(h))
