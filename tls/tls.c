#include <string.h>
#include <stdlib.h>
#include <time.h>

/* this first line is required in the main() file */
#define RAT_MAIN
/* you need to include this file */
#include "rat.h"
#include "tls.h"
#include "image_formats.h"


// tls is usually run in conjunction with Mat D's python script `run_tls.py`

int main(int argc,char **argv)
{
	char ip[MAXCHAR], op[MAXCHAR];
	RATobj *ratObj=NULL;
	tlsStruct *info=NULL;
	float *opBuf=NULL;
	int *matBuf=NULL, RATuserParse();
	struct header *ophd=NULL;
	int i=0, j=0, nargs = -1, thetaSteps=1, phiSteps=1;
	FILE *opfp=NULL;
	double direction[3];
	void doStuff(RATobj *, tlsStruct *, char **), setDefaults(tlsStruct *), jitter(double *, double *, tlsStruct *), RATuserInterrupt();

	if(!(info=(tlsStruct *)calloc(1,sizeof(tlsStruct)))){
		fprintf(stderr,"%s: error allocating tls struct\n",argv[0]);
		exit(1);
	}
	
	
	srand(time(NULL));

	/* defaults */
	setDefaults(info);
	
	/*
	** default librat stuff
	*/

	ratObj=RATinit(argc,argv);
	nargs=RATparse(ratObj,argc,argv,(tlsStruct *)info);
	info->verbose = RATgetVerboseLevel(ratObj);

	if(RATisWavefrontFile(ratObj))
		RATreadObject(ratObj);

	if(strcmp(info->ofile,"-")){
		if(!(info->ofp=fopen(info->ofile,"w"))){
	      		fprintf(stderr,"%s: couldn't open op file %s\n",argv[0],info->ofile);
	      		exit(1);
	   	}
	}
	else{
		info->ofp=stdout;
	}


	if(info->theta[2]==0||info->phi[2]==0){
		fprintf(stderr,"%s: can't have a zero angle increment\n",argv[0]);
		exit(1);
	}
	else{
		/*
		** round to nearest int
		*/
		info->thetaSteps = floor(((info->theta[1] - info->theta[0])/info->theta[2])+0.5);
		info->phiSteps = floor(((info->phi[1] - info->phi[0])/info->phi[2])+0.5);
	}

	if(info->verbose){
		fprintf(stderr,"\n%s: theta = %.2f %.2f %.2f phi = %.2f %.2f %.2f\n", 
			argv[0], info->theta[0], info->theta[1], info->theta[2], 
			info->phi[0], info->phi[1], info->phi[2]);
		fprintf(stderr,"%s: thetaSteps = %f phiSteps = %f\n",argv[0], info->thetaSteps, info->phiSteps);
	} 

	/*
	** loop over theta, then phi and get first return distance
	*/
	doStuff(ratObj, info, argv);

 
}

