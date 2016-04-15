import numpy as np

def bbox(obj):
	xmin, ymin, xmax, ymax = 0, 0, 0, 0
	with open(obj) as o:
		for i, line in enumerate(o.readlines()):
			if line.startswith('v'):
				v = np.asarray(line.split()[1:], dtype=float)
				if v[1] < xmin: xmin = v[1]
				if v[1] > xmax: xmax = v[1]
				if v[2] < ymin: ymin = v[2]
				if v[2] > ymax: ymax = v[2]

	print xmin, xmax, ymin, ymax
