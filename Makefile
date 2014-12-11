SAMPLES?=1000

all:
	gcc -lmemcached -g -o tester tester.c

run:
	python distributions.py ${SAMPLES} | ./tester ${SAMPLES} > out
	python dataprocess.py
