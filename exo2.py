import matplotlib.pyplot as plt
from collections import deque
 
class PetriNet:
    def __init__(self, places, transitions, pre, post, initial_marking):
        self.places = places
        self.transitions = transitions
        self.pre = pre
        self.post = post
        self.initial_marking = initial_marking
 
    def is_enabled(self, marking, transition):
        for place in self.pre.get(transition, {}):
            if marking.get(place, 0) < self.pre[transition][place]:
                return False
        return True
 
    def fire(self, marking, transition):
        new_marking = marking.copy()
        for place in self.places:
            pre_val = self.pre.get(transition, {}).get(place, 0)
            post_val = self.post.get(transition, {}).get(place, 0)
            new_val = marking.get(place, 0) - pre_val + post_val
            new_marking[place] = max(new_val, 0)
        return new_marking
 
    def marking_to_tuple(self, marking):
        return tuple(marking.get(p, 0) for p in self.places)
 
    def marking_str(self, marking):
        return "(" + ", ".join(f"{p}:{marking.get(p,0)}" for p in self.places) + ")"
 
    def generate_positions(self, nodes, edges):
        from collections import defaultdict
        levels = defaultdict(list)
        root = nodes[0][0]
        dist = {root:0}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for (src, dst, _) in edges:
                if src == u and dst not in dist:
                    dist[dst] = dist[u] + 1
                    queue.append(dst)
 
        max_level = max(dist.values())
        level_nodes = defaultdict(list)
        for nid, label in nodes:
            lvl = dist.get(nid, max_level)
            level_nodes[lvl].append((nid, label))
 
        positions = {}
        for lvl in range(max_level+1):
            n = len(level_nodes[lvl])
            for i, (nid, _) in enumerate(level_nodes[lvl]):
                x = i - n/2
                y = -lvl
                positions[nid] = (x, y)
        return positions
 
    def draw_graph(self, nodes, edges, positions):
        fig, ax = plt.subplots(figsize=(12,8))
 
        # Dessiner les arêtes (flèches)
        for (src, dst, label) in edges:
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            ax.annotate("",
                        xy=(x2, y2), xycoords='data',
                        xytext=(x1, y1), textcoords='data',
                        arrowprops=dict(arrowstyle="->", color='blue'))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, label, color='red', fontsize=9)
 
        # Dessiner les nœuds
        for (nid, label) in nodes:
            x, y = positions[nid]
            ax.plot(x, y, 'o', color='orange', markersize=15)
            ax.text(x, y, label, fontsize=10, ha='center', va='center', color='black')
 
        ax.axis('off')
        plt.title("Arborescence des états atteignables - Réseau borné")
        plt.show()
 
    def reachable_states_borne(self):
        visited = set()
        to_visit = deque()
        to_visit.append(self.initial_marking)
 
        nodes = []
        edges = []
 
        while to_visit:
            current = to_visit.popleft()
            current_id = self.marking_to_tuple(current)
            if current_id in visited:
                continue
            visited.add(current_id)
            nodes.append((current_id, self.marking_str(current)))
 
            for t in self.transitions:
                if self.is_enabled(current, t):
                    next_marking = self.fire(current, t)
                    next_id = self.marking_to_tuple(next_marking)
                    edges.append((current_id, next_id, t))
                    if next_id not in visited:
                        to_visit.append(next_marking)
 
        positions = self.generate_positions(nodes, edges)
        self.draw_graph(nodes, edges, positions)
 
# Exemple d'utilisation
if __name__ == "__main__":
    places = ['p1', 'p2']
    transitions = ['t1', 't2']
    pre = {
        't1': {'p1': 1},
        't2': {'p2': 1}
    }
    post = {
        't1': {'p2': 1},
        't2': {'p1': 1}
    }
    initial_marking = {'p1': 1, 'p2': 0}
 
    net = PetriNet(places, transitions, pre, post, initial_marking)
    net.reachable_states_borne()



    import matplotlib.pyplot as plt

from collections import deque
 
OMEGA = float('inf')
 