void doStuff(RATobj *ratObj, tlsStruct *info, char **argv){
	int t=0, p=0, chunks=MAXCHAR, i=0, nhits=0;
	float *opbuf=NULL;
	double direction[3], theta, phi, hit[3], oldhit[3], len=0., phiShift=0.;
	RATtree *ratTree=NULL;
	void jitter();

	int phil=0;

	opbuf = (float *)v_allocate(sizeof(float),info->thetaSteps*info->phiSteps);
	
	/* fprintf(stderr,"%i %i\n",info->thetaSteps,info->phiSteps); */

	ratTree=RATgetRatTree(ratObj);

	phiShift = atan2(info->origin[1],info->origin[0]);
	
	for(t=0;t<info->thetaSteps;t++){
		theta = (info->theta[0] + t * info->theta[2])*D2R;
		for(p=0;p<info->phiSteps;p++){
			phi = (info->phi[0] + p * info->phi[2])*D2R;
			if(info->verbose) fprintf(stderr,"\r(%8.4f)              ",(t*info->phiSteps+p)*100./(info->thetaSteps*info->phiSteps));
			

			/*
			** jitter over fov for rpp values
			*/
			
			nhits = 0;
			len = 0.;
			hit[0] = hit[1] = hit[2] = 0;
			for(i=0;i<info->rpp;i++){

				theta = (info->theta[0] + t * info->theta[2])*D2R;
				phi = (info->phi[0] + p * info->phi[2])*D2R;

				/*
				** jitter theta, phi over fov for now
				*/
				jitter(&theta, &phi, info);
			
				/*
				** sort out x, y directions so that we're always looking at 0, 0, 0
		        ** i.e. multiply nby -1 AND take into account displacement from the axes in phi only
				*/
				phi -= phiShift;

				direction[0] = -1.*(cos(theta)*cos(phi));
				direction[1] = 1.*(cos(theta)*sin(phi));
				direction[2] = 1.*sin(theta);

				/*
				** fprintf(stderr,"%f %f %f %f %f %f\n",theta,phi,phiShift,direction[0],direction[1],direction[2]);
				** exit(1);
				*/
				
				RATtraceRay(ratObj,info->origin,direction,NULL);
				ratTree=RATgetRatTree(ratObj);
		
				/*
				** single rtd for now i.e. ratTree->intersectionPoints[0] where 0 is RTD
				*/
				
				if(ratTree->thisRTD==0){
					nhits++;
					if(info->relative){
						hit[0] += info->origin[0] - ratTree->intersectionPoints[0][0];
						hit[1] += info->origin[1] - ratTree->intersectionPoints[0][1];
						hit[2] += info->origin[2] - ratTree->intersectionPoints[0][2];
					}else{
						hit[0] += ratTree->intersectionPoints[0][0];
						hit[1] += ratTree->intersectionPoints[0][1];
						hit[2] += ratTree->intersectionPoints[0][2];
					}						
					len += ratTree->rayLengths[0];
				}

			}
			
			if(nhits){
				hit[0] /= nhits;
				hit[1] /= nhits;
				hit[2] /= nhits;
				len /= nhits;
				fprintf(info->ofp,"%.6f %.6f %.6f\n", hit[0], hit[1], hit[2]);
				opbuf[t*(int)info->phiSteps+p] = len;
			}else{
				opbuf[t*(int)info->phiSteps+p] = -100.; 
			}
		}
	}
	
	if(info->imflag){
		if(!(info->opimagefp=fopen(info->opimage,"w"))){
			fprintf(stderr,"%s: couldn't open opimage file %s\n",argv[0],info->opimage);
			exit(1);
  		}
		RATputImage(info->opimage,opbuf,info->thetaSteps,info->phiSteps,1,IMAGE_FLOAT);
	}
  	return;
}



void setDefaults(tlsStruct *info)
{
 /* defaults */
  info->verbose = 0;
  info->rpp = 5;
  /* 
  ** need to think about this value
  ** eg see Pesci, Teza, Bonali 2011, Rem Sens, 3, 167-184: D = 0.17 mrad ~ 0.01 deg for Optech ILRIS-3D, but make larger for now 
  */
  info->fov = 0.01;
  strcpy(info->ifile,"-");
  strcpy(info->ofile,"-");
  info->theta[0] = -2.5; info->theta[1] = 2.5; info->theta[2] = 0.5;
  info->phi[0] = -2.5; info->phi[1] = 2.5; info->phi[2] = 0.5;
  info->thetaSteps = 0.1;
  info->phiSteps = 0.1;
  info->imflag = 0;
  info->relative = 0;
  /*
  ** default origin: from 1, 0, 1 to 0, 0, 1
  */
  info->origin[0] = 1; info->origin[1] = 0.; info->origin[2] = 1.;
  return;
}


void jitter(double *t, double *p, tlsStruct *info)
{

	/*
	** generate random dispersion of theta, phi over fov - CONVERT TO RAD
	*/
	float phi=*p;
	float theta=*t;
	*t += ((info->fov/-2.) + (rand()/(RAND_MAX + 1.0))*info->fov)*D2R;
	*p += ((info->fov/-2.) + (rand()/(RAND_MAX + 1.0))*info->fov)*D2R; 
	//printf("theta: %f %f phi: %f %f PHIL:%i %i\n", theta, *t, phi, *p, *phil, phil_n);
	return;
}

