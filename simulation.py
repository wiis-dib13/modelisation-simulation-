import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Set, Tuple

class PetriNet:
    def __init__(self):
        self.places = {}  
        self.transitions = set()
        self.input_arcs = {}  
        self.output_arcs = {} 
        self.graph = nx.DiGraph()
    
    def add_place(self, place_id: str, marking: int = 0):
   
        self.places[place_id] = marking
        self.graph.add_node(place_id, type='place', marking=marking)
    
    def add_transition(self, transition_id: str):

        self.transitions.add(transition_id)
        self.graph.add_node(transition_id, type='transition')
    
    def add_input_arc(self, place_id: str, transition_id: str, weight: int = 1):

        self.input_arcs[(place_id, transition_id)] = weight
        self.graph.add_edge(place_id, transition_id, weight=weight, type='input')
    
    def add_output_arc(self, transition_id: str, place_id: str, weight: int = 1):
     
        self.output_arcs[(transition_id, place_id)] = weight
        self.graph.add_edge(transition_id, place_id, weight=weight, type='output')
    
    def get_output_transitions(self, place_id: str) -> List[str]:
      
        return [trans for (place, trans) in self.input_arcs.keys() if place == place_id]
    
    def get_input_transitions(self, place_id: str) -> List[str]:
     
        return [trans for (trans, place) in self.output_arcs.keys() if place == place_id]
    
    def get_output_places(self, transition_id: str) -> List[str]:
     
        return [place for (trans, place) in self.output_arcs.keys() if trans == transition_id]
    
    def get_input_places(self, transition_id: str) -> List[str]:
      
        return [place for (place, trans) in self.input_arcs.keys() if trans == transition_id]
    
    def is_transition_enabled(self, transition_id: str) -> bool:
  
        for (place, trans) in self.input_arcs:
            if trans == transition_id:
                weight = self.input_arcs[(place, trans)]
                if self.places[place] < weight:
                    return False
        return True
    
    def fire_transition(self, transition_id: str) -> bool:
      
        if not self.is_transition_enabled(transition_id):
            return False
        
      
        for (place, trans) in self.input_arcs:
            if trans == transition_id:
                weight = self.input_arcs[(place, trans)]
                self.places[place] -= weight
         
                self.graph.nodes[place]['marking'] = self.places[place]
        
       
        for (trans, place) in self.output_arcs:
            if trans == transition_id:
                weight = self.output_arcs[(trans, place)]
                self.places[place] += weight
             
                self.graph.nodes[place]['marking'] = self.places[place]
        
        return True
    
    def visualize(self, title="Réseau de Petri"):
     
        plt.figure(figsize=(12, 8))
        
      
        pos = {}
        place_nodes = [node for node in self.graph.nodes() if node in self.places]
        transition_nodes = [node for node in self.graph.nodes() if node in self.transitions]
        
 
        for i, place in enumerate(place_nodes):
            pos[place] = (0, i)
        for i, trans in enumerate(transition_nodes):
            pos[trans] = (2, i)
        
       
        nx.draw_networkx_nodes(self.graph, pos, nodelist=place_nodes, 
                              node_shape='o', node_size=1000, 
                              node_color='lightblue', alpha=0.7)
        
      
        nx.draw_networkx_nodes(self.graph, pos, nodelist=transition_nodes, 
                              node_shape='s', node_size=1000, 
                              node_color='lightcoral', alpha=0.7)
        

        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, arrowstyle='->')
        
      
        labels = {}
        for place in place_nodes:
            labels[place] = f"{place}\n({self.places[place]})"
        for trans in transition_nodes:
            labels[trans] = trans
        
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=10)
        
     
        edge_labels = {}
        for (u, v), data in self.graph.edges.items():
            if 'weight' in data:
                edge_labels[(u, v)] = data['weight']
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def print_network_info(self):
        """Affiche des informations sur le réseau"""
        print("=== RÉSEAU DE PETRI ===")
        print(f"Places: {list(self.places.keys())}")
        print(f"Transitions: {list(self.transitions)}")
        print(f"Marquage initial: {self.places}")
        print()
        
   
        print("=== REQUÊTES ===")
        for place in self.places:
            print(f"Place {place}:")
            print(f"  - Transitions de sortie: {self.get_output_transitions(place)}")
            print(f"  - Transitions d'entrée: {self.get_input_transitions(place)}")
        
        for transition in self.transitions:
            print(f"Transition {transition}:")
            print(f"  - Places d'entrée: {self.get_input_places(transition)}")
            print(f"  - Places de sortie: {self.get_output_places(transition)}")
        print()


def create_example_network():
    """Crée un exemple de réseau de Petri"""
    net = PetriNet()
    
  
    net.add_place("P1", 1)
    net.add_place("P2", 0)
    net.add_place("P3", 0)
    
    net.add_transition("T1")
    net.add_transition("T2")
    
   
    net.add_input_arc("P1", "T1", 1)
    net.add_output_arc("T1", "P2", 1)
    net.add_input_arc("P2", "T2", 1)
    net.add_output_arc("T2", "P3", 2)
    
    return net

def simulate_network(net):

    print("=== SIMULATION ===")
    net.visualize("État initial")
    

    enabled_transitions = [t for t in net.transitions if net.is_transition_enabled(t)]
    print(f"Transitions enabled: {enabled_transitions}")
    
   
    steps = 0
    max_steps = 5
    
    while enabled_transitions and steps < max_steps:
        for transition in enabled_transitions:
            if net.fire_transition(transition):
                print(f"Franchissement de {transition}")
                net.visualize(f"Après franchissement de {transition}")
                steps += 1
                break
        
        enabled_transitions = [t for t in net.transitions if net.is_transition_enabled(t)]
        print(f"Transitions enabled: {enabled_transitions}")

if __name__ == "__main__":
   
    petri_net = create_example_network()
    

    petri_net.print_network_info()
    
  
    simulate_network(petri_net)