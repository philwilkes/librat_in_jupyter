#include <sys/time.h>
#include <math.h>
#ifndef _STDLIB_H
#include <stdlib.h>
#endif
#include <stdio.h>

#define BITSPERBYTE 8

#define MAXCHAR 4096
#define DOWN 1
#define UP 0

#define MAXSIZE 1e99
#define MINSIZE -1e99

#ifndef MAX
#define MAX(x,y) ((x)>(y)?(x):(y))
#endif
#ifndef MIN
#define MIN(x,y) ((x)<(y)?(x):(y))
#endif

#ifndef TOL
#define TOL 1e-99
#endif

#define R2D (180./3.14159265358979323846)
#define D2R (3.14159265358979323846/180.)

typedef struct {
  char ifile[MAXCHAR];
  char ofile[MAXCHAR];
  char opimage[MAXCHAR];
  FILE *ofp, *opimagefp;
  int verbose, imflag, relative;
  int rpp;
  double fov;
  double theta[3];
  double thetaSteps;
  double phi[3];
  double phiSteps;
  double origin[3];
} tlsStruct;
