from algorithm_animation import AlgorithmAnimation


class BFSAnimation(AlgorithmAnimation):
    def __init__(self, graph):
        self.graph = graph
        self.start_node = None
        self.queue = []
        self.visited = []  # used in the algorithm and for drawing the visited nodes
        self.edges = []
        self.prev_nodes = []

    def set_start_node(self, node):
        self.start_node = node
        self.queue = [node]
        self.print_algorithm()

    def is_ended(self):
        return len(self.queue) == 0

    def one_step(self):
        # One step in the BFS algorithm

        if self.start_node is None:
            return

        if len(self.queue) > 0:
            node = self.queue.pop(0)

            self.visited.append(node)

            # Get the path from startnode to node
            for visited_node in self.visited:
                edge = self.graph.get_edge(visited_node, node)
                if edge:
                    self.edges.append(edge)
                    self.prev_nodes.append(node)
                    break

            for adj_node in self.graph.get_adjacent_nodes(node):
                if not adj_node in self.visited:
                    self.queue.append(adj_node)
                    self.visited.append(adj_node)
        else:
            # BFS Ended
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

        queue = [self.start_node]
        visited = []

        while len(queue) > 0:
            node = queue.pop(0)
            visited.append(node.id)

            ret.append(node.id)

            for adj_node in self.graph.get_adjacent_nodes(node):
                if not adj_node.id in visited:
                    queue.append(adj_node)
                    visited.append(adj_node.id)

        print("BFS result:", " -> ".join([str(i) for i in ret]))
