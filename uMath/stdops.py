from . import simplify
from .core import symbolic as _sym

# comparison operations
Equal = _sym('==')
LessThan = _sym('<')
GreaterThan = _sym('>')
LessThanEq = _sym('<=')
GreaterThanEq = _sym('>=')

Add = _sym('+', identity=_sym(0), numeric='__add__', commutative=True, associative=True)
Sub = _sym('-', ridentity=_sym(0), numeric='__sub__')
Div = _sym('/', ridentity=_sym(1), numeric='__div__')
Mul = _sym('*', zero=_sym(0), identity=_sym(1), numeric='__mul__', commutative=True, associative=True)
Pow = _sym('**', ridentity=_sym(1), numeric='__pow__')
RShift = _sym('>>', cast=int, ridentity=_sym(0), numeric='__rshift__')
LShift = _sym('<<', cast=int, ridentity=_sym(0), numeric='__lshift__')
BitAnd = _sym('&', cast=int, zero=_sym(0), numeric='__and__', commutative=True, associative=True)
BitOr = _sym('|', cast=int, identity=_sym(0), numeric='__or__', commutative=True, associative=True)
BitXor = _sym('^', cast=int, identity=_sym(0), numeric='__xor__', commutative=True, associative=False)
#LogicalAnd = _sym('&&', cast=bool, zero=_sym(False), numeric='__and__', commutative=True, associative=True)
#LogicalOr = _sym('||', cast=bool, zero=_sym(True), numeric='__or__', commutative=True, associative=True)
#LogicalXor = _sym('^^', cast=bool, numeric='__xor__', commutative=True, associative=False)

# Sum(variable, min, max, expression)
Sum = _sym('Sum')
