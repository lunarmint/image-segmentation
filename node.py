class Node:
    # Disjoint nodes (singleton) where each node is a parent by itself and are all equal in rank and size.
    # Represents a pixel.
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank
        self.size = size

    # To String.
    def __repr__(self):
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)
