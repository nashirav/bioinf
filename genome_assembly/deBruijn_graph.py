"""
@description: Implementation of de Bruijn graph in genome assembly
"""

import networkx as nx

class deBruijnGraph: 
  
  def __init__(self, s, k):
    self.k = k
    self.string = s

    self.G = nx.MultiGraph() #MultiGraph, DiGraph
    self.add_nodes()

      
  def generate_k_mers(self):
    for i in xrange(len(self.string)-self.k+1):
      yield self.string[i:i+self.k]  
    
    
  def add_nodes(self):
    k_mers = self.generate_k_mers()
    km2_previous, j = None, 0
    
    for i in k_mers:
      km1, km2 = i[:-1], i[1:]
      self.G.add_edge(km1, km2)
      
      if j!=0:	self.G.add_edge(km2_previous, km1)
      km2_previous = km2
      j+=1
    
    
  def to_dot(self):
      """Return string with graphviz representation
      """
      ss = "digraph G {\n"
      for e in self.G.edges():
	ss += '"%s" -> "%s";\n' % (e[0], e[1])
      return ss + "}"
   
  def to_png(self, png_path = "graph.png"):
      """Graph graphviz representation in the PNG format
      """
      import subprocess, os
      dot_path = "./graph.dot"
      f = open(dot_path, "w")
      f.write(self.to_dot())
      f.close()
      subprocess.call("dot -Tpng %s -o %s" % (dot_path, png_path), shell=True)
      os.remove(dot_path)





