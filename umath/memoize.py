#!/usr/bin/env python
#import pprint

class Memoize(object):
    ''' 
        memoize a function:
        Memoize(myfunc)

        used to cache results from functions so that they are not called multiple times
    '''
    def __init__(self, f, results=None):
        self.f = f
        self.results = results if results != None else {}
        self.noargs = object()

    def clear_results(self):
      self.noargs = object()
      self.results = {}

    def __exit__(self,type,value,traceback):
        pass

    def __enter__(self):
        return self

    def __call__(self, *args, **kargs):
        #import bnrev.symbolic as sym

        # get our kargs into a standard format
        
        kkeys = list(kargs.keys())
       # print("1: ",kkeys)
        kkeys.sort()
        #print("2: ",kkeys)
        kkeys = tuple(kkeys)
        #print("3: ",kkeys)
        kvals = tuple([kargs[k] for k in kkeys])

        # finally make our key
        key = (tuple(args), kkeys, kvals)
        #print(key)

        #for i in args:
        #  if isinstance(i, sym.Number) and i.n == -0x88:
        #    print key

        # magic value for functions that have no arguments.. this requires slightly different logic
        skipargs = False
        if len(args) == 0 and len(kargs) == 0:
            key = self.noargs
            skipargs = True
        
        if key == type(0.1):
          pass
        else:
          # if we haven't called the function with the arguments yet, do it
          if key not in self.results:
              #print key
              tmp = self.f(*args, **kargs) if not skipargs else self.f()

              # generators only work once, so we have to expand them to lists in order for
              # memoization to work
              if type(tmp) is type(x for x in (0,)):
                  tmp = list(tmp)

              self.results[key] = tmp
          else:
              #print 'memoized!'
              pass

        # return the cached results
        return self.results[key]

    @staticmethod
    def MemoizeObject(obj, *memmethods):
        '''Memoize methods for object, if no method names are passed, then memoize *all* methods.  This is usually overkill'''
        memall = len(memmethods) == 0
        instancemethod = type(Memoize.__init__)
        for membername in dir(obj):
            value = getattr(obj, membername)
            if (memall or membername in memmethods) and type(value) is instancemethod and not isinstance(value, Memoize):
                setattr(obj, membername, Memoize(value))
                #print 'memoizing %s!' % (membername)
        return obj

    @staticmethod
    def DememoizeObject(obj, *memmethods):
        '''removes memoization of methods from object'''
        memall = len(memmethods) == 0
        for membername in dir(obj):
            value = getattr(obj,membername)
            if (memall or membername in memmethods) and isinstance(value, Memoize):
                #print 'memoizing %s!' % (membername)
                setattr(obj, membername, value.f)
        return obj

    @staticmethod
    def MemoizeMembers(obj, *items):
        import types
        memall = len(items) == 0
        for membername in dir(obj):
            value = getattr(obj, membername)
            if ((memall and '__' not in membername)  or membername in items) and not isinstance(value, Memoize) and \
            isinstance(value ,(types.FunctionType,types.BuiltinFunctionType)):
                #print 'memoizing %s' % (membername)
                setattr(obj, membername, Memoize(value))
                
        return obj

    @staticmethod
    def DememoizeMembers(obj, *items):
        memall = len(items) == 0
        for membername in dir(obj):
            value = getattr(obj, membername)
            if (memall or membername in items) and isinstance(value, Memoize):
                #print 'dememoizing %s' % (membername)
                setattr(obj, membername, value.f)
        return obj

class m(object):
    ''' 
    special class used for with statements to implement (dynamicly) scoped memoization 
    it works for modules, classes, and objects as the first argument

    the rest of the arguments are the members to memoize, in the case that there are no 
    other arguments, all members that qualify will be memoized

    example:
    with memoize.m(somemodule, 'somefunc', 'someotherfunc'):
        dostuff()
    '''
    def __init__(self, obj, *args):
        self.obj = obj
        self.args = args
        self.isobj = False

    def __enter__(self):
        import types
        if not isinstance(self.obj, (type, types.ModuleType)):
            self.isobj = True
            self.obj = Memoize.MemoizeObject(self.obj, *self.args)
        else:
            self.obj = Memoize.MemoizeMembers(self.obj, *self.args)

    def __exit__(self,type,value,traceback):
        if self.isobj:
            Memoize.DememoizeObject(self.obj, *self.args)
        else:
            Memoize.DememoizeMembers(self.obj, *self.args)

if __name__ == '__main__':
    from .memoize import Memoize

    @Memoize
    def identity(a):
        return a

    print(identity(5) == 5)
    print(5 in list(identity.results.values()))
    print(identity(7) == 7)
    print(7 in list(identity.results.values()))

    identity.f(10)
    print(10 not in list(identity.results.values()))

    import testm
    for j in range(2):
        with m(testm):
            for i in range(1,10):
                testm.printsomething(100)
                testm.printsomething(i)
