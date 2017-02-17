from .core import WildResults, wilds, symbolic, symbols, replace, Symbol
from .functions import *
from .stdops import *
from .memoize import Memoize

_known_functions = (Log, Add, Sub, Mul, Div, Pow, Sin, Cos, Tan, Exp, Sum, Sec)

class DifferentiationError(Exception):
  pass

def _diff_known_function(expression, variable):

  vals = WildResults()
  g,h = wilds('g h')

  if expression[0] not in _known_functions:
    raise DifferentiationError("d/d%s  %s" % (variable,expression))
    
  #constants eg (x*3+x*2) = 5.0
  if expression.match(g + h, vals):
    return diff(vals.g, variable) + diff(vals.h, variable)
  
  #constants eg (x*3-x*2) = 1.0
  elif expression.match(g - h, vals):
    return diff(vals.g, variable) - diff(vals.h, variable)

  #power rule (x**2) == 2.0 * x
  elif expression.match(variable ** g, vals):
    return vals.g * (variable ** (vals.g - 1))
  
  #product rule (x+3)*(x+2) = (x + (5.0 + x)) DONE: Simplify brackets
  elif expression.match(g * h, vals):
    return vals.g * diff(vals.h, variable) + vals.h * diff(vals.g, variable)
  
  #quotient rule (x/y) = (1/y)
  elif expression.match(g / h, vals):
    return (diff(vals.g, variable) * vals.h - vals.g * diff(vals.h, variable)) / (vals.h ** 2)
  
  #TODO: Impliment full chain rule
  
  #Exponent rule
  elif expression.match(Exp(variable)):
    return expression
  
  #Trig sine rule
  elif expression.match(Sin(variable)):
    return Cos(variable)
  
  #Trig cosine rule
  elif expression.match(Cos(variable)):
    return Sin(variable) * -1
   
  #Trig tangent rule
  elif expression.match(Tan(variable)):
    return Sec(variable) ** 2
  
  #Rules for sums
  elif expression.match(Sum(g, h), vals):
    if(variable(vals.g) in vals.h):
      return Sum(vals.g, diff(vals.h, variable(vals.g)))
    else:
      return Sum(vals.g, diff(vals.h, variable))
  
  #DONE: Hacked together an __rmul__ for logs
  elif expression.match(Log(variable), vals):
    return 1 / variable

  raise DifferentiationError("d/d%s  %s" % (variable,expression))

def decompose(expression, variable):
  result = []
  
  if expression.has(variable):
    return True
  
  #if variable in expression:
  #  result.append(variable)
  #  for atoms in expression.args:
  #    tempexp = atoms
  #    while len(tempexp.args) > 2:
        
      
  #    if str(atoms.name) in str(_known_functions):
        
  
def diff(expression, variable):

  vals = WildResults()
  f,a,b = wilds('f a b')

  expression = symbolic(expression)

  if variable not in expression:
    return symbolic(0)

  elif expression.match(variable):
    return symbolic(1)

  elif expression.match(f(a,b), vals) and vals.f in _known_functions:
    return _diff_known_function(expression, variable)

  elif expression.match(f(a), vals) and vals.f in _known_functions:
    return _diff_known_function(vals.f(vals.a), vals.a) * diff(vals.a, variable)

  raise DifferentiationError("d/d%s  %s" % (variable,expression))
