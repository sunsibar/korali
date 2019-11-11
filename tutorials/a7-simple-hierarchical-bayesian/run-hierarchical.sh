#!/bin/bash

# this will exit the script if a command fails
set -e

cd phase0
python3 phase0.py
cd ../

cd phase1
sh generateData.sh
cd ../

cd phase2
python3 phase2.py
cd ../

cd phase3a
python3 phase3a.py
cd ../

cd phase3b
python3 phase3b.py
cd ../
