def add(a, b):
    "Same as a + b."
    return a + b

def mul(a, b):
    return a * b
    
def pow(a, b):
    return a ** b
    
def sub(a, b):
    return a - b
	
__add__ = add
__mul__ = mul
__pow__ = pow
__sub__ = sub