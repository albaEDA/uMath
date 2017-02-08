#!/usr/bin/env python

import symath
import symath.solvers as solvers
import unittest

# only test if z3 is available
cls = unittest.TestCase if hasattr(solvers, 'z3') else object

class TestZ3(cls):

  def setUp(self):
    self.x, self.y = symath.symbols('x y')

  def test_basic_solver(self):
    cs = solvers.z3.ConstraintSet()
    cs.add(symath.stdops.Equal(self.x ** 2, 4))
    rv = cs.solve()
    self.assertNotEqual(rv, None)
    self.assertEqual(rv.x, 2)

  def test_more_complicated_solver(self):
    x,y = symath.symbols('x y')
    cs = solvers.z3.ConstraintSet()
    cs.add(x < 0)
    cs.add(x ** 3 < y ** 2)
    cs.add(y ** 2 < 9)
    cs.add(y > 0)
    cs.add(x < y)
    r = cs.solve()
    self.assertNotEqual(r, None)

if __name__ == '__main__':
  unittest.main()
