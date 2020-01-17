import collections
import networkx as nx


class Maze:
    def __init__(self):
        self.rocket = Captain("rocket")
        self.rocket_start_point = None
        self.lucky = Captain("lucky")
        self.lucky_start_point = None
        self.goal = None
        self.nodes = collections.OrderedDict()
        self.edges = []
        self.track = []

    def get_data(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE',  'AF',  'AG',  'AH',  'AI',  'AJ',  'AK']
        n, m = [int(i) for i in input().split()]
        colors = input().split()
        for i in range(n-1):
            self.nodes[i+1] = Node(i+1, alphabet.pop(0), colors.pop(0))
        self.nodes[n] = Node(n, alphabet.pop(0), None)
        self.goal = self.nodes.get(n)
        self.rocket_start_point, self.lucky_start_point = [int(i) for i in input().split()]
        self.rocket.set_current_node(self.nodes.get(self.rocket_start_point))
        self.lucky.set_current_node(self.nodes.get(self.lucky_start_point))
        for _ in range(m):
            data = input().split()
            n1, n2 = self.nodes.get(int(data[0])), self.nodes.get(int(data[1]))
            temp = Corridor(n1, n2, data[2])
            n1.add_corridor(temp)
            self.edges.append((int(data[0]), int(data[1]), {'color': data[2]}))

    def solved(self):
        if self.lucky.current_node == self.goal or self.rocket.current_node == self.goal:
            return True
        return False

    def get_graph(self):
        g = nx.DiGraph()
        for i in self.nodes.values():
            if i.color is not None:
                g.add_node(i.id-1, color=i.color)
            else:
                g.add_node(i.id-1, color='W')
        for i in self.edges:
            g.add_edge(i[0]-1, i[1]-1, color=i[2])
        return g

    def get_nodes(self):
        result = []
        for i in self.nodes.values():
            result.append(i.name)
        return result


class Node:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.corridors = []

    def add_corridor(self, corridor):
        self.corridors.append(corridor)

    def get_same_colored_corriders(self, color):
        result = []
        for i in self.corridors:
            if i.color == color:
                result.append(i)
        return result if result != [] else [None]

    def __str__(self):
        return f"{self.name} with color of {self.color}"


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

    def move(self, corridor):
        self.current_node = corridor.destination
        return f"{self.name} moved to {self.current_node}"
