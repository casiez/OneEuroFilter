PYTHON=python3

all: testJavascript

javascriptVersion:
	node test.js > test.csv

testJavascript: javascriptVersion
	$(PYTHON) ../test.py javascript test.csv