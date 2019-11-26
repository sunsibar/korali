#!/bin/bash

source ../functions.sh

logEcho "[Korali] Beginning Stat Test 005"

rm -rf _korali_result* >> $logFile 2>&1

python3 -m pip install --user scipy

for file in run-*.py
do
  logEcho "-------------------------------------"
  logEcho " Running $file"
  logEcho "-------------------------------------"
  ./"$file" >> $logFile
  check_result
done

log "[Korali] Removing results..."
rm -rf _result_run-* >> $logFile 2>&1
rm -rf _korali_result* >> $logFile 2>&1
check_result
