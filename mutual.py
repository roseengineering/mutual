#! /usr/bin/env python3

import subprocess, tempfile, os
import numpy as np

defaults = {
    "diameter": .025,
    "losses": 0,
    "loading": 0,
    "segments": 21,
    "vf": 0.66,
    "k": 0.25,
    "l": 25e-6,
    "power": 100,
    "feed": 50,
    "output": 50,
    "frequencies": [ 3.5 ],
    "element": []
}


#################################
# nec2 routines
#################################

def run_process(text):
    name = tempfile.mktemp()
    command = 'nec2c -i %s -o /dev/stdout' % name
    with open(name, "wb") as f:
        f.write(text.encode()) 
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = proc.stdout.read().decode()
    proc.wait()
    os.unlink(name)
    return result


def run_nec(text):
    tag = None
    im = []
    buf = run_process(text)
    f = iter(buf.splitlines())
    for line in f:
        data = line.split()
        if len(data) == 11 and data[0].isdigit() and '.' in line: break
    while True:
        data = line.split() 
        if not len(data): break
        x = np.complex(np.double(data[4]), np.double(data[5]))
        im.append(x)
        line = next(f)
    return im


def generate_input(data, voltages):
    frequency = data["frequency"]
    element = data['element']
    height = data['height']
    diameter = data["diameter"]
    losses = data["losses"]
    loading = data["loading"]
    segments = data["segments"]

    text = ""
    n = len(element)
    for i in range(n):
        tag = i + 1
        fmt = "GW {tag} {segments} {x:g} {y:g} 0 {x:g} {y:g} {height:g} {radius:g}\n"
        text += fmt.format(
                tag=tag, segments=segments, x=element[i][0], y=element[i][1], height=height, radius=diameter / 2)
    text += "GE 1\n"       # ground plane present
    text += "GN 1\n"   # perfect ground
    text += "FR 0 0 0 0 {:f}\n".format(frequency)
    for i in range(n):
        tag = i + 1
        text += "LD 4 {:d} 1 1 {:f} {:f}\n".format(tag, losses, loading)
    for i in range(n):
        tag = i + 1
        text += "EX 0 {:d} 1 0 {:g} {:g}\n".format(tag, voltages[i].real, voltages[i].imag)
    text += "XQ\n"
    text += "EN\n"
    return text


def autoload(data):
    d = { "element": [ (0, 0) ] }
    ei = [ 1 ]
    ii = run_nec(generate_input(dict(data, **d), ei))
    zself = 1 / ii[0]
    print('! autoload vertical base   = {:.4f}j'.format(-zself.imag))
    data["loading"] = -zself.imag


def mutual(data):
    n = len(data["element"])
    zij = np.zeros((n, n), dtype=np.complex)
    for k in range(n):
        ei = np.ones(n) * 1e-20
        ei[k] = 1
        ii = run_nec(generate_input(data, ei))
        zij[:,k] = ii
    zij = np.array(np.linalg.inv(np.matrix(zij)))
    return zij


def error_norm(zij, data):
    n = zij.shape[0]
    ii = np.ones(n)
    ei = multiply(zij, ii)
    err = ii - run_nec(generate_input(data, ei))
    print('! Zij error norm   = {:g}'.format(np.linalg.norm(err)))


def print_mutual(zij, data):
    n = zij.shape[0]
    frequency = data["frequency"]
    print('{:<8g}'.format(frequency), end="")
    for i in range(n):
        if i > 0: print('{:<8s}'.format(''), end="")
        print(' '.join([ ' {:8.4f} {:+8.4f}j'.format(
              zij[i][j].real, zij[i][j].imag) for j in range(n) ]))


#################################
# utilities
#################################

def multiply(zij, ii):
    ei = np.matrix(zij) * np.matrix(ii).T
    return np.array(ei).T[0]


