import symath
from symath.graph.algorithms import *
import symath.graph.generation as graphgen

import unittest

class TestDirectedGraph(unittest.TestCase):

  def setUp(self):
    self.x, self.y, self.z, self.w, self.e1, self.e2 = symath.symbols('x y z w e1 e2')
    self.g = symath.graph.directed.DirectedGraph()
    self.g.connect(self.x, self.y, self.e1)
    self.g.connect(self.y, self.z, self.e2)
    self.g.connect(self.x, self.y, self.e2)
    self.g.connect(self.z, self.w)
    self.g.connect(self.x, self.w)

  def test_edges(self):
    self.assertEqual(len(self.g.nodes[self.x].outgoing), 2)

  def test_union(self):
    og = symath.graph.directed.DirectedGraph()
    og.connect(self.x, symath.symbols('ognode'))
    og.union(self.g)
    self.assertTrue(og.connectedQ(self.x, self.y))

  def test_pathq(self):
    self.assertTrue(pathQ(self.g, self.x, self.z))

  def test_adj_matrix(self):
    mp,m = self.g.adjacency_matrix()
    self.assertEqual(m.shape[0], 4)
    self.assertEqual(m[mp[self.x],mp[self.y]], 1)
    self.assertEqual(m[mp[self.x],mp[self.x]], 0)

  def test_random_generation(self):
    randg = graphgen.random_graph(100, 0.05)

  def test_edgevalue_disconnect(self):
    g = symath.graph.directed.DirectedGraph()
    g.connect(self.x, self.y, self.e1)
    g.connect(self.x, self.y, self.e2)
    g.disconnect(self.x, self.y)
    self.assertFalse(g.connectedQ(self.x, self.y))

    g.connect(self.x, self.y, self.e1)
    g.connect(self.x, self.y, self.e2)
    g.disconnect(self.x, self.y, self.e1)
    self.assertTrue(g.connectedQ(self.x, self.y))
    g.disconnect(self.x, self.y, self.e2)
    self.assertFalse(g.connectedQ(self.x, self.y))
