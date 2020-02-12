#ifndef _MODEL_HPP_
#define _MODEL_HPP_

#include "korali.hpp"
#include "load_data.hpp"

#include <vector>
#include<cmath>

/*
Model 1:
A single Gaussian distribution, with
Hyperparameter = sigma, the standard deviation, and
Latent variable = mu, the mean. Assume a uniform prior distribution of the mean in [0,1].


Model 2:
Assume we have two gaussian distributions with peaks around two means, and identical
covariance = sigma.
Hyperparameters:
    mu1, mu2 and sigma
Latent variables:
    Assignment of each data point to the modes
*/


class ExponentialFamilyDistribution :
{
 private:
    pointsInfoStruct _p;

 public:
        virtual void S(korali::Sample& k);
        virtual void zeta(korali::Sample& k);
        virtual void phi(korali::Sample& k);
        virtual void init();
}

class ExampleDistribution1 : ExponentialFamilyDistribution
{
    _p = univariateData();
    void S(korali::Sample& k)
    {
      std::vector<double> hyperparams = k["Hyperparameters"];
      std::vector<double> latentVariables = k["Latent Variables"];
      double sigma = hyperparams[0];
      double mu = latentVariables[0];

      if (mu.length() != _p.nDimensions){
        korali::logError("Mean with wrong number of dimensions.\n");
      }

      // log(p) = -log(sigma*sqrt(pi*2)) - 0.5(x - mu)^2 * 1/sigma^2
      double sum = 0;
      double[_p.nPoints] mse_per_point = {0};
      for(size_t i = 0; i<_p.nPoints; i++){
       // double[_p.nDimensions] point = _p.points[]   // todo: = points[i*nDimensions : (i+1)*nDimensions]
         for (size_t j = 0; j<_p.nDimensions; i++)
            mse_per_point[i] += std::pow( _p.points[i*nDimensions + j] - mu[j] , 2);
            sum += std::pow( _p.points[i*nDimensions + j] - mu[j] , 2);
      }
      k["S"] = -0.5 * sum;  //or k["Evaluation"]["S"] ?
    }

    void zeta(korali::Sample& k)
    {
      std::vector<double> hyperparams = k["Hyperparameters"];
      std::vector<double> hyperparams = k["Latent Variables"];

      k["Evaluation"] = ;  //-0.5*x*x;
    }
    void phi(korali::Sample& k)
    {
      std::vector<double> hyperparams = k["Hyperparameters"];
      std::vector<double> hyperparams = k["Latent Variables"];

      k["Evaluation"] = ;  //-0.5*x*x;
    }
}


#endif
