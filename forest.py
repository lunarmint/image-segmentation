from node import Node


# A disjoint forest containing multiple MST(s). Each tree is a set representing a component of the image.
# Disjoint forest is a faster implementation to represent segmentation as described in the paper.
class Forest:
    # Return the size of node i in nodes[].
    def size_of(self, i):
        return self.nodes[i].size

    def find(self, n):
        temp = n
        while temp != self.nodes[temp].parent:
            temp = self.nodes[temp].parent
        self.nodes[n].parent = temp
        return temp

    # Merge two nodes into a new node with increased size (# of nodes) if either node rank is larger than the other one.
    # If ranks are equal then increment b rank (only happens the very first time merge() is called).
    # For each nodes merged, decrement the set count.
    # https://www.youtube.com/watch?v=Qijjibpg4m8
    def merge(self, a, b):
        if self.nodes[a].rank > self.nodes[b].rank:
            self.nodes[b].parent = a
            self.nodes[a].size = self.nodes[a].size + self.nodes[b].size
        else:
            self.nodes[a].parent = b
            self.nodes[b].size = self.nodes[b].size + self.nodes[a].size
            if self.nodes[a].rank == self.nodes[b].rank:
                self.nodes[b].rank += 1
        self.num_sets -= 1

    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_sets = num_nodes
