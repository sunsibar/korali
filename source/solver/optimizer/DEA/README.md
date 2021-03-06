This is an implementation of the *Differential Evolution Algorithm* algorithm, as published in [Storn1997](https://link.springer.com/article/10.1023/A:1008202821328).

DEA optimizes a problem by updating a population of candidate solutions through mutation and recombination. The update rules are simple and the objective function must not be differentiable. Our implementation includes various adaption and updating strategies [Brest2006](https://ieeexplore.ieee.org/document/4016057).

**Usage:**

```python
  k["Solver"]["Type"] = "DEA"
```
  
**Requirements:**

+ The *Sample Count* needs to be defined..
+ The *Lower Bound* needs to be defined for each variable.
+ The *Upper Bound* needs to be defined for every variable.

## Configuration

### Solver Settings
 
### Variable-Specific Settings

### Termination Criteria

## Plotting
