import numpy as np

def bbox(obj):
	xmin, ymin, xmax, ymax, zmax, zmin = 0, 0, 0, 0, 0, 0
	with open(obj) as o:
		for i, line in enumerate(o.readlines()):
			if line.startswith('v'):
				v = np.asarray(line.split()[1:], dtype=float)
				if v[0] < xmin: xmin = v[0]
				if v[0] > xmax: xmax = v[0]
				if v[1] < ymin: ymin = v[1]
				if v[1] > ymax: ymax = v[1]
				if v[2] < zmin: zmin = v[2]
				if v[2] > zmax: zmax = v[2]

	return xmin, xmax, ymin, ymax, zmin, zmax
