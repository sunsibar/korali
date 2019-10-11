###### Auxiliar Functions and Variables #########

curdir=$PWD
logFile=$curdir/test.log
echo "" > $logFile

# Check valid return code of shell comand
function check_result()
{
 if [ ! $? -eq 0 ]
 then
  echo "[Korali] Error running test: (check log: $logFile)"
  tail $logFile
  exit -1
 fi 
}

tstart=0

function timerStart()
{
 tstart=$(date +%s%N)
}

function timerEnd()
{
 if [ $tstart -gt 0 ]
 then
    now=$(date +%s%N)
    duration=$(((now - tstart)/1000000))
    logEcho " Duration $duration milliseconds."
    tstart=0
 else
    logEcho " Timer not started (no measurements)."
 fi
}

# Logging and printing function.
function logEcho ()
{
 echo "$1"
 echo "$1" >> $logFile
}

# Logging function.
function log ()
{
 echo "$1" >> $logFile
}




