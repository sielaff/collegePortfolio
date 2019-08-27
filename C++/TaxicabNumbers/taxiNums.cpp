#include "priorityQueue.h"
#include <iostream>

using namespace std;

struct cubeSet {
	
	int a;
	int b;
	int cubeSum;
};

int main () {
	
	priorityQueue<cubeSet> myQueue;

	int limit;
	unsigned long long priority;
	
	cout << "Enter limit:" << endl;
	cin >> limit;
	
	cubeSet thisCubeSet;
	
	for (int i = 0; i < limit; i++) {
		thisCubeSet.a = i;
		thisCubeSet.b = i;
		thisCubeSet.cubeSum = (i * (i * i)) + (i * (i * i));
		priority = thisCubeSet.cubeSum;
		myQueue.insert(thisCubeSet, priority);
	}
	
	int count = 1;
	cubeSet prevCubeSet, currCubeSet, newCubeSet;
	prevCubeSet.a = 0;
	prevCubeSet.b = 0;
	prevCubeSet.cubeSum = 0;
	
	
	while (!myQueue.isEmpty()) {
		myQueue.deleteMin(currCubeSet, priority);
		if (currCubeSet.cubeSum == prevCubeSet.cubeSum) {
			count++;
			if (count == 2) 
				cout << "Taxicab number: " << currCubeSet.a << "^3 + " << currCubeSet.b << "^3 and "
					<< prevCubeSet.a << "^3 + " << prevCubeSet.b << "^3" << endl;
		}
		else
			count = 1;
		prevCubeSet = currCubeSet;
		if (currCubeSet.b < limit) {
			priority = currCubeSet.a * currCubeSet.a * currCubeSet.a + (currCubeSet.b+1) * (currCubeSet.b+1) * (currCubeSet.b+1);
			newCubeSet.a = currCubeSet.a;
			newCubeSet.b = currCubeSet.b + 1;
			newCubeSet.cubeSum = priority;
			myQueue.insert(newCubeSet, priority);
		}
	}
	
	return 0;
}