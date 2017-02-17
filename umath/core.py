from . import operator
from . import util
import random

from .memoize import Memoize

def collect(exp, fn):
  rv = set()
  
  def _collect(exp):
    if fn(exp):
      rv.add(exp)
    return exp

  exp.walk(_collect)
  return rv

def _replace_one(expr, match, repl):
  vals = WildResults()
  if expr.match(match, vals):
    expr = repl.substitute({wilds(w): vals[w] for w in vals})

  if len(expr) > 1:
    return expr[0](*[_replace_one(x, match, repl) for x in expr.args])
  else:
    return expr

def replace(expr, d, repeat=True):
  while True:
    old_expr = expr
    for k in d:
      expr = _replace_one(expr, k, d[k])

    if old_expr == expr or not repeat:
      return expr


class _Symbolic(object):

  def match(self, other, valuestore=None):
    '''
    matches against a pattern, use wilds() to generate wilds
  
    Example:
      a,b = wilds('a b')
      val = WildsResults()
      
      if exp.match(a(b + 4), val):
        print val.a
        print val.b
    '''
    from . import match
    return match.match(self, other, valuestore)

  def __new__(typ):
    return object.__new__(typ)
    
  def __hash__(self):
    return hash(self.name)

  def simplify(self):
    from . import simplify
    return simplify.simplify(self)

  def walk(self, *fns):
    if len(fns) > 1:
      def _(exp):
        for f in fns:
          exp = f(exp)
        return exp
      return self.walk(_)

    exp = self
    fn = fns[0]
    if len(exp) == 1:
      oldexp = exp
      exp = fn(exp)
      while exp != oldexp:
        oldexp = exp
        exp = fn(exp)

    else:
      args = list([x.walk(fn) for x in exp.args])
      oldexp = self
      exp = fn(fn(exp[0])(*args))
     
    return exp

  def _dump(self):
    return {
        'name': self.name,
        'id': id(self)
        }

  def __contains__(self, exp):
    rv = {}
    rv['val'] = False

    def _(_exp):
      if _exp.match(exp):
        rv['val'] = True
      return _exp
    self.walk(_)

    return rv['val']

  def substitute(self, subs):
    '''
    takes a dictionary of substitutions
    returns itself with substitutions made
    '''
    if self in subs:
      self = subs[self]

    return self

  def compile(self, *arguments):
    '''compiles a symbolic expression with arguments to a python function'''

    def _compiled_func(*args):
      assert len(args) == len(arguments)
      argdic = {}
      for i in range(len(args)):
        argdic[arguments[i]] = args[i]
      rv = self.substitute(argdic).simplify()
      return desymbolic(rv)

    return _compiled_func

  def __eq__(self, other):
    #return type(self) == type(other) and self.name == other.name
    return id(self) == id(other)

  def __ne__(self, other):
    return not self.__eq__(other)

  def __getitem__(self, num):
    if num == 0:
      return self

    raise BaseException("Invalid index")

  def __len__(self):
    return 1

  # comparison operations notice we don't override __eq__
  def __gt__(self, obj):
    return Fn.GreaterThan(self, obj)

  def __ge__(self, obj):
    return Fn.GreaterThanEq(self, obj)

  def __lt__(self, obj):
    return Fn.LessThan(self, obj)

  def __le__(self, obj):
    return Fn.LessThanEq(self, obj)

  # arithmetic overrides
  def __mul__(self, other):
    return Fn.Mul(self, other)

  def __pow__(self, other):
    return Fn.Pow(self, other)

  def __rpow__(self, other):
    return Fn.Pow(other, self)

  def __truediv__(self, other):
    return Fn.Div(self, other)

  def __add__(self, other):
    return Fn.Add(self, other)

  def __sub__(self, other):
    return Fn.Sub(self, other)

  def __or__(self, other):
    return Fn.BitOr(self, other)

  def __and__(self, other):
    return Fn.BitAnd(self, other)

  def __xor__(self, other):
    return Fn.BitXor(self, other)

  def __rmul__(self, other):
    return Fn.Mul(other, self)

  def __rtruediv__(self, other):
    return Fn.Div(other, self)

  def __radd__(self, other):
    return Fn.Add(other, self)

  def __rsub__(self, other):
    return Fn.Sub(other, self)

  def __ror__(self, other):
    return Fn.BitOr(other, self)

  def __rand__(self, other):
    return Fn.BitAnd(other, self)

  def __rxor__(self, other):
    return Fn.BitXor(other, self)

  def __rshift__(self, other):
    return Fn.RShift(self, other)

  def __lshift__(self, other):
    return Fn.LShift(self, other)

  def __rrshift__(self, other):
    return Fn.RShift(other, self)

  def __rlshift__(self, other):
    return Fn.LShift(other, self)

  def __neg__(self):
    return self * -1

class _KnownValue(_Symbolic):
  def value(self):
    raise BaseException('not implemented')

