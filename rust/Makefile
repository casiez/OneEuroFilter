CARGO=cargo
PYTHON=python3

all: testrust

# Build (no external dependencies, so this works fully offline) and run,
# writing the filtered ground-truth signal to test.csv.
rust:
	$(CARGO) build --release --quiet
	./target/release/one_euro_filter > test.csv

testrust: rust
	$(PYTHON) ../test.py rust test.csv
