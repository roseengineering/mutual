
import os, subprocess 

def run(command):
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

Install 
-------------

Use 'pip install .' to install.

Command Line
-------------

The program takes the following command line options:

```
-freq      : simulation frequency (or frequencies) in megahertz 
-loss      : vertical antenna resistive loss
-load      : vertical antenna loading impedance
-diam      : vertical antenna diameter
-height    : vertical antenna height
-segs      : number of segments to divide the simulated vertical into
-autoload  : automatically tune the self impedance of the vertical antennas
-debug     : show the current error norm when simulating the array
-el        : x,y location of a vertical antenna element
-currents  : list of antenna elements currents j or / complex notation
-tlines    : list of transmission lines in j or / complex notation (used with currents)
```

Note the -diam, -height, and -el options can take the following suffix modifiers:
cm, mm, ft, and in.  Otherwise distance is provided in meters.

Examples
--------

2-element, quarter-wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0") }

3-element in-line, quarter wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0") }

2-element, half-wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 130ft,0") }

Triangular array, 0.289 wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,-11.41 -el 0,11.41 -el 19.74,0") }

4-square array, quarter-wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 0,65ft -el 65ft,65ft") }

4-square array, 1/8-wave spacing

{ run("mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 32ft,0 -el 0,32ft -el 32ft,32ft") }

Two element base-fed array from Orr and Cowan, Vertical Antenna Handbook p148-150 based on
W7EL's design in August 1979 QST.  A ground loss of 9 ohms was assumed.

{ run("mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0") }

The Orr design above but for multiple frequencies.

{ run("mutual -loss 9 -diam .7in -height 33.4ft -freq 7.0,7.1,7.2,7.3 -el 0,0 -el 35.14ft,0") }

The Orr design above but solving with element currents using / notation.  (Use / between the magnitude and the angle in degrees).

{ run("mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,1/90") }

... or using j notation for the complex currents.

{ run("mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,j") }

The Orr design above with the Christman matching transmission lines.

{ run("mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,1/-90 -tlines 75/90,75/180") }

The Orr design above but 20 feet high and "autoloaded".

{ run("mutual -loss 9 -diam .7in -height 20ft -freq 7.1 -el 0,0 -el 35.14ft,0 -autoload") }

""")







