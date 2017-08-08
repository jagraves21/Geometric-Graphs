import argparse
from collections import Counter

import urllib2
from bs4 import BeautifulSoup

import networkx
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib import pyplot

def get_html(url):
	response = urllib2.urlopen(url)
	html = response.read()
	return html

def html_to_graph(html):
	soup = BeautifulSoup(html, "html5lib")

	graph = networkx.DiGraph()
	color_map = {}

	next_id = {"value": 0}
	def dfs(node,  parent_id=None):
		cur_id = next_id["value"]
		next_id["value"] += 1
		name = getattr(node, "name", "leaf")
		
		color = color_map.setdefault(name, len(color_map))

		graph.add_node(cur_id, {"tag_color": color})

		if parent_id:
			graph.add_edge(parent_id, cur_id)

		if "childGenerator" in dir(node):
			for child in node.childGenerator():
				dfs(child, cur_id)
	
	dfs(soup)
	return graph

def main(hostname):
	html = get_html(hostname)
	graph= html_to_graph(html)

	pos = graphviz_layout(graph)

	colors = [attributes["tag_color"] for node,attributes in graph.nodes_iter(data=True)]
	color_map = pyplot.get_cmap("jet", max(colors))

	counts = Counter(colors)
	max_count = counts.most_common(1)[0][1]
	max_count = max_count + 0.25*max_count

	node_size = [100 * (1 - counts[attributes["tag_color"]]/max_count) for node,attributes in graph.nodes_iter(data=True)]

	node_size=10
	networkx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=colors, cmap=color_map)
	networkx.draw_networkx_edges(graph, pos, arrows=False)

	pyplot.axes().set_aspect('equal', 'datalim')
	pyplot.axis("off")
	pyplot.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="HTML to Graph", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#parser = argparse.ArgumentParser(description="Triangle Count")

	parser.add_argument("hostname", metavar="url", help="Website to convert to a graph.")
	
	arguments = vars(parser.parse_args())
	main(**arguments)
