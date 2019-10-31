#!/usr/bin/env python

# Single function evaluation
def model(p):
  x = p["Parameters"][0]
  modifier = p["Job Id"] + 5 
  for x in range (100000):
   p["Evaluation"] = -0.5*x*x*modifier

# Function and Gradient function evaluation
def model_with_gradient(p):
  X = p["Parameters"];
  gradient = [];
  evaluation = 0
  for x in X:
    evaluation  += -0.5*x*x
    gradient.append( -x )

  p["Evaluation"] = evaluation
  p["Gradient"]   = gradient;
