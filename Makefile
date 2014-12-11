SAMPLES?=10

all:
	gcc -g -o tester tester.c

run:
	python distributions.py ${SAMPLES} | ./tester > out
	python dataprocess.py
