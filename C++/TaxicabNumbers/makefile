OBJS 	= taxiNums.o
CC	= g++ taxiNums.cpp
DEPS	= priorityQueue.h

all: taxiNums

taxiNums.o: taxiNums.cpp $(DEPS)
	$(CC) -c taxiNums.cpp

taxiNums: taxiNums.o $(DEPS)
	$(CC) -o taxiNums 

clean:
	rm $(OBJS)
