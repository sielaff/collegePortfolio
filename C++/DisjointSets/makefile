# Make file for percolate game assignment

CC	= g++ -Wall -pedantic -std=c++11 -g
OBJS	= identify.o connectedComponents.o disjointSets.o
DEPS	= connectedComponents.h disjointSets.h

all: identify testDS

testDS.o: testDS.cpp disjointSets.h
	$(CC) -c testDS.cpp

testDS: testDS.o disjointSets.o disjointSets.h
	$(CC) -o testDS testDS.o disjointSets.o


connectedComponents.o: connectedComponents.cpp $(DEPS)
	$(CC) -c connectedComponents.cpp

disjointSets.o: disjointSets.cpp $(DEPS)
	$(CC) -c disjointSets.cpp

identify.o: identify.cpp $(DEPS)
	$(CC) -c identify.cpp

identify: identify.o connectedComponents.o disjointSets.o $(DEPS)
	$(CC) -o identify $(OBJS)


# -----
# clean by removing object files.

clean:
	rm	$(OBJS)