int RATuserParse(RATobj *ratObj,int thisarg,int argc,char **argv,  void *info){
  int numberOfArguments=-1,i, atoi();
  tlsStruct *doStruct=NULL;


  doStruct = (tlsStruct *)info;

  if(!strncasecmp(argv[thisarg],"-ip",3)){
    numberOfArguments=1;
    if(thisarg+numberOfArguments >= argc){
      fprintf(stderr,"%s: error in number of arguments for -ip option: 1 required\n",argv[0]);
        exit(1);
    }
    strcpy(doStruct->ifile,argv[thisarg+numberOfArguments]);
  }else if(!strncasecmp(argv[thisarg],"-op",3)){
    numberOfArguments=1;
    if(thisarg+numberOfArguments >= argc){
      fprintf(stderr,"%s: error in number of arguments for -op option: 1 required\n",argv[0]);
        exit(1);
    }
    strcpy(doStruct->ofile,argv[thisarg+numberOfArguments]);
  }else if(!strncasecmp(argv[thisarg],"-im",3)){
    numberOfArguments=1;
    if(thisarg+numberOfArguments >= argc){
      fprintf(stderr,"%s: error in number of arguments for -im option: 1 required\n",argv[0]);
        exit(1);
    }
    strcpy(doStruct->opimage,argv[thisarg+numberOfArguments]); 
	doStruct->imflag=1; 
  }else if(!strncasecmp(argv[thisarg],"-rel",4)){
    numberOfArguments=1;
    if(thisarg+numberOfArguments >= argc){
      fprintf(stderr,"%s: error in number of arguments for -rel option: 1 required\n",argv[0]);
        exit(1);
    }
	doStruct->relative=1;   
  }else if(!strncasecmp(argv[thisarg],"-th",2)){
    numberOfArguments=3;
    for(i=0;i<numberOfArguments;i++){
      /* check we dont overrun */
      if(thisarg+1+i >= argc){
        fprintf(stderr,"%s: error in number of arguments for -t: 3 required\n",argv[0]);
        exit(1);
      }
      doStruct->theta[i]=atof(argv[thisarg+1+i]);
    }
  }else if(!strncasecmp(argv[thisarg],"-ph",2)){
    numberOfArguments=3;
    for(i=0;i<numberOfArguments;i++){
      /* check we dont overrun */
      if(thisarg+1+i >= argc){
        fprintf(stderr,"%s: error in number of arguments for -p: 3 required\n",argv[0]);
        exit(1);
      }
      doStruct->phi[i]=atof(argv[thisarg+1+i]);
    }
  }else if(!strncasecmp(argv[thisarg],"-or",2)){
    numberOfArguments=3;
    for(i=0;i<numberOfArguments;i++){
      /* check we dont overrun */
      if(thisarg+1+i >= argc){
        fprintf(stderr,"%s: error in number of arguments for -or: 3 required\n",argv[0]);
        exit(1);
      }
      doStruct->origin[i] = atof(argv[thisarg+1+i]);
    }
  }else if(!strncasecmp(argv[thisarg],"-rpp",3)){
    numberOfArguments=1;
    for(i=0;i<numberOfArguments;i++){
      /* check we dont overrun */
      if(thisarg+1+i >= argc){
        fprintf(stderr,"%s: error in number of arguments for -rpp: 1 required\n",argv[0]);
        exit(1);
      }
      doStruct->rpp = atoi(argv[thisarg+1+i]);
    }
  }else if(!strncasecmp(argv[thisarg],"-fov",3)){
    numberOfArguments=1;
    for(i=0;i<numberOfArguments;i++){
      /* check we dont overrun */
      if(thisarg+1+i >= argc){
        fprintf(stderr,"%s: error in number of arguments for -fov: 1 required\n",argv[0]);
        exit(1);
      }
      doStruct->fov = atof(argv[thisarg+1+i]);
    }

  }else{
   fprintf(stderr,"%s: argument %s not recognised\n",argv[0],argv[thisarg]);
   exit(1);
  }
  return(numberOfArguments);
}


/* user arguments for help */
void RATuserPrintOptions(RATobj *ratObj){
  fprintf(stderr,"[-op op.dat] [-th th_start th_end th_step][-ph ph_start ph_end ph_step][-or orig_z orig_y orig_z][-rpp rpp][-fov fov][-relative]");
  return;
}

void RATuserInterrupt(RATobj *ratObj,int sig){
	return;
}

