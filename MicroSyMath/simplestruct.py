#from pprint import PrettyPrinter

class SimpleStruct(object):

  def __init__(self, **kargs):

    for k in kargs:
      setattr(self,k,kargs[k])

  def __to_dict__(self):
    rv = {}
    mems = [k for k in dir(self) if k[:2] != '__']
    for k in mems:
      r = getattr(self, k)
      if type(r) == type(self):
        r = r.__to_dict__()
      rv[k] = r

    return rv

  def __str__(self):
    pp = PrettyPrinter()
    return pp.pformat(self.__to_dict__())

  def __repr__(self):
    return str(self)
