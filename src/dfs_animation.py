from algorithm_animation import AlgorithmAnimation


class DFSAnimation(AlgorithmAnimation):
    def __init__(self, graph):
        self.graph = graph
        self.start_node = None
        self.stack = []  # used in the algorithm
        self.visited = []  # used in the algorithm and for drawing the visited nodes
        self.edges = []
        self.prev_nodes = []

    def set_start_node(self, node):
        self.start_node = node
        # Print the entire DFS
        self.print_algorithm()

    def is_ended(self):
        return self.start_node is None and len(self.stack) == 0

    def one_step(self):
        # One step in the DFS algorithm
        if self.start_node is None:
            return

        # Dfs
        if not self.start_node in self.visited:
            self.stack.append(self.start_node)
        if len(self.stack) > 0:
            node = self.stack[-1]
            self.stack.pop()

            if not node in self.visited:
                self.start_node = node
                for visited in self.visited:
                    edge = self.graph.get_edge(visited, node)
                    if edge:
                        self.edges.append(edge)
                        self.prev_nodes.append(node)
                self.visited.append(node)

            for neighbour in self.graph.get_adjacent_nodes(node):
                if not neighbour in self.visited:
                    self.stack.append(neighbour)
        else:
            self.start_node = None

    def get_drawn_nodes(self):
        ret = []

        if self.start_node:
            ret.append({
                "node": self.start_node,
                "color": "#0f0"
            })

        length = len(self.prev_nodes)
        if length > 1:
            for i in range(length - 1):
                ret.append({
                    "node": self.prev_nodes[i],
                    "color": "#f00"
                })

        if length > 0:
            ret.append({
                "node": self.prev_nodes[-1],
                "color": "#ff0"
            })

        return ret

    def get_drawn_edges(self):
        ret = []

        length = len(self.edges)
        if length > 1:
            for i in range(length - 1):
                ret.append({
                    "edge": self.edges[i],
                    "color": "#f0f"
                })

        if length > 0:
            ret.append({
                "edge": self.edges[-1],
                "color": "#ff0"
            })

        return ret

    def print_algorithm(self):

        ret = []
        visited = []
        stack = [self.start_node]

        while len(stack) > 0:
            node = stack[-1]
            stack.pop()

            if not node.id in visited:
                ret.append(node.id)
                visited.append(node.id)

            for neighbour in self.graph.get_adjacent_nodes(node):
                if not neighbour.id in visited:
                    stack.append(neighbour)

        print("DFS result:", " -> ".join([str(i) for i in ret]))
