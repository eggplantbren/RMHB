#ifndef _Data_
#define _Data_

#include <vector>

class Data
{
	private:
		std::vector<int> t1, t2;
		std::vector<double> Y1, Y2;
		std::vector<double> sig1, sig2;

	public:
		Data();
		void load(const char* filename1, const char* filename2);

		// Accessors
		int get_t1(int i) const { return t1[i]; }
		double get_Y1(int i) const { return Y1[i]; }
		double get_sig1(int i) const { return sig1[i]; }
		int get_N1() const { return t1.size(); }
		// Accessors
		int get_t2(int i) const { return t2[i]; }
		double get_Y2(int i) const { return Y2[i]; }
		double get_sig2(int i) const { return sig2[i]; }
		int get_N2() const { return t2.size(); }


	private:
		static Data instance;
	public:
		static Data& get_instance() { return instance; }

};

#endif

