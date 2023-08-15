CC=gcc
CFLAGS=-I.
PYTHON=python3

all: testc

SF1eFilter.o:
	$(CC) -c -o SF1eFilter.o SF1eFilter.c $(CFLAGS)

c: SF1eFilter.o 
	$(CC) -o 1eurofilter SF1eFilter.o test.c ; \
	./1eurofilter > test.csv

testc: c
	$(PYTHON) ../test.py Cversion test.csv