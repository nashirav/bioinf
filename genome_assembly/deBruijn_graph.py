"""
@description: De Bruijn graph implementation in genome assembly
"""

class Node:
  
  def __init__(self, s):
    self.n_in = None
    self.n_out = None
    self.s = s
  
  def __str__(self):
    return self.s
  
  def __repr__(self):
    return self.__str__()
  
  def __eq__(self, node):
    return self.s == node.s
      
  def __hash__(self):
    return hash(self.s) #Two objects with the same value have the same hash value.
  
  def isBalanced(self):
    return self.n_in == self.n_out
  
  def isSemiBalanced(self):
    return self.n_in + 1 == self.n_out or self.n_in - 1 == self.n_out




class deBruijnGraph: 
   
    
  def __init__(self, s, k):
    """de Bruijn multigraph with given string iterator and k-mer length k 
    """
    self.k = k
    self.string = s

    self.edges, self.nodes = [], []
    self.build_graph() 


  def generate_k_mers(self):
    for i in xrange(len(self.string)-self.k+1):
      yield self.string[i:i+self.k]  
    
   
  def add_node(self, n): 
    if n not in self.nodes:
	self.nodes.append(n)
   
   
  def del_small_loops(self):
      "removes all edges that lead from and to the same node, e.g. node1 -> node1"
      self.edges = [i for i in self.edges if not i[0]==i[1]]
    
   
  def build_graph(self):
    """Build MultiGraph"""
    
    n2_previous, j = None, 0
    
    for i in self.generate_k_mers():
      
      km1, km2 = i[:-1], i[1:]
      n1, n2 = Node(km1), Node(km2)      
      if j!=0:
	self.edges.append( (n2_previous, n1) )
      self.edges.append( (n1, n2) )
      n2_previous = n2
      j+=1 
      
      self.add_node(n1)
      self.add_node(n2)  
    
    self.del_small_loops()  
  
  
      
  def to_dot(self):
      """Return string with graphviz representation
      """
      ss = "digraph deBruijnGraph {\n" #directed graph
      for e in self.edges:
	ss += '"%s" -> "%s";\n' % (e[0], e[1])
      return ss + "}"
   
  def to_png(self, png_path = "deBruijnGraph.png"):
      """Return file that contains graph visualization in the PNG format
      """
      import subprocess, os
      dot_path = "./deBruijnGraph.dot"
      f = open(dot_path, "w")
      f.write(self.to_dot())
      f.close()
      subprocess.call("dot -Tpng %s -o %s" % (dot_path, png_path), shell=True)
      os.remove(dot_path)
   
   
G = deBruijnGraph("AAABB", 3)  
#G = deBruijnGraph("a_long_long_long_time", 5)  
print G.edges
print G.nodes
G.to_png()