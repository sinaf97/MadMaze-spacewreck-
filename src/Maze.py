import collections
import networkx as nx
import matplotlib.pyplot as plt


class Maze:
    """Main class for our maze"""
    def __init__(self):
        self.rocket = Captain("Rocket")
        self.rocket_start_point = None
        self.lucky = Captain("Lucky")
        self.lucky_start_point = None
        self.goal = None
        self.nodes = collections.OrderedDict()
        self.edges = []
        self.track = []

    def get_data(self):
        """ data fetch from File """
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE',  'AF',  'AG',  'AH',  'AI',  'AJ',  'AK']
        with open('input.txt') as f:
            n, m = [int(i) for i in f.readline().split()]
            colors = f.readline().split()
            for i in range(n-1):
                self.nodes[i+1] = Node(i+1, alphabet.pop(0), colors.pop(0))
            self.nodes[n] = Node(n, 'Goal', None)
            self.goal = self.nodes.get(n)
            self.rocket_start_point, self.lucky_start_point = [int(i) for i in f.readline().split()]
            self.rocket.set_current_node(self.nodes.get(self.rocket_start_point))
            self.lucky.set_current_node(self.nodes.get(self.lucky_start_point))
            for _ in range(m):
                data = f.readline().split()
                n1, n2 = self.nodes.get(int(data[0])), self.nodes.get(int(data[1]))
                temp = Corridor(n1, n2, data[2])
                n1.add_corridor(temp)
                self.edges.append((int(data[0]), int(data[1]), {'color': data[2]}))

    def get_nodes(self):
        """ returns all the nodes """
        result = []
        for i in self.nodes.values():
            result.append(i.name)
        return result

    def create_child_nodes(self):
        moving_captain = self.rocket
        result = []
        controlling_captain_color = self.lucky.current_node.color
        corridors_to_use = moving_captain.current_node.get_same_colored_corridors(controlling_captain_color)
        if corridors_to_use is not None:
            result = [(i.destination, self.lucky.current_node) for i in corridors_to_use]
        moving_captain = self.lucky
        controlling_captain_color = self.rocket.current_node.color
        corridors_to_use = moving_captain.current_node.get_same_colored_corridors(controlling_captain_color)
        if corridors_to_use is not None:
            result += [(self.rocket.current_node, i.destination) for i in corridors_to_use]
        return result

    def apply(self, front):
        self.rocket.move2(self.nodes.get(front[0]))
        self.lucky.move2(self.nodes.get(front[1]))

    def solved(self):
        """ test to see whether the maze is solved or not """
        if self.lucky.current_node == self.goal or self.rocket.current_node == self.goal:
            return True
        return False

    def get_graph(self):
        """ returns the graph related to the current state """
        g = nx.DiGraph()
        for i in self.nodes.values():
            if i.color is not None:
                g.add_node(i.id, color=i.color)
            else:
                g.add_node(i.id, color='W')
        for i in self.edges:
            g.add_edge(i[0], i[1], color=i[2])
        return g

    @staticmethod
    def draw_graph(graph, pos, captains_position, i):
        # all colors, white for end node
        colors = ('B', 'R', 'Y', 'G', 'W')
        plt.style.use(['dark_background'])
        # size of plot
        plt.figure(figsize=(8, 8), dpi=100)

        # draw nodes
        colored_nodes = {}
        nodes_sizes = {}
        for color in colors:
            nodes_sizes[color] = []
            colored_nodes[color] = []
        for node in graph.nodes():
            nodes_sizes[graph.nodes[node]['color']].append(1000 if node in captains_position else 250)
            colored_nodes[graph.nodes[node]['color']].append(node)
        for col in colored_nodes:
            nx.draw_networkx_nodes(graph, pos,
                                   nodelist=colored_nodes[col],
                                   node_color=col, node_size=nodes_sizes[col], alpha=0.9)

        # draw edges
        colored_edges = {}
        for color in colors:
            colored_edges[color] = []
        for edge in graph.edges:
            colored_edges[graph.edges[edge]['color']['color']].append(edge)
        for col in colored_edges:
            nx.draw_networkx_edges(graph, pos,
                                   edgelist=colored_edges[col],
                                   width=3, alpha=0.9, edge_color=col)
        # draw network labels
        labels = {}
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK']
        for node in graph.nodes():
            # label according to PDF problem statement node labeling standard
            labels[node] = alphabet.pop(0)
            # the FINAL NODE is WHITE and labeled as END
        labels[len(graph.nodes()) - 1] = 'Goal'
        nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_weight='bold')
        plt.axis('off')

        plt.show()
        # plt.savefig(f'{i}.png')


class Node:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.corridors = []

    def add_corridor(self, corridor):
        self.corridors.append(corridor)

    def get_same_colored_corridors(self, color):
        result = []
        for i in self.corridors:
            if i.color == color:
                result.append(i)
        return result if result != [] else None

    def __str__(self):
        return f"{self.name}"


class Corridor:
    def __init__(self, origin, destination, color):
        self.origin = origin
        self.destination = destination
        self.color = color


class Captain:
    def __init__(self, name):
        self.name = name
        self.current_node = None

    def set_current_node(self, node):
        self.current_node = node

    def move2(self, destination):
        self.current_node = destination
