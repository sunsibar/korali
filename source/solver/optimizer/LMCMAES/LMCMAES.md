This is the implementation of the *Limitded Memory - Covariance Matrix Adaptation Evolution Strategy*, as published in [Loshchilov2015](http://loshchilov.com/publications/LMCMA.pdf).

For a general overview on evolution strategies and CMAES we refer to CMAES.md.
In LM-CMAES the memory footprint of the  decomposition of the covariance matrix is reduced. LM-CMAES is said to outperform the original CMA-ES on non-separable ill-conditioned problems with a factor increasing with problem dimension (see reference).
CMAES works iteratively, evaluating a number $\lambda$ of samples per generation, and improving the covariance matrix for the samples in the next generation.

**Usage:**
```python
  k["Solver"] = "LMCMAES"
```

**Base Requirements:**

+ The *Sample Count* $\lambda$ needs to be defined.
+ The *Initial Mean* needs to be defined for every variable.
+ The *Initial Standard Deviation* needs to be defined for every variable.

## Configuration

### Solver Settings
 
### Variable-Specific Settings

### Termination Criteria

