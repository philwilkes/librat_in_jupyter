#!/usr/bin/env python

import argparse
import numpy as np
import os, sys, stat, errno, datetime
from collections import deque
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# script to get cylinders from obj file in order to calculate total cyl area
# and location/size of branches

#Author Ernesto P. Adorio, Ph.D.
 
def gramm(X,inplace = False):
	# Returns the Gramm-Schmidt orthogonalization of matrix X
	if not inplace:
		V = [row[:] for row in X]  # make a copy.
	else:
		V = X
	k = len(X[0])
	n = len(X)
 
	for j in range(k):
		for i in range(j):
			# D = < Vi, Vj>
			D = sum([V[p][i]*V[p][j] for p in range(n)])
 
			for p in range(n):
				# Note that the Vi's already have length one!
				# Vj = Vj - <Vi,Vj> Vi/< Vi,Vi >
				V[p][j] -= (D * V[p][i])
 
		# Normalize column V[j]
		invnorm = 1.0 / np.sqrt(sum([(V[p][j])**2 for p in range(n)]))
		for p in range(n):
			V[p][j] *= invnorm
	return V


def getCyls(strdata,start):
	ncyl = 0
	for l in strdata[start:len(strdata)]:
		if l.split()[0] == 'cyl':
			ncyl += 1
	return ncyl


def vect_dot(v1, v2):
	return v1 * v2

def vect_norm(v):
	return v/np.sqrt((v**2).sum())

def vect_norm2(r):
	ret = np.zeros(r.shape)
	mag = vect_mag2(r)
	ret[:,0] = r[:,0]/mag
	ret[:,1] = r[:,1]/mag
	ret[:,2] = r[:,2]/mag
	return ret

def vect_mag(v):
	return np.sqrt((v**2).sum())
	
def vect_mag2(r):
	return np.sqrt(r[:,0]**2 + r[:,1]**2 + r[:,2]**2)
	
def rotVect(v,theta,axis):
	# http://en.wikipedia.org/wiki/Rotation_matrix
	ct = np.cos(theta)
	st = np.sin(theta)
	if axis == 'X': return np.dot(v, np.array([[1., 0., 0.], [0., ct, -st ], [0., st, ct]]))
	if axis == 'Y': return np.dot(v, np.array([[ct, 0., st], [0., 1., 0.], [-st, 0, ct]]))
	if axis == 'Z': return np.dot(v, np.array([[ct, -st, 0.], [st, ct, 0.], [0., 0., 1.]]))


def rotVect4(v,theta,axis):
	# http://en.wikipedia.org/wiki/Rotation_matrix
	ct = np.cos(theta)
	st = np.sin(theta)
	if axis == 'X': return np.dot(v, np.array([[1., 0., 0., 0,], [0., ct, -st, 0.], [0., st, ct, 0.], [0., 0., 0., 1.]]))
	if axis == 'Y': return np.dot(v, np.array([[ct, 0., st, 0,], [0., 1., 0., 0.], [-st, 0., ct, 0.], [0., 0., 0., 1.]]))
	if axis == 'Z': return np.dot(v, np.array([[ct, -st, 0., 0,], [st, ct, 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]]))


def rotVect2(v,angles,axis):
	# http://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Rotation_matrix_.E2.86.94_Euler_angles
	cp = np.cos(angles[0])
	sp = np.sin(angles[0])
	ct = np.cos(angles[1])
	st = np.sin(angles[1])
	ch = np.cos(angles[2])
	sh = np.sin(angles[2])
	if axis == 'X': return np.dot(v, np.array([[1., 0., 0.], [0., cp, sp], [0., -sp, cp]]))
	if axis == 'Y': return np.dot(v, np.array([[ct, 0., -st], [0., 1., 0.], [st, 0., ct]]))
	if axis == 'Z': return np.dot(v, np.array([[ch, sh, 0.], [-sh, ch, 0.], [0., 0., 1.]]))
	
def rotate_vector(v,angles):
	# /Users/mdisney/bpms/src/lib/vect/vectors2.c
	out = np.copy(v)
	cp = np.cos(angles[0])
	sp = np.sin(angles[0])
	ct = np.cos(angles[1])
	st = np.sin(angles[1])
	cps = np.cos(angles[2])
	sps = np.sin(angles[2])
	out[1] = v[1]*cp + v[2]*sp
	out[2] = v[2]*cp - v[1]*sp
	hold = np.copy(out)
	out[2] = hold[2]*ct + hold[0]*st
	out[0] = hold[0]*ct - hold[2]*st
	hold = np.copy(out)
	out[0] = hold[0]*cps + hold[1]*sps
	out[1] = hold[1]*cps - hold[0]*sps
	return out
	
	

		
	


