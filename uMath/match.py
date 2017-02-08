#!/usr/bin/env python

from . import core

def extract(a,b,rv=None):
  '''
  extract values from an expression
  returns a dictionary of wild names => values where b contains the wilds
  '''
  if rv == None:
    rv = {}

  if isinstance(b, core.Wild):
    if b.name in rv and rv[b.name] != a:
      return None
    rv[b.name] = a
    return rv

  elif len(a) != len(b):
    return None

  elif len(b) > 1:
    for i in range(len(b)):
      if extract(a[i], b[i], rv) == None:
        return None
    return rv

  elif a == b:
    return a

  else:
    return None

def match(a, b, valuestore=None):
  '''
  matches against a pattern, use wilds() to generate wilds

  Example:
    a,b = wilds('a b')
    val = WildsResults()
    
    if exp.match(a(b + 4), val):
      print val.a
      print val.b
  '''

  if valuestore != None:
    valuestore.clear()

  d = extract(a,b)
  if d == None:
    return False

  if valuestore != None:
    for k in d:
      if d[k] == core.wild(k):
        continue
      valuestore[k] = d[k]

  return True
