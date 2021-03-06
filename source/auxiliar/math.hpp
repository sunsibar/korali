#ifndef _KORALI_AUXILIARS_KORALIMATH_HPP_
#define _KORALI_AUXILIARS_KORALIMATH_HPP_

// Auxiliar library for Korali's math and time operations.

#include <stdlib.h>
#include <limits>
#include <string>
#include <vector>

namespace korali
{

template <typename T>
double sign( T val )
{
  return (T(0) < val) - (val < T(0));
}

const double NaN    = std::numeric_limits<double>::quiet_NaN();
const double Inf    = std::numeric_limits<double>::infinity();
const double Lowest = std::numeric_limits<double>::lowest();
const double Max    = std::numeric_limits<double>::max();
const double Min    = std::numeric_limits<double>::min();
const double Eps    = std::numeric_limits<double>::epsilon();

double logSumExp(const std::vector<double>& logValues );
double vectorNorm(const std::vector<double>& x );
double vectorDistance(const std::vector<double>& x, const std::vector<double>& y );
bool isanynan(const std::vector<double>& x );
std::string getTimestamp();
size_t getTimehash();

}

#endif // _KORALI_AUXILIARS_KORALIMATH_HPP_
