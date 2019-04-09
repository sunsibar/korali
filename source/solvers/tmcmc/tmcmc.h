#ifndef _KORALI_TMCMC_H_
#define _KORALI_TMCMC_H_

#include "solvers/base/base.h"
#include <gsl/gsl_rng.h>
#include <gsl/gsl_vector.h>

namespace Korali::Solver
{

typedef struct fparam_s {
    const double *fj;
    int           fn;
    double        pj;
    double        tol;
} fparam_t;

class TMCMC : public Korali::Solver::Base
{
 public:

 // TMCMC Configuration
 double _tolCOV;              /* Target coefficient of variation of weights */
 double _minStep;             /* Min update of rho */
 double _bbeta;               /* Covariance scaling parameter */
 size_t  _s; // Population Size
 bool _useLocalCov;

 // TMCMC Runtime Variables

 size_t nChains;
 size_t  _currentGeneration;
 size_t  _burnIn;
 double  _varianceCoefficient;
 double  _annealingRatio;
 size_t  _uniqueSelections;
 size_t  _uniqueEntries;
 double  _logEvidence;
 double  _acceptanceRate;
 double* _covarianceMatrix;            /*[PROBDIM][PROBDIM];*/
 double* _meanTheta;     /*[PROBDIM]*/
 size_t _maxGens;

 gsl_rng  *range;

 double* clPoints;   // Chain Leader Parameter Values
 double* clFitness;  // Chain Leader Fitness

 double* ccPoints;   // Chain Candidate Parameter Values
 double* ccFitness;  // Chain Candidate Fitness
 gsl_rng** chainGSLRange;

 bool*   chainPendingFitness; // Indicates that the fitness result for the chain is pending
 size_t  finishedChains;
 size_t* chainCurrentStep;
 size_t* chainLength;

 size_t  databaseEntries;
 double* databasePoints;
 double* databaseFitness;

 double **local_cov;     /* [DATANUM][PROBDIM*PROBDIM] */

  // Korali Methods
 void initialize();
 void run();

  // Internal TMCMC Methods
 void saveResults();
 void resampleGeneration();
 void updateDatabase(double* point, double fitness);
 void processSample(size_t c, double fitness);
 void generateCandidate(int c);
 void computeChainCovariances(double** chain_cov, int newchains);
 void minSearch(double const *fj, int fn, double pj, double objTol, double *xmin, double *fmin);
 static double tmcmc_objlogp(double x, const double *fj, int fn, double pj, double zero);
 static double objLog(const gsl_vector *v, void *param);

 // Serialization Methods
 virtual nlohmann::json getConfiguration();
 virtual void setConfiguration(nlohmann::json js);
 virtual nlohmann::json getState();
 virtual void setState(nlohmann::json js);
};

} // namespace Korali

#endif // _KORALI_TMCMC_H_