from forest import Forest


# Create an edge between two pixels (x, y) and (x1, y1).
# Diff is the distance between two pixels, defined in 'main.py'.
def create_edge(img, width, x, y, x1, y1, diff):
    def vertex_id(x, y): return y * width + x
    w = diff(img, x, y, x1, y1)
    return vertex_id(x, y), vertex_id(x1, y1), w


# Build the graph with edges for each row and column of pixels in an image.
def build_graph(img, width, height, diff):
    graph_edges = []
    # For y = 0; y < height; y++...
    for y in range(height):
        # For x = 0; x < width; x++...
        for x in range(width):
            # Create edge from pixel (x, y) with (x - 1, y).
            if x > 0:
                graph_edges.append(create_edge(img, width, x, y, x - 1, y, diff))
            # Create edge from pixel (x, y) with (x, y - 1).
            if y > 0:
                graph_edges.append(create_edge(img, width, x, y, x, y - 1, diff))
            # Create edge with other pixels in diagonal directions.
            if x > 0 and y > 0:
                graph_edges.append(create_edge(img, width, x, y, x - 1, y - 1, diff))
            if x > 0 and y < height - 1:
                graph_edges.append(create_edge(img, width, x, y, x - 1, y + 1, diff))
    return graph_edges


# Merge two components only if its size (pixels) is larger than a pre-determined value.
def merge_components(forest, graph, min_size):
    for edge in graph:
        a = forest.find(edge[0])
        b = forest.find(edge[1])
        if a != b and (forest.size_of(a) < min_size or forest.size_of(b) < min_size):
            forest.merge(a, b)
    return forest


# Create a segmented graph. 'num_nodes' is the number of pixels (width * height) of the image.
def segment_graph(graph_edges, num_nodes, const, min_size, threshold_func):
    forest = Forest(num_nodes)
    def weight(weighted_edge): return weighted_edge[2]
    # Sort the graph edges by weight.
    sorted_graph = sorted(graph_edges, key=weight)
    threshold = [threshold_func(1, const) for _ in range(num_nodes)]
    for edge in sorted_graph:
        parent_a = forest.find(edge[0])
        parent_b = forest.find(edge[1])
        a_condition = weight(edge) <= threshold[parent_a]
        b_condition = weight(edge) <= threshold[parent_b]
        if parent_a != parent_b and a_condition and b_condition:
            forest.merge(parent_a, parent_b)
            a = forest.find(parent_a)
            threshold[a] = weight(edge) + threshold_func(forest.nodes[a].size, const)
    return merge_components(forest, sorted_graph, min_size)
