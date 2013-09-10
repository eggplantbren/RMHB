/*
* Copyright (c) 2009, 2010, 2011, 2012 Brendon J. Brewer.
*
* This file is part of DNest3.
*
* DNest3 is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* DNest3 is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with DNest3. If not, see <http://www.gnu.org/licenses/>.
*/

#include "TimeSeriesModel.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include "Data.h"
#include <cmath>

using namespace std;
using namespace DNest3;

TimeSeriesModel::TimeSeriesModel()
:n(1500), y(1500), y_response(Data::get_instance().get_N2())
{

}

void TimeSeriesModel::fromPrior()
{
	L = exp(log(1.) + log(1E6)*randomU());
	beta = exp(log(1E-3) + log(1E6)*randomU());
	mu = 100.*tan(M_PI*(randomU() - 0.5));

	max_lag = exp(log(1E-3) + log(1E3)*randomU());
	K = randomU();

	A = exp(log(1E-3) + log(1E6)*randomU());
	C = 100.*tan(M_PI*(randomU() - 0.5));	

	for(size_t i=0; i<n.size(); i++)
		n[i] = randn();
	calculate_y();
}

double TimeSeriesModel::perturb()
{
	double logH = 0.;

	int which = randInt(7);
	if(which == 0)
	{
		L = log(L);
		L += log(1E6)*pow(10., 1.5 - 6.*randomU())*randn();
		L = mod(L - log(1.), log(1E6)) + log(1.);
		L = exp(L);
	}
	else if(which == 1)
	{
		beta = log(beta);
		beta += log(1E6)*pow(10., 1.5 - 6.*randomU())*randn();
		beta = mod(beta - log(1E-3), log(1E6)) + log(1E-3);
		beta = exp(beta);
	}
	else if(which == 2)
	{
		mu = atan(mu/100.)/M_PI + 0.5;
		mu += pow(10., 1.5 - 6.*randomU())*randn();
		mu = mod(mu, 1.);
		mu = 100.*tan(M_PI*(mu - 0.5));
	}
	else if(which == 3)
	{
		max_lag = log(max_lag);
		max_lag += log(1E6)*pow(10., 1.5 - 6.*randomU())*randn();
		max_lag = mod(max_lag - log(1E-3), log(1E6)) + log(1E-3);
		max_lag = exp(max_lag);

	}
	else if(which == 4)
	{
		K += pow(10., 1.5 - 6.*randomU())*randn();
		K = mod(K, 1.);
	}
	else if(which == 5)
	{
		A = log(A);
		A += log(1E6)*pow(10., 1.5 - 6.*randomU())*randn();
		A = mod(A - log(1E-3), log(1E6)) + log(1E-3);
		A = exp(A);
	}
	else if(which == 6)
	{
		C = atan(C/100.)/M_PI + 0.5;
		C += pow(10., 1.5 - 6.*randomU())*randn();
		C = mod(C, 1.);
		C = 100.*tan(M_PI*(C - 0.5));
	}

	// Always do this
	double chance = pow(10., 0.5 - 4.*randomU());
	double scale = pow(10., 1.5 - 6.*randomU());
	bool full = randomU() <= 0.3;
	for(size_t i=0; i<n.size(); i++)
	{
		if(randomU() <= chance)
		{
			if(full)
				n[i] = randn();
			else
			{
				logH -= -0.5*pow(n[i], 2);
				n[i] += scale*randn();
				logH += -0.5*pow(n[i], 2);
			}
		}
	}

	calculate_y();
	return logH;
}

void TimeSeriesModel::calculate_y()
{
	double alpha = exp(-1./L);
	for(size_t i=0; i<y.size(); i++)
	{
		if(i == 0)
			y[i] = mu + beta/sqrt(1. - pow(alpha, 2))*n[0];
		else
			y[i] = mu + alpha*(y[i-1] - mu) + beta*n[i];
	}

	double min_lag = K*max_lag;

	int a = (int)min_lag;
	int b = (int)max_lag;

	// Second time series
	for(int i=0; i<Data::get_instance().get_N2(); i++)
	{
		double tot = 0.;
		int num = 0;
		for(int j=(Data::get_instance().get_t2(i) - b); j<(Data::get_instance().get_t2(i) - a); j++)
		{
			if(j >= 0 && j < (int)y.size())
			{
				tot += (y[j] + C);
				num++;
			}
		}
		y_response[i] = A*tot/num;
	}
}

double TimeSeriesModel::logLikelihood() const
{
	double logL = 0.;

	// First time series data
	for(int i=0; i<Data::get_instance().get_N1(); i++)
	{
		logL += -0.5*pow((Data::get_instance().get_Y1(i) - y[Data::get_instance().get_t1(i)])/Data::get_instance().get_sig1(i), 2);
	}

	// Second time series data
	for(int i=0; i<Data::get_instance().get_N2(); i++)
	{
		logL += -0.5*pow((Data::get_instance().get_Y2(i) - y_response[i])/Data::get_instance().get_sig2(i), 2);
	}
	return logL;
}

void TimeSeriesModel::print(std::ostream& out) const
{
	out<<0.5*(K*max_lag + max_lag)<<' ';
	out<<L<<' '<<beta<<' '<<mu<<' '<<max_lag<<' '<<K<<' '<<A<<' '<<C<<' ';
	for(size_t i=0; i<y.size(); i++)
		out<<y[i]<<' ';
	for(size_t i=0; i<y_response.size(); i++)
		out<<y_response[i]<<' ';
}

string TimeSeriesModel::description() const
{
	return string("tau, L, beta, mu, max_lag, K, A, C, y, y_response");
}

