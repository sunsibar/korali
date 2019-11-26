#!/bin/bash

source functions.sh

#Running tutorials

for dir in */
do
  echo "[Korali] Running test in folder ${dir} ..."
  pushd $dir
  ./run_test.sh
  if [ ! $? -eq 0 ]; then exit -1; fi
  popd
done

echo "[Korali] All tests ran correctly."
