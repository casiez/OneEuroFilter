all: testcplusplus testpython

cplusplus:
	cd cpp ; \
	g++ -o OneEuroFilterCpp OneEuroFilter.cc ; \
	./OneEuroFilterCpp > test.csv

testcplusplus: cplusplus
	python3 test.py cpp cpp/test.csv

cplusplusUsingTemplates:
	cd CppUsingTemplates ; \
	g++ -o g++ -o 1efilter 1efilter.cc  ; \
	./1efilter > test.csv

testcplusplusUsingTemplates: cplusplusUsingTemplates
	python3 test.py cpp CppUsingTemplates/test.csv

testpython: 
	cd python ; \
	python3 OneEuroFilterTest.py > test.csv ; \
	cd .. ; \
	python3 test.py python python/test.csv