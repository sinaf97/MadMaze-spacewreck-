from src.Maze import Maze
import copy
import time
import networkx as nx


class MazeSolver:
    def __init__(self, model):
        self.maze = model
        self.captains = [self.maze.lucky, self.maze.rocket]
        self.track = []
        self.visited = []
        self.frontier = [(self.maze.rocket_start_point, self.maze.lucky_start_point, None, None), ]

    def solve(self):
        while len(self.frontier):
            """ Check model """
            if self.maze.solved():
                self.track = self.get_track(front)  # Fetching the path to the root
                self.print_track()                  # Printing the path to Goal
                self.animate_route()                # Animating the solution
                return
            """ End of Check model """

            """ BFS Algorithm """
            front = self.frontier.pop(0)
            self.maze.apply(front)  # Moves captains to the front nodes
            self.frontier += [(i[0].id, i[1].id, front[0], front[1]) for i in self.maze.create_child_nodes() if i not
                              in self.visited]
            self.visited.append(front)
            """ End of BFS Algorithm """

        print("No Solution")
        return

    def get_track(self, front):
        result = []
        while front[3] is not None:
            for i in self.visited:
                if (i[0], i[1]) == (front[2], front[3]):
                    result.append((front[0], front[1]))
                    front = i
                    break
        result.append((front[0], front[1]))
        result.reverse()
        return result

    def print_track(self):
        track = copy.deepcopy(self.track)
        s1 = track.pop(0)
        while track:
            s2 = track.pop(0)
            if s2[0] == s1[0]:
                print(f"L {s2[1]}      // Lucky to {self.maze.nodes.get(s2[1]).name}")
            else:
                print(f"R {s2[0]}      // Rocket to {self.maze.nodes.get(s2[0]).name}")
            s1 = s2

    def animate_route(self):
        g = self.maze.get_graph()
        counter = 1
        for i in self.track:
            self.maze.draw_graph(g, nx.kamada_kawai_layout(g), i, counter)
            counter += 1
            time.sleep(1)


if __name__ == "__main__":
    model = Maze()          # Creating our model
    model.get_data()        # Initiating out model
    maze_solver = MazeSolver(model)
    maze_solver.solve()     # Solve our model


