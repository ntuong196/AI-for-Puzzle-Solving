

"""
An example using Graph as a weighted network.

https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.drawing.nx_pylab.draw_networkx_edge_labels.html

"""


import matplotlib.pyplot as plt
    
import networkx as nx

import numpy as np

import search


class MyDiGraphProblem(search.Problem):

    def __init__(self, 
                 G, # DiGraph
                 initial, 
                 goal_set=set(),
                    edge_label_name = 'w'):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.G = G # graph
        self.initial = initial; self.goal_set = goal_set
        self.edge_label_name = edge_label_name

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        return sorted(self.G.neighbors(state))
        

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        return action

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state in self.goal_set

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + self.G.adj[state1][state2][self.edge_label_name]



def make_digraph_1():
    '''
    Make a weighted digraph 'G'
    and compute positions 'pos' for its vertices
    return G, pos
    '''
    G = nx.DiGraph()  # directed graph
    #  add weighted arcs  
    G.add_edge('a','b',w=6)
    G.add_edge('a','h',w=3)
    G.add_edge('b','c',w=2)
    G.add_edge('b','g',w=4)
    G.add_edge('c','d',w=1)
    G.add_edge('c','e',w=7)
    G.add_edge('d','e',w=2)
    G.add_edge('e','f',w=2)
    G.add_edge('e','i',w=6)
    G.add_edge('f','i',w=1)
    G.add_edge('g','e',w=5)
    G.add_edge('g','e',w=4)
    G.add_edge('h','e',w=2)
    G.add_edge('i','d',w=7)
    # specify position of vertices
    #pos=nx.spring_layout(G) # positions for all nodes
    #pos=nx.spectral_layout(G) # positions for all nodes    
    pos = {'a': np.array([ 0.55952541,  1.2        ]),
     'b': np.array([ 1.2, 1]),
     'c': np.array([ 0.93293402,  0.3241465 ]),
     'd': np.array([ 0.51165237,  0.        ]),
     'e': np.array([ 0.55777832,  0.48437183]),
     'f': np.array([ -0.20        ,  0.7]),
     'g': np.array([ 0.75975912,  0.83144263]),
     'h': np.array([ 0.25864231,  0.97354648]),
     'i': np.array([ 0.07071249,  0.2463135 ])}
    #
    return G, pos


def show_graph(G,pos):
    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=700)    
    # labels
    nx.draw_networkx_labels(G,pos, font_size=20,font_family='sans-serif')    
    # edges
    nx.draw_networkx_edges(G,pos, width=2)
        
    #nx.draw_networkx_edges(G,pos,edgelist=elarge,
    #                    width=6)
    #nx.draw_networkx_edges(G,pos,edgelist=esmall,
    #                    width=6,alpha=0.5,edge_color='b',style='dashed')
    
#    el_dict = dict( ((u,v),d['w']) for (u,v,d) in  G.edges_iter(data=True) )
        
    #elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['w'] >0.5]
    #esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['w'] <=0.5]
    #nx.draw_networkx_edge_labels(G,pos, edge_labs=el_dict, width=2)
    nx.draw_networkx_edge_labels(G,pos, edge_labs='w', width=2)
        
    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display


#
def mid_q3c():
    G, pos = make_digraph_1()  
    mdgp = MyDiGraphProblem(G, # DiGraph
                     initial='a', 
                     goal_set=set('i'),
                        edge_label_name = 'w')
    
    #sol = search.breadth_first_graph_search(mdgp)
    mdgp.goal_set = set(['c','d','i'])

    sol = search.depth_first_tree_search(mdgp)
    
    print('solution ', sol.path())
    
def mid_q3d():
    G, pos = make_digraph_1()  
    mdgp = MyDiGraphProblem(G, # DiGraph
                     initial='a', 
                     goal_set=set('i'),
                        edge_label_name = 'w')
    
    #sol = search.breadth_first_graph_search(mdgp)
    mdgp.goal_set = set(['c','d','i'])

    sol = search.depth_first_tree_search(mdgp)
    
    print('solution ', sol.path())
    
    
def mid_q3e():
    G, pos = make_digraph_1()  
    mdgp = MyDiGraphProblem(G, # DiGraph
                     initial='a', 
                     goal_set=set(['d','i']),
                        edge_label_name = 'w')
    
    #sol = search.breadth_first_graph_search(mdgp)
#    mdgp.goal_set = set(['c','d','i'])
    
    def _path_cost(node):
        if node.parent is None:
            return 0
        else:
            return node.parent.path_cost+G.adj[node.parent.state][node.state]['w']

    sol =  search.best_first_tree_search(mdgp,_path_cost)
    print('total cost ',sol.path_cost)    
    print('solution ', sol.path())
    



if __name__ == "__main__":
    pass  
    G, pos = make_digraph_1()  
    show_graph(G,pos)
#    mid_q3e()


#try:
#    import matplotlib.pyplot as plt
#except:
#    raise
#
#import networkx as nx
#
#G=nx.path_graph(8)
#nx.draw(G)
#plt.savefig("simple_path.png") # save as png
#plt.show() # display
#G.add_edge('a','b')
#G.add_edge('a','c')
#G.add_edge('c','d')
#G.add_edge('c','e')
#G.add_edge('c','f')
#G.add_edge('a','d')
#
