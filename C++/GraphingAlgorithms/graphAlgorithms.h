
#include <string>

class graphAlgorithms {
		
	public:
		~graphAlgorithms();
		graphAlgorithms(int = 5);
		void newGraph(int);
		void addEdge(int, int, int);
		bool readGraph(const std::string);
		int getVertexCount() const;
		void printMatrix() const;
		void topoSort();
		void dijkstraSP(int);
		void printPath(const int, const int) const;
		std::string getGraphTitle() const;
		void setGraphTitle(const std::string);
		void printDistances(const int) const;
	
	private:
		int vertexCount;
		std::string title;
		int **graphMatrix;
		int *dist;
		int *prev;
		int *topoNodes;
		int topoCount;
		void showPath(const int) const;
		void destroyGraph();
		void dfs(int, bool[]);

};

