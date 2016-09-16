#!/usr/bin/env python

import argparse
import numpy as np
import os, sys, stat, errno, datetime
from matplotlib.pyplot import *
import matplotlib.pyplot as plt


def main():
	
	op = 'locations.all.dat'
	theta = [10., 360., 10.]
	r = 20000.0
	z = 1500.0
	
	if options.r: r = options.r
	if options.z: z = options.z
	if options.op: op = options.op
	if options.theta: theta = options.theta
	
	# just want a few of these to add in to the mix over and above the azimuth variations
	phi = [-90, -45, 45, 90]
	

	x = np.cos(np.arange(theta[0], theta[1], theta[2])*np.pi/180.)*r
	y = np.sin(np.arange(theta[0], theta[1], theta[2])*np.pi/180.)*r
	h = np.ones(np.size(x))*z
	
	data = np.transpose([x,y,h])
	
	x = np.cos(np.array(phi)*np.pi/180.)*r
	y = np.zeros(np.size(phi))
	h = np.sin(np.array(phi)*np.pi/180.)*r + z
	
	dd = np.transpose([x,y,h])
	
	np.savetxt(op,np.concatenate((data,dd)),fmt='%.1f')
	
	
	if options.sort:
		# do subsets for sorting
		#angs = np.arange(-len(data)/4, len(data)/4+1, 1)
		mid = len(data)/4
		angs = np.arange(mid, -1, -1)
		subset = [[]]
		for i in np.arange(1,mid+1):
			opsub = 'sort.subset.' + np.str(i-1) + '.' + op
			subset = [data[mid], data[mid-i], data[mid+i]]
			np.savetxt(opsub, subset, fmt='%.1f')
	
	
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--op",dest="op", help="op file", metavar="FILE")
	parser.add_argument("-r", dest="r", help="distance from origin")
	parser.add_argument("-z", dest="z", help="distance above 0, 0 plane")
	parser.add_argument("-sort", action="store_true", help="do subsets for sorting")
	parser.add_argument("-theta",dest="theta", nargs=3, help="th_start th_stop th_step")
	options = parser.parse_args()
	main()
