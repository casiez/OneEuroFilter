PYTHON=python3

all:
	npm install ; \
	tsc ; \
	node dist/test.js > test.csv ; \
	$(PYTHON) ../test.py typescript test.csv