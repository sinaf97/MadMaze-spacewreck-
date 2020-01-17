from src.Maze import Maze
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


class MazeSolver:
    def __init__(self, model):
        self.maze = model
        self.captains = [self.maze.lucky, self.maze.rocket]
        self.track = []
        self.graph_track = []

    def solve(self):
        attempts = 0
        while not self.maze.solved():
            if random.random() < 0.5:
                moving_captain = self.captains[0]
                controlling_captain_color = self.captains[1].current_node.color
            else:
                moving_captain = self.captains[1]
                controlling_captain_color = self.captains[0].current_node.color
            corridor_to_use = \
                random.choice(moving_captain.current_node.get_same_colored_corriders(controlling_captain_color))
            if corridor_to_use is None:
                attempts += 1
                if attempts == 20:
                    return False
                continue
            self.track.append(moving_captain.move(corridor_to_use))
            self.graph_track.append((model.lucky.current_node.id-1, model.rocket.current_node.id-1))
        return True

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
        labels[len(graph.nodes()) - 1] = 'end'
        nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_weight='bold')

        plt.axis('off')
        # plt.savefig(f'{i}.png')
        plt.show()


if __name__ == "__main__":
    model = Maze()
    model.get_data()
    maze_solver = MazeSolver(model)
    status = maze_solver.solve()
    while not status:
        model.rocket.set_current_node(model.nodes.get(model.rocket_start_point))
        model.lucky.set_current_node(model.nodes.get(model.lucky_start_point))
        maze_solver.track = []
        maze_solver.graph_track = []
        status = maze_solver.solve()
    for i in maze_solver.track:
        print(i)

    g = model.get_graph()
    counter = 1

    for i in maze_solver.graph_track:
        maze_solver.draw_graph(g, nx.kamada_kawai_layout(g), i, counter)
        counter += 1
        time.sleep(0.25)
    print("solved")