class Boolean(_KnownValue):

  @Memoize
  def __new__(typ, b):
    self = _KnownValue.__new__(typ)
    self.name = str(b)
    self.boolean = b
    return self

  def value(self):
    return bool(self.boolean)

  def __str__(self):
    return str(self.boolean)

  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    if isinstance(other, Boolean):
      return bool(self.boolean) == bool(other.boolean)
    elif isinstance(other, _Symbolic):
      return other.__eq__(self)
    else:
      return bool(self.boolean) == other

class Number(_KnownValue):

  FFORMAT = str

  @Memoize
  def __new__(typ, n):
    n = float(n)
    self = _KnownValue.__new__(typ)
    self.name = str(n)
    self.n = n
    return self

  def __hash__(self):
    return hash(self.name)
	
  @property
  def is_integer(self):
    return self.n.is_integer()

  def value(self):
    return self.n

  def __eq__(self, other):
    if isinstance(other, Number):
      return self.n == other.n
    elif isinstance(other, _Symbolic):
      return other.__eq__(self)
    else:
      return self.n == other

  def __ne__(self, other):
    if isinstance(other, _Symbolic):
      return super(Number, self).__ne__(other)
    else:
      return self.n != other

  def __str__(self):
      return Number.FFORMAT(self.n)

  def __repr__(self):
    return str(self)


class WildResults(object):

  def __init__(self):
    self._hash = {}

  def clear(self):
    self._hash.clear()

  def __setitem__(self, idx, val):
    self._hash.__setitem__(idx, val)

  def __contains__(self, idx):
    return idx in self._hash

  def __getitem__(self, idx):
    return self._hash[idx]

  def __getattr__(self, idx):
    return self[idx]

  def __iter__(self):
    return self._hash.__iter__()

  def __str__(self):
    return str(self._hash)

  def __repr__(self):
    return str(self)

  def __len__(self):
    return len(self._hash)

class Wild(_Symbolic):
  '''
  wilds will be equal to anything, and are used for pattern matching
  '''

  @Memoize
  def __new__(typ, name, **kargs):
    self = _Symbolic.__new__(typ)
    self.name = name
    self.kargs = kargs
    return self

  def __str__(self):
    return self.name

  def __repr__(self):
    return str(self)

  def __call__(self, *args):
    return Fn(self, *args)

  def _dump(self):
    return {
        'type': type(self),
        'name': self.name,
        'kargs': self.kargs,
        'id': id(self)
        }

