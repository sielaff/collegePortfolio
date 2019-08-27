//  Main program for testing

#include <iostream>
#include <sstream>
#include <string>
#include <cstdlib>

#include "graphAlgorithms.h"

using namespace std;

// ************************************************************************
//  Get and check command line arguments...
//	./graphs <-t | -gf <inputFileName> -sn <startNode> 
//					-dn <destNode> <-sm> >

bool	getArgs(int argc, char *argv[], bool &doTesting,
			string &graphFileName, int &stNode,
			int &dNode, bool &showMatrix)
{
	stringstream ss;

	if (argc == 1) {
		cout << "Usage: ./graphs <-t | -gf <inputFileName> "
			<< "-sn <startNode> -dn <destNode> <-sm> >" << endl;
		return	false;
	}

	if (argc == 2 && string(argv[1]) == "-t") {
		doTesting = true;
		return	true;
	}

	if (!(argc == 7 || argc == 8)) {
		cout << "Error, invalid command line arguments." << endl;
		return	false;
	}

	doTesting = false;

	if (string(argv[1]) != "-gf") {
		cout << "Error, invalid graph file specifier." << endl;
		return	false;
	}

	graphFileName = string(argv[2]);

	if (string(argv[3]) != "-sn") {
		cout << "Error, invalid start node specifier." << endl;
		return	false;
	}

	if (string(argv[4]) != "") {
		ss.clear();
		ss << argv[4];
		ss >> stNode;
	}

	if (string(argv[5]) != "-dn") {
		cout << "Error, invalid destination node specifier." << endl;
		return	false;
	}

	if (string(argv[6]) != "") {
		ss.clear();
		ss << argv[6];
		ss >> dNode;
	}

	if (stNode == dNode) {
		cout << "Error, start node and destination should " <<
			"not be the same." << endl;
		return	false;
	}

	showMatrix = false;
	if (argc == 8) {
		if (string(argv[7]) == "-sm") {
			showMatrix = true;
		} else {
			cout << "Error, invalid show matrix specifier." << endl;
			return	false;
		}
	}

	return	true;
}

// ************************************************************************
//  Main program for testing graph algorithms object.

int main(int argc, char *argv[])
{

// ------------------------------------------------------------------
//  Declare variables and display some cute headers...

	string		stars, bars, dashes;
	string		fName;
	const char	*bold = "\033[1m";
	const char	*unbold = "\033[0m";
	bool		doTesting = false;
	bool		showMatrix = false;
	string		graphFile = "";
	int		startNode, destNode;

	dashes.append(40,'-');
	stars.append(65, '*');
	bars.append(65, '=');

	cout << stars << endl << bold << "CS 302 - Assignment #10" << endl;
	cout << "Graph Algorithms" << unbold << endl;
	cout << endl;

// ------------------------------------------------------------------
//  Check/get arguments

	if (!getArgs(argc, argv, doTesting, graphFile,
		startNode, destNode, showMatrix))
			exit(1);

// ------------------------------------------------------------------
//  Basic error testing...

	if (doTesting) {
		cout << bars << endl;
		cout << "Error testing: " << endl << endl;

		graphAlgorithms	badGraph1(-1);
		graphAlgorithms	badGraph2(3);
		graphAlgorithms	badGraph3(10);
		graphAlgorithms	tmpGraph4;

		badGraph3.newGraph(-2);
		badGraph3.newGraph(2);
		badGraph3.newGraph(20);
		badGraph3.addEdge(11, -11, 100);
		badGraph3.addEdge(51, 11, 100);
		badGraph3.addEdge(-11, 11, 100);
		badGraph3.addEdge(3, 3, 10);
		badGraph3.addEdge(5, 7, 100);			// ok
		badGraph3.setGraphTitle("Unused Example");

		if (badGraph3.getGraphTitle() != "Unused Example")
			cout << "main: title functions do not work." << endl;

		if (tmpGraph4.getVertexCount() != 5)
			cout << "main, constructor did not set"
				<< "vertex count correctly." << endl;

		tmpGraph4.newGraph(1000);
		if (tmpGraph4.getVertexCount() != 1000)
			cout << "main, newGraph() and/or getVertexCount()"
				<< "functions did not work correctly." << endl;

		cout << endl;
		badGraph2.topoSort();

		cout << endl;
		badGraph2.printMatrix();

		cout << endl;
		badGraph2.dijkstraSP(0);

		cout << endl;
		badGraph3.dijkstraSP(40);

		cout << endl;
	}

// ------------------------------------------------------------------
//  Graph Algorithms -> Dijkstra and Topo sort
//	read graph file
//	if print option selected, print
//	topo sort (which prints results)
//	find shortest path (which prints results)

	if (!doTesting) {

		cout << bars << endl;
		cout << bold << "Graph Algorithms" << unbold << endl << endl;

		graphAlgorithms	myGraph;

		if (myGraph.readGraph(graphFile)) {
			if (showMatrix)
				myGraph.printMatrix();
			myGraph.topoSort();
			myGraph.dijkstraSP(startNode);
			cout << dashes << endl;
			myGraph.printPath(startNode, destNode);
		} else {
			cout << "main: Error reading " << graphFile << "." << endl;
		}

		cout << endl;
	}

// ------------------------------------------------------------------
//  All done.

	cout << endl << stars << endl <<
		"Game Over, thank you for playing." << endl;

	return 0;
}

