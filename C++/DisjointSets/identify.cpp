//  CS 302
//  Main program for Percolate Game

#include <iostream>
#include <string>
#include <sstream>
#include <cstdlib>

#include "connectedComponents.h"

using namespace std;

// *********************************************************************
//  Get and check command line arguments...
//	-th <threshold> -fv <fillValue> -if <inputFileName> -of <outputFileName>

bool	getArgs(int argc, char *argv[], int &threshold, int &fillValue,
		string &inputFileName, string &outputFileName)
{
	stringstream ss;

	if (argc == 1) {
		cout << "Usage: ./identify -th <threshold> -fv <fillValue> " <<
			"-if <inputFileName> -of <outputFileName>" << endl;
		return	false;
	}

	if (argc != 9) {
		cout << "Error, invalid command line arguments." << endl;
		return	false;
	}

	if (string(argv[1]) != "-th") {
		cout << "Error, invalid threshold specifier." << endl;
		return	false;
	}

	if (string(argv[2]) != "") {
		ss.clear();
		ss << argv[2];
		ss >> threshold;
	}

	if(threshold < 0 || threshold > 255) {
		cout << "Error, invalid threshold value." << endl;
		return	false;
	}

	if (string(argv[3]) != "-fv") {
		cout << "Error, invalid fill value specifier." << endl;
		return	false;
	}

	if (string(argv[4]) != "") {
		ss.clear();
		ss << argv[4];
		ss >> fillValue;
	}

	if(fillValue < 0 || fillValue > 255) {
		cout << "Error, invalid fill value." << endl;
		return	false;
	}

	if (string(argv[5]) != "-if") {
		cout << "Error, invalid input file specifier." << endl;
		return	false;
	}

	inputFileName = string(argv[6]);

	if (string(argv[7]) != "-of") {
		cout << "Error, invalid output file specifier." << endl;
		return	false;
	}

	outputFileName = string(argv[8]);

	return	true;
}

// *****************************************************************

int main(int argc, char *argv[])
{

// ------------------------------------------------------------------
//  Declarations and headers...

	string	stars, bars, dashes;
	stars.append(65, '*');
	bars.append(65, '=');
	dashes.append(40,'-');
	const char* bold   = "\033[1m";
	const char* unbold   = "\033[0m";

	int	threshold;
	int	fillValue;
	string	inFileName;
	string	outFileName;

	cout << stars << endl << bold << "CS 302 - Assignment #9" << endl;
	cout << "Identify Connected Components" << unbold << endl;
	cout << endl;

// ------------------------------------------------------------------
//  Identify connected components for image from command line.
//	get command line arguments
//	

	connectedComponents	myImage;

	if (getArgs (argc, argv, threshold, fillValue, inFileName, outFileName)) {
		myImage.setThreshold(threshold);
		if (myImage.readImageFile(inFileName)) {
			myImage.identify();
			myImage.showStatus();
			myImage.fillComponent(fillValue);
			if (myImage.writeImageFile(outFileName))
				myImage.showStatus();
			else
				cout << "Error writing output file." << endl;
		} else {
			cout << "Error reading input file." << endl;
		}
	}

// ------------------------------------------------------------------
//  All done.

	cout << endl << stars << endl <<
		"Game Over, thank you for playing." << endl;

	return 0;
}

