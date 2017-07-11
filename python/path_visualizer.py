import argparse
import networkx
from matplotlib import pyplot
from graph_utils import read_graph

def main(graph_filename, graph_type=None, undirected=False):
	
	if undirected:
		graph = read_graph(graph_filename, graph_type, networkx.Graph())
	else:
		graph = read_graph(graph_filename, graph_type, networkx.DiGraph())

	pos = networkx.get_node_attributes(graph, "pos")
	if not pos:
		pos = networkx.spring_layout(graph)
	
	count = 0
	colors = ["Reds_r", "Greens_r", "Blues_r", "Greys_r", "Purples_r"]
	unused = dict(pos)
	while unused:
		min_vertex,position = unused.items()[0]
		min_dist = position[0]**2 + position[1]**2
		for vertex,position in unused.iteritems():
			dist = position[0]**2 + position[1]**2
			if dist < min_dist:
				min_vertex = vertex
				min_dist = dist
		path = networkx.single_source_shortest_path_length(graph, min_vertex)
		
		for vertex in path.iterkeys():
			unused.pop(vertex, None)
		
		color_map = cmap=pyplot.get_cmap(colors[count % len(colors)])
		vmin = float(min(path.itervalues()))
		vmax = float(max(path.itervalues()))
		if vmin == vmax:
			vmax += 2
		vmax *= 1.5

		networkx.draw_networkx_nodes(graph, pos, nodelist=path.keys(), node_size=50, node_color=path.values(), vmin=vmin, vmax=vmax, cmap=color_map)
		count += 1	

	networkx.draw_networkx_edges(graph, pos, arrows=not undirected)

	pyplot.axes().set_aspect('equal', 'datalim')
	pyplot.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Graph to RDF Converter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("graph_filename", metavar="infile", help="graph file name")
	parser.add_argument("-t", "--graph-type", default=None, metavar="type", help="graph type")

	parser.add_argument("-u", "--undirected", action="store_true", help="construct an undirected graph, directed by default")
	

	arguments = vars(parser.parse_args())
	main(**arguments)
