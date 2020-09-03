class Edge():
    def __init__(self,s,t,weight):
        self.s = s
        self.t = t
        self.weight = weight

class Node():
    def __init__(self,name):
        self.name = name
        self.neighbors = []
        self.h_dist = 0
        self.dist_from_start = None
        self.total_distance = None
        self.prev_vertex = None

class Graph():
    def __init__(self,edge_list):
        self.edge_list = edge_list
        self.list_of_edges = []
        self.create_nodes()
        self.create_graph()
    def create_nodes(self):
        self.node_names = list(set([s for s,t,d in self.edge_list] + [t for s,t,d in self.edge_list]))
        self.nodes = {n : Node(n) for n in self.node_names}
    def create_graph(self):
        for s,t,d in self.edge_list:
            e1 = Edge(s,t,d)
            e2 = Edge(t,s,d)
            self.list_of_edges.append(e1)
            self.add_edges(e1)
            self.list_of_edges.append(e2)
            self.add_edges(e2)
    def add_edges(self,edge):
        self.nodes[edge.s].neighbors.append(edge)

edge_list1 = [("A","B",5),("A","C",5),("B","C",4),("B","D",3),("C","D",7),("C","E",20),("D","E",6)]
graph1 = Graph(edge_list1)
graph1.nodes["A"].h_dist = 16
graph1.nodes["B"].h_dist = 17
graph1.nodes["C"].h_dist = 13
graph1.nodes["D"].h_dist = 16

edge_list2 = [("A","S",7),("A","B",3),("A","D",4),("S","B",2),("S","C",3),("B","H",1),("B","D",4),("D","F",5),("H","F",3),("H","G",2),
("G","E",2),("C","L",2),("L","I",4),("L","J",4),("I","K",4),("I","K",4),("I","J",6),("K","E",5)]
graph2 = Graph(edge_list2)
graph2.nodes["A"].h_dist = 9
graph2.nodes["B"].h_dist = 7
graph2.nodes["C"].h_dist = 8
graph2.nodes["D"].h_dist = 8
graph2.nodes["E"].h_dist = 0
graph2.nodes["F"].h_dist = 6
graph2.nodes["G"].h_dist = 3
graph2.nodes["H"].h_dist = 6
graph2.nodes["I"].h_dist = 4
graph2.nodes["J"].h_dist = 4
graph2.nodes["K"].h_dist = 3
graph2.nodes["L"].h_dist = 6
graph2.nodes["S"].h_dist = 10


def find_path(graph,start,end):
    open = []
    closed = []
    shortest_route = []

    graph.nodes[start].dist_from_start = 0
    graph.nodes[start].total_distance = graph.nodes[start].h_dist
    current_node = graph.nodes[start]

    while (current_node != graph.nodes[end]):
        open.append(current_node.name)
        for edge in current_node.neighbors:
            if edge.t in closed:
                continue
            elif graph.nodes[edge.t].prev_vertex != None:
                ##Heuristic
                if graph.nodes[edge.t].total_distance > (graph.nodes[edge.t].h_dist + edge.weight + current_node.dist_from_start):
                    graph.nodes[edge.t].prev_vertex = current_node.name
                    graph.nodes[edge.t].dist_from_start = edge.weight + current_node.dist_from_start
                    graph.nodes[edge.t].total_distance = graph.nodes[edge.t].h_dist + graph.nodes[edge.t].dist_from_start
                    if edge.t not in closed:
                        open.append(edge.t)
            else:
                #First initilization
                ##Heuristic
                graph.nodes[edge.t].prev_vertex = current_node.name
                graph.nodes[edge.t].dist_from_start = edge.weight + current_node.dist_from_start
                graph.nodes[edge.t].total_distance = graph.nodes[edge.t].h_dist + graph.nodes[edge.t].dist_from_start
                if edge.t not in closed:
                    open.append(edge.t)
        open = set(open)
        open = list(open)
        open.remove(current_node.name)
        closed.append(current_node.name)

        #Determine the next current value
        chosen_node_name = None
        for elm in open:
            if chosen_node_name != None:
                if graph.nodes[elm].total_distance < graph.nodes[chosen_node_name].total_distance:
                    chosen_node_name = elm
            else:
                chosen_node_name = elm
        current_node = graph.nodes[chosen_node_name]

    #Initilize the Shortest_Route List
    shortest_route.append(end)
    helper_node = graph.nodes[end]
    while helper_node.prev_vertex != None:
        shortest_route.append(helper_node.prev_vertex)
        helper_node = graph.nodes[helper_node.prev_vertex]

    shortest_route = shortest_route[::-1]
    print(shortest_route)


find_path(graph1,"A","E")
find_path(graph2,"A","E")