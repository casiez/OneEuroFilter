CSC = mcs
MONO = mono
PYTHON = python3

.PHONY: all testCSharpUnity clean

all: testCSharpUnity

GroundTruthRunner.exe: OneEuroFilter3.cs Tests/Standalone/GroundTruthRunner.cs Tests/Standalone/UnityEngineStub.cs
	$(CSC) -out:$@ OneEuroFilter3.cs Tests/Standalone/GroundTruthRunner.cs Tests/Standalone/UnityEngineStub.cs

testCSharpUnity: GroundTruthRunner.exe
	$(MONO) GroundTruthRunner.exe ../groundTruth.csv > test.csv
	$(PYTHON) ../test.py CSharpUnity test.csv

clean:
	rm -f GroundTruthRunner.exe test.csv