import random
import sys
from threading import Thread
from igraph import Graph, plot
import networkx as nx

check = nx.erdos_renyi_graph(500, 0.5, seed=123, directed=False)

vertex_counter = int(check[1])


def draw(graph):
    for es in graph.es:
        es['label'] = es['weight']

    for i, vs in enumerate(graph.vs):
        vs['label'] = i
        vs['color'] = 'gray'

    plot(graph, **{'vertex_size': 40},
         margin=50,
         bbox=(480, 320),
         layout=graph.layout_circle())


def prim(in_graph, out_graph, current_vertex=0, done=[]):

    incident_edges = [in_graph.es[id] for id in in_graph.incident(current_vertex)]
    incident_edges = list(
        filter(lambda edge: edge.source not in done and edge.target not in done, incident_edges))
    if not incident_edges:
        return
    min_incident_edge = min(incident_edges, key=lambda edge: edge['weight'])
    out_graph.add_edge(source=min_incident_edge.source,
                       target=min_incident_edge.target,
                       weight=min_incident_edge['weight'])
    next_vertex = min_incident_edge.target if min_incident_edge.target != current_vertex else min_incident_edge.source
    done.append(current_vertex)
    prim(in_graph, out_graph, next_vertex, done)


source = Graph.Full(vertex_counter)

for es in source.es:
    es['weight'] = random.randint(1, 9)

min_ost = Graph(vertex_counter)
prim(source, min_ost)

Thread(target=lambda: draw(source)).start()
Thread(target=lambda: draw(min_ost)).start()
