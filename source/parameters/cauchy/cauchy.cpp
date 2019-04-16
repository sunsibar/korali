#include "korali.h"

using namespace Korali::Parameter;

/************************************************************************/
/*                  Constructor / Destructor Methods                    */
/************************************************************************/

Cauchy::Cauchy(double loc, double scale, size_t seed) : Base::Base(seed)
{
	_loc = loc;
	_scale = scale;
	initialize();
}

Cauchy::Cauchy(nlohmann::json& js, int seed) : Base::Base(js, seed)
{
 setConfiguration(js);
 initialize();
}

Cauchy::~Cauchy()
{

}

/************************************************************************/
/*                    Configuration Methods                             */
/************************************************************************/

nlohmann::json Cauchy::getConfiguration()
{
 auto js = this->Base::getConfiguration();

 js["Distribution"] = "Cauchy";
 js["Location"] = _loc;
 js["Scale"] = _scale;

 return js;
}

void Cauchy::setConfiguration(nlohmann::json& js)
{
	_loc  = consume(js, { "Location" }, KORALI_NUMBER);
 _scale = consume(js, { "Scale" }, KORALI_NUMBER);
}

/************************************************************************/
/*                    Functional Methods                                */
/************************************************************************/

void Cauchy::initialize()
{
	_aux = -gsl_sf_log( _scale * M_PI );
}

double Cauchy::getDensity(double x)
{
 return gsl_ran_cauchy_pdf( x-_loc, _scale );
}

double Cauchy::getDensityLog(double x)
{
 return  _aux - gsl_sf_log( 1. + gsl_sf_pow_int((x-_loc)/_scale,2) );
}

double Cauchy::getRandomNumber()
{
 return _loc + gsl_ran_cauchy(_range, _scale);
}

void Cauchy::printDetails()
{
  printf("Cauchy(%.3g,%.3g)", _loc, _scale);
}
