
import sys
import skrf as rf

def main(filename):
    net = rf.Network(filename)
    n = net.z[0][0].size
    print("# MHZ Z RI")
    if n == 2: print("!             Z11               Z12               Z21               Z22")
    for f, zij in zip(net.f, net.z):
        print('{:<8g}'.format(f / 1e6), end="")
        for i, x in enumerate(zij.flatten()):
            if i > 0 and n > 2 and i % n == 0: print("\n        ", end="")
            print(' {:8.4f} {:8.4f}'.format(x.real, x.imag), end="")
        print()


main(*sys.argv[1:])

