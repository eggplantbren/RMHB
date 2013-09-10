#include "Data.h"
#include <fstream>

using namespace std;

Data Data::instance;

Data::Data()
{

}

void Data::load(const char* filename1, const char* filename2)
{
	t1.clear(); Y1.clear(); sig1.clear();

	fstream fin;
	fin.open(filename1, ios::in);
	double temp1, temp2, temp3;
	while(fin>>temp1 && fin>>temp2 && fin>>temp3)
	{
		t1.push_back((int)temp1);
		Y1.push_back(temp2);
		sig1.push_back(temp3);
	}
	fin.close();

	t2.clear(); Y2.clear(); sig2.clear();
	fin.open(filename2, ios::in);
	while(fin>>temp1 && fin>>temp2 && fin>>temp3)
	{
		t2.push_back((int)temp1);
		Y2.push_back(temp2);
		sig2.push_back(temp3);
	}
	fin.close();
}

