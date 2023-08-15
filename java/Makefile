PYTHON=python3

all: testJava

javaVersion:
	javac Test.java ; \
	java Test > test.csv ; \

testJava: javaVersion
	$(PYTHON) ../test.py java test.csv