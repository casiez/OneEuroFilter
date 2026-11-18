PYTHON=python3

all:
	npm install ; \
	npx tsc ; \
	node dist/test.js > test.csv ; \
	$(PYTHON) ../test.py typescript test.csv