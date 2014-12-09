#
# This file is part of Lyra2, a password hashing scheme
# Copyright (c) 2013-2014 by Lyra2 Project - - <http://www.lyra2.net/>
#

CC?=gcc
NVCC=nvcc
CFLAGS=-std=c99 -Wall -pedantic -O3 -msse2 -ftree-vectorizer-verbose=1 -fopenmp -fopenmp-simd -funroll-loops -march=native -Ofast -mprefer-avx128 -flto -Wno-unused-variable

BINDIR=../bin
BIN=$(BINDIR)/Lyra2
BINCUDA=$(BINDIR)/Lyra2CUDA
nCols=256
bSponge=12
Sponge=0
nThreads=1
nSyncs=2
Bench=0

parameters=-DN_COLS=$(nCols) -DBLOCK_LEN_INT64=$(bSponge) -DSPONGE=$(Sponge) -DnPARALLEL=$(nThreads) -DSIGMA=$(nSyncs) -DBENCH=$(Bench)

SSEDIR=sse/


default:	$(SSEDIR)Lyra2.c $(SSEDIR)Sponge.c Main.c $(SSEDIR)Lyra2.h $(SSEDIR)Sponge.h
	mkdir -p $(BINDIR)
	$(CC) $(CFLAGS) $(SSEDIR)Sponge.c $(SSEDIR)Lyra2.c Main.c -o $(BIN) $(parameters)
	@echo "Build completed, binaries in $(BIN)"
	
clean:
	rm -rf *.o $(BIN) $(BINDIR)


