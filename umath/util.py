import umath.core
#import pprint

DEBUG = False

def pretty(exp):
  p = pprint.PrettyPrinter(indent=2)
  p.pprint(exp)

def debug(exp):
  if DEBUG:
    if type(exp) == type('str'):
      print(exp)
    else:
      pretty(exp)

def dict_reverse(d):
  rv = {}
  for k in d:
    rv[d[k]] = k
  return rv

def has_wilds(exp):
  rv = {}
  rv['val'] = False

  def _(exp):
    if isinstance(exp, symath.core.Wild):
      rv['val'] = True
    return exp

  exp.walk(_)
  return rv['val']

