import math
import pygame
pygame.init()

class Edge:
    def __init(self,s,t):
        self.s = s
        self.t = t

class Node:
    def __init__(self, name):
        self.name = name
        self.neigh = []
        self.h_dist = 0
        self.dist_from_start = None
        self.total_distance = None
        self.prev_vertex = None

class Graph:
    def __init__(self, edge_list):
        self.edge_list = edge_list
        self.list_of_edges = []
        self.create_nodes()
        self.create_edges()
    def create_nodes(self):
        self.node_names = list(set([s for s,t in self.edge_list] + [t for s,t in self.edge_list]))
        self.nodes = {n: Node(n) for n in self.node_names}
    def create_edges(self):
        for edge in self.edge_list:
            e1 = Edge()
            e1.s = edge[0]
            e1.t = edge[1]
            e2 = Edge()
            e2.s = edge[1]
            e2.t = edge[0]
            self.add_edge(e1)
            self.add_edge(e2)
            self.list_of_edges.append(e1)
            self.list_of_edges.append(e2)
    def add_edge(self, edge):
        self.nodes[edge.s].neigh.append(edge)

edge_list = []
chosen_point = ()
chosen_order = 1
source = ()
target = ()
obstacle_list = []

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("A* Path Finding Visual")
color = (255,255,255)   
screen.fill(color)


def edge_list_creator(obstacle_list):
    for y_coor in range(0,800,16):
        for x_coor in range(0,800,16):
            if (x_coor,y_coor) not in obstacle_list:
                if x_coor == 784 and y_coor != 784:
                    if (x_coor,y_coor + 16) not in obstacle_list:
                        edge_list.append(((x_coor,y_coor),(x_coor, y_coor + 16)))
                elif y_coor == 784 and x_coor != 784:
                    if (x_coor + 16,y_coor) not in obstacle_list:
                        edge_list.append(((x_coor,y_coor),(x_coor + 16, y_coor)))
                elif x_coor == 784 and y_coor == 784:
                    continue
                else:
                    if (x_coor + 16,y_coor) not in obstacle_list:
                        edge_list.append(((x_coor,y_coor),(x_coor + 16, y_coor)))
                    if (x_coor,y_coor + 16) not in obstacle_list:
                     edge_list.append(((x_coor,y_coor),(x_coor, y_coor + 16)))
            else:
                continue


def find_chosen_block(chosen_coor):
    coor_x = chosen_coor[0]
    coor_y = chosen_coor[1]

    divided_x = int(coor_x / 16)
    divided__y = int(coor_y / 16)

    return ((divided_x * 16, divided__y * 16))


def set_heuristic_distances(graph,target):
    target_x = target[0]
    target_y = target[1]
    for node_name in graph.node_names:
        answer = (graph.nodes[node_name].name[0] - target_x)**2 + (graph.nodes[node_name].name[1] - target_y)**2
        answer = math.sqrt(answer)
        graph.nodes[node_name].h_dist = answer


for x in range(800):
    if (x % 16 == 0):
        pygame.draw.line(screen, (0, 0, 0), (x, 800), (x, 0))
        pygame.display.flip()
        x += 1

for y in range(800):
    if (y % 16 == 0):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (800, y))
        pygame.display.flip()
        y += 1 


def find_path(graph,start,end):
    open = []
    closed = []
    shortest_route = []

    graph.nodes[start].dist_from_start = 0
    graph.nodes[start].total_distance = graph.nodes[start].h_dist
    current_node = graph.nodes[start]

    while (current_node != graph.nodes[end]):
        open.append(current_node.name)
        pygame.time.delay(10)
        for edge in current_node.neigh:
            if edge.t in closed:
                continue
            elif graph.nodes[edge.t].prev_vertex != None:
                if graph.nodes[edge.t].total_distance > (graph.nodes[edge.t].h_dist + 16 + current_node.dist_from_start):
                    graph.nodes[edge.t].prev_vertex = current_node.name
                    graph.nodes[edge.t].dist_from_start = 16 + current_node.dist_from_start
                    graph.nodes[edge.t].total_distance = graph.nodes[edge.t].h_dist + graph.nodes[edge.t].dist_from_start
                    pygame.draw.rect(screen, (255,0,0), (edge.t[0], edge.t[1], 16, 16))
                    if edge.t not in closed:
                        open.append(edge.t)
            else:
                graph.nodes[edge.t].prev_vertex = current_node.name
                graph.nodes[edge.t].dist_from_start = 16 + current_node.dist_from_start
                graph.nodes[edge.t].total_distance = graph.nodes[edge.t].h_dist + graph.nodes[edge.t].dist_from_start
                pygame.draw.rect(screen, (255,0,0), (edge.t[0], edge.t[1], 16, 16))
                if edge.t not in closed:
                    open.append(edge.t)
        pygame.display.update()
        open = set(open)
        open = list(open)
        open.remove(current_node.name)
        closed.append(current_node.name)

        #Repaint the Target
        pygame.draw.rect(screen, (0,0,255), (end[0], end[1], 16, 16))
        pygame.display.update()

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

    #Visual
    for x in range(800):
        if (x % 16 == 0):
            pygame.draw.line(screen, (0, 0, 0), (x, 800), (x, 0))
            pygame.display.flip()
            x += 1

    for y in range(800):
        if (y % 16 == 0):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (800, y))
            pygame.display.flip()
            y += 1 
    
    #Trace From Start
    for coor in shortest_route:
        pygame.time.delay(25)
        pygame.draw.rect(screen, (138,43,226), (coor[0],coor[1],16,16))
        pygame.display.update()

    #Visual
    for x in range(800):
        if (x % 16 == 0):
            pygame.draw.line(screen, (0, 0, 0), (x, 800), (x, 0))
            pygame.display.flip()
            x += 1

    for y in range(800):
        if (y % 16 == 0):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (800, y))
            pygame.display.flip()
            y += 1 


run = True
while run:
    for event in pygame.event.get():
         #Getting the mouse left click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
            chosen_point = event.pos
            determined_point = find_chosen_block(chosen_point)
            if (chosen_order == 1):
                pygame.draw.rect(screen, (255,255,0), (determined_point[0], determined_point[1], 16, 16))
                chosen_order += 1
                source = determined_point
                pygame.display.update()
            elif (chosen_order == 2):
                pygame.draw.rect(screen, (0,0,255), (determined_point[0], determined_point[1], 16, 16))
                chosen_order += 1
                target = determined_point
                pygame.display.update()

        if pygame.mouse.get_pressed()[0] and chosen_order == 3:
            chosen_point = event.pos
            determined_point = find_chosen_block(chosen_point)
            pygame.draw.rect(screen, (0,0,0), (determined_point[0], determined_point[1], 16, 16))
            obstacle_list.append(determined_point)
            pygame.display.update()
                
        obstacle_list = set(obstacle_list)
        obstacle_list = list(obstacle_list)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            edge_list_creator(obstacle_list)
            graph = Graph(edge_list)
            set_heuristic_distances(graph,target)
            find_path(graph,source,target)
        
        if event.type == pygame.QUIT:
            run = False

pygame.quit()