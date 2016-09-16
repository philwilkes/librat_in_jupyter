#!/usr/bin/env python

import argparse
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():

	locations = [[14100.0, 14100.0, 1500.0]]

	f1 = 'opdir/SE30.singleTree.needleFib.obj_-14100.0_14100.0_1500.0.all'
	f2 = 'opdir/SE30.singleTree.needleFib.obj_14100.0_14100.0_1500.0.all'
	f3 = 'opdir/SE30.singleTree.needleFib.obj_20000.0_0.0_1500.0.all'

	d1 = np.genfromtxt(f1,unpack=True).transpose()

	fig = plt.figure()
	ax = Axes3D(fig)
	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')
	ax.plot(d1[0::100], d1[1::100], d1[2::100], ms=0.1, label="BLAH")
	ax.legend()
	if options.f:
		plt.savefig(options.opfile)
	else:
		plt.show()

			
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--location",dest="locfile", help="location file", metavar="FILE")
	parser.add_argument("--obj",dest="obj", help="obj file", metavar="FILE")
	parser.add_argument("-f",dest="opfile", help="op file", metavar="FILE")
	parser.add_argument("-d", "--dir",dest="ipdir", help="ip dir", metavar="FILE")
	options = parser.parse_args()
	main()
