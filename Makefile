all: testcplusplus testpython

cplusplus:
	cd cpp ; \
	g++ -o OneEuroFilterCpp OneEuroFilter.cc ; \
	./OneEuroFilterCpp > test.csv

testcplusplus: cplusplus
	python3 test.py cpp cpp/test.csv

testpython: 
	cd python ; \
	python3 OneEuroFilterTest.py > test.csv ; \
	cd .. ; \
	python3 test.py python python/test.csv