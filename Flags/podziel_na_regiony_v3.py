import sys
from datetime import datetime

from graph import Vertex, Edge, Graph2D
from geometry import Point2D
from flag_5 import EdgeWithArcs, Graph2DWithArcs, get_regions
from gparser import GraphParser

NR_OF_REGIONS = 128

def print_time(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(message, current_time, flush=True)

#graph = Graph2D()
edge_dict = dict()

def simple_test():
    for i in range(13):
        graph.add_vertex(i, Point2D(0, i))

    graph.add_edge(0, 1, 2, 10)
    graph.add_edge(1, 2, 1, 20)
    graph.add_edge(2, 5, 7, 30)
    graph.add_edge(3, 5, 7, 40)
    graph.add_edge(35, 0, 4, 100)
    graph.add_edge(4, 0, 1, 50)# 8, 50, 4)
    graph.add_edge(5, 4, 1, 60)
    graph.add_edge(6, 7, 8, 70)
    graph.add_edge(7, 8, 7, 80)
    graph.add_edge(8, 8, 5, 90)
    graph.add_edge(9, 7, 2, 100)
    graph.add_edge(10, 11, 12, 10)
    graph.add_edge(11, 11, 6, 10)
    
    ea = EdgeWithArcs(17, 18, 19, 20, 4)
    ea.update_arc_flag_value(3, 1)
    
vert_filename = sys.argv[1]
edge_filename = sys.argv[2]
max_accumulation = 100000
save_filename = sys.argv[4]

print_time("Started")

#with open(vert_filename) as vert_filestream, open(edge_filename) as edge_filestream:
#    parser = GraphParser()
#    parser.parse_csv(vert_filestream, edge_filestream)

#    graph = parser.get_graph()
 
#simple_test()
 
print_time("Imported")
 
#test_graph_with_arcs = Graph2DWithArcs(graph)

#del graph
#gc.collect()

regions_info = dict()
#regions_info = get_regions(test_graph_with_arcs, max_accumulation=100000)

#with open("plik_posredni", 'w') as file:
#    for vertex_id in regions_info:
#        file.write(str(vertex_id) + " " + str(regions_info[vertex_id]) + "\n")
#    file.close()

with open("plik_posredni", 'r') as file:
    contents = file.readlines()
    for line in contents:
        strings = line.split()
        regions_info[int(strings[0])] = int(strings[1])
    
    file.close()

#arcs_filename = sys.argv[5]

    
with open("arcs", "r") as arcs:
    contents = arcs.readlines()
    for i in range(128):
        print_time(i)
        with open("arcs" + str(i), 'a') as file:# , open("plik_posredni", 'r') as regions_info_file:
            
            for line in contents:
                strings = line.split()
                
                if regions_info[int(strings[1])] != i and regions_info[int(strings[2])] != i:
                    continue
                
                flags = strings[4]
                
                edge_id , vert_1 , vert_2 , edge_weight = (int(strings[0]) , int(strings[1]) , int(strings[2]) , int(strings[3]))
                
                edge = EdgeWithArcs(edge_id , vert_1 , vert_2 , 0)
                
                reg_1 , reg_2 = (regions_info[vert_1] , regions_info[vert_2])
                
                if reg_1 == reg_2 and reg_1 == i:
                    file.write(str(edge.id) + "," + str(vert_1) + "," + str(vert_2)  + "," + str(edge_weight) + "," + flags + "\n")
                    continue
                    
                if reg_1 == i:
                    file.write(str(edge.id) + "," + str(vert_1) + "," + str(vert_2)  + "," + str(edge_weight) + "," + flags + "\n")
                
                if reg_2 == i:
                    file.write(str(edge.id) + "," + str(vert_1) + "," + str(vert_2)  + "," + str(edge_weight) + "," + flags + "\n")

            file.close()
            #regions_info_file.close()
            
