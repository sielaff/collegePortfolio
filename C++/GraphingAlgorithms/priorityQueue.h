#include <iostream>
#include <string>
#include <fstream>

using namespace std;

template <class myType> 
struct heapNode{

	myType item;
	unsigned long long priority;
};

template <class myType>
class priorityQueue {

	public:
		priorityQueue(int = 5000);
		~priorityQueue();
		
		int entries() const;
		void insert(const myType, const unsigned long long);
		bool deleteMin(myType &, unsigned long long &);
		bool isEmpty() const;
		void printHeap() const;
		bool readData(const string);
		
	private:
		int count;
		int heapSize;
		heapNode<myType> *myHeap;
		
		void reheapUp(int);
		void reheapDown(int);
		void buildHeap();
		void resize();
		
};

template <class myType>
priorityQueue<myType>::priorityQueue(int size) {
	
	myHeap = new heapNode<myType>[size];
	for (int i = 0; i < size; i++) 
		myHeap[i].priority = 0;
	
	count = 0;
	heapSize = size;
}

template <class myType>
priorityQueue<myType>::~priorityQueue() {
	
	delete [] myHeap;
}

template <class myType>
void priorityQueue<myType>::reheapUp(int last) {
	
	int parent;
	if (last > 1) {
		parent = last/2;
		if (myHeap[last].priority < myHeap[parent].priority) {
			heapNode<myType>tmp = myHeap[last];
			myHeap[last] = myHeap[parent];
			myHeap[parent] = tmp;
			reheapUp(parent);
		}
	}
}

template <class myType>
void priorityQueue<myType>::reheapDown(int passed) {
	
	int leftChild;
	int rightChild;
	int maxChild;
	
	leftChild = 2 * passed + 1;
	rightChild = leftChild + 1;
	
	if (leftChild <= count % 2) {
		
		if (leftChild == count % 2)
			maxChild = leftChild;
		
		else {
			if (myHeap[leftChild].priority <= myHeap[rightChild].priority)
				maxChild = rightChild;
			else
				maxChild = leftChild;
		}
		
		if (myHeap[passed].priority < myHeap[maxChild].priority) {
			
			heapNode<myType>tmp = myHeap[passed];
			myHeap[passed] = myHeap[maxChild];
			myHeap[maxChild] = tmp;
			reheapDown(maxChild);
		}
	}
}

template <class myType>
void priorityQueue<myType>::buildHeap() {
	
	for (int i = 0; i < heapSize; i++) {
		reheapUp(i);
		reheapDown(i);
	}
}

template <class myType>
void priorityQueue<myType>::resize() {
	
	heapNode<myType>*newHeap;
	newHeap = new heapNode<myType>[heapSize*2];
	
	for (int i = 0; i < heapSize; i++)
		newHeap[i] = myHeap[i];
	for (int j = heapSize; j < 2*heapSize; j++) 
		newHeap[j].priority = 0;
		
	heapSize = 2*heapSize;
	myHeap = newHeap;
}

template <class myType>
int priorityQueue<myType>::entries() const {
	
	return count;
}

template <class myType>
void priorityQueue<myType>::insert(const myType item1, unsigned long long priority1) {
	
	if (count == heapSize)
		resize();
	
	myHeap[count].item = item1;
	myHeap[count].priority = priority1;
	reheapUp(count);
	count++;
}

template <class myType>
bool priorityQueue<myType>::deleteMin(myType &item1, unsigned long long &priority1) {
	
	if (isEmpty())
		return false;
	else {
		priority1 = myHeap[0].priority;
		item1 = myHeap[0].item;
		for (int i = 0; i < count; i++) 
			myHeap[i] = myHeap[i + 1];
		count -= 1;
		reheapDown(0);
	}
}

template <class myType>
bool priorityQueue<myType>::isEmpty() const {
	
	if (count == 0)
		return true;
	else
		return false;
}

template <class myType>
void priorityQueue<myType>::printHeap() const {
	
}

template <class myType>
bool priorityQueue<myType>::readData(const string fName) {

	ifstream inFile(fName.c_str());							
	if(!inFile.is_open()) 									
		return false;
	
	else {
		count = 0;
		while (inFile) {
			string str;
			string num;
		
			if (count >= heapSize)
				resize();
		
			getline(inFile, str, ' ');	 
			getline(inFile, num);	 
			num = num.substr(6);
//			int num1 = stoi(num);
			myHeap[count].item = str;
			myHeap[count].priority = num;
			count++;
		}
		buildHeap();
	}	
}

