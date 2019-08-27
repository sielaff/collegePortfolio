#include "disjointSets.h"
#include <iostream>

using namespace std;

disjointSets::disjointSets() {
	
	totalSize = 0;
	setsCount = 0;
	links = NULL;
	sizes = NULL;
}

disjointSets::~disjointSets() {
	
	delete [] sizes;
	delete [] links;
}

void disjointSets::createSets(int size) {
	
	if (size > 0) {
		sizes = new int[size];
		links = new int[size];
		for (int i = 0; i < size; i++) {
			links[i] = -1;
			sizes[i] = 1;
		}
		
		totalSize = size;
		setsCount = size;
	}
}

int disjointSets::getTotalSets() const {
	
	return totalSize;
}

int disjointSets::getSetCount() const {
	
	return setsCount;
}

int disjointSets::getSetSize(const int set) const {
	
	return sizes[set];
}

void disjointSets::printSets() const {
	
	cout << "index:";
	for (int i = 0; i < totalSize; i++)
		cout << "  " << i;
	cout << endl;
	cout << "links:";
	for (int j = 0; j < totalSize; j++) {
		if (links[j] < 0)
			cout << " " << links[j];
		else
			cout << "  " << links[j];
	}
	cout << endl;
	cout << "sizes:";
	for (int k = 0; k < totalSize; k++)
		cout << "  " << sizes[k];
	cout << endl;
}

int disjointSets::setUnion(int first, int second) {

	int parent, child;
	
	if (setFind(first) != -1)
		first = setFind(first);
	if (setFind(second) != -1)
		second = setFind(second);
	
	if (first != second) {
		if (sizes[first] < sizes[second]) {
			parent = second;
			child = first;
		}
		else {
			parent = first;
			child = second;
		}
		
		links[child] = parent;
		sizes[parent] += sizes[child];
		return parent;
	}
	else
		return first;
}

int disjointSets::setFind(int find) {
	
	if (links[find] < 0)
		return find;
	else 
		return links[find] = setFind(links[find]);
}