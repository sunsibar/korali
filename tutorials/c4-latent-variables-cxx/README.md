# Under Construction! (todo)



# C.4 - Running Korali with Compiled CXX Code, for optimizing parameters in a latent variable model

In this tutorial we show how Korali can be used with c++.
Here we optimize a model with the solver `SA-EM` .
The problem is the sample application (ch. 6) of [[1]](https://www.tandfonline.com/doi/abs/10.1198/106186006X157469). 
We want to find the parameters theta =  (...) that maximize the posterior in a Bayesian problem with latent variables.  

## How to run the example

Run the `Makefile` to compile the executables: In the command line, in the
c4-... sub-folder, type
```
make
```
*Make* finds our `Makefile` and reads the instructions inside how to make the first target listed there.
 This will will create an executable out of each of our .cpp files. To run one of them, type their name prepended 
 with `./`, for example,
```
./run-saem
```
This should output information about the process and result of the optimization.


## Code explanation



 #### Computational Model and Data Points

First, we create the Korali engine and an experiment that we will configure,

```c++
 auto k = korali::Engine();
 auto e = korali::Experiment();
 auto p = heat2DInit(&argc, &argv);
```



```c++
 e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference";
 e["Problem"]["Likelihood Model"] = "Additive Normal";
 e["Problem"]["Reference Data"] = p.refTemp;
 e["Problem"]["Computational Model"] = &heat2DSolver;
```

Function [`...`](model/heat2d.cpp) internally already has access to the data points created by `heat2DInit`. The function calculates temperature values iteratively on a grid over the domain of xPos and yPos, using the Gauss-Seidel method. To get the temperature values at the data points and set them as `Reference Evaluations`, `heat2DSolver` finds a point on the grid close to each data point and returns the temperature value at this grid point.

#### Solver

Then, we decide on `SAEM` as solver and configure its parameters,

```c++
```

#### Variables and Prior Distributions


#### Running the Optimization

Finally, we call the `run()` routine to run the optimization, to find those
parameters v that are most likely, using Bayes rule: We want to find v that
maximize $P(v|X) = P(X|v)*prior(v)$, i.e, the likelihood of
the data times their prior.


```c++
 k.run(e);
```
We can then compile and run the code.   

### References

[1] Jank, Wolfgang. "Implementing and diagnosing the stochastic approximation EM algorithm." Journal of Computational and Graphical Statistics 15.4 (2006): 803-829.