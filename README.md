

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


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0
! MHZ Z RI R 1
3.8       35.7663   1.6553  19.1265 -15.6098
          19.1265 -15.6098  35.7663   1.6553
```


3-element in-line, quarter wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0
! MHZ Z RI R 1
3.8       35.9915   1.7995  18.9637 -15.2582  -7.9517 -14.3998
          18.9637 -15.2582  35.2301   1.4898  18.9637 -15.2582
          -7.9517 -14.3998  18.9637 -15.2582  35.9915   1.7995
```


2-element, half-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 130ft,0
! MHZ Z RI R 1
3.8       36.5277   1.9638  -7.4151 -14.2346
          -7.4151 -14.2346  36.5277   1.9638
```


Triangular array, 0.289 wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,-11.41 -el 0,11.41 -el 19.74,0
! MHZ Z RI R 1
3.8       35.3455   1.9616  14.1233 -17.6202  14.1532 -17.6084
          14.1233 -17.6202  35.3455   1.9616  14.1532 -17.6084
          14.1532 -17.6084  14.1532 -17.6084  35.3436   1.9610
```


4-square array, quarter-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 0,65ft -el 65ft,65ft
! MHZ Z RI R 1
3.8       35.0071   1.8355  18.2490 -15.2982  18.2490 -15.2982   5.7212 -19.4799
          18.2490 -15.2982  35.0071   1.8355   5.7212 -19.4799  18.2490 -15.2982
          18.2490 -15.2982   5.7212 -19.4799  35.0071   1.8355  18.2490 -15.2982
           5.7212 -19.4799  18.2490 -15.2982  18.2490 -15.2982  35.0071   1.8355
```


4-square array, 1/8-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 32ft,0 -el 0,32ft -el 32ft,32ft
! MHZ Z RI R 1
3.8       36.0350  -0.8168  31.6442  -4.0790  31.6442  -4.0790  27.5287 -10.7007
          31.6442  -4.0790  36.0350  -0.8168  27.5287 -10.7007  31.6442  -4.0790
          31.6442  -4.0790  27.5287 -10.7007  36.0350  -0.8168  31.6442  -4.0790
          27.5287 -10.7007  31.6442  -4.0790  31.6442  -4.0790  36.0350  -0.8168
```


Two element base-fed array from Orr and Cowan, Vertical Antenna Handbook p148-150 based on
W7EL's design in August 1979 QST.  A ground loss of 9 ohms was assumed.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0
! MHZ Z RI R 1
7.1       44.5846   1.0047  18.6465 -15.8822
          18.6465 -15.8822  44.5846   1.0047
```


The Orr design above but for multiple frequencies.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.0,7.1,7.2,7.3 -el 0,0 -el 35.14ft,0
! MHZ Z RI R 1
7         43.1299  -7.4624  18.3324 -15.0070
          18.3324 -15.0070  43.1299  -7.4624
7.1       44.5846   1.0047  18.6465 -15.8822
          18.6465 -15.8822  44.5846   1.0047
7.2       46.0983   9.4591  18.9448 -16.8045
          18.9448 -16.8045  46.0983   9.4591
7.3       47.6771  17.9112  19.2272 -17.7738
          19.2272 -17.7738  47.6771  17.9112
```


The Orr design above but solving with element currents using / notation.  (Use / between the magnitude and the angle in degrees).


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,1/90
! MHZ Z RI R 1
7.1       60.4668  19.6511  28.7024 -17.6418
! E in RA notation =  63.5799  18.0037  33.6906  58.4232
! Z in parallel    =  23.2125  -6.1608j
```


... or using j notation for the complex currents.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,j
! MHZ Z RI R 1
7.1       60.4668  19.6511  28.7024 -17.6418
! E in RA notation =  63.5799  18.0037  33.6906  58.4232
! Z in parallel    =  23.2125  -6.1608j
```


The Orr design above with the Christman matching transmission lines.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0 -currents 1,1/-90 -tlines 75/90,75/180
! MHZ Z RI R 1
7.1      142.2399  87.4274  60.4668  19.6511
! E in RA notation =  75.0000  90.0000  63.5799 108.0037
! Z in parallel    =  43.0123  17.1476j
```


The Orr design above but 20 feet high and "autoloaded".


```
$ mutual -loss 9 -diam .7in -height 20ft -freq 7.1 -el 0,0 -el 35.14ft,0 -autoload
! MHZ Z RI R 1
! auto loading vertical  = 256.2944j at 7.1 MHz
7.1       18.6136  -0.0069   5.2691  -4.7229
           5.2691  -4.7229  18.6136  -0.0069
```



