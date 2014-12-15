all:
	gcc -g -o tester tester.c

run:
	python distributions.py 2000 > blah
	cat blah | ./tester > out
	python dataprocess.py
