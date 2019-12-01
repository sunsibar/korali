import sys
import os
import json
from buildAux import *

def buildProblems(koraliDir):
 # Processing Problems
 problemsDir = koraliDir + '/source/problem'
 
 # Creating directory
 outputDir = koraliDir + '/docs/docs/manual/problem/'
 if (not os.path.isdir(outputDir)): os.makedirs(outputDir)
 
 # Creating problem list string
 problemListString = ''
 
 # Detecting Problems
 problemPaths  = os.listdir(problemsDir)
 for problemPath in problemPaths:
  problemPath =  problemsDir + '/' + problemPath
  if (os.path.isdir(problemPath)):
   problemName = problemPath.replace(problemsDir + '/', '')
  
   # Loading JSON Configuration
   problemJsonFile = problemPath + '/' + problemName + '.json'
   if (not os.path.isfile(problemJsonFile)): continue 
   with open(problemJsonFile, 'r') as file: problemJsonString = file.read()
   problemConfig = json.loads(problemJsonString)
   
   ####### Producing problem page
 
   problemDocFile = problemPath + '/' + problemName + '.md'
   with open(problemDocFile, 'r') as file: problemDocStringFile = file.read()
   
   problemDocString = '# ' + problemConfig["Name"] + '\n\n'
   problemDocString += '### Compatible Problems: \n'
  # for v in problemConfig["Compatible Problems"]:
  #  problemDocString += '+ ' + v + '\n\n' 
   
   problemDocString += problemDocStringFile 
   
   problemSettingsString = '### Configuration Settings\n\n'
   if (not "Configuration Settings" in problemConfig): problemSettingsString += '*none*'
   else:
    for v in problemConfig["Configuration Settings"]:
     problemSettingsString += getVariableInfo(v, problemName)
   problemDocString = problemDocString.replace('### Problem Settings', problemSettingsString + '\n\n')  
     
   variableSettingsString = '### Variable-Specific Settings\n\n'
   if (not "Variables Configuration" in problemConfig): variableSettingsString += '*none*'
   else:
    for v in problemConfig["Variables Configuration"]: 
     variableSettingsString += getVariableInfo(v, problemName)
   problemDocString = problemDocString.replace('### Variable-Specific Settings', variableSettingsString + '\n\n')
     
   terminationSettingsString = '### Termination Criteria\n\n'
   if (not "Termination Criteria" in problemConfig): terminationSettingsString += '*none*'
   else:
    for v in problemConfig["Termination Criteria"]: 
     terminationSettingsString += getVariableInfo(v, problemName)
   problemDocString = problemDocString.replace('### Termination Criteria', terminationSettingsString + '\n\n')
 
   subproblemSettingsString = '### Subproblems Configuration\n\n'
   if (not "Termination Criteria" in problemConfig): subproblemSettingsString+= '*none*'
   else:
    for v in problemConfig["Subprblems Configuration"]: 
     subproblemsSettingsString += getVariableInfo(v, problemName)
     print("TEST: " + v)
   problemDocString = problemDocString.replace('### Subrpoblems Configuration', subproblemsSettingsString + '\n\n')
     
   mdFileName = koraliDir + '/docs/docs/manual/problem/' + problemName + '.md'
   print('[Korali] Creating ' + mdFileName + '...')    
   with open(mdFileName, 'w+') as file: file.write(problemDocString)

   ####### Adding model list entry
   
   problemListString += '+ [' + problemConfig["Name"] + '](problem/' + problemName + ')\n'
   
 ###### Returning problem list
 
 return problemListString

