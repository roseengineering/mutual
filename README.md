

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
-freq      : simulation frequency in megahertz 
-loss      : vertical antenna resistive loss
-load      : vertical antenna loading impedance
-diam      : vertical antenna diameter
-height    : vertical antenna height
-seg       : number of segments to divide the simulated vertical into
-autoload  : automatically tune the self impedance of the vertical antennas
-el        : x,y location of a vertical antenna element
```

Note the -diam, -height, and -el options can take the following suffix modifiers:
cm, mm, ft, and in.  Otherwise distance is provided in meters.

Examples
--------

2-element, quarter-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0
! element self impedance : 36.3204+1.8171j
! current error norm     : 5.06585e-05
# MHZ Z RI
3.8       35.7663   1.6553  19.1265 -15.6098  19.1265 -15.6098  35.7663   1.6553
```


3-element in-line, quarter wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 130ft,0
! element self impedance : 36.3204+1.8171j
! current error norm     : 7.2784e-05
# MHZ Z RI
3.8       35.9915   1.7995  18.9637 -15.2582  -7.9517 -14.3998
          18.9637 -15.2582  35.2301   1.4898  18.9637 -15.2582
          -7.9517 -14.3998  18.9637 -15.2582  35.9915   1.7995
```


2-element, half-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 130ft,0
! element self impedance : 36.3204+1.8171j
! current error norm     : 3.52974e-06
# MHZ Z RI
3.8       36.5277   1.9638  -7.4151 -14.2346  -7.4151 -14.2346  36.5277   1.9638
```


Triangular array, 0.289 wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,-11.41 -el 0,11.41 -el 19.74,0
! element self impedance : 36.3204+1.8171j
! current error norm     : 5.56771e-05
# MHZ Z RI
3.8       35.3455   1.9616  14.1233 -17.6202  14.1532 -17.6084
          14.1233 -17.6202  35.3455   1.9616  14.1532 -17.6084
          14.1532 -17.6084  14.1532 -17.6084  35.3436   1.9610
```


4-square array, quarter-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 65ft,0 -el 0,65ft -el 65ft,65ft
! element self impedance : 36.3204+1.8171j
! current error norm     : 5.9178e-05
# MHZ Z RI
3.8       35.0071   1.8355  18.2490 -15.2982  18.2490 -15.2982   5.7212 -19.4799
          18.2490 -15.2982  35.0071   1.8355   5.7212 -19.4799  18.2490 -15.2982
          18.2490 -15.2982   5.7212 -19.4799  35.0071   1.8355  18.2490 -15.2982
           5.7212 -19.4799  18.2490 -15.2982  18.2490 -15.2982  35.0071   1.8355
```


4-square array, 1/8-wave spacing


```
$ mutual -diam .7in -height 62.7ft -freq 3.8 -el 0,0 -el 32ft,0 -el 0,32ft -el 32ft,32ft
! element self impedance : 36.3204+1.8171j
! current error norm     : 0.000204788
# MHZ Z RI
3.8       36.0350  -0.8168  31.6442  -4.0790  31.6442  -4.0790  27.5287 -10.7007
          31.6442  -4.0790  36.0350  -0.8168  27.5287 -10.7007  31.6442  -4.0790
          31.6442  -4.0790  27.5287 -10.7007  36.0350  -0.8168  31.6442  -4.0790
          27.5287 -10.7007  31.6442  -4.0790  31.6442  -4.0790  36.0350  -0.8168
```


Two element base-fed array from Orr and Cowan, Vertical Antenna Handbook p148-150 based on
W7EL's design in August 1979 QST.  A ground loss of 9 ohms was assumed.


```
$ mutual -loss 9 -diam .7in -height 33.4ft -freq 7.1 -el 0,0 -el 35.14ft,0
! element self impedance : 45.2009+1.1565j
! current error norm     : 1.5132e-05
# MHZ Z RI
7.1       44.5846   1.0047  18.6465 -15.8822  18.6465 -15.8822  44.5846   1.0047
```



