#!/usr/bin/env python

import umath
from . import memoize

@memoize.Memoize
def is_factor(x, y):
  '''
  return True if x is a factor of y
  will return True for any 2 numbers because we use floating point
  '''
  a, b = umath.wilds('a b')
  val = umath.WildResults()

  if x == y:
    return True

  elif isinstance(x, umath.Number) and isinstance(y, umath.Number):
    return True

  elif y.match(a * b, val):
    return is_factor(x, val.a) or is_factor(x, val.b)

  elif y.match(a + b, val):
    return is_factor(x, val.a) and is_factor(x, val.b)

  elif y.match(a - b, val):
    return is_factor(x, val.a) and is_factor(x, val.b)

  else:
    return False

@memoize.Memoize
def get_coefficient(y, x):
  '''
  divides y by x and returns
  - only works if x is a factor of y
  '''
  assert is_factor(x, y)
  assert x != 1

  a,b,c = umath.wilds('a b c')
  val = umath.WildResults()

  if y == x:
    return umath.symbolic(1)

  if y.match(a * b, val):
    if is_factor(x, val.a):
      return get_coefficient(val.a, x) * val.b
    else:
      return get_coefficient(val.b, x) * val.a

  elif y.match(c(a, b), val):
    return val.c(get_coefficient(val.a, x), get_coefficient(val.b, x))
