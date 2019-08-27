// amicableNumes.cpp

#include <iostream>
#include <thread>
#include <chrono>
#include <mutex>

using namespace std;

int getNext();
void foundPair();
void checkAmic(int);

int amicNumCount = 0;
int currentNum = 0;
mutex myLock;
int upperLimit = 0;	


int main (int argc, char *argv[] ) {
	
	if (argc != 5 || argv[1] != "-t" || argv[3] != "-l") {						//	//
		cout << "Please format arguments correctly." << endl;						//
		cout << "./amicableNumes -t <threadCount> -l <limitValue>" << endl;			//
		return 0;																	//
	}																				//
																					// check command line arguments
	int size = argv[2];																//
																					//
	if (size <= 0 || size > 32) {													//
		cout << "Please enter a thread count between 0 and 32." << endl;			//
		return 0;																	//
	}																			//	//
	
	thread *myThread = new thread[size];											// dynamically allocate array of threads
	
	cout << "Enter an upper bound: " << endl;									//	//
	cin >> upperLimit;																//
																					//
	if (upperLimit <= 10 || upperLimit > 500000) {									// prompt for and check upper bound
		cout << "Please enter an upper bound between 10 and 500,000." << endl;		//
		return 0;																	//
	}																			//	//
	
	for (int i = 0; i < size; i++)													// loop through threads and check for amicable numbers
		myThread[i](checkAmic);
	
	for (int j = 0; j < size; j++)													// wait for all threads to close out
		myThread[j].join();
	
	cout << "There are " << amicNumCount << " amicable numbers between 10 and " << upperLimit << "." << endl;
	
	return 0;																		// output results
}

int getNext() {
	lock_guard<mutex> guard(myLock);
	currentNum++;
	return currentNum;
}

void checkAmic () {										

	int divisorSum1 = 0;
	int divisorSum2 = 0;

	while (num = getNext() < = upperLimit) {
		divisorSum1 = 0;
		for (int j = 0; j < num; j++)					// find the sum of all the divisors of the current number 
			if (num % j == 0)
				divisorSum += j;
		if (divisorSum > num && divisorSum != 1) {		// continue if not prime, not perfect, and sum isn't less than the number itself
			for (int i = 0; i < num; i++) {				// go through each number from 0 to the current number 
				divisorSum2 = 0;
				for (int k = 0; k < i; k++)				// find the divisor sum of each number and check if the numbers are amicable
					if (i % k == 0)
						divisorSum2 += k;
				if (divisorSum2 == num && divisorSum1 == i)
					foundPair();
			}				
		}
	}
}

void foundPair () {
	lock_guard<mutex> guard(myLock);
	amicNumCount++;
}
	
	
	
	
	