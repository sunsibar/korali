#!/bin/bash
source ../functions.sh

#################################################
# Checking for MPI
#################################################

if [[ $MPICXX == "" ]]
then
 echo "[Korali] MPI not installed, skipping test."
 exit 0
fi

#################################################
# Clone korali-apps repository
#################################################

logEcho ""
logEcho "[Korali] Cloning korali-apps repository"                                   

rm -rf korali-apps
git clone git://github.com/cselab/korali-apps.git >> $logFile
check_result

#################################################
# Test Korali+LAMMPS
#################################################


logEcho ""
logEcho "[Korali] Testing Korali+LAMMPS..."

pushd korali-apps/LAMMPS

logEcho "[Korali] Converting to dry run..."
cat run-tmcmc.py | sed -e 's/run()/dry()/g' > sample_dry.py
check_result

logEcho "[Korali] Setting permissions..."
chmod a+x sample_dry.py
check_result

logEcho "[Korali] Running sample_dry.py..."
./sample_dry.py 2 >> $logFile
check_result

popd

#################################################
# Test Korali+Mirheo
#################################################

logEcho ""
logEcho "[Korali] Testing Korali+Mirheo..."

pushd korali-apps/mirheo/rbc_stretching

logEcho "[Korali] Converting to dry run..."
cat run-cmaes.py | sed -e 's/run()/dry()/g' > cmaes_dry.py
check_result

cat run-tmcmc.py | sed -e 's/run()/dry()/g' > tmcmc_dry.py
check_result

logEcho "[Korali] Setting permissions..."
chmod a+x cmaes_dry.py
check_result

chmod a+x tmcmc_dry.py
check_result

logEcho "[Korali] Running cmaes_dry.py..."
mpirun -n 3 ./cmaes_dry.py 2 >> $logFile
check_result

logEcho "[Korali] Running tmcmc_dry.py..."
mpirun -n 3 ./tmcmc_dry.py 2 >> $logFile
check_result

popd

#################################################
# Test Korali+MSolve
#################################################

logEcho ""
logEcho "[Korali] Testing Korali+MSolve (Heat EQ)..."

pushd korali-apps/MSolve/heatEq

logEcho "[Korali] Converting to dry run..."
cat heatPosterior.py | sed -e 's/run()/dry()/g' > run_dry.py
check_result

logEcho "[Korali] Setting permissions..."
chmod a+x run_dry.py
check_result

logEcho "[Korali] Running run_dry.py..."
./run_dry.py 2 >> $logFile
check_result

popd
