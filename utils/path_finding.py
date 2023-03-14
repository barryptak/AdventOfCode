"""
Path finding helpers for Advent of Code problems.
"""

import math

def dijkstra(start_node, nodes, edges):
    """
    Calculates the shortest distance from start_node to every node in nodes.
    edges is a tuple of (dest_node, edge_cost).
    """

    # Helper function to pop the node with the smallest dist value
    # from the queue
    def pop_smallest_dist(queue, dist):
        filtered_dist = {k: v for k, v in dist.items() if k in queue}
        min_dist = min(filtered_dist, key=filtered_dist.get)
        queue.remove(min_dist)
        return min_dist

    node_queue = []
    dist = {}
    prev = {}

    # Initialise our data
    for node in nodes:
        dist[node] = math.inf
        prev[node] = None
        node_queue.append(node)
    dist[start_node] = 0

    # Iterate over every node in our queue pulling out the least expensive to
    # get to first. This ensure that when we encounter more expensive nodes
    # later we might already have found a cheaper path to them through other
    # nodes previously processed
    while len(node_queue) > 0:
        current_node = pop_smallest_dist(node_queue, dist)

        # Iterate through all nodes that you can travel to from current_node
        for node in [edge for edge in edges[current_node] if edge[0] in node_queue]:
            # Determine the cost to traverse to node via current_node
            alt = dist[current_node] + node[1]
            # If this cost is less than the current lowest cost to get to node
            # then update the lowest cost and prev values for node
            if alt < dist[node[0]]:
                dist[node[0]] = alt
                prev[node[0]] = current_node

    # We now have the lowest cost for travelling to all nodes from start_node
    # and the paths to get there
    return dist, prev


def astar_path_length(start_list, goal, dist_heuristic, get_neighbours):
    """
    Returns the shortest path length from any start pos to the end pos.
    Implements A*
    """
    open_set = set(start_list)
    came_from = {}
    g = {s : 0 for s in start_list}
    f = {s : dist_heuristic(s, goal) for s in start_list}

    while len(open_set) > 0:
        # Pull the pos from the open set that we think is closest to the goal
        pos = sorted(open_set, key = lambda p: f[p])[0]

        # Have we reached the goal?
        if pos == goal:
            # Calculate the length of this path and return it
            path_length = 0
            # Walk backwards from pos pulling out the previous position that
            # got us here. Keep going until we've completed the path backwards
            # so that there's no predecessor left.
            while pos in came_from:
                pos = came_from[pos]
                path_length += 1
            return path_length

        open_set.remove(pos)

        # Examine all of the valid neighbours of pos
        for neighbour in get_neighbours(pos):
            # Is the path from pos to neighbour the cheapest one so far?
            tentative_g = g[pos] + 1
            neighbour_g = g[neighbour] if neighbour in g else math.inf
            if tentative_g < neighbour_g:
                # Pos -> neighbour is the cheapest path we've found to neighbour
                # so far.
                # Update come_from to indicate that the best path to neighbour
                # is from pos.
                # Update the heuristic scores for neighbour and add it to the
                # open set.
                came_from[neighbour] = pos
                g[neighbour] = tentative_g
                f[neighbour] = tentative_g + dist_heuristic(neighbour, goal)
                if neighbour not in open_set:
                    open_set.add(neighbour)

    # No path found :(
    return None
