import numpy as np
import sys


def bbox(obj):
    xmin, ymin, xmax, ymax, zmax, zmin = 0, 0, 0, 0, 0, 0
    with open(obj) as o:
        for i, line in enumerate(o.readlines()):
            if line.startswith('v') or 'clone' in line:
                v = np.asarray(line.split()[1:4], dtype=float)
                if v[0] < xmin: xmin = v[0]
                if v[0] > xmax: xmax = v[0]
                if v[1] < ymin: ymin = v[1]
                if v[1] > ymax: ymax = v[1]
                if v[2] < zmin: zmin = v[2]
                if v[2] > zmax: zmax = v[2]

    return xmin, xmax, ymin, ymax, zmin, zmax


if __name__ == '__main__':

    obj = sys.argv[1]
    print "processing object:", obj
    for D, V in zip(['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'],
                    bbox(obj)):
        print '{}:{:.2f}'.format(D, V)
