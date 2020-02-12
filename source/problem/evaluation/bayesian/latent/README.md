In a Bayesian *latent variable* problem, the model includes a set of unobserved variables, in addition to 
the parameter values that we want to estimate.  

That is, we have a probability distribution of the following form:    
 $$ p( d, z  | \vartheta )  $$
Here, d are observed data points, z the latent variables, and $\vartheta$ a parameter. Note: We restrict the probability 
distribution to be from the exponential family, that is, it must be possible to bring it into the following form:  

 $$ p( d, z  | \vartheta )  = exp{-\zeta(\vartheta)  + S(y, \psi) * \phi(\vartheta) } $$

! Question: Is it a problem that we need the normalized probability distribution in the maximization step? 
Shouldn't any solver work with unnormalized probability distributions?  

One goal is to find $\vartheta$, for example as the value that maximizes its a-posteriori probability: 
 $$ argmax_{\vartheta} \int_{z} p(\vartheta, z | d) dz =  argmax_{\vartheta} \int_{z} \frac{p(d, z | \vartheta) p(\vartheta)}{p(d)} dz $$.
 p(d) does not depend on z or $\vartheta$, so we can ignore p(d) and maximize the unnormalized probability, 
 $$  argmax_{\vartheta} \int_{z} p(d, z | \vartheta) p(\vartheta) dz $$.


## Configuration

#### Functions composing the log-likelihood:
 S, zeta, phi are functions that should be passed by the user. They take as argument a "sample" object and return  nothing; they internally set result variables of the sample.  

 How to define a function that takes as argument a "sample", and how to, internally, set the necessary result values?  
The sample object acts similar to a dictionary. You can access the variable values as "Parameters", set the result by setting "Evaluation".
 For example, in Python:

 ```python
def model(s):
   x = s["Parameters"][0]
   s["Evaluation"] = -0.5*x*x
 ```

C++:
```C++
#include "korali.hpp"

void model(korali::Sample& s)
{
  float x = s["Parameters"][0];
  s["Evaluation"] = -0.5*x*x;
}
```

Other attributes you can access are: 
```
s["Reference Evaluations"] // In "reference" problem types
s["Sample Id"]
```

I believe you can set and retrieve any key-value pair of choice. For the current problem, we will assume you to set "S", "zeta" and "psi", respectively. "S" and "psi" can be vector valued. Use the variable "Latent Variables" to refer to the latent variables, and "Hyperparameters" to access hyperparameters. 

You need to remember which variable has which position, to access it. (I might add fields for the sample to contain latent variables and hyperparameter values separately.)





### Problem Settings

### Variable-Specific Settings
