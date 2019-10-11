#!/bin/bash

source ../functions.sh

############# STEP 1 ##############

logEcho "[Korali] Beginning minimization with non-finites tests..."

for file in run*.py
do
  logEcho "-------------------------------------"
  logEcho " Running $file"
  timerStart
  ./"$file" >> $logFile 2>&1
  check_result
  timerEnd
  logEcho "-------------------------------------"
done

log "[Korali] Removing results..."
rm -rf _results_* >> $logFile 2>&1


