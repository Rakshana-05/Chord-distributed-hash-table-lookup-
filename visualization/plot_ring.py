import networkx as nx
import matplotlib.pyplot as plt

def draw_ring(ring, path=None):
    G = nx.DiGraph()

    for nid in ring.node_ids:
        G.add_node(nid)

    for node in ring.nodes.values():
        if node.is_active and node.successor:
            G.add_edge(node.id, node.successor.id)

    pos = nx.circular_layout(G)
    fig, ax = plt.subplots(figsize=(7, 7))

    # Base nodes
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', 
            node_size=800, font_weight='bold', ax=ax)

    # Highlight lookup path
    if path and len(path) > 1:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3, ax=ax)
        
        # Highlight start and end nodes
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='lightgreen', node_size=800, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='gold', node_size=800, ax=ax)

    return fig