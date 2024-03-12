from datetime import time,datetime
from math import sin,cos,tan,acos,asin,atan2,radians,degrees,pi,ceil,floor

#convert UTC Time to Julian Date
def to_julian_date_2000(dt):
    """ Converts to Julian Date - J2000
    """
    tt = (dt - datetime(2000, 1, 1, 12)).total_seconds() / 86400
    return tt

def to_julian_date(dt):
    return to_julian_date_2000(dt) + 2451545.0



#calculate solar Right Ascension/Declination
#uses Zhang et al. 2021 solar azimuth algorithm
def solar_ra_dec(jd):
    n=jd
    L=(280.460 + 0.9856474*n)%360
    g=(375.528 + 0.9856003*n)%360
    La=(L + 1.915*sin(radians(g)) + 0.020*sin(radians(2*g)))%360
    e=23.439 - 0.0000004*n
    #
    dec=degrees(asin(sin(radians(e))*sin(radians(La))))
    ra=degrees(atan2(cos(radians(e))*sin(radians(La)),cos(radians(La))))
    if ra<0:
        ra=ra+360
    return (ra,dec)

def constrain(x):
    if x<0:
        x=float(x)+1.0
    elif x>1:
        x=float(x)-1.0
    return round(x,4)


def dec_to_time(t):
    h=floor(t)
    me=60*(t-h)
    m=floor(me)
    se=60*(me-m)
    s=floor(se)
    out=datetime.strptime("%i:%i:%i"%(h,m,s),"%H:%M:%S").time()
    return out

def degrees_to_time(d):
    h=d/15
    m=(h-floor(h))*60
    s=floor((h-floor(h)-floor(m)/60)*60*60)
    out=datetime.strptime("%i:%i:%i"%(floor(h),floor(m),floor(s)),"%H:%M:%S").time()
    return out


#Caclulate sunset time
def sunset_time(jd0,lat,lon,h=-0.8333):
    """ Return the Rise/Set Time for a given date

    Keyword Arguments:
    jd0 -- Julian Date at 0hUTC on date
    lat -- Latitude
    lon -- Longitude
    h   -- apparent sun set angle using a refraction model
    """
    ra,dec=solar_ra_dec(jd0)
    cosH=(sin(radians(h))-sin(radians(lat))*sin(radians(dec)))/(cos(radians(lat))*cos(radians(dec)))
    if cosH<-1 or cosH>1:
        print("Error: no sunrise/set. Are you in the arctic circle?")
        return (0,0)
    H=acos(cosH)
    # time in Julian Centuries UTC0 Today
    T=jd0/36525.0 
    #Sideral Angle at Greenwich UTC0 Today
    Th=(280.46061837 + 360.98564736629*jd0 + 0.000387933*T**2 - (T**3)/38710000.0)%360

    transit=(dec+(-lon)-Th)/360
    rise=constrain(transit-(degrees(H)/360))*24
    sset=constrain(transit+(degrees(H)/360))*24
    return (rise,sset)

