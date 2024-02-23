# Itsy Bitsy M0 Express IO demo
# Welcome to CircuitPython 2.2 :)xz

import board
import gc
import time
import neopixel
from digitalio import DigitalInOut, Direction, Pull

gc.collect()   # make some rooooom

#debug
debug=True

# led
pixels = neopixel.NeoPixel(board.D3,1)

#switches
reset_switch = DigitalInOut(board.D2)
reset_switch.direction = Direction.INPUT
reset_switch.pull = Pull.UP
#
switch1 = DigitalInOut(board.D4)
switch1.direction = Direction.INPUT
switch1.pull = Pull.UP
#
switch2 = DigitalInOut(board.D7)
switch2.direction = Direction.INPUT
switch2.pull = Pull.UP
#
switch3 = DigitalInOut(board.D10)
switch3.direction = Direction.INPUT
switch3.pull = Pull.UP
#
switch4 = DigitalInOut(board.D11)
switch4.direction = Direction.INPUT
switch4.pull = Pull.UP
#
switch5 = DigitalInOut(board.D12)
switch5.direction = Direction.INPUT
switch5.pull = Pull.UP
#
switch6 = DigitalInOut(board.D13)
switch6.direction = Direction.INPUT
switch6.pull = Pull.UP

cols = [
 (255,0,0),  #R
 (230,80,0), #O
 (255,150,0), #Y
 (0,255,0),  #G
 (0,0,255),  #B
 (128,0,128), #V
 (255,255,255) #White
]

def linspace(n):
    out=[i/(n-1) for i in list(range(0,n-1))]
    out.append(1)
    return(out)
    

# take a color and ramp it over n brightness values
def ramp(col, n):
    col=tuple([float(i) for i in col])
    if sum(col)==0:
        return(col)
    else:
        out=list()
        for ramp in list(linspace(n)):
            out.append(tuple([round(i*ramp) for i in col]))
        out.pop(0) # remove "off" state
        rev=out.copy()
        rev.reverse()
        return out + rev

def switch_status():
    R=reset_switch.value
    status=(
    (switch1.value!=R) + 
    (switch2.value!=R) + 
    (switch3.value!=R) + 
    (switch4.value!=R) + 
    (switch5.value!=R) + 
    (switch6.value!=R)
    )
    return status

victory=False
while True:
    status=switch_status()
    # if complete
    while switch_status()==6:
        if debug:
            print("All complete")
        entry=switch_status()
        #if completed since reset, do a little dance
        if victory!=reset_switch.value:
            new_cols=cols.copy()
            new_cols.reverse()
            new_cols=cols + new_cols
            for col in new_cols:
                for br in ramp(col, 30):
                    if entry==switch_status():
                        pixels[0] = br
                        time.sleep(0.005)
                    else:
                        break
            victory=not victory
        else:
            for br in ramp(cols[6],35):
                if entry==switch_status():
                    pixels[0]=br
                    time.sleep(0.125)
                else:
                    break
    # if none
    while switch_status()==0:
        if debug:
            print("%s complete" % switch_status())
        entry=switch_status()
        for br in ramp(cols[0],50):
            if entry==switch_status():
                pixels[0]=br
                time.sleep(0.125)
            else:
                break
    # if some but not all
    while 0<switch_status()<6:
        if debug:
            print("%s complete" % switch_status())
        entry=switch_status()
        new_cols=cols[0:switch_status()+1]
        new_cols.reverse()
        for col in new_cols:
            for br in ramp(col, 50):
                if entry==switch_status():
                    pixels[0] = br
                    time.sleep(0.075)
                else:
                    break



