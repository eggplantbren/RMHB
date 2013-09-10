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
	alpha = 0.99 + 0.01*randomU();
	beta = -log(randomU());
	mu = 1000.*randn();
	max_lag = 2.-100.*log(randomU());
	K = 0.9*randomU();
	A = -log(randomU());
	B = 100.*randn();
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
		logH -= 19.*log(alpha);
		alpha += pow(10., 1.5 - 6.*randomU())*randn();
		alpha = mod(alpha, 1.);
		logH += 19.*log(alpha);
	}
	else if(which == 1)
	{
		beta = 1. - exp(-beta);
		beta += pow(10., 1.5 - 6.*randomU())*randn();
		beta = mod(beta, 1.);
		beta = -log(1. - beta);
	}
	else if(which == 2)
	{
		logH -= -0.5*pow(mu/1000., 2);
		mu += 1000.*pow(10., 1.5 - 6.*randomU())*randn();
		logH += -0.5*pow(mu/1000., 2);
	}
	else if(which == 3)
	{
		max_lag = 1. - exp(-(max_lag - 2.)/100.);
		max_lag += pow(10., 1.5 - 6.*randomU())*randn();
		max_lag = mod(max_lag, 1.);
		max_lag = 2 - 100.*log(1. - max_lag);
		min_lag = K*max_lag;
	}
	else if(which == 4)
	{
		K += 0.9*pow(10., 1.5 - 6.*randomU())*randn();
		K = mod(K, 0.9);
		min_lag = K*max_lag;
	}
	else if(which == 5)
	{
		A = 1. - exp(-A);
		A += pow(10., 1.5 - 6.*randomU())*randn();
		A = mod(A, 1.);
		A = -log(1. - A);
	}
	else if(which == 6)
	{
		logH -= -0.5*pow(B/100., 2);
		B += 100.*pow(10., 1.5 - 6.*randomU())*randn();
		logH += -0.5*pow(B/100., 2);
	}


	// Always do this
	double chance = pow(10., 0.5 - 4.*randomU());
	double scale = pow(10., 1.5 - 6.*randomU());
	for(size_t i=0; i<n.size(); i++)
	{
		if(randomU() <= chance)
		{
			logH -= -0.5*pow(n[i], 2);
			n[i] += scale*randn();
			logH += -0.5*pow(n[i], 2);
		}
	}

	calculate_y();
	return logH;
}

void TimeSeriesModel::calculate_y()
{
	for(size_t i=0; i<y.size(); i++)
	{
		if(i == 0)
			y[i] = mu + 1000.*n[0];
		else
			y[i] = mu + alpha*(y[i-1] - mu) + beta*n[i];
	}

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
				tot += (y[j] + B);
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
	out<<alpha<<' '<<beta<<' '<<mu<<' '<<max_lag<<' '<<K<<' '<<A<<' '<<B<<' ';
	for(size_t i=0; i<y.size(); i++)
		out<<y[i]<<' ';
	for(size_t i=0; i<y_response.size(); i++)
		out<<y_response[i]<<' ';
}

string TimeSeriesModel::description() const
{
	return string("tau, alpha, beta, mu, max_lag, K, A, B, y, y_response");
}