def to_complex(buf, f=None, vf=None):
    buf = buf.strip()
    if '/' in buf:
        r, theta = buf.split('/')
        if theta[-2:] == 'ft':
            theta = np.double(theta[:-2]) * .3048
            theta = 360 * theta / vf / (300 / f)
        elif theta[-1:] == 'm':
            theta = np.double(theta[:-1])
            theta = 360 * theta / vf / (300 / f)
        return np.double(r) * np.exp(1j * np.deg2rad(np.double(theta)))
    else:
        return np.complex(buf)


def to_distance(buf):
    buf = buf.strip()
    if len(buf) > 2:
        suffix = buf[-2:]
        s = buf[:-2]
        if suffix == 'cm':
            return np.double(s) * .01
        if suffix == 'mm':
            return np.double(s) * .001
        if suffix == 'in':
            return np.double(s) * .0254
        if suffix == 'ft':
            return np.double(s) * .3048
    return np.double(buf)
    

def bisect(f, a, b):
    for n in range(100):
        c = (a + b) / 2
        fc = f(c)
        fa = f(a)
        if np.abs(fc - fa) < 1e-5: break
        if np.sign(fc) == np.sign(fa): a = c
        else: b = c
    return c


def component(x, f, precision=5):
    if np.isinf(x) or np.isnan(x) or x == 0: return '-'
    assert(x.imag == 0)
    f = f * 1e6
    w = 2 * np.pi * f
    x = 1 / (w * x) if x < 0 else x / w
    UNITS = 'FH'
    SUFFIX = ["f", "p", "n", "u", "m", "", "k", "M", "G"]
    exp = np.floor(np.log10(np.abs(x)))
    mant = np.round(x / 10**exp, precision-1)
    p = np.int(exp // 3)
    value = (mant * 10**exp) / 10**(3 * p)
    if p - 4 >= 0 or p - 4 < -len(SUFFIX):
        return "%7.2g%s" % (np.abs(x), UNITS[0 if x < 0 else 1])
    else:
        return "%6.4g%s%s" % (np.abs(value), SUFFIX[p-4], UNITS[0 if x < 0 else 1])


def _assert(condition):
    if not condition:
        print("?!", end="")


#################################
# rf routines
#################################

def parallel(zi):
    return 1 / np.sum([ 1 / x for x in zi ])


def tline(deg, zo=50):
    theta = np.deg2rad(deg)
    return np.matrix([
        [ np.cos(theta), 1j * zo * np.sin(theta) ],
        [ 1j * np.sin(theta) / zo, np.cos(theta) ]
    ])


def lmatch(ZS, ZL):
    """
    ZS <---+---X2--< ZL
           X1   
    """
    RS, XS = ZS.real, ZS.imag
    RL, XL = ZL.real, ZL.imag
    QS = RS / RL - 1 + XS**2 / (RS * RL)
    Q = np.sqrt(QS)
    X1 = (XS + np.array([1, -1]) * Q * RS) / (RS / RL - 1)
    X2 = -(XL + np.array([1, -1]) * Q * RL)
    return np.array([X1, X2]).T


def pishift(theta, r1, r2):
    x1, x2, x3 = teeshift(theta, 1/r1, 1/r2)
    return -1/x1, -1/x2, -1/x3


def teeshift(theta, r1, r2):
    theta = np.deg2rad(theta)
    zo = np.sqrt(np.abs(r1 * r2))
    x1 = np.sign(r1) * (zo - np.abs(r1) * np.cos(theta)) / np.sin(theta)
    x2 = np.sign(r1) * -zo / np.sin(theta)
    x3 = np.sign(r1) * (zo - np.abs(r2) * np.cos(theta)) / np.sin(theta)
    return x1, x2, x3


def watts(v):
    return np.abs(v[1])**2 * (v[0]/v[1]).real


def pinet(v, x1, x2, x3):
    v = np.array(v)
    y1 = 1 / x1
    y3 = 1 / x3
    v = multiply([[1, 0], [-1j*y1, 1]], v)  # shunt
    v = multiply([[1, 1j*x2], [0, 1]], v)   # series
    v = multiply([[1, 0], [-1j*y3, 1]], v)  # shunt
    return v


def teenet(v, x1, x2, x3):
    v = np.array(v)
    y2 = 1 / x2
    v = multiply([[1, 1j*x1], [0, 1]], v)   # series
    v = multiply([[1, 0], [-1j*y2, 1]], v)  # shunt
    v = multiply([[1, 1j*x3], [0, 1]], v)   # series
    return v


def lmatchnet(v, x, reverse=False):
    y = 1 / np.array(x)
    if reverse:
        v = multiply([[1, 1j*x[1]], [0, 1]], v)   # series
        v = multiply([[1, 0], [-1j*y[0], 1]], v)  # shunt
    else:
        v = multiply([[1, 0], [-1j*y[0], 1]], v)  # shunt
        v = multiply([[1, 1j*x[1]], [0, 1]], v)   # series
    return v
                    

def shuntdivider(v, L1, L, K, F=0):
    w = 2 * np.pi * F * 1e6 if F else 1
    L2 = L - L1
    x1 = w * L1
    x2 = w * L2
    M = K * np.sqrt(L1 * L2)
    xm = w * M
    return teenet(v, -xm, x1 + xm, x2 + xm)


#################################
# main
#################################

def print_drive(zij, data):
    n = zij.shape[0]
    frequency = data["frequency"]
    ii = np.array(data["current"])
    ei = multiply(zij, ii)

    if data.get("tline1"):
        for i in range(len(data["tline1"])):
            x = to_complex(data["tline1"][i], f=frequency, vf=data["vf"])
            ei[i], ii[i] = multiply(tline(np.rad2deg(np.angle(x)), zo=np.abs(x)), [ei[i], ii[i]])

    if data.get("gehrke") or data.get("tee") is not None or data.get("shunt"):
        solve(ei, ii, data)
    else:
        zi = ei / ii
        ztot = parallel(zi)
        print('{:<8g}'.format(frequency), end="")
        print(' '.join([ ' {:8.4f} {:+8.4f}j'.format(x.real, x.imag) for x in zi ]))
        print('! E in MA notation =', end="")
        print(','.join([ ' {:8.4f} {:8.4f}'.format(np.abs(x), np.rad2deg(np.angle(x))) for x in ei ]))
        print('! I in MA notation =', end="")
        print(','.join([ ' {:8.4f} {:8.4f}'.format(np.abs(x), np.rad2deg(np.angle(x))) for x in ii ]))
        print('! Z in parallel    =', end="")
        print(' {:8.4f} {:+8.4f}j'.format(ztot.real, ztot.imag))

   
def main(*args):
    args = list(args)
    kw = dict(defaults)

    while args:
        opt = args.pop(0)
        if False:
            pass
        elif opt == '-debug':
            kw["debug"] = True
        elif opt == '-autoload':
            kw["autoload"] = True
        elif opt == '-freq':
            kw["frequencies"] = [ np.double(x) for x in args.pop(0).split(',') ]
        elif opt == '-loss':
            kw["losses"] = np.double(args.pop(0))
        elif opt == '-load':
            kw["loading"] = np.double(args.pop(0))
        elif opt == '-segments':
            kw["segments"] = np.int(args.pop(0))
        elif opt == '-height':
            kw["height"] = to_distance(args.pop(0))
        elif opt == '-diam':
            kw["diameter"] = to_distance(args.pop(0))
        elif opt == '-el':
            kw["element"].append([ to_distance(x) for x in args.pop(0).split(',') ])

        elif opt == '-gehrke':
            kw["gehrke"] = True
        elif opt == '-shunt':
            kw["shunt"] = True
        elif opt == '-tee':
            kw["tee"] = np.double(args.pop(0))
        elif opt == '-z':
            kw["z"] = [ np.complex(x) for x in args.pop(0).split(',') ]
        elif opt == '-current':
            kw["current"] = [ to_complex(x) for x in args.pop(0).split(',') ]
        elif opt == '-tie':
            kw["tie"] = [ np.int(x) for x in args.pop(0).split(',') ]
        elif opt == '-tline1':
            kw["tline1"] = args.pop(0).split(',')
        elif opt == '-tline2':
            kw["tline2"] = args.pop(0).split(',')
        elif opt == '-vf':
            kw["vf"] = np.double(args.pop(0))
        elif opt == '-k':
            kw["k"] = np.double(args.pop(0))
        elif opt == '-l':
            kw["l"] = np.double(args.pop(0))
        elif opt == '-power':
            kw["power"] = np.double(args.pop(0))
        elif opt == '-feed':
            kw["feed"] = np.double(args.pop(0))
        elif opt == '-output':
            kw["output"] = np.double(args.pop(0))
        else:
            raise ValueError("unknown option:", opt)

    if not kw.get("gehrke") and not kw.get("shunt") and kw.get("tee") is None:
        print("! MHZ Z RI R 1")

    for frequency in kw["frequencies"]:
        kw["frequency"] = frequency

        if kw.get('z'):
            zij = kw["z"] * np.identity(len(kw["z"]))
        else:
            if kw.get('autoload'):
                autoload(kw)
            zij = mutual(kw)
            if kw.get("debug"): 
                error_norm(zij, kw)

        # display results

        if kw.get("current"):
            print_drive(zij, kw)
        else:
            print_mutual(zij, kw)


#################################
# directional antenna routines
#################################

def solve(ei, ii, data):

    print("! MHZ LINE   POWER               ZA        LMATCH                  ZIN        ELINE                    ", end="")
    print("PI                          TEE              PHASOR            ZOUT         EOUT      ", end="")
    if data.get("shunt"):
        print("  SHUNTPH /       L1          ZFEED         EFEED      ", end="")
    print()

    n = len(ei)
    zi = ei / ii
    power = np.abs(ii**2) * zi.real
    ratio = np.sqrt(data["power"] / np.sum(power))
    ei *= ratio
    ii *= ratio
    power = np.abs(ii**2) * zi.real

    # tie

    if data.get("tie"):
        isum = np.sum([ ii[i-1] for i in data["tie"] ])
        for i in data["tie"]: ii[i-1] = isum
        zi = ei / ii
        power = np.abs(ii**2) * zi.real

    # acu

    feede_common = np.sqrt(data["power"] * data["output"])
    divz = np.array([ feede_common**2 / w for w in power ])
    acuz = [ np.sign(w) * data["feed"] for w in power ]
    if data.get("gehrke"):
        acuz = divz
    if data.get("shunt"):
        divz = acuz

    # l-match

    aculm = [ np.concatenate([ lmatch(zi[i], acuz[i]), lmatch(acuz[i], zi[i]) ]) for i in range(n) ]
    combo = np.array([ [ i // (4 ** (n - k - 1)) % 4 for k in range(n) ] for i in range(4 ** n) ])

    for neti in combo:
        net = np.array([ aculm[i][k] for i, k in enumerate(neti) ])
        if np.any(np.isnan(net.flatten())): continue

        print('!')
        for ref in range(n):
            line = np.array([ ei, ii ]).T
            for i, m, reverse in zip(range(n), net, neti > 1):
                line[i] = lmatchnet(line[i], m, reverse)

            if data.get("tline2"):
                x = to_complex(data["tline2"][i], f=data["frequency"], vf=data["vf"])
                line[i] = multiply(tline(np.rad2deg(np.angle(x)), zo=np.abs(x)), line[i])

            print_solution(line=line, zi=zi, ref=ref, net=net, neti=neti, divz=divz, data=data)


def print_solution(line, zi, ref, net, neti, divz, data):
    n = len(line)
    power = [ watts(v) for v in line ]
    frequency = data["frequency"]
    L = data["l"]
    K = data["k"] 

    adjust = [0] * n
    if data.get("shunt"):
        if np.argmax(power) != ref: return
        V = np.sqrt(power[ref] * divz[ref])
        shunt = [0] * n
        def trans(L1, P, R):
            v1 = [ np.sqrt(R * P), np.sqrt(P / R) ]
            v2 = shuntdivider(v1, L1=L1, L=L, F=frequency, K=K)
            return np.abs(v2[0]), np.angle(v2[0]) - np.angle(v1[0])
        for i in range(n):
            volts = lambda L1: V - trans(L1, P=power[i], R=divz[i])[0]
            shunt[i] = bisect(volts, 1e-10, L)
            res = trans(L1=shunt[i], P=power[i], R=divz[i])
            adjust[i] = res[1]

    for i, m, reverse in zip(range(n), net, neti > 1):

        print('{:<7g} {:2d}'.format(frequency, i + 1), end="")
        print(' {:7.3f}'.format(power[i]), end="")
        print(' {:16.5g}'.format(zi[i]), end="")

        # ACU l-match

        if reverse:
            print(' {:>8s} / {:>8s}'.format(component(m[1], frequency), component(m[0], frequency)), end="")
        else:
            print(' {:>8s} \\ {:>8s}'.format(component(m[0], frequency), component(m[1], frequency)), end="")

        zo = line[i][0] / line[i][1]
        print(' {:14.2f}'.format(zo), end="")
        print(' {:9.4f} {:8.3f}'.format(np.abs(line[i][0]), np.rad2deg(np.angle(line[i][0]))), end="")
        _assert(np.abs(zo.imag) < 1e-3) 

        # calculate phase shifts from end of ACU feed lines

        ref_theta = np.angle(line[ref][0])
        if data.get("tee") is not None:
            ref_theta -= np.deg2rad(data.get("tee"))
        if data.get("shunt"):
            ref_theta -= adjust[i] - adjust[ref]
        theta = np.rad2deg(np.angle(line[i][0]) - ref_theta)
        theta = np.mod(theta + 180, 360) - 180

        # phasor tee and pi match

        v = line[i].copy()
        x1, x2, x3 = pishift(-theta, zo.real, divz[i])
        print(' {:>8s} {:>8s} {:>8s}'.format(component(x1, frequency), component(x2, frequency), component(x3, frequency)), end="")
        if np.abs(theta) > 1e-3: v = pinet(v, x1, x2, x3)
        res = v[0] / v[1]
        _assert(np.abs(res.imag) < 1e-3) 
        _assert(np.abs(res.real - divz[i]) < 1e-3) 
        _assert(np.abs(np.mod(np.rad2deg(np.angle(v[0]) - ref_theta) + 180, 360) - 180) < 1e-3)

        v = line[i].copy()
        x1, x2, x3 = teeshift(-theta, zo.real, divz[i])
        print(' | {:>8s} {:>8s} {:>8s}'.format(component(x1, frequency), component(x2, frequency), component(x3, frequency)), end="")
        if np.abs(theta) > 1e-3: v = teenet(v, x1, x2, x3)
        res = v[0] / v[1]
        _assert(np.abs(res.imag) < 1e-3) 
        _assert(np.abs(res.real - divz[i]) < 1e-3) 
        _assert(np.abs(np.mod(np.rad2deg(np.angle(v[0]) - ref_theta) + 180, 360) - 180) < 1e-3)

        # results

        print(' {:8.3f}{:1s}'.format(theta, '*' if np.abs(theta) > 100 else ''), end="")
        print(' {:14.2f}'.format(v[0] / v[1]), end="")
        print(' {:9.4f} {:8.3f}'.format(np.abs(v[0]), np.rad2deg(np.angle(v[0]))), end="")

        if data.get("shunt"):
            if np.argmax(power) == i:
                print(' {:>8s} / {:>8s}'.format("-", "-"), end="")
            else:
                v = shuntdivider(v, L1=shunt[i], L=L, F=frequency, K=K)
                print(' {:8.3f}'.format(np.rad2deg(-adjust[i])), end="")
                print(' /', end="")
                print(' {:>8s}'.format(component(shunt[i] * 2 * np.pi * frequency * 1e6, frequency)), end="")
            res = v[0] / v[1]
            print(' {:14.2f} '.format(res), end="")
            print(' {:9.4f} {:8.3f}'.format(np.abs(v[0]), np.rad2deg(np.angle(v[0]))), end="")

        print()


if __name__ == "__main__":
    import sys
    np.seterr(divide='ignore', invalid='ignore')
    main(*sys.argv[1:])

