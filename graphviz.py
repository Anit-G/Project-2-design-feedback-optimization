import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

def graphviz(url):
    g = rdflib.Graph()
    result = g.parse(url, format='turtle')

    G = rdflib_to_networkx_multidigraph(result)

    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, with_labels=True)

    #if not in interactive mode for 
    plt.show()

if __name__=="__main__":
    # graph visualization
    url = 'tbl3.ttl'
    graphviz(url)