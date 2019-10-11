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
 tstart=$SECONDS

}

function timerEnd()
{
 if [ $tstart -eq 0 ]
 then
    duration=$(( $SECONDS-tstart ))
    logEcho "Duration $duration seconds."
 else
    logEcho "Timer not started (no measurements)."
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




