#!/usr/bin/env python

import platform
import argparse
import numpy as np
import os, sys, stat, errno, datetime


def checkFile(fname):
	try:
		open(fname)
	except IOError, e:
	# for 3.2 print("({})".format(e))
		print("%s: ({0})".format(e)%(sys.argv[0]))
		sys.exit(1)
	

def sortFileName(f,ll,ntheta,nphi,ext):
	if np.size(ll) != 3:
		print("%s: error in sortFileName() - not enough fields in ll\n"%(sys.argv[0]))
		sys.exit(1)
	return f + '_' + str(ll[0]) + '_' + str(ll[1]) + '_' + str(ll[2]) + '.' + 'theta.' + str(ntheta) + '.phi.' + str(nphi) + '.' + ext




def main():
	# some stuff
	
	obj = 'SE30.singleTree.needleFib.obj'
	opdir = 'opdir'
	locfile = 'locations.dat'
	rpp = 3
	
	
	
	# angles: start, stop, step
	theta = [-4.2, 40, 0.01]
	phi = [-11.5, 11.5, 0.01]
	
	# how many chunks do want to break these into?
	n_theta = 10 
	n_phi = 10
	
	
	# default locations: note these are assuning mm
	locations = [[14100.0, 14100.0, 1500.0], [20000.0, 0.0, 1500.0], [-14100.0, 14100.0, 1500.0]]
	
	if options.locfile:
		locfile = options.locfile
		checkFile(locfile)
		locations = np.genfromtxt(locfile,unpack=True).transpose()
		
	if options.opdir:
		opdir = options.opdir
	
	# check opdir exists and if not create it
	try:
		os.makedirs(opdir)
	except OSError, e:
		if e.errno != errno.EEXIST:
			raise
	
	
	if options.n_theta: n_theta = options.n_theta
	if options.n_phi: n_phi = options.n_phi
	if options.rpp: rpp = options.rpp
	if options.obj: obj = options.obj
	if options.theta: theta = [np.float(i) for i in options.theta]
	if options.phi: phi = [np.float(i) for i in options.phi]


	# calculate number of grabmes i.e. n_locations * n_theta * n_phi
	tot = np.shape(np.array(locations))[0] * n_theta * n_phi

	# loop over locations and then loop over angle segments
	count = 0
	for l in locations:
		x, y, z = l
		
		# loop over theta chunks
		for th in np.arange(0,n_theta):
			thetaStart = theta[0] + th * (theta[1]-theta[0])/n_theta
			thetaEnd = thetaStart + (theta[1]-theta[0])/n_theta
			thetaStep = theta[2]
			
			# loop over phi chunks
			for ph in np.arange(0,n_phi):
				phiStart = phi[0] + ph * (phi[1]-phi[0])/n_phi
				phiEnd = phiStart + (phi[1]-phi[0])/n_phi
				phiStep = phi[2]
									
		
				# sort out grabme
				grabme = opdir + '/' + sortFileName(obj,l,th,ph,'grabme')
		
				# check if grabme exists
		
				if not os.path.exists(grabme):
					count += 1
					grabmefp = open(grabme, 'w')
					logfile = opdir + '/' + sortFileName(obj,l,th,ph,'log')
					opfile = opdir + '/' + sortFileName(obj,l,th,ph,'dat')
					imfile = opdir + '/' + sortFileName(obj,l,th,ph,'hips')
			
					# cmd = "#(tls -RATv -origin %f %f %f -theta %f %f %f "%(l[0], l[1], l[2], thetaStart, thetaEnd, thetaStep)
					cmd = "(nice +19 tls -origin %f %f %f -theta %f %f %f "%(l[0], l[1], l[2], thetaStart, thetaEnd, thetaStep)
					#cmd += "-phi %f %f %f -image %s "%(phiStart, phiEnd, phiStep, imfile)
					cmd += "-phi %f %f %f "%(phiStart, phiEnd, phiStep)
					if options.rpp: cmd += "-rpp %i "%(rpp)
					#cmd += "%s > %s)>& %s\n"%(obj, opfile, logfile)
					cmd += "%s > %s)\n"%(obj, opfile)
					grabmefp.write("#!/bin/csh -f\n")
					#grabmefp.write("#host: %s\n"%os.environ['HOST'])
					grabmefp.write("#host: %s\n"%platform.uname()[1])
					grabmefp.write("# %s\n"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
					# grabmefp.write('echo \"grabme no. %i\"\n'%(count))
					grabmefp.write(cmd)
					grabmefp.flush()
					os.chmod(grabme,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
					grabmefp.close()
					#os.execl(grabme)
					os.system(grabme)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--location",dest="locfile", help="location file", metavar="FILE")
	parser.add_argument("-o", "--opdir",dest="opdir", help="location file", metavar="FILE")
	parser.add_argument("--obj",dest="obj", help="object file", metavar="FILE")
	parser.add_argument("-t", "--ntheta",dest="n_theta", help="n theta chunks")
	parser.add_argument("--theta",dest="theta", nargs=3, help="th_start th_stop th_step")
	parser.add_argument("-p", "--nphi",dest="n_phi", help="n phi chunks")
	parser.add_argument("--phi",dest="phi", nargs=3, help="ph_start ph_stop ph_step")
	parser.add_argument("-r", "--rpp",dest="rpp", help="rpp value")
	options = parser.parse_args()
	main()
