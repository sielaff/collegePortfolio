#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <limits>
#include "graphAlgorithms.h"
#include "priorityQueue.h"

using namespace std;
const int INF = numeric_limits<int>::max();

graphAlgorithms::graphAlgorithms(int count) {
	
	if (count >= 5) {
		title = "";
		vertexCount = count;
		
		newGraph(count);
		
		dist = NULL;
		prev = NULL;  
		topoNodes = NULL;
		
		topoCount = 0;
	}
	else
		cout << "Error, invalid graph size." << endl;
}

graphAlgorithms::~graphAlgorithms() {
	
	destroyGraph();
}

void graphAlgorithms::newGraph(int count) {
	
	destroyGraph();
	graphMatrix = new int*[count];
	for (int i = 0; i < count; i++)
		graphMatrix[i] = new int[count];
	
	for (int j = 0; j < vertexCount; j++)
		for (int k = 0; k < vertexCount; k++)
			graphMatrix[j][k] = 0;
}

void graphAlgorithms::destroyGraph() {
	
	delete [] dist;
	delete [] prev;
	delete [] topoNodes;
	
	title = "";
	topoCount = 0;
	
	for (int i = 0; i < vertexCount; i++)
		for (int j = 0; j < vertexCount; j++)
			delete [] graphMatrix[i];
	delete [] graphMatrix;
}

string graphAlgorithms::getGraphTitle() const {
	
	return title;
}

void graphAlgorithms::setGraphTitle(const string newTitle) {
	
	title = newTitle;
}

int graphAlgorithms::getVertexCount() const {
	
	return vertexCount;
}

void graphAlgorithms::addEdge(int from, int to, int weight) {
	
	if (from == to)
		cout << "Error, vertex to and from cannot be the same." << endl;
	
	if (to > vertexCount || from > vertexCount)
		cout << "Error, invalid vertex." << endl;
	
	if (from != to && to <= vertexCount && from <= vertexCount)
		graphMatrix[to][from] = weight;
}

void graphAlgorithms::topoSort() {
	
	bool *visited = new bool[vertexCount];
	topoNodes = new int[vertexCount];
	for (int i = 0; i < vertexCount; i++) {
		topoNodes[i] = -1;
		visited[i] = false;
	}
	
	for (int j = 0; j < vertexCount; j++) {
		if (visited[j] == false)
			dfs(j, visited);
	}
}

void graphAlgorithms::dfs(int u, bool visited[]) {
	
	visited[u] = true;
	for (int i = 0; i < vertexCount; i++)
		if (graphMatrix[u][i] != 0 && visited[i] == false)
			dfs(i, visited);
	topoNodes[topoCount++] = u;
}

void graphAlgorithms::dijkstraSP(int src) {
	
	if (src > vertexCount)
		cout << "Invalid vertex." << endl;
	else {
		dist = new int[vertexCount];
		prev = new int[vertexCount];
		
		for (int i = 0; i < vertexCount; i++) {
			dist[i] = INF;
			prev[i] = -1;
		}
		
		priorityQueue<int> myQueue;
		myQueue.insert(src, 0);
		dist[src] = 0;
		
		int u, newDist;
		unsigned long long pr;
		
		while (!myQueue.isEmpty()) {
			myQueue.deleteMin(u, pr);
			for (int j = 0; j < vertexCount; j++) {
				if (graphMatrix[u][j] != 0) {
					newDist = dist[u] + graphMatrix[u][j];
					if (newDist < dist[j]) {
						dist[j] = newDist;
						prev[j] = u;
						myQueue.insert(j, newDist);
					}
				}
			}
		}
		printDistances(src);
	}
}

void graphAlgorithms::printPath(const int src, const int dest) const {
	
	if (dist[dest] == INF)
		cout << "There is no path between these two nodes." << endl;
	else {
		cout << "Path from " << src << " to " << dest << endl;
		cout << dest;
		showPath(dest);
	}
}

void graphAlgorithms::showPath(const int dest) const {
	
	if (dest == -1)
		cout << endl;
	else {
		cout << " - " << prev[dest];
		showPath(prev[dest]);
	}
}

void graphAlgorithms::printDistances(const int src) const {
	
	if (dist == NULL)
		cout << "Error. No distances array." << endl;
	else {
		cout << "Shortest Paths:" << endl;
		cout << "From Node: " << src << " to: " << endl;
		cout << setw(10) << right << "Vertex" << setw(10) << right << "Dist" << setw(10) << right << "From" << endl;
		for (int i = 0; i < vertexCount; i++) {
			cout << setw(10) << right << i;
			if (dist[i] == INF)
				cout << setw(20) << right << "not reachable." << endl;
			else {
				cout << setw(10) << right << dist[i];
				if (i == src)
					cout << setw(10) << right << "-" << endl;
				else
					cout << setw(10) << right << prev[i] << endl;
			}
		}
	}
}

bool graphAlgorithms::readGraph(const string fName) {

	ifstream inFile(fName.c_str());							
	if(!inFile.is_open()) 									
		return false;
	
	else {
		string field;
		int a, b, c;
		getline(inFile, field);
		inFile >> vertexCount;
		if (vertexCount >= 5) {
			newGraph(vertexCount);
			while (inFile) {
				inFile >> a >> b >> c;
				addEdge(a, b, c);
			}
		}
		else
			cout << "Error, invalid vertex count." << endl;
	}
}

void graphAlgorithms::printMatrix() const {

	cout << "Graph Adjacency Matrix:" << endl;
	cout << "    ";
	for (int i = 0; i < vertexCount; i++)
		cout << "   " << i;
	cout << endl;
	cout << "    ";
	for (int j = 0; j < vertexCount; j++)
		cout << "----";
	
	for (int k = 0; k < vertexCount; k++) {
		cout << k << "|  ";
		for (int l = 0; l < vertexCount; l++) {
			if (k == l)
				cout << "   0";
			else if (graphMatrix[k][l] == 0)
				cout << "  --";
			else 
				cout << setw(4) << right << graphMatrix[k][l];
		}
		cout << endl;
	}
	cout << endl;
}