def pointsOnCyl(cyls,pd,op,v):
	''' 
	function to generate pd points per unit area on cylinder
	'''

	opf = open(op,'w')
	
	T1 = np.eye(3)

	if v:
		# area * point_den
		tot = np.int(cyls[:,7].sum() * pd + .5)		
		sys.stderr.write("total points on cyls: %i\n"%(tot))

	for c in cyls:
		# area * point_den
		n = np.int(c[7].sum() * pd + .5)
		
		# do all this in xy plane ie. with vector centre line of cyl aligned with z, then rotate the points
		# around the actual centre line vector
		
		
		# get orig cyl vector line, and angles
		r = (c[3:6] - c[0:3])
		l = vect_mag(r)
		r = vect_norm(r)
		angles = np.arccos(np.dot(r,T1))
		
		# test rotations
		rr = ([0., 0., l])
		
		rrot = rotVect(rr,-angles[2],'Y')
		rrot = rotVect(rrot,angles[0],'Z')
	
	
		
		np.savetxt('x',c[0:6].reshape(2,3),fmt='%.2f')
		

		##############
		v0 = np.array([1., 1., 1.])
		v1 = np.array([2., 2., 2.])
		r = v1 - v0
		r = vect_norm(r)
		angles = np.arccos(np.dot(r,T1))
		
		
		# single line
		pp = np.array([0., 0., 1.])
		ppr = [rotVect(pp, -angles[0], 'Y')]
		ppr = [rotVect(ppr, -angles[1], 'Z')]
		ppr = [rotVect(ppr, -angles[2], 'X')]
		ppr = ppr + v0
		

		# rectangle
		v0 = np.array([1., 0., 1.])
		v1 = np.array([2., 0., 2.])
		r = v1 - v0
		r = vect_norm(r)
		angles = np.arccos(np.dot(r,T1))
		pp = np.array(([-0.5, 0., 0.],[-0.5, 0., 1.],[.5, 0., 1.],[.5, 0., 0.])).reshape(4,3)
		pp = np.array(([-0.5, 0., 0.],[-0.5, 0., 1.],[.5, 0., 1.],[.5, 0., 0.])).reshape(4,3)
		ppr = ([rotVect(pp[0], -angles[0], 'Y')], [rotVect(pp[1], -angles[0], 'Y')], \
		[rotVect(pp[2], -angles[0], 'Y')], [rotVect(pp[3], -angles[0], 'Y')])
		
		ppr = ([rotVect(ppr[0], -angles[1], 'Z')], [rotVect(ppr[1], -angles[1], 'Z')], \
		[rotVect(ppr[2], -angles[1], 'Z')], [rotVect(ppr[3], -angles[1], 'Z')])
		
		ppr = ([rotVect(ppr[0], -angles[2], 'X')], [rotVect(ppr[1], -angles[2], 'X')], \
		[rotVect(ppr[2], -angles[2], 'X')], [rotVect(ppr[3], -angles[2], 'X')])
		ppr = ppr + v0
		ppr = np.array(ppr).reshape(4,3)
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',ppr,fmt='%.2f')
		#############
		
		
		#############
		# only in xz plane
		v0 = np.array([1., 0., 1.])
		v1 = np.array([2., 0., 2.])
		r = v1 - v0
		r = vect_norm(r)
		angles = np.arccos(np.dot(r,T1))
		nn = 1000
		pp = np.zeros((nn,3))
		pp[:,0] = -0.5 + np.random.rand(nn)
		pp[:,2] = np.random.rand(nn)
		ppr = ([rotVect(pp, -angles[0], 'Y')])
		ppr = ppr + v0
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',np.array(ppr).reshape(nn,3),fmt='%.2f')
		
		
		# xyz plane
		v0 = np.array([1., 1., 1.])
		v1 = np.array([2., 2., 2.])
		r = v1 - v0
		r = vect_norm(r)
		angles = np.arccos(np.dot(r,T1))
		angles = np.array([np.arctan2(r[1],r[0]), np.arctan2(r[2],r[0]), np.arctan2(r[2],r[1])])
		ppr = ([rotVect(pp, -angles[0], 'Z')])
		ppr = ([rotVect(ppr, -angles[2], 'X')])
		ppr = ([rotVect(ppr, -angles[1], 'Y')])
		ppr = ppr + v0
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',np.array(ppr).reshape(nn,3),fmt='%.2f')
		
		#############
		
		
		#############
		r = ([1., 1., 1.])
		r = ([1., 1., 1., 1.])
		pp = np.zeros((nn,4))
		nn = 1000
		pp[:,0] = -0.5 + np.random.rand(nn)
		pp[:,2] = np.random.rand(nn)
		v0 = np.array([1., 1., 1.])
		d = np.sqrt(r[1]**2 + r[2]**2)
		vv = v0 * -1.0
		Tm = np.eye(4)
		Tm[0,3] = vv[0]
		Tm[1,3] = vv[1]
		Tm[2,3] = vv[2]
		
		ppr = np.dot(Tm,pp.transpose())
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',ppr.reshape(nn,4),fmt='%.2f')
		
	
		# rotate about x to lie in xz plane
		m = np.eye(4)
		m[1][1] = r[2]/d
		m[1][2] = r[1]/d
		m[2][1] = -r[1]/d
		m[2][2] = r[2]/d
		Tm = np.dot(Tm,m)
		
		ppr = np.dot(Tm,ppr).transpose()
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',ppr,fmt='%.2f')
		
		# rotate about y to line up with z-axis
		m = np.eye(4)
		m[0][0] = d
		m[0][2] = r[0]
		m[2][0] = -r[0]
		m[2][2] = d
		Tm = np.dot(Tm,m)
		
		# rotate about z using i/p angle
		theta = np.pi/4.
		Tm = rotVect4(Tm, theta, 'Z')


		ppr = np.dot(Tm,ppr.transpose()).transpose()
		np.savetxt('x',np.array([v0,v1]),fmt='%.2f')
		np.savetxt('x1',pp,fmt='%.2f')
		np.savetxt('x1sr',ppr,fmt='%.2f')
		
		
		m = np.eye(4)
		m[0,3] = v0[0]
		m[1,3] = v0[1]
		m[2,3] = v0[2]
		Tm = np.dot(Tm,m)
		
		
		
		#############
		
		#############
		# gram-schmidt
		v0 = np.array([1., 1., 1.])
		v1 = np.array([2., 2., 2.])
		v = v1 - v0
		l = vect_mag(v)
		r = vect_norm(v)
		ll = l * np.random.random_sample(n).reshape(n,1)
		phi = 2.* np.pi * np.random.random_sample(n).reshape(n,1)
		ll = l * np.random.random_sample(n).reshape(n,1)
		rad =  c[6]
		n = 10
		xx = v0 + (np.random.random_sample(n).reshape(n,1)) * v
		np.savetxt('zz',xx,fmt='%.2f')
		xxg = gramm(xx,inplace='False')
		
		
		
		#############
		
		

		# then from there random angles
		phi = 2.* np.pi * np.random.random_sample(n).reshape(n,1)
		ll = l * np.random.random_sample(n).reshape(n,1)

		points[:,0] = (c[6] * np.cos(phi)).transpose()
		points[:,1] = (c[6] * np.sin(phi)).transpose()
 		points[:,2] = ll.transpose()
		
	
		#r = np.array([1., 1., 1.])
		#r = np.array([ 100.,   100., 0.])
		
		# new array for o/p points
		r = np.zeros(points.shape)
		for i, p in enumerate(points):
			# reverse transform to original cyl direction
			rrot = rotVect(p,angles[2],'Y')
			r[i] = rotVect(rrot,angles[0],'Z')
	

		# translate all points to origin of cyl & then scale by l
		r += c[3:6]
		
		np.savetxt('points2.dat',r,fmt='%.2f')


	return npoints




