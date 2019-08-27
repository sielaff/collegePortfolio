
class disjointSets {
	
	private:
		int totalSize;
		int setsCount;
		int *links;
		int *sizes;
		
	public:
		disjointSets();
		~disjointSets();
		void createSets(int);
		int getTotalSets() const;
		int getSetCount() const;
		int getSetSize(const int) const;
		void printSets() const;
		int setUnion(int, int);
		int setFind(int);
};

