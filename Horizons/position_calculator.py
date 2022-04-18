import datetime
import math

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

        # All variables defined in degrees
    
    def meanAnomaly(self, dtLCL, tzdiff):
        n = 0.9856076686/(self.a**(3/2))
        print("timediff = " + str(tzdiff))
        # FIX
        
        dtLCLutc = dtLCL + tzdiff
        diff  = dtLCLutc - self.dtInit
        diff  = dtLCLutc - self.dtInit
        
        # CONVERT DIF TO A DECIMAL POINT
        diff_float = diff.total_seconds()/(60*60*24) # In Days
        print("diff = " +  str(diff_float))
        M = self.M_0 + n*diff_float# CHECK THIS
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
        print("M = " + str(math.degrees(M)))
        time  = (time.hour*60*60 + time.minute*60 + time.second)/(60*60) # Time in hours 
        print("time = " + str((time)))

        tzdiff = tzdiff.total_seconds()/(60*60)
        print("tzdiff = " + str(tzdiff))

        Theta = math.degrees(M) + math.degrees(Pi) + 15 * (time + tzdiff)
        # print("Theta: " + str(Theta % 360))

        Theta = math.radians(Theta % 360)

        print("Theta = " + str(math.degrees(Theta)))

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
    print("H = " + str(math.degrees(H)))

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

### MAIN SCRIPT

#datetimeInitial = datetime.datetime(2000, 1, 1, 0, 0, 0)
#datetimeObervation = datetime.datetime(2004, 1, 1, 0, 0, 0)
tzdiff = tzDiff() # Time zone difference between LCL and UTC

dtLCL = datetime.datetime.now() + datetime.timedelta(hours = 16) # Local time
#dtLCL = datetime.datetime(2004, 1, 1, 1, 0, 0)

# Intialise location
latitude = -34
longlitude = 151

#jupiter = planet(aj, 0.0487, i, w, Omega, M_0, dtInit) #current (2020)
jupiter = planet(5.20260, 0.04849, 1.303, 273.867, 100.464, 20.020, datetime.datetime(2000, 1, 1, 12, 0, 0)) # FROM 2000
earth  =  planet(1.00000, 0.01671, 0.000, 288.064, 174.873, 357.529, datetime.datetime(2000, 1, 1, 12, 0, 0)) # FROM 2000
epsilon = math.radians(23.4397)

Mj = jupiter.meanAnomaly(dtLCL, tzdiff)
print("Mj = " + str(math.degrees(Mj)))

Ej = jupiter.keplerEq(Mj)
print("Ej = " + str(math.degrees(Ej)))
vj = jupiter.trueAnomaly(Ej, Mj)
print("vj = " + str(math.degrees(vj)))
#vj = math.radians(144.637)


rj = jupiter.distFromSun(vj)
print("rj = " + str(rj))

xj, yj, zj = jupiter.rectangularHelioCoords(vj, rj, tzdiff)
print("xj, yj, zj = " + str(xj) +","+ str(yj) +","+ str(zj))

Me = earth.meanAnomaly(dtLCL, tzdiff)
Ee = earth.keplerEq(Me)
ve = earth.trueAnomaly(Ee, Me)
re = earth.distFromSun(ve)
print("re = " + str((re)))
print("ve = " + str(math.degrees(ve)))
xe, ye, ze = earth.rectangularHelioCoords(ve, re, tzdiff)
print("xe, ye, ze = " + str(xe) +","+ str(ye) +","+ str(ze))


theta = earth.sidrealTime(Me, longlitude, dtLCL, tzdiff) 
print("theta = " + str(math.degrees(theta)))

x, y, z = plantet2Planet(xj, yj, zj, xe, ye, ze)
print("x, y, z = " + str(x) +","+ str(y) +","+ str(z))
print("dist = " + str(math.sqrt(x**2 + y**2 + z**2)))
lambdaVal, beta = geoElipLongLat(x, y, z)
print("lambda, beta =" +str(math.degrees(lambdaVal)) + ", " + str(math.degrees(beta)))

alpha, delta = equatorialCoords(lambdaVal, beta, epsilon)
print("alpha, delta =" +str(math.degrees(alpha)) + ", " + str(math.degrees(delta)))

A, h =  hourAngle(theta, alpha, delta, latitude)
print("A, h = " + str(A) + ',' + str(h))
