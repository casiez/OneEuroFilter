all: testcplusplus testcplusplusUsingTemplates testc testpython testJava testJavascript testTypescript

# C++ version original
testcplusplus:
	cd cpp ; make

# C++ version using templates
testcplusplusUsingTemplates:
	cd CppUsingTemplates ; make

# C version
testc:
	cd C ; make

# Python version
testpython: 
	cd python ; make

# Java
testJava: 
	cd java ; make

# Javascript
testJavascript:
	cd javascript ; make

# Typescript
testTypescript:
	cd typescript ; make