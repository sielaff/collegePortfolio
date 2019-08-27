# Make file for percolate game assignment

CC	= g++ -Wall -pedantic -std=c++11 -g
OBJS	= graphs.o priorityQueue.o graphAlgorithms.o
DEPS	= priorityQueue.h graphAlgorithms.h

all: graphs

graphs.o: graphs.cpp graphAlgorithms.h
	$(CC) -c graphs.cpp

graphs: graphs.o graphAlgorithms.o graphAlgorithms.h
	$(CC) -o graphs graphs.o graphAlgorithms.o


priorityQueue.o: priorityQueue.h $(DEPS)
	$(CC) -c priorityQueue.cpp

disjointSets.o: disjointSets.cpp $(DEPS)
	$(CC) -c disjointSets.cpp



# -----
# clean by removing object files.

clean:
	rm	all