class Symbol(_Symbolic):
  '''
  symbols with the same name and kargs will be equal
  (and in fact are guaranteed to be the same instance)
  '''

  @Memoize
  def __new__(typ, name, **kargs):
    self = Wild.__new__(typ, name)
    self.name = name
    self.kargs = kargs
    self.is_integer = False # set to true to force domain to integers
    self.is_bitvector = 0 # set to the size of the bitvector if it is a bitvector
    self.is_bool = False # set to true if the symbol represents a boolean value
    return self

  def __str__(self):
    return self.name

  def __repr__(self):
    return str(self)

  def __call__(self, *args):
    return Fn(self, *args)

  def _dump(self):
    return {
        'type': type(self),
        'name': self.name,
        'kargs': self.kargs,
        'id': id(self)
        }

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
        
        
class Fn(_Symbolic):

  @Memoize
  def __new__(typ, fn, *args):
    '''
    arguments: Function, *arguments, **kargs
    valid keyword args:
      commutative (default False) - order of operands is unimportant
    '''

    if None in args:
      raise BaseException('NONE IN ARGS %s %s' % (fn, args))

    if not isinstance(fn, _Symbolic):
      fn = symbolic(fn)
      return Fn.__new__(typ, fn, *args)

    for i in args:
      if not isinstance(i, _Symbolic):
        args = list(map(symbolic, args))
        return Fn.__new__(typ, fn, *args)

    self = _Symbolic.__new__(typ)
    kargs = fn.kargs
    self.kargs = fn.kargs

    self.name = fn.name
    self.fn = fn
    self.args = args

    #import simplify
    #rv = simplify.simplify(self)

    return self

  def _dump(self):
    return {
        'id': id(self),
        'name': self.name,
        'fn': self.fn._dump(),
        'kargs': self.kargs,
        'args': list([x._dump() for x in self.args]),
        'orig kargs': self.orig_kargs,
        'orig args': list([x._dump() for x in self.orig_args])
        }

  def __call__(self, *args):
    return Fn(self, *args)

  def has(self,x):
    return self.__contains__(x)
    
  def is_Symbols(self):
    if isinstance(self, _Symbolic):
      return True
    else:
      return False
    
  
  def substitute(self, subs):
    args = list([x.substitute(subs) for x in self.args])
    newfn = self.fn.substitute(subs)
    self = Fn(newfn, *args)

    if self in subs:
      self = subs[self]

    return self

  def recursive_substitute(self, subs):
    y = self
    while True:
      x = y.substitute(subs)
      if x == y:
        return x
      y = x

  def __getitem__(self, n):
    if n == 0:
      return self.fn

    return self.args[n - 1]

  def __len__(self):
    return len(self.args) + 1

  def _get_assoc_arguments(self):
    from . import simplify
    rv = []

    args = list(self.args)
    def _(a, b):
      if (isinstance(a, Fn) and a.fn == self.fn) and not (isinstance(b, Fn) and b.fn == self.fn):
        return -1

      if (isinstance(b, Fn) and b.fn == self.fn) and not (isinstance(a, Fn) and a.fn == self.fn):
        return 1

      return simplify._order(a, b)

    args.sort(key=cmp_to_key(_))

    for i in args:
      if isinstance(i, Fn) and i.fn == self.fn:
        for j in i._get_assoc_arguments():
          rv.append(j)
      else:
        rv.append(i)

    return rv

  @staticmethod
  def LessThan(lhs, rhs):
    return Fn(stdops.LessThan, lhs, rhs)

  @staticmethod
  def GreaterThan(lhs, rhs):
    return Fn(stdops.GreaterThan, lhs, rhs)

  @staticmethod
  def LessThanEq(lhs, rhs):
    return Fn(stdops.LessThanEq, lhs, rhs)

  @staticmethod
  def GreaterThanEq(lhs, rhs):
    return Fn(stdops.GreaterThanEq, lhs, rhs)

  @staticmethod
  def Add(lhs, rhs):
    return Fn(stdops.Add, lhs, rhs)

  @staticmethod
  def Sub(lhs, rhs):
    return Fn(stdops.Sub, lhs, rhs)

  @staticmethod
  def Div(lhs, rhs):
    return Fn(stdops.Div, lhs, rhs)

  @staticmethod
  def Mul(lhs, rhs):
    return Fn(stdops.Mul, lhs, rhs)

  @staticmethod
  def Pow(lhs, rhs):
    return Fn(stdops.Pow, lhs, rhs)

  @staticmethod
  def RShift(lhs, rhs):
    return Fn(stdops.RShift, lhs, rhs)

  @staticmethod
  def LShift(lhs, rhs):
    return Fn(stdops.LShift, lhs, rhs)

  @staticmethod
  def BitAnd(lhs, rhs):
    return Fn(stdops.BitAnd, lhs, rhs)

  @staticmethod
  def BitOr(lhs, rhs):
    return Fn(stdops.BitOr, lhs, rhs)

  @staticmethod
  def BitXor(lhs, rhs):
    return Fn(stdops.BitXor, lhs, rhs)

  def __str__(self):
    if isinstance(self.fn, Symbol) and not self.name[0].isalpha() and len(self.args) == 2:
      return '(%s %s %s)' % (self.args[0], self.name, self.args[1])

    return '%s(%s)' % (self.fn, ','.join(map(str, self.args)))

  def __repr__(self):
    return str(self)

def symbols(symstr=None, **kargs):
  '''
  takes a string of symbols seperated by whitespace
  returns a tuple of symbols
  '''
  if symstr == None:
    syms = [''.join(random.choice(string.ascii_lowercase) for x in range(12))]
  else:
    syms = symstr.split(' ')

  if len(syms) == 1:
    return Symbol(syms[0], **kargs)

  rv = []
  for i in syms:
    rv.append(Symbol(i, **kargs))

  return tuple(rv)

def wilds(symstr, **kargs):
  '''
  wilds should match anything
  '''
  syms = symstr.split(' ')
  if len(syms) == 1:
    return Wild(syms[0], **kargs)

  rv = []
  for i in syms:
    rv.append(Wild(i, **kargs))

  return tuple(rv)

def wild(name=None, **kargs):
  if name == None:
    name = ''.join(random.choice(['a','b','c','d','e']) for x in range(12))
  return Wild(name, **kargs)

def symbolic(obj, **kargs): 
  '''
  makes the symbolic version of an object
  '''
  if type(obj) in [type(0), type(0.0), type(0)]:
    return Number(obj, **kargs)
  elif type(obj) == type('str'):
    return Symbol(obj, **kargs)
  elif type(obj) == type(True):
    return Boolean(obj, **kargs)
  elif isinstance(obj, _Symbolic):
    return obj
  else:
    msg = "Unknown type (%s) %s passed to symbolic" % (type(obj), obj)
    raise BaseException(msg)

def desymbolic(s):
  '''
  returns a numeric version of s
  '''

  if type(s) in (int,int,float):
    return s

  s = s.simplify()
  if not isinstance(s, Number):
    raise BaseException("Only numbers can be passed to desymbolic")

  return s.value()

from . import stdops#

Log,Exp,Sin,Cos,Tan,ArcCos,ArcSin,ArcTan,Sec,Sum = symbols('Log Exp Sin Cos Tan ArcCos ArcSin ArcTan Sec Sum')
_known_functions = (Log,Exp,Sin,Cos,Tan,ArcCos,ArcSin,ArcTan,Sec,Sum)