
import os, subprocess 

def run(command, language="python3"):
    if language: command = language + " " + command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    buf = proc.stdout.read().decode()
    proc.wait()
    return f"""
```
$ {command}
{buf}\
```
"""


print(f"""

mutual
----------

Python 3 script for finding the mutual impedance 
matrix for a vertical antenna array.
The script requires the numpy library.  It also
requires the nec2c binary to be installed.

Command Line
-------------

The program takes the following command line options:

```
-freq          : simulation frequency (or frequencies) in megahertz 
-loss          : vertical antenna resistive loss
-load          : vertical antenna base loading impedance
-diam          : vertical antenna diameter
-height        : vertical antenna height
-segments      : number of segments to divide the simulated vertical into
-autoload      : automatically base load the element vertical antenna
-el            : x,y location of a vertical antenna element
-current       : list of antenna elements currents j or "/" complex notation
-debug         : show current error norm of simulated mutual impedance matrix

-z             : set driving impedance of the array instead of simulating
-tline1        : transmision lines from antenna to antenna tuning unit (ATU)
-tline2        : transmision lines from antenna tuning unit (ATU) to phaser
-vf            : velocity factor of the transmission line if angle given in feet or meters
-k             : coefficient of coupling for shunt method, by default .25
-l             : inductance of shunt method power divider inductor, by default 25uH
-tie           : list of lines to tie together
-power         : transmitter power output, by default 100 watts
-output        : transmitter coax feedline impedance, by default 50 ohms
-feed          : ATU to phasor feedline impedance, by default 50 ohms
-gehrke        : solve phase budget using K2BT method
-shunt         : solve phase budget using shunt, or ohms law, method 
-tee           : solve phase budget using tee network method, must pass reference phase shift
```

Note, the -diam, -height, and -el options can take the following suffix modifiers:
cm, mm, ft, and in.  Otherwise distance is provided in meters.
Also options -tline1 and
-tline2 can take m or ft as angle units using "/" notation besides degrees.  The magnitude
is taken as the characteristic impedance of the transmission line.
Z12 and Z21 are not swapped on touchstone output.

stoz.py
--------

The python script stoz.py converts s-parameters of an arbitrary size into z-parameters.
It is intended for use when measuring an antenna array using s-parameters. 
Also, Z12 and Z21 are not swapped on touchstone output.

Examples
--------

A 2-element, quarter-wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0") }

A 3-element in-line, quarter wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0") }

A 2-element, half-wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 130ft,0") }

A triangular array, 0.289 wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,-11.41 -el 0,11.41 -el 19.74,0") }

A 4-square array, quarter-wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 0,65ft -el 65ft,65ft") }

A 4-square array, 1/8-wave spacing array.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 32ft,0 -el 0,32ft -el 32ft,32ft") }

Two element base-fed array from Orr and Cowan, Vertical Antenna Handbook p148-150 based on
W7EL's design in August 1979 QST.  A ground loss of 9 ohms was assumed.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0") }

The Orr design above but for multiple frequencies.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.0,7.1,7.2,7.3 -el 0,0 -el 35.14ft,0") }

The Orr design above but solving with element currents using / complex notation.  (Use a / between the magnitude and the angle in degrees).

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -current 1,1/-90") }

... or using j notation for the complex currents.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -current 1,-j") }

The Orr design above with the Christman matching transmission lines.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -current 1,-j -tline1 75/90.64,75/176.205") }

... or using feet instead of degrees.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -current 1,-j -tline1 75/23.19ft,75/45.10ft") }

The Orr design above but with 90 degree transmission lines to the elements for current forcing.

{ run("mutual.py -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -current 1,-j -tline1 75/90,75/90") }

The Orr design above but 20 feet high and "autoloaded".

{ run("mutual.py -loss 9 -diam .7in -height 20ft -freq 7.1 -el 0,0 -el 35.14ft,0 -autoload") }

The designs from Orr on page 149.  All of which use the Christman matching method.

{ run("mutual.py -loss 9 -diam .7in -freq 3.6  -height 66.8ft -el 0,0 -el 70.28ft,0 -current 1,-j -tline1 75/46.39ft,75/92.77ft") }
{ run("mutual.py -loss 9 -diam .7in -freq 7.1  -height 33.4ft -el 0,0 -el 35.14ft,0 -current 1,-j -tline1 75/23.19ft,75/45.10ft") }
{ run("mutual.py -loss 9 -diam .7in -freq 10.1 -height 23.2ft -el 0,0 -el 24.36ft,0 -current 1,-j -tline1 75/16.07ft,75/32.15ft") }
{ run("mutual.py -loss 9 -diam .7in -freq 14.1 -height 16.7ft -el 0,0 -el 17.57ft,0 -current 1,-j -tline1 75/11.60ft,75/22.55ft") }

Solve the matching network for a 3-element in-line, quarter-wave spacing array using the K2BT method.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0 -current 1,1/-90,-1 -gehrke") }

Solve the matching network for a 4-square, quarter-wave spacing array using the K2BT method.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 0,65ft -el 65ft,0 -el 65ft,65ft -current 1,-j,-j,-1 -gehrke -tline1 50/100,50/100,50/100,50/100 -tie 2,3") }

Solve the matching network for a 2-element, quarter-wave spacing array using the K2BT method.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -current 1,-j -gehrke") }

Solve the matching network for a 2-element, quarter-wave spacing array using the shunt / ohms law power divider method and a 7uH shunt inductor.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -l 7e-6 -current 1,-j -shunt") }

Solve the matching network for a 2-element, quarter-wave spacing array using the tee power divider method.

{ run("mutual.py -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -current 1,-j -tee 90") }

""")



