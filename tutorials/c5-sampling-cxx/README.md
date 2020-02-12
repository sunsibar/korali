# C.1 - Running Korali with Compiled CXX Code

In this tutorial we show how Korali can be used with c++ for sampling.
The content is the same as for a2-sampling, except now in C++. 
## How to run the example

Run the `Makefile` to compile the executables: In the command line, in the
c5-... sub-folder, type
```
make
```
*Make* finds our `Makefile` and reads the instructions inside how to make the first target listed there. This will will create an executable out of each of our .cpp files. To run one of them, type their name prepended with `./`, for example,
```
./run-mcmc
```
This should output information about the process and result of the optimization.


## Code explanation

See a2-sampling.


