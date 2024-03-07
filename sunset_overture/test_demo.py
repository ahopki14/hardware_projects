import sunset_time as st
from datetime import time,datetime
#this won't run on a CircuitPython board, but using it to check
from astropy.coordinates import get_sun
from astropy.time import Time

def test_always_passes():
    assert True

def test_sum():
    assert sum([1,2,3]) == 6, "Should be 6"

#the beach of a nearby lake
LAT=42.42
#LON=-83.91
LON=0 # Greenwich

#test_now=datetime.utcnow()
test_now=datetime.strptime("4/10/1987 19:21:0","%m/%d/%Y %H:%M:%S")
test_0h=datetime.combine(test_now.date(), time(0,0))
truth=get_sun(Time(test_now))


def test_truth():
    assert float(truth.ra.to_string(decimal=True))==18.9993,"True RA is incorrect"
    assert float(truth.dec.to_string(decimal=True))==8.03483,"True Dec is incorrect"

def test_jd():
    assert st.to_julian_date(test_now)==2446896.30625,"wrong JD"
    assert st.to_julian_date_2000(test_now)==-4648.69375,"wrong JD2000"

def test_ra_dec_vs_truth():
    ra,dec=st.solar_ra_dec(st.to_julian_date_2000(test_now))
    dec_error=(dec-float(truth.dec.to_string(decimal=True)))/dec
    ra_error=(ra-float(truth.ra.to_string(decimal=True)))/ra
    # the derived RA and Dec should be +/- 2% of the ephemera-based value from astropy
    assert -0.02<ra_error<0.02, "Unacceptable Right Ascenscion error"
    assert -0.02<dec_error<0.02, "Unacceptable Declination error"
