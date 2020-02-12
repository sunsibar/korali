
#include <stdio.h>
#include <math.h>
#include <limits>
#include "load_data.hpp"
#include "string.h"

pointsInfo __p;

pointsInfoStruct& univariateData(int* argc, char** argv[])
{
 // Also contains assignment information; remove to be sure you are not using it
 FILE *problemFile;
 size_t nPoints = 0;
 size_t nDimensions = 0;

 printf("Loading data from data_single.in ... \n");
 problemFile = fopen("model/data_single.in", "r");
 fscanf(problemFile, "%lu", &nPoints);
 fscanf(problemFile, "%lu", &nDimensions);

 __p.points.resize(nPoints * nDimensions );
 __p.assignments.resize(0);

 for (size_t i = 0; i < nPoints; i++)
 {
  double val;
  for (size_t j = 0; j < nDimensions; j++){
      fscanf(problemFile, "%le ", &val); __p.points[i*nDimensions + j] = val;
  }
 }
 __p.nDimensions = nDimensions;
 __p.nPoints = nPoints;

 return __p;
}



pointsInfoStruct& multivariateData(int* argc, char** argv[])
{
 // Also contains assignment information; remove to be sure you are not using it
 FILE *problemFile;

 size_t nPoints = 0;
 size_t nDimensions = 0;

 printf("Loading data from data_multiple.in ... \n");
 problemFile = fopen("model/data_multiple.in", "r");
 fscanf(problemFile, "%lu", &nPoints);
 fscanf(problemFile, "%lu", &nDimensions);

 __p.points.resize(nPoints * nDimensions );
 __p.assignments.resize(nPoints);

 for (size_t i = 0; i < nPoints; i++)
 {
  double val;
  for (size_t j = 0; j < nDimensions; j++){
      fscanf(problemFile, "%le ", &val); __p.points[i*nDimensions + j] = val;
  }
  fscanf(problemFile, "%lu ", &val); __p.assignments[i] = val;
 }
 __p.nDimensions = nDimensions;
 __p.nPoints = nPoints;

 return __p;
}

