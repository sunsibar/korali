#ifndef _KORALI_SOLVER_TMCMC_HPP_
#define _KORALI_SOLVER_TMCMC_HPP_

#include "solvers/base.hpp"
#include <gsl/gsl_rng.h>
#include <gsl/gsl_vector.h>

namespace Korali { namespace Solver {

/******************************************************************************
Module Name: Transitional Markov Chain Monte Carlo
Type: Solver, Sampler
Alias: TMCMC
Description:
This is the implementation of the *Transitional Markov Chain Monte Carlo*
algorithm, as published in [Ching2007](https://ascelibrary.org/doi/abs/10.1061/%28ASCE%290733-9399%282007%29133%3A7%28816%29).

TMCMC avoids sampling from difficult target probability densities
(e.g. posterior distributions in a Bayesian inference problem) but samples from
a series of intermediate PDFs that converge to the target PDF.
This technique is also known as Sampling Importance Resampling in the Bayesian community.

** Usage **

```python
  k["Solver"] = "TMCMC"
```
	
**Requirements:**

+ The *Population Size* used at every generation needs to be defined.
+ The *Problem* needs to be of type Bayesian.
******************************************************************************
Plotting:
Here we explain technical details of the **TMCMC** result plot.

The `python3 -m korali.plotter` command plots the distribution of the samples at every
generation. The samples are read from the json-files stored in the output
directory (`/_korali_result/`).

A plot of the samples obtained after the final generation of TMCMC
function is given below. Here, the target function is the exponential of the
negative of the 2-dimensional [Rosenbrock](https://en.wikipedia.org/wiki/Rosenbrock_function)
function.

![figure](sampling_rosenbrock.png)

**Diagonal Plots**. The diagonal plots show the marginal probability densities of the samples for
each variable. Note that the indices of the vertical axes correspond to the
upper and lower triangle plot and not to the diagonal plots.

**Upper Triangle**. In the plots in the upper triangle we see the actual realization of the samples.
The axes represent the dimensions, respectively the objective variables,
of the problem and we show a two-dimensional plot for every variable pair.

**Lower Triangle**. The lower triangle shows the probability density of the samples for each variable pair.
The density is approximated through a smoothening operator applied to the number
of samples that can be found in a given area.
******************************************************************************/


class TMCMC : public Base
{
 public:

/******************************************************************************
Setting Name: Population Size
Type: Solver Setting
Default Value:
Default Enabled:
Description:
Specifies the number of samples drawn from the posterior distribution at each generation.
******************************************************************************/
size_t _populationSize;

/******************************************************************************
Setting Name: Burn In Default
Type: Solver Setting
Default Value: 0
Default Enabled:
Description:
Specifies the number of additional TMCMC steps per sample per generation.
Note that only the last sample per chain is considered for the recombination.
******************************************************************************/
size_t _burnInDefault;

/******************************************************************************
Setting Name: Burn In Steps
Type: Solver Setting
Default Value: 0
Default Enabled:
Description:
Specifies the number of additional TMCMC steps per sample at specified
generations.
******************************************************************************/
std::vector<size_t> _burnInSteps;

/******************************************************************************
Setting Name: Target Coefficient of Variation
Type: Solver Setting
Default Value: 1.0
Default Enabled:
Description:
Initial value for the target coefficient of variation to search for the exponent
 $\rho_{i+1}$. By default, Korali will set this value to 1.00 as suggested in 
 [Ching2007].
******************************************************************************/
double _targetCVar;

/******************************************************************************
Setting Name: Covariance Scaling
Type: Solver Setting
Default Value: 0.04
Default Enabled:
Description:
Covariance scaling factor $\beta^2$ of proposal distribution.
By default, Korali sets this value 0.04 as suggested in [Ching2007].
******************************************************************************/
double _covarianceScaling;

/******************************************************************************
Setting Name: Use Local Covariance
Type: Solver Setting
Default Value: false
Default Enabled:
Description:
If $true, TMCMC calculates a local covariance matrix per sample from its 
neighbours.
******************************************************************************/
bool _useLocalCovariance;

/******************************************************************************
Setting Name: Min Rho Update
Type: Solver Setting
Default Value: 0.00001
Default Enabled:
Description:
Minimum increment of the exponent $\rho_{i+1}$. This parameter prevents TMCMC 
from stalling.
******************************************************************************/
double _minRhoUpdate;

/******************************************************************************
Setting Name: Max Rho Update
Type: Solver Setting
Default Value: 1.0
Default Enabled:
Description:
Maximum increment of the exponent $\rho{i+1}$. By default, Korali will set this 
value to 1.0 (inactive).
******************************************************************************/
double _maxRhoUpdate;

/******************************************************************************
Setting Name: Burn In
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Actual placeholder for burn in steps per generation, initialized from $Burn In 
Default$ and $Burn In Steps$.
******************************************************************************/
std::vector<size_t> _burnIn;

/******************************************************************************
Setting Name: Chain Pending Fitness
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Indicates that the fitness result for the chain is pending
******************************************************************************/
std::vector<bool> _chainPendingFitness;

/******************************************************************************
Setting Name: Chain Candidate Parameters
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Current (theta) parameters of the chain leader sample.
******************************************************************************/
std::vector<double> _chainCandidatesParameters;

/******************************************************************************
Setting Name: Chain Candidates LogLikelihoods
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
The logLikelihoods of the chain candidates.
******************************************************************************/
std::vector<double> _chainCandidatesLogLikelihoods;

/******************************************************************************
Setting Name: Chain Leader Parameters
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Current (theta) parameters of the chain leader sample.
******************************************************************************/
std::vector<double> _chainLeadersParameters;

/******************************************************************************
Setting Name: Chain Leaders LogLikelihoods
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
The logLikelihoods of the chain leaders.
******************************************************************************/
std::vector<double> _chainLeadersLogLikelihoods;

/******************************************************************************
Setting Name: Finished Chains Count
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Number of finished chains.
******************************************************************************/
size_t _finishedChainsCount;

/******************************************************************************
Setting Name: Current Chain Step
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
The current execution step for every chain.
******************************************************************************/
std::vector<size_t> _currentChainStep;

/******************************************************************************
Setting Name: Chain Lengths
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Length for each of the chains.
******************************************************************************/
std::vector<size_t> _chainLengths;

/******************************************************************************
Setting Name: Coefficient of Variation
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Current coefficient of variation
******************************************************************************/
double _coefficientOfVariation;

/******************************************************************************
Setting Name: Chain Count
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Unique selections after resampling (forming new chain)
******************************************************************************/
size_t _chainCount;

/******************************************************************************
Setting Name: Annealing Exponent
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Indicates how the calculated distribution fits the real distribution
******************************************************************************/
double _annealingExponent;

/******************************************************************************
Setting Name: Accepted Samples Count
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Accepted samples after proposal
******************************************************************************/
size_t _acceptedSamplesCount;

/******************************************************************************
Setting Name: logEvidence
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Calculated logEvidence of the model so far
******************************************************************************/
double _logEvidence;

/******************************************************************************
Setting Name: Proposals Acceptance Rate
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Acceptance rate calculated from samples
******************************************************************************/
double _proposalsAcceptanceRate;

/******************************************************************************
Setting Name: Selection Acceptance Rate
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Acceptance rate calculated from chain count
******************************************************************************/
double _selectionAcceptanceRate;

/******************************************************************************
Setting Name: Covariance Matrix
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Sample covariance of leader fitness values
******************************************************************************/
std::vector<double> _covarianceMatrix;

/******************************************************************************
Setting Name: Mean Theta
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Mean of leader fitness values
******************************************************************************/
std::vector<double> _meanTheta;

/******************************************************************************
Setting Name: Database Entry Count
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Number of accepted samples stored in the database.
******************************************************************************/
size_t _databaseEntryCount;

/******************************************************************************
Setting Name: Sample Parameters Database
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Variable values of samples stored in the database.
******************************************************************************/
std::vector<double> _sampleParametersDatabase;

/******************************************************************************
Setting Name: Sample Fitness Database
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Fitness of the samples stored in the database.
******************************************************************************/
std::vector<double> _sampleFitnessDatabase;

/******************************************************************************
Setting Name: Local Covariance Matrices
Type: Internal Attribute
Default Value:
Default Enabled:
Description:
Local covariances of chain leaders
******************************************************************************/
std::vector<std::vector<double>> _localCovarianceMatrices;

/******************************************************************************
* Variable Settings
******************************************************************************/

struct variableSetting
{

};

std::vector<variableSetting> _variableSettings;

/*****************************************************************************/

 // TMCMC Status variables
 gsl_rng  *range;

 TMCMC();
 ~TMCMC();

  // Korali Methods
 void initialize() override;
 void finalize() override;

 void runGeneration() override;
 void processSample(size_t c, double fitness) override;
 bool checkTermination() override;

  // Internal TMCMC Methods
 void processGeneration();
 void updateDatabase(double* point, double fitness);
 void generateCandidate(size_t candidate);
 void evaluateSample(size_t candidate);
 void computeChainCovariances(std::vector< std::vector<double> >& chain_cov, size_t newchains);
 void minSearch(double const *fj, size_t fn, double pj, double objTol, double& xmin, double& fmin);
 bool isFeasibleCandidate(size_t candidate);
 static double tmcmc_objlogp(double x, const double *fj, size_t fn, double pj, double zero);
 static double objLog(const gsl_vector *v, void *param);

 void setConfiguration() override;
 void getConfiguration() override;
 void printGeneration() override;
};

} } // namespace Korali::Solver

#endif // _KORALI_SOLVER_TMCMC_HPP_