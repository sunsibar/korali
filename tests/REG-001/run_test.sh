#!/bin/bash

##############################################################################
# Brief: Re-run all Python example applications for basic sanity check.
# Type: Regression Test
# Description:
# This test finds and runs A Tutorials /tutorials folder to make sure
# the typical use cases still work.
# Steps:
# 1 - Operation: List and run all .py scripts in the tutorials/python folder.
#     Expected result: all of the .py scripts will run for less than 20 secs
#     and rc = 0.
###############################################################################

###### Auxiliar Functions and Variables #########

source ../functions.sh

############# STEP 1 ##############

pushd ../../tutorials

logEcho "[Korali] Beginning tutorial tests..."

for dir in ./a*/
do
  logEcho "-------------------------------------"
  logEcho " Entering Folder: $dir"
  pushd $dir >> $logFile 2>&1
  timerStart

  log "[Korali] Removing any old result files..."
  rm -rf *_result* >> $logFile 2>&1
  check_result

  for file in run-*.{py,sh}
  do
    # In case there are no files matching the pattern 'run-*.py', break
    if [ ! -f "$file" ]; then
      continue
    fi

    logEcho "  + Running File: $file"
    if [ ${file: -3} == ".py" ]; then
      python3 $file >> $logFile 2>&1
    fi
    if [ ${file: -3} == ".sh" ]; then
      sh $file >> $logFile 2>&1
    fi
    check_result
  done

  timerEnd
  popd >> $logFile 2>&1
  logEcho "-------------------------------------"
done

popd
