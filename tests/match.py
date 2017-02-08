import unittest
import symath

class TestCoreClasses(unittest.TestCase):

  def setUp(self):
    self.w, self.v = symath.wilds('w v')
    self.x, self.y = symath.symbols('x y')
    self.head = symath.symbols('head')

  def test_match(self):
    m = symath.WildResults()
    self.assertTrue(self.head(self.x, 3).match(self.w(self.x, self.v), m))
    self.assertEqual(m['w'], self.head)
    self.assertEqual(m['v'], 3)
    self.assertEqual(m.v, 3)

    self.assertFalse(self.head(self.x, self.y).match(self.head(self.v, self.v)))

    self.assertTrue(self.head(self.x, self.x).match(self.head(self.v, self.v), m))
    self.assertEqual(m['v'], self.x)

  def test_none_wild_match(self):
    m = {'should be removed': True}
    self.assertTrue(self.head(self.x).match(symath.wild()(self.x), m))

  def test_replace_all(self):
    a,b,c = symath.wilds('a b c')
    x,y,z = symath.wilds('x y z')

    term = (x & (y | z))
    self.assertEqual(y | z, symath.replace(term, { a & b: b }))

if __name__ == '__main__':
  unittest.main()
