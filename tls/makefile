CC = gcc
BIN = ${HOME}/bin
LEWIS_LIB = ${HOME}/bpms/src
SDKROOT = /Developer/SDKs/MacOSX10.6.sdk
LIBS = -lmatrix_${ARCH} -lalloc_${ARCH} -lvect_${ARCH} -lerr_${ARCH} -lhipl_${ARCH} -lrand_${ARCH} -limage_${ARCH} -lrat_${ARCH}  -lm -lc 
LIBRARY = ${LEWIS_LIB}
CFLAGS += -DDOUBLEDEF  -DMATCHK -D${ARCH} -D_NO_NAG

#CFLAGS += -g -DTEST
CFLAGS += -O

THIS = tls

#	build executables

THIS:		
		make clean ${THIS} 


${THIS}:	makefile ${THIS}.o 
		$(CC) $(CFLAGS) -L${SDKROOT}/usr/lib -L${LEWIS_LIB}/lib -L. -L${LIBRARY}/lib ${THIS}.o -o $@ ${LIBS}

# object building

.c.o:		makefile $<
		$(CC) -I${SDKROOT}/usr/include -I/usr/5include -D${ARCH} ${CFLAGS} -I${LIBRARY}/lib -o $@ -c $< 


# -I/usr/5include -I${HOME}/src/gcc-4.0.3/fixincludes/tests/base
install:	${THIS}
		cp ${THIS} ${BIN}/${ARCH}
		# cp ${THIS}.1 $(HOME)/man/man1

clean:		
		rm -f *% *.o

