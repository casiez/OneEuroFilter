CPP=g++
PYTHON=python3

all: testcplusplusUsingTemplates

cplusplusUsingTemplates:
	$(CPP) -o 1efilter 1efilter.cc  ; \
	./1efilter > test.csv

testcplusplusUsingTemplates: cplusplusUsingTemplates
	$(PYTHON) ../test.py cppUsingTemplates test.csv