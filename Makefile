CPP=g++
CC=gcc
CFLAGS=-I.
PYTHON=python3

all: testcplusplus testcplusplusUsingTemplates testc testpython testJava

# C++ version original
cplusplus:
	cd cpp ; \
	$(CPP) -o OneEuroFilterCpp OneEuroFilter.cc ; \
	./OneEuroFilterCpp > test.csv

testcplusplus: cplusplus
	$(PYTHON) test.py cpp cpp/test.csv

# C++ version using templates
cplusplusUsingTemplates:
	cd CppUsingTemplates ; \
	$(CPP) -o 1efilter 1efilter.cc  ; \
	./1efilter > test.csv

testcplusplusUsingTemplates: cplusplusUsingTemplates
	$(PYTHON) test.py cppUsingTemplates CppUsingTemplates/test.csv

# C version
SF1eFilter.o:
	cd C ; \
	$(CC) -c -o SF1eFilter.o SF1eFilter.c $(CFLAGS)

c: SF1eFilter.o 
	cd C ; \
    $(CC) -o 1eurofilter SF1eFilter.o test.c ; \
	./1eurofilter > test.csv

testc: c
	$(PYTHON) test.py Cversion C/test.csv

# Python version
testpython: 
	cd python ; \
	$(PYTHON) OneEuroFilterTest.py > test.csv ; \
	cd .. ; \
	$(PYTHON) test.py python python/test.csv

# Java
javaVersion:
	cd java ; \
	javac Test.java ; \
	java Test > test.csv ; \

testJava: javaVersion
	$(PYTHON) test.py java java/test.csv