def main():
	
	obj = 'SE30.singleTree.needleFib.obj.needle_off'
	op = obj + '.filt'
	op2 = obj + '.pts'
	
	# point density - equates to 1 point per cm^2 *IF* object units are mm
	pd = 0.01

	if options.obj: obj = options.obj
	if options.op: op = options.op
	if options.op2: op2 = options.op2
	if options.pd: pd = options.pd
	
	ipf = open(obj,'r')

	# read whole file in in one go as list
	strdata = ipf.readlines()
	
	# find location of where we want to start
	start = strdata.index('g plant 0\n')
	
	# get number of cyls to make cylinder array
	ncyl = getCyls(strdata,start)
	
	# so need an array to store each i.e.
	# xs ys zs xe ye ze r area vol
	cyls = np.zeros((ncyl,9))
	
	sys.stderr.write("ncyls: %i\n"%(ncyl))
	
	#import pdb; pdb.set_trace()

	cylCount = 0
	for l in strdata[start:len(strdata)]: 
		if l.split()[0] == 'cyl':
			line = strdata.index(l)
			
			# radius
			cyls[cylCount][6] = float(strdata[line].split()[3])
			
			# nice: start
			s = strdata[line + np.int(strdata[line].split()[1])].split()
			cyls[cylCount][0:3] = [float(i) for i in s[1:4]]
			
			# end
			s = strdata[line + np.int(strdata[line].split()[2])].split()
			cyls[cylCount][3:6] = [float(i) for i in s[1:4]]
			
			cylCount += 1
			
			#if options.v:
			#	sys.stderr.write("\b\b\b\b\b\b\b\b\b(%i)"%(cylCount))
						
			cylCount += 1
				
	# do all in one go at the end
	# area
	cyls[:,7] = 2. * np.pi * cyls[:,6] * np.sqrt(((cyls[:,3:6] - cyls[:,0:3])**2).sum(axis=1))
	# vol
	cyls[:,8] = np.pi * cyls[:,6]**2 * np.sqrt(((cyls[:,3:6] - cyls[:,0:3])**2).sum(axis=1))



	if options.stats:
		# collect stats regarding cylinders
		# histo of cylinder sizes
		
		




	if options.t:
		# do some points on the cyla - fuck all that shit right now though
		p = pointsOnCyl(cyls,pd,op2,options.v)
			

	# cyls = np.genfromtxt(op,unpack=True).transpose()
	
	# for plotting
	if options.p:
		base = cyls[:,0:3]
		tip = cyls[:,3:6]
		fig = plt.figure()
		#ax = fig.add_subplot(111)
		ax = Axes3D(fig)
		ax.set_xlabel('X axis')
		ax.set_ylabel('Y axis')
		ax.set_zlabel('Z axis')
		#ax.legend()
		#ax.plot(base[::100,0],base[::100,1],base[::100,2],label='base',linestyle='none',marker='.')
		#ax.plot(base[:,0],base[:,1],base[:,2],label='base',linestyle='none',marker='.')
		#ax.plot(points[:,0], points[:,1], points[:,2], label='stuff',linestyle='none',marker='o', ms=1, mfc='black')
		ax.plot(r[:,0], r[:,1], r[:,2], label='stuff',linestyle='none',marker='o', ms=1, mfc='black')
		#ax.pbaspect = [0.1, 0.1, 1.]
		#ax.autoscale_view(scalez=True)
		# plt.show()
			
		#np.savetxt('base.dat',base,fmt='%.1f')
		#np.savetxt('tip.dat',tip,fmt='%.1f')
	
		if options.plotfile:
			plt.savefig(options.plotfile)
		else:
			plt.show()
	
	#np.savetxt(op,cyls,fmt='%.2f')
	
	
	if options.v:
		sys.stderr.write('ncyls in %s: %i\n'%(obj,cylCount))
		sys.stderr.write('cyl area in %s: %.2f\n'%(obj,cyls[:,7].sum()))
		sys.stderr.write('cyl volume in %s: %.2f\n'%(obj,cyls[:,8].sum()))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--obj",dest="obj", help="object file", metavar="FILE")
	parser.add_argument("-f", "--op",dest="op", help="output file", metavar="FILE")
	parser.add_argument("-p", action="store_true", help="switch plotting on")
	parser.add_argument("-v", action="store_true", help="switch verbose on")
	parser.add_argument("-stats", action="store_true", help="switch stats on")
	parser.add_argument("-s", "--saveplot",dest="plotfile", help="switch plotting on", metavar="FILE")
	parser.add_argument("-t", dest="op2", help="op file for points on cyls", metavar="FILE")
	options = parser.parse_args()
	main()
