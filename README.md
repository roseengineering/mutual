

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
-load      : vertical antenna base loading impedance
-diam      : vertical antenna diameter
-height    : vertical antenna height
-segs      : number of segments to divide the simulated vertical into
-autoload  : automatically base load the element vertical antenna
-debug     : show the current error norm when simulating the array
-el        : x,y location of a vertical antenna element
-currents  : list of antenna elements currents j or / complex notation
-tlines    : list of transmission lines in j or / complex notation (used with currents)
-vf        : velocity factor of the transmission line if angle given in feet or meters
```

Note the -diam, -height, and -el options can take the following suffix modifiers:
cm, mm, ft, and in.  Otherwise distance is provided in meters.

Examples
--------

2-element, quarter-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0
! MHZ Z RI R 1
3.8       35.7663  +1.6553j  19.1265 -15.6098j
          19.1265 -15.6098j  35.7663  +1.6553j
```


3-element in-line, quarter wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0
! MHZ Z RI R 1
3.8       35.9915  +1.7995j  18.9637 -15.2582j  -7.9517 -14.3998j
          18.9637 -15.2582j  35.2301  +1.4898j  18.9637 -15.2582j
          -7.9517 -14.3998j  18.9637 -15.2582j  35.9915  +1.7995j
```


2-element, half-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 130ft,0
! MHZ Z RI R 1
3.8       36.5277  +1.9638j  -7.4151 -14.2346j
          -7.4151 -14.2346j  36.5277  +1.9638j
```


Triangular array, 0.289 wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,-11.41 -el 0,11.41 -el 19.74,0
! MHZ Z RI R 1
3.8       35.3455  +1.9616j  14.1233 -17.6202j  14.1532 -17.6084j
          14.1233 -17.6202j  35.3455  +1.9616j  14.1532 -17.6084j
          14.1532 -17.6084j  14.1532 -17.6084j  35.3436  +1.9610j
```


4-square array, quarter-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 0,65ft -el 65ft,65ft
! MHZ Z RI R 1
3.8       35.0071  +1.8355j  18.2490 -15.2982j  18.2490 -15.2982j   5.7212 -19.4799j
          18.2490 -15.2982j  35.0071  +1.8355j   5.7212 -19.4799j  18.2490 -15.2982j
          18.2490 -15.2982j   5.7212 -19.4799j  35.0071  +1.8355j  18.2490 -15.2982j
           5.7212 -19.4799j  18.2490 -15.2982j  18.2490 -15.2982j  35.0071  +1.8355j
```


4-square array, 1/8-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 32ft,0 -el 0,32ft -el 32ft,32ft
! MHZ Z RI R 1
3.8       36.0350  -0.8168j  31.6442  -4.0790j  31.6442  -4.0790j  27.5287 -10.7007j
          31.6442  -4.0790j  36.0350  -0.8168j  27.5287 -10.7007j  31.6442  -4.0790j
          31.6442  -4.0790j  27.5287 -10.7007j  36.0350  -0.8168j  31.6442  -4.0790j
          27.5287 -10.7007j  31.6442  -4.0790j  31.6442  -4.0790j  36.0350  -0.8168j
```


Two element base-fed array from Orr and Cowan, Vertical Antenna Handbook p148-150 based on
W7EL's design in August 1979 QST.  A ground loss of 9 ohms was assumed.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0
! MHZ Z RI R 1
7.1       44.5846  +1.0047j  18.6465 -15.8822j
          18.6465 -15.8822j  44.5846  +1.0047j
```


The Orr design above but for multiple frequencies.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.0,7.1,7.2,7.3 -el 0,0 -el 35.14ft,0
! MHZ Z RI R 1
7         43.1299  -7.4624j  18.3324 -15.0070j
          18.3324 -15.0070j  43.1299  -7.4624j
7.1       44.5846  +1.0047j  18.6465 -15.8822j
          18.6465 -15.8822j  44.5846  +1.0047j
7.2       46.0983  +9.4591j  18.9448 -16.8045j
          18.9448 -16.8045j  46.0983  +9.4591j
7.3       47.6771 +17.9112j  19.2272 -17.7738j
          19.2272 -17.7738j  47.6771 +17.9112j
