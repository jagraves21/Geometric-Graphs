import sys, os
import networkx
import numpy

def get_graph_type(filename):
	name, extension = os.path.splitext(filename)

	if extension:
		extension = extension[1:]
	
	return extension

def read_graph(filename, file_type=None, create_using=networkx.DiGraph):
	if not file_type:
		file_type = get_graph_type(filename)
		if not file_type:
			raise RuntimeError("Unable to determine graph file type.")
	
	if file_type == "adjlist":
		return networkx.read_adjlist(filename, nodetype=int, create_using=create_using())
	elif file_type == "edgelist":
		return networkx.read_edgelist(filename, nodetype=int, create_using=create_using())
	elif file_type == "gexf":
		return networkx.read_gexf(filename, nodetype=int)
	elif file_type == "gml":
		return networkx.read_gml(filename) 
	elif file_type == "gpickle":
		return networkx.read_gpickle(filename)
	elif file_type == "graphml":
		return networkx.read_graphml(filename, nodetype=int)
	elif file_type == "yaml":
		return networkx.read_yaml(filename)
	elif file_type == "pajek":
		return networkx.read_pajek(filename)
	elif file_type == "adjmat":
		matrix = numpy.loadtxt(filename, delimiter=",")
		return networkx.from_numpy_matrix(matrix)
	else:
		raise RuntimeError("Unrecognized input graph file type (" + str(file_type) + ").")

def write_graph(graph, filename, file_type=None):
	if not file_type:
		file_type = get_graph_type(filename)
		if not file_type:
			raise RuntimeError("Unable to determine graph file type.")
	
	if file_type == "adjlist":
		networkx.write_adjlist(graph, filename)
	elif file_type == "edgelist":
		networkx.write_edgelist(graph, filename)
	elif file_type == "gexf":
		networkx.write_gexf(graph, filename)
	elif file_type == "gml":
		networkx.write_gml(graph, filename)
	elif file_type == "gpickle":
		networkx.write_gpickle(graph, filename)
	elif file_type == "graphml":
		networkx.write_graphml(graph, filename)
	elif file_type == "yaml":
		networkx.write_yaml(graph, filename)
	elif file_type == "pajek" or file_type == "net":
		networkx.write_pajek(graph, filename)
	elif file_type == "adjmat":
		#sparse_matrix = networkx.adjacency_matrix(graph)
		#dense_matrix = sparse_matrix.todense()
		#dense_matrix.tofile(filename, sep=",", format="%g")

		matrix = networkx.to_numpy_matrix(graph)
		numpy.savetxt(filename, matrix, delimiter=",", newline="\n", fmt="%g")
	else:
		raise RuntimeError("Unrecognized output graph file type.")