class PetriNet:

    def __init__(self, places, transitions, pre, post, initial_marking):

        self.places = places

        self.transitions = transitions

        self.pre = pre

        self.post = post

        self.initial_marking = initial_marking
 
    def is_enabled(self, marking, transition):

        for place in self.pre.get(transition, {}):

            val = marking.get(place, 0)

            req = self.pre[transition][place]

            if val != OMEGA and val < req:

                return False

        return True
 
    def fire(self, marking, transition):

        new_marking = marking.copy()

        for place in self.places:

            pre_val = self.pre.get(transition, {}).get(place, 0)

            post_val = self.post.get(transition, {}).get(place, 0)

            val = marking.get(place, 0)

            if val == OMEGA:

                new_marking[place] = OMEGA

            else:

                new_val = val - pre_val + post_val

                new_marking[place] = max(new_val, 0)

        return new_marking
 
    def less_or_equal(self, m1, m2):

        """Test m1 ≤ m2 avec OMEGA : ω ≥ n pour tout n."""

        for p in self.places:

            v1 = m1.get(p, 0)

            v2 = m2.get(p, 0)

            if v1 == OMEGA:

                if v2 != OMEGA:

                    return False

            else:

                if v2 != OMEGA and v1 > v2:

                    return False

        return True
 
    def greater_than(self, m1, m2):

        """Test strict m1 > m2."""

        geq = True

        strict = False

        for p in self.places:

            v1 = m1.get(p, 0)

            v2 = m2.get(p, 0)

            if v1 == OMEGA:

                if v2 != OMEGA:

                    strict = True

            else:

                if v2 == OMEGA:

                    return False

                elif v1 < v2:

                    return False

                elif v1 > v2:

                    strict = True

        return geq and strict
 
    def omega_covering(self, new_marking, visited_markings):

       

        updated = False

        for old in visited_markings:

            if self.less_or_equal(old, new_marking) and self.greater_than(new_marking, old):

                # on remplace dans new_marking les places où new_marking > old par ω

                for p in self.places:

                    v_new = new_marking.get(p,0)

                    v_old = old.get(p,0)

                    if v_new != OMEGA and (v_old == OMEGA or v_new > v_old):

                        new_marking[p] = OMEGA

                        updated = True

        return new_marking, updated
 
    def marking_to_tuple(self, marking):

        return tuple(OMEGA if marking.get(p,0) == OMEGA else marking.get(p,0) for p in self.places)
 
    def marking_str(self, marking):

        def val_str(v):

            return 'ω' if v == OMEGA else str(v)

        return "(" + ", ".join(f"{p}:{val_str(marking.get(p,0))}" for p in self.places) + ")"
 
    def generate_positions(self, nodes, edges):

        from collections import defaultdict

        levels = defaultdict(list)

        root = nodes[0][0]

        dist = {root:0}

        queue = deque([root])

        while queue:

            u = queue.popleft()

            for (src, dst, _) in edges:

                if src == u and dst not in dist:

                    dist[dst] = dist[u] + 1

                    queue.append(dst)
 
        max_level = max(dist.values()) if dist else 0

        level_nodes = defaultdict(list)

        for nid, label in nodes:

            lvl = dist.get(nid, max_level)

            level_nodes[lvl].append((nid, label))
 
        positions = {}

        for lvl in range(max_level+1):

            n = len(level_nodes[lvl])

            for i, (nid, _) in enumerate(level_nodes[lvl]):

                x = i - n/2

                y = -lvl

                positions[nid] = (x, y)

        return positions
 
    def draw_graph(self, nodes, edges, positions):

        fig, ax = plt.subplots(figsize=(12,8))
 
        for (src, dst, label) in edges:

            x1, y1 = positions[src]

            x2, y2 = positions[dst]

            ax.annotate("",

                        xy=(x2, y2), xycoords='data',

                        xytext=(x1, y1), textcoords='data',

                        arrowprops=dict(arrowstyle="->", color='blue'))

            mx, my = (x1 + x2) / 2, (y1 + y2) / 2

            ax.text(mx, my, label, color='red', fontsize=9)
 
        for (nid, label) in nodes:

            x, y = positions[nid]

            ax.plot(x, y, 'o', color='orange', markersize=15)

            ax.text(x, y, label, fontsize=10, ha='center', va='center', color='black')
 
        ax.axis('off')

        plt.title("Arborescence des états atteignables - Réseau non borné")

        plt.show()
 
    def reachable_states_non_borne(self):

        visited = []

        to_visit = deque()

        to_visit.append(self.initial_marking)
 
        nodes = []

        edges = []
 
        while to_visit:

            current = to_visit.popleft()

           

            for i, v in enumerate(visited):

                new_marking, updated = self.omega_covering(current.copy(), [v])

                if updated:

                    current = new_marking

            current_id = self.marking_to_tuple(current)

            if current_id in [self.marking_to_tuple(m) for m in visited]:

                continue

            visited.append(current)

            nodes.append((current_id, self.marking_str(current)))
 
            for t in self.transitions:

                if self.is_enabled(current, t):

                    next_marking = self.fire(current, t)


                    for v in visited:

                        next_marking, _ = self.omega_covering(next_marking, [v])

                    next_id = self.marking_to_tuple(next_marking)

                    edges.append((current_id, next_id, t))

                    if next_id not in [self.marking_to_tuple(m) for m in visited]:

                        to_visit.append(next_marking)
 
        positions = self.generate_positions(nodes, edges)

        self.draw_graph(nodes, edges, positions)
 


if __name__ == "__main__":

    places = ['p1', 'p2']

    transitions = ['t1', 't2']

    pre = {

        't1': {'p1': 1},

        't2': {'p2': 1}

    }

    post = {

        't1': {'p1': 1, 'p2': 1},  # t1 ajoute un jeton dans p2 (augmentation possible)

        't2': {'p2': 0}

    }

    initial_marking = {'p1': 1, 'p2': 0}
 
    net = PetriNet(places, transitions, pre, post, initial_marking)

    net.reachable_states_non_borne()

 