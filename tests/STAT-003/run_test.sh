#!/bin/bash

source ../functions.sh

############# STEP 1 ##############

logEcho "[Korali] Beginning STAT-003 test"
logEcho "[Korali] minimization with non-finites tests..."

for file in run*.py
do
  logEcho "-------------------------------------"
  logEcho " Running $file"
  logEcho "-------------------------------------"
  ./"$file" >> $logFile 2>&1
  check_result
done

log "[Korali] Removing results..."
rm -rf _results_* >> $logFile 2>&1


