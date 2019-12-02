# A.1 - Model Optimization: Finding the Global Maximum

In this tutorial we show how to **optimize** a given function.

## Source Code

## Problem Setup

We are given the function $f(\vartheta)=-\vartheta^2$ for $\vartheta\in[-10,10]$.
We want to find the maximum of the function in the given interval.

##  The Objective Function

Create a folder named `model`. Inside, create a file with name `directModel.py` and paste the following code,

```python
#!/usr/bin/env python

def evaluateModel( s ):
  x = s.getVariable(0)
  r = -x*x
  s.addResult(r)
```

This is the computational model that represents our objective function.


## Optimization with CMAES

First, open a file and import the korali module
```python
#!/usr/bin/env python3
import korali
```
Import the computational model,
```python
import sys
sys.path.append('./model')
from directModel import *
```

###  The Korali Object

Next we construct a `Korali` object and set the computational model,
```python
k = korali.initialize()
k.setModel(evaluateModel)
```

###  The Problem Type
Then, we set the type of the problem to `Direct Evaluation`
```python
k["Problem"] = "Direct Evaluation"
```

###  The Variables
In this problem there is only one variable,
```python
k["Variables"][0]["Name"] = "X";
```

###  The Solver
We choose the solver `CMAES`, set the domain of the parameter `X`, the population size to be `5` and two termination criteria,

```python
k["Solver"]  = "CMAES"

k["Variables"][0]["CMA-ES"]["Lower Bound"] = -10.0;
k["Variables"][0]["CMA-ES"]["Upper Bound"] = +10.0;

k["CMA-ES"]["Objective"] = "Maximize"
k["CMA-ES"]["Termination Criteria"]["Max Generations"]["Value"] = 500
k["CMA-ES"]["Sample Count"] = 5
```
For a detailed description of CMAES settings see [here](../../usage/solvers/cmaes.md).

Finally, we need to add a call to the run() routine to start the Korali engine.

```python
k.run()
```

###  Running

We are now ready to run our example:

```bash
./a1-optimization
```

Or, alternatively:

```bash
python3 ./a1-optimization
```
The results are saved in the folder `_korali_result/`.

###  Plotting

You can see the results of CMA-ES by running the command,
```sh
python3 -m korali.plotter
```

![figure](direct-cma.png)
