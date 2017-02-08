#!/usr/bin/env python

import unittest
import symath

class TestAlgorithms(unittest.TestCase):

  def setUp(self):
    pass

  def test_simplestruct(self):
    st = symath.SimpleStruct(test1='one')
    st.test2 = 2

    self.assertEqual(st.test1, 'one')
    self.assertEqual(st.test2, 2)

if __name__ == '__main__':
  unittest.main()