```


The Orr design above but solving with element currents using / complex notation.  (Use a / between the magnitude and the angle in degrees).


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,1/-90
! MHZ Z RI R 1
7.1       28.7024 -17.6418j  60.4668 +19.6511j
! E in MA notation =  33.6906 -31.5768   63.5799 -71.9963 
! I in MA notation =   1.0000   0.0000    1.0000 -90.0000 
! Z in parallel    =  23.2125  -6.1608j
```


... or using j notation for the complex currents.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,-j
! MHZ Z RI R 1
7.1       28.7024 -17.6418j  60.4668 +19.6511j
! E in MA notation =  33.6906 -31.5768   63.5799 -71.9963 
! I in MA notation =   1.0000   0.0000    1.0000 -90.0000 
! Z in parallel    =  23.2125  -6.1608j
```


The Orr design above with the Christman matching transmission lines.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,-j -tlines 75/90.64,75/176.205
! MHZ Z RI R 1
7.1      145.9689 +86.2965j  58.5139 +17.5013j
! E in MA notation =  75.1931  90.2443   62.0860 103.6427 
! I in MA notation =   0.4434  59.6528    1.0166  86.9910 
! Z in parallel    =  42.3487 +15.6908j
```


... or using feet instead of degrees.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,-j -tlines 75/23.19ft,75/45.10ft
! MHZ Z RI R 1
7.1      149.5365 +85.0475j  59.1250 +18.2238j
! E in MA notation =  75.3683  90.4743   62.5679 105.1016 
! I in MA notation =   0.4381  60.8456    1.0113  87.9709 
! Z in parallel    =  42.8408 +15.9557j
```


The Orr desgin above but with 90 degree transmission lines to the elements for current forcing.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,-j -tlines 75/90,75/90
! MHZ Z RI R 1
7.1      142.2399 +87.4274j  84.1395 -27.3445j
! E in MA notation =  75.0000  90.0000   75.0000  -0.0000 
! I in MA notation =   0.4492  58.4232    0.8477  18.0037 
! Z in parallel    =  63.0503  -1.4208j
```


The Orr design above but 20 feet high and "autoloaded".


```
$ mutual -loss 9 -diam .7in -height 20ft -freq 7.1 -el 0,0 -el 35.14ft,0 -autoload
! MHZ Z RI R 1
! autoload vertical base = 256.2944j at 7.1 MHz
7.1       18.6136  -0.0069j   5.2691  -4.7229j
           5.2691  -4.7229j  18.6136  -0.0069j
```


All designs from Orr on page 149.


```
$ mutual -loss 9 -diam .7in -freq 3.6  -height 66.8ft -el 0,0 -el 70.28ft,0 -currents 1,-j -tlines 75/46.39ft,75/92.77ft
! MHZ Z RI R 1
3.6      179.3650 +51.4636j  66.4021 +29.2599j
! E in MA notation =  75.4356  90.9908   70.2040 118.1315 
! I in MA notation =   0.4043  74.9815    0.9675  94.3509 
! Z in parallel    =  48.6652 +19.2746j
```


```
$ mutual -loss 9 -diam .7in -freq 7.1  -height 33.4ft -el 0,0 -el 35.14ft,0 -currents 1,-j -tlines 75/23.19ft,75/45.10ft
! MHZ Z RI R 1
7.1      149.5365 +85.0475j  59.1250 +18.2238j
! E in MA notation =  75.3683  90.4743   62.5679 105.1016 
! I in MA notation =   0.4381  60.8456    1.0113  87.9709 
! Z in parallel    =  42.8408 +15.9557j
```


```
$ mutual -loss 9 -diam .7in -freq 10.1 -height 23.2ft -el 0,0 -el 24.36ft,0 -currents 1,-j -tlines 75/16.07ft,75/32.15ft
! MHZ Z RI R 1
10.1     120.4103 +97.3445j  58.8678 +14.1678j
! E in MA notation =  74.9791  89.9803   60.5585 103.4938 
! I in MA notation =   0.4842  51.0268    1.0002  89.9617 
! Z in parallel    =  41.5647 +15.6262j
```


```
$ mutual -loss 9 -diam .7in -freq 14.1 -height 16.7ft -el 0,0 -el 17.57ft,0 -currents 1,-j -tlines 75/11.60ft,75/22.55ft
! MHZ Z RI R 1
14.1     142.6727 +89.7992j  58.3616 +16.4840j
! E in MA notation =  75.2037  90.2424   61.5930 102.7736 
! I in MA notation =   0.4461  58.0558    1.0156  87.0015 
! Z in parallel    =  42.2217 +15.4461j
```



