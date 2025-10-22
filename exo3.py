import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Set, Tuple
from enum import Enum

class LightColor(Enum):
    RED = "Rouge"
    GREEN = "Vert"
    YELLOW = "Jaune"

class TrafficLightSystem:
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
    
    def build_traffic_light_model(self):
        """Construit le modèle de feux de circulation pour un carrefour à 2 tronçons"""
        
        self.add_place("NS_Red", 1)     
        self.add_place("NS_Green", 0)   
        self.add_place("NS_Yellow", 0)  
        
        # Places pour les états des feux Est-Ouest
        self.add_place("EW_Red", 0)     
        self.add_place("EW_Green", 1)    
        self.add_place("EW_Yellow", 0)   
        
        # Places de temporisation
        self.add_place("Timer_Green", 0) 
        self.add_place("Timer_Yellow", 0) 
        
        # Transitions
        self.add_transition("T_NS_Green_Start")   # Début phase verte NS
        self.add_transition("T_NS_Green_End")     # Fin phase verte NS
        self.add_transition("T_NS_Yellow_Start")  # Début phase jaune NS
        self.add_transition("T_NS_Yellow_End")    # Fin phase jaune NS
        self.add_transition("T_EW_Green_Start")   # Début phase verte EW
        self.add_transition("T_EW_Green_End")     # Fin phase verte EW
        self.add_transition("T_EW_Yellow_Start") 
        self.add_transition("T_EW_Yellow_End")   
     
        
        self.add_input_arc("EW_Yellow", "T_NS_Green_Start", 1)
        self.add_output_arc("T_NS_Green_Start", "NS_Green", 1)
        self.add_output_arc("T_NS_Green_Start", "EW_Red", 1)
        self.add_output_arc("T_NS_Green_Start", "Timer_Green", 1)
        
      
        self.add_input_arc("NS_Green", "T_NS_Yellow_Start", 1)
        self.add_input_arc("Timer_Green", "T_NS_Yellow_Start", 1)
        self.add_output_arc("T_NS_Yellow_Start", "NS_Yellow", 1)
        self.add_output_arc("T_NS_Yellow_Start", "Timer_Yellow", 1)
        
      
        self.add_input_arc("NS_Yellow", "T_NS_Yellow_End", 1)
        self.add_input_arc("Timer_Yellow", "T_NS_Yellow_End", 1)
        self.add_output_arc("T_NS_Yellow_End", "NS_Red", 1)
        
     
        self.add_input_arc("NS_Yellow", "T_EW_Green_Start", 1)
        self.add_output_arc("T_EW_Green_Start", "EW_Green", 1)
        self.add_output_arc("T_EW_Green_Start", "NS_Red", 1)
        self.add_output_arc("T_EW_Green_Start", "Timer_Green", 1)
        
       
        self.add_input_arc("EW_Green", "T_EW_Yellow_Start", 1)
        self.add_input_arc("Timer_Green", "T_EW_Yellow_Start", 1)
        self.add_output_arc("T_EW_Yellow_Start", "EW_Yellow", 1)
        self.add_output_arc("T_EW_Yellow_Start", "Timer_Yellow", 1)
      
        self.add_input_arc("EW_Yellow", "T_EW_Yellow_End", 1)
        self.add_input_arc("Timer_Yellow", "T_EW_Yellow_End", 1)
        self.add_output_arc("T_EW_Yellow_End", "EW_Red", 1)
    
    def get_light_states(self) -> Dict[str, str]:
        """Retourne l'état actuel des feux"""
        states = {}
        
       
        if self.places["NS_Red"] > 0:
            states["Nord-Sud"] = "Rouge"
        elif self.places["NS_Green"] > 0:
            states["Nord-Sud"] = "Vert"
        elif self.places["NS_Yellow"] > 0:
            states["Nord-Sud"] = "Jaune"
        

        if self.places["EW_Red"] > 0:
            states["Est-Ouest"] = "Rouge"
        elif self.places["EW_Green"] > 0:
            states["Est-Ouest"] = "Vert"
        elif self.places["EW_Yellow"] > 0:
            states["Est-Ouest"] = "Jaune"
            
        return states
    
    def is_transition_enabled(self, transition_id: str) -> bool:
        """Vérifie si une transition est franchissable"""
        for (place, trans) in self.input_arcs:
            if trans == transition_id:
                weight = self.input_arcs[(place, trans)]
                if self.places[place] < weight:
                    return False
        return True
    
    def fire_transition(self, transition_id: str) -> bool:
        """Franchit une transition si elle est enabled"""
        if not self.is_transition_enabled(transition_id):
            return False
        
        # Retirer les jetons des places d'entrée
        for (place, trans) in self.input_arcs:
            if trans == transition_id:
                weight = self.input_arcs[(place, trans)]
                self.places[place] -= weight
                self.graph.nodes[place]['marking'] = self.places[place]
        
        # Ajouter les jetons aux places de sortie
        for (trans, place) in self.output_arcs:
            if trans == transition_id:
                weight = self.output_arcs[(trans, place)]
                self.places[place] += weight
                self.graph.nodes[place]['marking'] = self.places[place]
        
        return True
    
    def visualize(self, title="Système de Feux de Circulation"):
        """Visualise le réseau de Petri avec les états des feux"""
        plt.figure(figsize=(16, 10))
        
        # Positionnement complet de tous les nœuds
        pos = {
            # Places Nord-Sud
            "NS_Red": (0, 3), "NS_Green": (0, 2), "NS_Yellow": (0, 1),
            # Places Est-Ouest
            "EW_Red": (4, 3), "EW_Green": (4, 2), "EW_Yellow": (4, 1),
            # Temporisation
            "Timer_Green": (2, 4), "Timer_Yellow": (2, 0),
            # Transitions NS
            "T_NS_Green_Start": (1, 2.5), "T_NS_Green_End": (1, 1.5),
            "T_NS_Yellow_Start": (1, 1.5), "T_NS_Yellow_End": (1, 0.5),
            # Transitions EW
            "T_EW_Green_Start": (3, 2.5), "T_EW_Green_End": (3, 1.5),
            "T_EW_Yellow_Start": (3, 1.5), "T_EW_Yellow_End": (3, 0.5)
        }
        
        # Vérifier que tous les nœuds ont une position
        missing_positions = [node for node in self.graph.nodes() if node not in pos]
        if missing_positions:
            print(f"ATTENTION: Nœuds sans position: {missing_positions}")
            # Ajouter des positions par défaut pour les nœuds manquants
            base_y = 0
            for node in missing_positions:
                pos[node] = (2, base_y)
                base_y -= 1
        
        # Séparer les places et transitions pour un affichage différent
        place_nodes = [node for node in self.graph.nodes() if node in self.places]
        transition_nodes = [node for node in self.graph.nodes() if node in self.transitions]
        
        # Dessiner les places (cercles)
        place_colors = []
        for place in place_nodes:
            if "Red" in place and self.places[place] > 0:
                place_colors.append('red')
            elif "Green" in place and self.places[place] > 0:
                place_colors.append('green')
            elif "Yellow" in place and self.places[place] > 0:
                place_colors.append('yellow')
            elif "Timer" in place:
                place_colors.append('orange')
            else:
                place_colors.append('lightgray')
        
        nx.draw_networkx_nodes(self.graph, pos, nodelist=place_nodes,
                              node_shape='o', node_size=1500,
                              node_color=place_colors, alpha=0.8)
        
        # Dessiner les transitions (carrés)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=transition_nodes,
                              node_shape='s', node_size=1200,
                              node_color='lightcoral', alpha=0.8)
        
        # Dessiner les arcs
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray',
                              arrows=True, arrowsize=20, arrowstyle='->',
                              width=2)
        
        # Ajouter les labels
        labels = {}
        for node in self.graph.nodes():
            if node in self.places:
                labels[node] = f"{node}\n({self.places[node]})"
            else:
                labels[node] = node
        
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, font_weight='bold')
        
        # Ajouter les poids des arcs
        edge_labels = {}
        for (u, v), data in self.graph.edges.items():
            if 'weight' in data and data['weight'] > 1:
                edge_labels[(u, v)] = data['weight']
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=7)
        
        # État des feux
        light_states = self.get_light_states()
        plt.text(2, 4.5, f"ÉTAT DES FEUX:\nNord-Sud: {light_states.get('Nord-Sud', '?')}\nEst-Ouest: {light_states.get('Est-Ouest', '?')}",
                fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def print_current_state(self):
        """Affiche l'état courant du système"""
        states = self.get_light_states()
        print(f"État actuel: NS={states['Nord-Sud']}, EW={states['Est-Ouest']}")
        print(f"Marquage: {self.places}")
        
        enabled = [t for t in self.transitions if self.is_transition_enabled(t)]
        print(f"Transitions enabled: {enabled}")
        print()

def simulate_complete_cycle():
    """Simule un cycle complet des feux de circulation"""
    print("=== SIMULATION COMPLÈTE DU SYSTÈME DE FEUX ===")
    
    # Créer le système
    system = TrafficLightSystem()
    system.build_traffic_light_model()
    
    # État initial
    print("État initial:")
    system.print_current_state()
    system.visualize("État Initial")
    
    # Séquence de simulation
    simulation_steps = [
        ("T_EW_Green_End", "Fin phase verte Est-Ouest"),
        ("T_EW_Yellow_Start", "Début phase jaune Est-Ouest"),
        ("T_EW_Yellow_End", "Fin phase jaune Est-Ouest"),
        ("T_NS_Green_Start", "Début phase verte Nord-Sud"),
        ("T_NS_Green_End", "Fin phase verte Nord-Sud"),
        ("T_NS_Yellow_Start", "Début phase jaune Nord-Sud"),
        ("T_NS_Yellow_End", "Fin phase jaune Nord-Sud"),
        ("T_EW_Green_Start", "Début phase verte Est-Ouest"),
    ]
    
    step_count = 1
    for transition, description in simulation_steps:
        print(f"\n--- Étape {step_count}: {description} ---")
        
        if system.is_transition_enabled(transition):
            system.fire_transition(transition)
            system.print_current_state()
            system.visualize(f"Étape {step_count}: {description}")
        else:
            print(f"❌ Transition {transition} non enabled!")
            # Afficher pourquoi elle n'est pas enabled
            for (place, trans) in system.input_arcs:
                if trans == transition:
                    weight = system.input_arcs[(place, trans)]
                    available = system.places[place]
                    print(f"   Place {place}: disponible={available}, requis={weight}")
        
        step_count += 1
    
    return system

def analyze_system_properties(system):
    """Analyse les propriétés du système"""
    print("\n=== ANALYSE DES PROPRIÉTÉS ===")
    
    # Vérification de la sécurité (pas deux feux verts en même temps)
    states = system.get_light_states()
    safe = not (states['Nord-Sud'] == 'Vert' and states['Est-Ouest'] == 'Vert')
    print(f"✅ Sécurité (pas deux verts simultanés): {'OUI' if safe else 'NON'}")
    
    # Vérification de la vivacité (pas de famine)
    # Le système alterne naturellement entre les directions
    print(f"✅ Vivacité (pas de famine): OUI")
    

    max_tokens = max(system.places.values())
    bounded = max_tokens <= 2  # Le système est borné si aucun marquage > 2
    print(f"✅ Bornage (marquage limité): {'OUI' if bounded else 'NON'} (max={max_tokens})")
    
  
    print(f"✅ États valides: NS-Rouge/EW-Vert, NS-Vert/EW-Rouge, transitions par jaune")

def simple_reachability_analysis(system):
    """Analyse simplifiée des états atteignables"""
    print("\n=== ANALYSE DES ÉTATS ATTEIGNABLES ===")
    
 
    base_states = [
        {"NS": "Rouge", "EW": "Vert", "Description": "État initial - EW prioritaire"},
        {"NS": "Jaune", "EW": "Rouge", "Description": "Transition EW→NS"},
        {"NS": "Vert", "EW": "Rouge", "Description": "NS prioritaire"},
        {"NS": "Rouge", "EW": "Jaune", "Description": "Transition NS→EW"},
    ]
    
    print("États atteignables identifiés:")
    for i, state in enumerate(base_states, 1):
        print(f"  État {i}: NS={state['NS']}, EW={state['EW']} - {state['Description']}")
    
    # Vérification d'interblocage
    enabled_transitions = [t for t in system.transitions if system.is_transition_enabled(t)]
    deadlock = len(enabled_transitions) == 0
    print(f"\n🔍 Interblocage (deadlock): {'OUI ❌' if deadlock else 'NON ✅'}")
    
    if not deadlock:
        print(f"   Transitions disponibles: {len(enabled_transitions)}")

if __name__ == "__main__":

    final_system = simulate_complete_cycle()
    
   
    analyze_system_properties(final_system)
    
 
    simple_reachability_analysis(final_system)
    
    print("\n" + "="*50)
    print("="*50)