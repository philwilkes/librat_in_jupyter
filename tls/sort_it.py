#!/usr/bin/env python

import argparse
import numpy as np
import os, sys, stat, errno, glob, tempfile

def checkFile(fname):
        try:
                open(fname)
        except IOError, e:
        # for 3.2 print("({})".format(e))
                print("%s: ({0})".format(e)%(sys.argv[0]))
                sys.exit(1)


def main():

	ipdir = 'opdir'
	obj = 'SE30.singleTree.needleFib.obj'
	locfile = 'locations.dat'
	

	locations = [[14100.0, 14100.0, 1500.0]]
	
	if options.locfile:
		locfile = options.locfile
		checkFile(locfile)
		locations = np.genfromtxt(locfile,unpack=True).transpose()
	else:
		locations = np.array(locations)

	if options.obj: obj = options.obj
	if options.ipdir: ipdir = options.ipdir

	for l in locations:
		base = ipdir + '/' + obj + '_' + str(l[0]) + '_' + str(l[1]) + '_' + str(l[2])
		opfile = base + '.all'

		files = glob.glob(base + '.*.dat')
		#cmd = "cat %s.*.dat > %s\n"%(base,opfile)
		#os.system(cmd)
		
		sys.stderr.write('%s: %s\n'%(sys.argv[0],opfile))
	
		if np.size(files):
			f = ' '.join(files)
			tmpfd, tmp = tempfile.mkstemp(dir='/tmp')
			cmd = "cat %s > %s\n"%(f,tmp)
			os.system(cmd)
			os.close(tmpfd)
			data = np.genfromtxt(tmp,unpack=True,invalid_raise=False).transpose()
			data = l - data
			np.savetxt(opfile,data,fmt='%.2f')
		else:
			sys.stderr.write('%s: couldn\'t find files with locations: %f %f %f\n'%(sys.argv[0], l[0], l[1], l[2]))

			
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--location",dest="locfile", help="location file", metavar="FILE")
	parser.add_argument("--obj",dest="obj", help="obj file", metavar="FILE")
	parser.add_argument("-d", "--dir",dest="ipdir", help="ip dir", metavar="FILE")
	options = parser.parse_args()
	main()
