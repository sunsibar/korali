#!/bin/bash

##############################################################################
# Brief: Test correct configuration of Korali-Apps
# Type: Regression Test 
# Description:
# This test configures (without running) all the applications in the korali-
# apps repository to make sure they are up-to-date with Korali's syntax.
###############################################################################

source ../functions.sh

#################################################
 Checking for MPI
#################################################

if [[ $MPICXX == "" ]]
then
 echo "[Korali] MPI not installed, skipping test."
 exit 0
fi

#################################################
 Clone korali-apps repository
#################################################

logEcho "[Korali] Cloning korali-apps repository"                                   
rm -rf korali-apps
git clone git://github.com/cselab/korali-apps.git >> $logFile
check_result

#################################################
# Test Korali+LAMMPS
#################################################

pushd korali-apps/LAMMPS/LJ
logEcho "[Korali] Testing Korali+LAMMPS..."
popd

#################################################
# Test Korali+Mirheo
#################################################

logEcho "[Korali] Testing Korali+Mirheo..."

pushd korali-apps/mirheo/rbc_stretching

logEcho "[Korali] Converting to dry run..."
cat run.py | sed -e 's/run()/dry()/g' > run_dry.py
check_result

logEcho "[Korali] Setting permissions..."
chmod a+x run_dry.py
check_result

logEcho "[Korali] Running run_dry.py..."
mpirun -n 3 ./run_dry.py >> $logFile
check_result

popd

#################################################
# Test Korali+MSolve
#################################################

logEcho "[Korali] Testing Korali+MSolve (Heat EQ)..."

pushd korali-apps/MSolve/heatEq

logEcho "[Korali] Converting to dry run..."
cat heatPosterior.py | sed -e 's/run()/dry()/g' > run_dry.py
check_result

logEcho "[Korali] Setting permissions..."
chmod a+x run_dry.py
check_result

logEcho "[Korali] Running run_dry.py..."
mpirun -n 3 ./run_dry.py >> $logFile
check_result

popd