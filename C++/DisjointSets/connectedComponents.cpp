#include "connectedComponents.h"
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

connectedComponents::connectedComponents() {
	
	image = NULL;
	rows = 0;
	columns = 0;
	threshold = 0;
	
}

connectedComponents::~connectedComponents() {
	
}

bool connectedComponents::readImageFile(string fName) {
	
	ifstream inFile(fName.c_str(), ios::binary);		// try to open the binary file					
	if(!inFile.is_open()) 									
		return false;
	
	else {	
		string field, field1;
		char ch;
		
		getline(inFile, field);							// make sure it's flagged right
		if (field != "P5")
			return false;

		getline(inFile, field);							// get rid of comments
		while (field[0] == '#')
			getline(inFile, field);
		
		char ch1 = 'a';
		int n = 0;
		while (ch1 != ' ') {
			ch1 = field[n];
			n++;
		}
		
		field1 = field.substr(field.find(" ") + 1);
		size_t pos = field.find(" ");
		field = field.substr(0, pos);
		
		rows = stoi(field1);
		columns = stoi(field);
			
		if (rows < MIN_SIZE || rows > MAX_SIZE || columns < MIN_SIZE || columns > MAX_SIZE)
			return 0;
		
		image = new unsigned char *[rows];
		for (int i = 0; i < rows; i++)					// dynamically allocate two dimensional character array
			image[i] = new unsigned char[columns];
		
		getline(inFile, field);							// read in the maximal gray value
		if (field != "255")
			return false;
		
		for (int i = 0; i < rows; i++)					// loop through the rows and columns and fill the image array
			for (int j = 0; j < columns; j++) {
				inFile.get(ch);
				image[i][j] = ch;
			}
		
		inFile.close();
		return true;
	}
}
		
void connectedComponents::identify() {
	
	imageSet.createSets(rows * columns);
	
	unsigned char *ds = new unsigned char[rows * columns];						
												// 1d array used to store image chars
	int cnt = 0;								// used to track position in this array
	
	for (int i = 0; i < rows; i++)				// insert things from the 2d to the 1d
		for (int j = 0; j < columns; j++) {		
			ds[cnt] = image[i][j];
			cnt++;
		}
	
	cnt = 0;
	bool up, down, left, right;
	
	for (int k = 0; k < rows; k++)				// now go back thru the 2d array and check for adjacency
		for (int l = 0; l < columns; l++) {
			up = true;
			down = true;
			left = true;
			right = true;
			
			if (k == 0)
				up = false;
			if (k+1 == rows)
				down = false;
			if (l == 0)
				left = false;
			if (l+1 == columns)
				right = false;
			
			if (up)
				if (ds[cnt] == ds[cnt-columns])
					imageSet.setUnion(cnt, cnt-columns);
			if (down)
				if (ds[cnt] == ds[cnt+columns])
					imageSet.setUnion(cnt, cnt+columns);
			if (left)
				if (ds[cnt] == ds[cnt-1])
					imageSet.setUnion(cnt, cnt-1);
			if (right)
				if (ds[cnt] == ds[cnt+1])
					imageSet.setUnion(cnt, cnt+1);
			
			cnt++;
		}
}

bool connectedComponents::writeImageFile(const string fName) {
	
	ofstream oFile(fName.c_str(), ios::binary);				
	if(!oFile.is_open()) 									
		return false;
	
	else {
		oFile << "P5" << endl;
		oFile << columns << " " << rows << endl;
		oFile << 255 << endl;
		for (int i = 0; i < rows; i++)
			for (int j = 0; j < columns; j++) {
				oFile << image[i][j];
				if (j == columns-1)
					oFile << endl;
				else
					oFile << " ";
			}
		return true;
	}
}

void connectedComponents::setThreshold(const int th) {
	
	if (th < 255 && th > 0)
		threshold = th;
}

void connectedComponents::fillComponent(const int newVal) {
	
	int largest = -1;
	int second = -1;
	int indexOfLargest, indexOfSecond;
	
	for (int i = 0; i < (rows * columns); i++)
		if (imageSet.getSetSize(i) > largest) {
			indexOfLargest = i;
			largest = imageSet.getSetSize(i);
		}
	
	for (int j = 0; j < (rows * columns); j++)
		if (imageSet.getSetSize(j) > second && imageSet.getSetSize(j) < largest) {
			indexOfSecond = j;
			second = imageSet.getSetSize(j);
		}
	
	cout << "1st largest set size = " << largest << endl << "1st largest set parent = " << imageSet.setFind(indexOfLargest) << endl;
	cout << "2nd largest set size = " << second << endl << "2nd largest set parent = " << imageSet.setFind(indexOfSecond) << endl;
			
	unsigned char *ds = new unsigned char[rows * columns];						
	int cnt = 0;								
	
	for (int l = 0; l < rows; l++)				
		for (int m = 0; m < columns; m++) {		
			ds[cnt] = image[l][m];
			cnt++;
		}	
	
	for (int k = 0; k < (rows * columns); k++)
		if (imageSet.setFind(k) == indexOfSecond)
			ds[k] = newVal;
	
	cnt = 0;
	
	for (int n = 0; n < rows; n++)				
		for (int o = 0; o < columns; o++) {		
			image[n][o] = ds[cnt];
			cnt++;
		}	
}

void connectedComponents::showStatus() const {
	
	cout << "Total possible sets: " << imageSet.getTotalSets() << endl;
	cout << "Sets: " << imageSet.getSetCount() << endl;
	cout << "Image: " << columns << " " << rows << " = " << rows * columns << endl;
}

bool connectedComponents::withinThreshold(const unsigned char first, const unsigned char second) const {
	
	if (first >= 0 && first <= threshold && second >= 0 && second <= threshold)
		return true;
	else
		return false;
}
		
			
			