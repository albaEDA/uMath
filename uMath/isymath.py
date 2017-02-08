# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from symath import symbols, wilds, WildResults, functions, stdops
from IPython.display import Latex

_greek = symbols('theta gamma Theta Gamma alpha beta Alpha Beta Delta delta pi Pi phi Phi')

def _idisplay(exp):
    x,y,z,n = wilds('x y z n')
    ws = WildResults()
    
    if exp.match(x ** y, ws):
        return r"{%s} ^  {%s}" % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp in _greek:
        return r'\%s' % (str(exp),)
    
    elif exp.match(-1 * x, ws):
        return r'-{%s}' % (_idisplay(ws.x),)
    
    elif exp.match(x + y, ws):
        return r'{%s} + {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp.match(x - y, ws):
        return r'{%s} - {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp.match(x * y, ws):
        return r'{%s} {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp.match(x / y, ws):
        return r'\frac{%s}{%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp.match(x ^ y, ws):
        return r'{%s}  \oplus  {%s}' % (_idisplay(ws.x), _idisplay(ws.y))
    
    elif exp.match(functions.Exp(x), ws):
        return r'e^{%s}' % (_idisplay(ws.x),)
    
    elif exp.match(x(y), ws) and ws.x in [
            functions.ArcCos, functions.ArcSin,
            functions.ArcTan, functions.Cos,
            functions.Sin, functions.Tan]:
        return r'\%s{%s}' % (str(ws.x).lower(), _idisplay(ws.y))
    
    elif exp.match(stdops.Equal(x,y), ws):
        return r'%s = %s' % (_idisplay(ws.x), _idisplay(ws.y))

    elif exp.match(functions.Sum(n, x), ws):
      return r'\sum_{%s}{%s}' % (_idisplay(ws.n), _idisplay(ws.x))
    
    else:
        return str(exp)
    
def idisplay(exp):
    return Latex("$" + _idisplay(exp) + "$")

# <codecell>

a,b,c,j,theta,e,alpha = symbols('a b c j theta e alpha')
idisplay(stdops.Equal(functions.Exp(j * theta) / alpha, (functions.Cos(theta) + j * functions.Sin(theta)) / alpha))

# <codecell>


