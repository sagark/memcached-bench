all:
	gcc -lmemcached -g -o tester tester.c

run:
	./tester > out
	python dataprocess.py
