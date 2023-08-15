CPP=g++
PYTHON=python3

all: testcplusplus

OneEuroFilter.o:
	$(CPP) -c -o OneEuroFilter.o OneEuroFilter.cpp 

cplusplus: OneEuroFilter.o
	$(CPP) -o OneEuroFilterCpp OneEuroFilter.o Test.cpp ; \
	./OneEuroFilterCpp > test.csv

testcplusplus: cplusplus
	$(PYTHON) ../test.py cpp test.csv