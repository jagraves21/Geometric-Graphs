import argparse
import networkx
from matplotlib import pyplot
from graph_utils import read_graph

def main(graph_filename, graph_type=None, undirected=False, databases=2):
	
	if undirected:
		graph = read_graph(graph_filename, graph_type, networkx.Graph())
	else:
		graph = read_graph(graph_filename, graph_type, networkx.DiGraph())

	pos = networkx.get_node_attributes(graph, "pos")
	if not pos:
		pos = networkx.spring_layout(graph)

	color_map = pyplot.cm.tab20

	nodes = graph.nodes(data=False)
	colors = [node % databases for node in nodes]
	networkx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_size=50, node_color=colors, cmap=color_map, vmin=0, vmax=databases)

	edges = graph.edges()
	
	colors = [pair[0] % databases for pair in edges]
	networkx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color=colors, edge_cmap=color_map, edge_vmin=0, edge_vmax=databases, arrows=False)

	pyplot.axes().set_aspect('equal', 'datalim')
	pyplot.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Graph to RDF Converter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("graph_filename", metavar="infile", help="graph file name")
	parser.add_argument("-t", "--graph-type", default=None, metavar="type", help="graph type")

	parser.add_argument("-u", "--undirected", action="store_true", help="construct an undirected graph, directed by default")
	
	parser.add_argument("-d", "--databases", type=int, default=5, help="number of databases")

	arguments = vars(parser.parse_args())
	main(**arguments)
