#!/usr/bin/env python3
import os, glob

def find_last_generation( dir ):
  lst = []
  for file in glob.glob(dir+"/gen*.json"):
    lst.append(file)

  return sorted(lst)[-1]
