import numpy
from sklearn.neighbors import BallTree
import networkx

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

def generate_geometric_circle_graph(graph=networkx.Graph(), vertex_count=100, neighbors=1, distance=1.0):
	generate_circular_vertices(graph, vertex_count)
	add_knn_edges(graph, neighbors+1, distance)
	return graph

