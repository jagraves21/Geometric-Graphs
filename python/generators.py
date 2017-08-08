import numpy
from sklearn.neighbors import BallTree
import networkx
import itertools

def generate_points(count):
	from math import pi
	
	radius = numpy.random.uniform(size=count)
	theta = numpy.random.uniform(size=count) * 2 * pi
	
	xx = numpy.sqrt(radius) * numpy.cos(theta)
	yy = numpy.sqrt(radius) * numpy.sin(theta)
	return xx, yy


def generate_circular_vertices(graph, vertex_count):
	xx, yy = generate_points(vertex_count)
	graph.add_nodes_from(xrange(vertex_count))
	
	pos = {}
	for ii in xrange(vertex_count):
		pos[ii] = [xx[ii],yy[ii]]
	
	networkx.set_node_attributes(graph, "pos", pos)

def add_knn_edges(graph, kk, distance):
	tree = BallTree(networkx.get_node_attributes(graph, "pos").values(), leaf_size=2)
	
	if distance:
		distances, edge_lists = tree.query(networkx.get_node_attributes(graph, "pos").values(), return_distance=True, k=kk)
	else:
		edge_lists = tree.query(networkx.get_node_attributes(graph, "pos").values(), return_distance=False, k=kk)
	
	for edge_list in edge_lists:
		src = edge_list[0]
		for ii, dst in enumerate(edge_list[1:], 1):
			if not distance or distance >= distances[ii][1]:
				graph.add_edge(src,dst)

def generate_circle_graph(graph=networkx.Graph(), vertex_count=100, neighbors=1, distance=1.0):
	generate_circular_vertices(graph, vertex_count)
	add_knn_edges(graph, neighbors+1, distance)
	return graph

def add_spanning_tree_edges(graph):
	complete_graph = networkx.complete_graph(networkx.number_of_nodes(graph))
	print graph

	def generate_edges(graph):
		pos = networkx.get_node_attributes(graph, "pos")
		for src,dst in itertools.combinations(range(networkx.number_of_nodes(graph)), 2):
			distance = (pos[src][0] - pos[dst][0])**2 + (pos[src][1] - pos[dst][1])**2
			yield (src,dst,distance)
	
	complete_graph.add_weighted_edges_from(generate_edges(graph))
	tree = networkx.minimum_spanning_tree(complete_graph)
	
	graph.add_edges_from(tree.edges())

def generate_circle_spanning_tree_graph(graph=networkx.Graph(), vertex_count=100):
	generate_circular_vertices(graph, vertex_count)
	add_spanning_tree_edges(graph)
	return graph
