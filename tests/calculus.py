#!/usr/bin/env python

import unittest
import umath
import umath.util as util
from umath.calculus import *

class TestCalculus(unittest.TestCase):

  def setUp(self):
    util.DEBUG = True
    pass

  def test_diff_power_rule(self):
    x = symath.symbols('x')
    dx = diff(x ** 2, x)
    self.assertEqual(dx.simplify(), (2 * x).simplify())

  def test_diff_non_var(self):
    x,y = symath.symbols('x y')
    dx = diff(y, x)
    self.assertEqual(dx, 0)

  def test_diff_product(self):
    x,y = symath.symbols('x y')
    
    self.assertEqual(diff(x * y, x).simplify(), y)
    self.assertEqual(diff(y * x ** 3, x).simplify(), (3 * y * x ** 2).simplify())

  def test_diff_chain_rule(self):
    Exp,x,y = symath.symbols('Exp x y')
    self.assertEqual(diff(Exp(2 * x), x).simplify(), (2 * Exp(2 * x)).simplify())

  def test_diff_fail_on_unknown_function(self):
    with self.assertRaises(DifferentiationError):
      Unknown,x = symath.symbols('Unknown x')
      diff(Unknown(x), x)

  def test_diff_quotient_rule(self):
    x = symath.symbols('x')
    print(diff(1 / x, x))
    self.assertEqual(diff(1 / x, x).simplify(), (-1 / x**2).simplify())

  def test_summation(self):
    x,n,y = symath.symbols('x n y')
    expression = symath.functions.Sum(n, x(n) ** y)
    expression_dx = diff(expression, x).simplify()

    valid = (symath.functions.Sum(n, y * (x(n) ** (y - 1)))).simplify()
    self.assertEqual(valid, expression_dx)

  def test_log(self):
    x,y = symath.symbols('x y')
    expression = symath.functions.Log(x * y)
    dx = diff(expression, x).simplify()

    self.assertEqual(dx, (y / (x * y)).simplify())

if __name__ == '__main__':
  unittest.main()
