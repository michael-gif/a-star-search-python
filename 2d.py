import math


# to make this algorithm work in 3d space, a z component is introduced into each node. this is the only major change


class Node:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None


def compare_tuple(t1, t2):
    if t1[0] == t2[0] and t1[1] == t2[1]:
        return True
    else:
        return False


'''
0 = traversable node
1 = start node
2 = end node
3 = non-traversable node (a wall)
'''
maze = [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 0, 3, 3, 0, 0, 0],
        [3, 0, 0, 0, 3, 0, 0, 0],
        [3, 0, 0, 0, 3, 0, 0, 0],
        [3, 1, 0, 0, 3, 0, 0, 0],
        [3, 3, 3, 3, 3, 0, 0, 0]]

start = (0, 0)
end = (0, 0)
walls = []
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 1:
            start = (x, y)
        elif maze[y][x] == 2:
            end = (x, y)
        elif maze[y][x] == 3:
            walls.append((x, y))


def search(start, end):
    open_list = [Node(start)]
    closed_list = []
    found_end = False

    while open_list and not found_end:
        # get lowest node
        open_list.sort(key=lambda node: node.f)
        lowest_node = open_list.pop(0)
        # generate child nodes
        children = [
            Node((lowest_node.x - 1, lowest_node.y)),
            Node((lowest_node.x + 1, lowest_node.y)),
            Node((lowest_node.x, lowest_node.y + 1)),
            Node((lowest_node.x, lowest_node.y - 1))
        ]
        # get rid of un-traversable nodes
        i = 0
        while i < len(children):
            if children[i].pos in walls:
                children.pop(i)
                i = 0
            else:
                i += 1
        # do the stuff a* does
        i = 0
        while i < len(children):
            child = children[i]
            child.parent = lowest_node
            found_end = False
            if compare_tuple(child.pos, end):
                closed_list.append(child)
                found_end = True
                break
            child.g = lowest_node.g + math.dist(child.pos, lowest_node.pos)
            child.h = math.dist(child.pos, end)
            child.f = child.g + child.h
            skip_child = False
            for open_node in open_list:
                if compare_tuple(open_node.pos, child.pos) and open_node.f < child.f:
                    skip_child = True
            for closed_node in closed_list:
                if compare_tuple(closed_node.pos, child.pos) and closed_node.f < child.f:
                    skip_child = True
            if not skip_child:
                open_list.append(child)
            closed_list.append(lowest_node)
            i += 1

    # find end node in closed_list
    path = []
    for node in closed_list:
        if compare_tuple(node.pos, end):
            path.append(node)
    if not path:
        print(f"No path from {start} to {end} exists")
    else:
        # backtrack from end node and find path
        parent = path[-1].parent
        while parent is not None:
            path.append(parent)
            parent = parent.parent
        path.reverse()
        print([node.pos for node in path])


search(start, end)
