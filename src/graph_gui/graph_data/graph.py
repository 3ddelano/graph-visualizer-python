"""
File: graph.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""
import os
import heapq
from .interfaces.graph_interface import GraphInterface
from .node import Node
from .edge import Edge


class Graph(GraphInterface):
    def __init__(self):
        self.nodes = []
        self.edges = []

    # ----------
    # Node Methods
    # ----------

    def add_node(self, node):
        self.nodes.append(node)

    def delete_node(self, node_or_id):
        node = self.resolve_node(node_or_id)
        if node:
            self.nodes.remove(node)

    def get_adjacent_nodes(self, node_or_id):
        node = self.resolve_node(node_or_id)
        if not node:
            return []

        connected_nodes = []

        for edge in self.edges:
            if edge.nodeA == node:
                connected_nodes.append(edge.nodeB)
            elif edge.nodeB == node:
                connected_nodes.append(edge.nodeA)

        return connected_nodes

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    # ----------
    # Edge Methods
    # ----------

    def add_edge(self, edge):
        self.edges.append(edge)

    def update_edge_weight(self, edge_or_id, weight):
        edge = self.resolve_edge(edge_or_id)
        if edge:
            edge.weight = weight

    def delete_edge(self, edge_or_id):
        edge = self.resolve_edge(edge_or_id)
        self.edges.remove(edge)

    def get_adjacent_edges(self, node_or_id):
        node = self.resolve_node(node_or_id)
        if not node:
            return []

        connected_edges = []

        for edge in self.edges:
            if edge.nodeA == node or edge.nodeB == node:
                connected_edges.append(edge)

        return connected_edges

    def get_edge_by_id(self, edge_id):
        for edge in self.edges:
            if edge.id == edge_id:
                return edge
        return None

    def get_edge_between_nodes(self, nodeA_or_id, nodeB_or_id):
        nodeA = self.resolve_node(nodeA_or_id)
        nodeB = self.resolve_node(nodeB_or_id)
        if not nodeA or not nodeB:
            return None

        for edge in self.edges:
            if (edge.nodeA == nodeA and edge.nodeB == nodeB) or (
                edge.nodeA == nodeB and edge.nodeB == nodeA
            ):
                return edge
        return None

    # ----------
    # Pathfinding Methods
    # ----------

    def find_shortest_path(self, algorithm, start_node_or_id, end_node_or_id):
        found_path = self._get_shortest_path(
            algorithm, start_node_or_id, end_node_or_id
        )
        if found_path:
            return found_path["final_path"]

    def animate_shortest_path(self, algorithm, start_node_or_id, end_node_or_id):
        return self._get_shortest_path(algorithm, start_node_or_id, end_node_or_id)

    def _get_shortest_path(self, algorithm, start_node_or_id, end_node_or_id):
        start_node = self.resolve_node(start_node_or_id)
        end_node = self.resolve_node(end_node_or_id)

        if not start_node or not end_node:
            print("Invalid start or end node to find shortest path")
            return None

        if algorithm == "dijkstra":
            return self.dijkstra(start_node, end_node)
        elif algorithm == "astar":
            return self.astar(start_node, end_node)
        elif algorithm == "bfs":
            return self.bfs(start_node, end_node)
        elif algorithm == "dfs":
            return self.dfs(start_node, end_node)
        else:
            print("Invalid algorithm to find shortest path")
            return None

    def get_euclidean_distance(self, nodeA, nodeB):
        x1 = nodeA.pos[0]
        y1 = nodeA.pos[1]
        x2 = nodeB.pos[0]
        y2 = nodeB.pos[1]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_manhattan_distance(self, nodeA, nodeB):
        x1 = nodeA.pos[0]
        y1 = nodeA.pos[1]
        x2 = nodeB.pos[0]
        y2 = nodeB.pos[1]
        return abs(x1 - x2) + abs(y1 - y2)

    def dijkstra(self, start_node, end_node):
        dist = {}

        # Initialize distances to infinity
        for node in self.nodes:
            dist[node.id] = 1e7

        dist[start_node.id] = 0
        cur_node = start_node

        path = {}
        path[start_node.id] = None

        cur_node = start_node
        visited_nodes = []
        visited_edges = []
        while cur_node:
            visited_nodes.append(cur_node.id)
            for adj_node in self.get_adjacent_nodes(cur_node):
                if adj_node.id in visited_nodes:
                    continue
                edge = self.get_edge_between_nodes(cur_node, adj_node)
                visited_edges.append([cur_node.id, adj_node.id, edge])
                edge_cost = edge.weight

                # Relaxation
                if dist[cur_node.id] + edge_cost < dist[adj_node.id]:
                    dist[adj_node.id] = dist[cur_node.id] + edge_cost
                    path[adj_node.id] = cur_node.id
                else:
                    path[adj_node.id] = edge_cost

            # Find the next node to visit (the one with least cost from the starting node)
            dist_list = []
            for node_id, d in dist.items():
                if not node_id in visited_nodes:
                    dist_list.append([node_id, d])
            dist_list = sorted(dist_list, key=lambda x: x[1])

            if len(dist_list) == 0:
                cur_node = None
            else:
                cur_node_id = dist_list[0][0]
                cur_node = self.get_node_by_id(cur_node_id)

        return {
            "final_path": self.build_path(path, start_node, end_node),
            "visited_nodes": visited_nodes,
            "visited_edges": visited_edges,
        }

    def astar(self, start_node, end_node, heu_func="euclidean"):
        path = {}

        g_scores = {node.id: float("inf") for node in self.nodes}  # g_score
        g_scores[start_node.id] = 0

        # Straight line distance from any node to the end node
        heu = {}  # h_score
        if heu_func == "euclidean":
            heu = {
                node.id: self.get_euclidean_distance(node, end_node)
                for node in self.nodes
            }
        elif heu_func == "manhattan":
            heu = {
                node.id: self.get_manhattan_distance(node, end_node)
                for node in self.nodes
            }
        else:
            print("Invalid heuristic function in A*")
            raise Exception("Invalid heuristic function in A*")
        f_scores = {}
        f_scores[start_node.id] = g_scores[start_node.id] + heu[start_node.id]
        openset = []  # f_score stored in a min heap
        heapq.heappush(openset, (heu[start_node.id], start_node))

        visited_nodes = []
        visited_edges = []

        while len(openset) > 0:
            _f_score, current_node = heapq.heappop(openset)
            if current_node == end_node:
                # Reached the goal
                print("Reached the goal node in A*")
                return {
                    "final_path": self.build_path(path, start_node, end_node),
                    "visited_nodes": visited_nodes,
                    "visited_edges": visited_edges,
                }

            # Visiting the node with id=current_node.id
            visited_nodes.append(current_node.id)
            for node in self.get_adjacent_nodes(current_node.id):
                # Get the edge between cur_noed and each neighbour
                edge = self.get_edge_between_nodes(current_node.id, node.id)

                temp_g_score = g_scores[current_node.id] + edge.weight
                temp_f_score = temp_g_score + heu[node.id]

                visited_edges.append([current_node.id, node.id, edge])

                if node.id in visited_nodes and temp_f_score >= g_scores[node.id]:
                    continue

                if not node.id in visited_nodes or temp_f_score < f_scores[node.id]:
                    g_scores[node.id] = temp_g_score
                    f_scores[node.id] = temp_f_score
                    path[node.id] = current_node.id

                    if not (f_scores[node.id], node) in openset:
                        heapq.heappush(openset, (f_scores[node.id], node))

        # No path found
        print("No path found in A*")
        return {
            "final_path": [],
            "visited_nodes": visited_nodes,
            "visited_edges": visited_edges,
        }

    def bfs(self, start_node, end_node):
        visited_nodes = []
        visited_edges = []

        queue = []
        queue.append(start_node)
        path = {}
        while queue:
            cur_node = queue.pop(0)
            visited_nodes.append(cur_node.id)
            if cur_node == end_node:
                # Reached end node
                break

            for adj_node in self.get_adjacent_nodes(cur_node):
                if adj_node.id in visited_nodes:
                    continue

                edge = self.get_edge_between_nodes(cur_node, adj_node)
                visited_edges.append([cur_node.id, adj_node.id, edge])
                path[adj_node.id] = cur_node.id
                if adj_node == end_node:
                    queue = []
                    break
                queue.append(adj_node)

        return {
            "final_path": self.build_path(path, start_node, end_node),
            "visited_nodes": visited_nodes,
            "visited_edges": visited_edges,
        }

    def dfs(self, start_node, end_node):
        visited_nodes = []
        visited_edges = []

        stack = []
        stack.append(start_node)
        path = {}
        while stack:
            cur_node = stack[-1]
            stack.pop()

            if not cur_node.id in visited_nodes:
                for visited_node_id in visited_nodes:
                    edge = self.get_edge_between_nodes(
                        cur_node, self.get_node_by_id(visited_node_id)
                    )
                    if edge:
                        visited_edges.append([visited_node_id, cur_node.id, edge])
                        path[cur_node.id] = visited_node_id

                visited_nodes.append(cur_node.id)
                if cur_node.id == end_node.id:
                    stack = []
                    break

                for adj_node in self.get_adjacent_nodes(cur_node):
                    if adj_node.id in visited_nodes:
                        continue
                    stack.append(adj_node)

        print("Visited nodes: ", [str(node_id) for node_id in visited_nodes])

        return {
            "final_path": self.build_path(path, start_node, end_node),
            "visited_nodes": visited_nodes,
            "visited_edges": visited_edges,
        }

    def build_path(self, path, start_node, end_node):
        current_node = end_node
        path_list = []
        current_node_id = current_node.id
        start_node_id = start_node.id

        while current_node_id and current_node_id != start_node_id:
            path_list.append(current_node_id)
            current_node_id = path[current_node_id]
        path_list.append(start_node_id)
        path_list.reverse()

        edge_path = []
        if len(path_list) < 2:
            return None

        # Find the edge between every 2 adjacent nodes in path_list
        for i in range(len(path_list) - 1):
            edge = self.get_edge_between_nodes(path_list[i], path_list[i + 1])
            edge_path.append(edge)

        ret = []
        for i in range(len(path_list)):
            if i == 0:
                ret.append([path_list[i], None])
            else:
                ret.append([path_list[i], edge_path[i - 1]])

        return ret

    # ----------
    # Misc Methods
    # ----------

    def save_to_files(self, nodelist_path, edgelist_path):
        # Save the list of nodes to a csv file
        print(f"Saving graph to {nodelist_path} and {edgelist_path}")

        try:
            with open(nodelist_path, "w") as file:
                for i, node in enumerate(self.nodes):
                    # id,x,y
                    line = f"{node.id},{node.pos[0]},{node.pos[1]}"
                    if i != len(self.nodes) - 1:
                        line += "\n"

                    file.write(line)

            with open(edgelist_path, "w") as file:
                for i, edge in enumerate(self.edges):
                    # id,nodeA_id,nodeB_id,weight
                    line = f"{edge.id},{edge.nodeA.id},{edge.nodeB.id},{edge.weight}"
                    if i != len(self.edges) - 1:
                        line += "\n"

                    file.write(line)
            return True
        except Exception as e:
            return False

    def load_from_files(self, nodelist_path, edgelist_path):
        # Load nodes and edges from nodelist_path and edgelist_path
        if not os.path.exists(nodelist_path) or not os.path.exists(edgelist_path):
            print(
                f"Load Graph Error: No {nodelist_path} and {edgelist_path} files found"
            )
            return
        print(f"Loading graph from {nodelist_path} and {edgelist_path}")

        self.nodes = []
        self.edges = []
        with open(nodelist_path, "r") as file:
            for line in file:
                # id,x,y
                line = line.strip().split(",")
                node = Node(int(line[0]), float(line[1]), float(line[2]))
                self.add_node(node)

        with open(edgelist_path, "r") as file:
            for line in file:
                # id,nodeA_id,nodeB_id,weight?
                line = line.strip().split(",")
                nodeA = self.get_node_by_id(int(line[1]))
                nodeB = self.get_node_by_id(int(line[2]))
                weight = 1.0
                if len(line) >= 4:
                    weight = float(line[3])
                edge = Edge(int(line[0]), nodeA, nodeB, weight)
                self.add_edge(edge)

    def resolve_node(self, node_or_id):
        node = None
        if isinstance(node_or_id, int):
            node = self.get_node_by_id(node_or_id)
        if isinstance(node_or_id, float):
            node = self.get_node_by_id(int(node_or_id))
        elif isinstance(node_or_id, Node):
            node = node_or_id

        return node

    def resolve_edge(self, edge_or_id):
        edge = None
        if isinstance(edge_or_id, int):
            edge = self.get_edge_by_id(edge_or_id)
        elif isinstance(edge_or_id, Edge):
            edge = edge_or_id

        return edge
