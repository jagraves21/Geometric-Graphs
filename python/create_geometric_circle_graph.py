import argparse
import networkx
from generators import generate_geometric_circle_graph
from graph_utils import write_graph

def main(vertex_count, neighbors, distance, undirected, append_attributes, output_file, output_type):
	
	if undirected:
		graph = generate_geometric_circle_graph(networkx.Graph(), vertex_count, neighbors, distance)
	else:
		graph = generate_geometric_circle_graph(networkx.DiGraph(), vertex_count, neighbors, distance)
	
	if not output_file:
		output_file = "/dev/stdout"
		if not output_type:
			output_type = "gml"
	
	write_graph(graph, output_file, output_type)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Circular Geometric Graph Creator", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("-o",  "--output-file",               metavar="outfile", help="output graph name, standard out by default")
	parser.add_argument("-ot", "--output-type", default=None, metavar="type",    help="output type")
	
	parser.add_argument("-v", "--vertex-count", type=int,   default=100,  metavar="n", help="number of vertices")
	parser.add_argument("-n", "--neighbors",    type=int,   default=5,    metavar="n", help="number of neighbors")
	parser.add_argument("-d", "--distance",     type=float, default=None, metavar="n", help="number of neighbors")
	
	parser.add_argument("-u", "--undirected", action="store_true", help="construct an undirected graph, directed by default")
	parser.add_argument("-a", "--append-attributes", action="store_true", help="write graph attributes to RDF file")

	arguments = vars(parser.parse_args())
	main(**arguments)
