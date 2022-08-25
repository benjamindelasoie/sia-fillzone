import numpy as np
import node

colors = 5
dim = 6

# arrays para movernos hacia los bloques adyacentes
# index = 0 ---> ARRIBA
# index = 1 ---> IZQUIERDA
# index = 2 ---> DERECHA
# index = 3 ---> ABAJO
row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]


# devuelve una matriz con 1's donde se ubica nuestra isla principal
def get_main_island_rec(matrix, visited, i, j, color):
    if i < 0 or j < 0 or i >= dim or j >= dim or visited[i][j]:
        return visited

    if matrix[i][j] == color:
        visited[i][j] = True
        new_visited = visited

        for k in range(4):
            new_visited = get_main_island_rec(matrix, new_visited, i + row[k], j + col[k], color)

        return new_visited

    return visited


# cambia el color de la isla principal
def change_color(matrix, visited, color):
    for i in range(dim):
        for j in range(dim):
            if visited[i][j]:
                matrix[i][j] = color
    return matrix


def is_goal(node):
    for i in range(dim):
        for j in range(dim):
            if node.state[i][j] != node.color:
                return False
    return True


def is_insignificant_move(visited, new_visited):
    for i in range(dim):
        for j in range(dim):
            if visited[i][j] != new_visited[i][j]:
                return False
    return True


# armo una cola y voy sacando el nodo que hace más tiempo se encuentra en la cola
def bfs(root):
    queue = [root]

    while queue:
        actual_node = queue.pop(0)
        if is_goal(actual_node):
            print('GOAL')
            print(actual_node.state)
            return actual_node

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = change_color(actual_node.state, actual_node.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island = get_main_island_rec(new_state, blank_matrix, 0, 0, color)
                if not is_insignificant_move(actual_node.visited, main_island):
                    print('                 ')
                    print(new_state)
                    new_node = node.Node(new_state, main_island, actual_node.cost + 1, actual_node, color)
                    queue.append(new_node)


def dfs(actual_node):
    if is_goal(actual_node):
        return actual_node
    for color in range(colors):
        if color != actual_node.color:
            new_state = change_color(actual_node.state, actual_node.visited, color)
            new_node = node.Node(new_state, false , actual_node.cost + 1, node, color)
            dfs(new_node)


def dfs_non_recursive(graph, source):
    if source is None or source not in graph:
        return "Invalid input"
    path = []
    stack = [source]
    while (len(stack) != 0):
        s = stack.pop()
        if s not in path:
            path.append(s)
        if s not in graph:
            # leaf node
            continue
        for neighbor in graph[s]:
            stack.append(neighbor)
    return " ".join(path)


def recursive_dfs(graph, source, path=[]):
    if source not in path:
        path.append(source)
        if source not in graph:
            # leaf node, backtrack
            return path
        for neighbour in graph[source]:
            path = recursive_dfs(graph, neighbour, path)
    return path


def main():
    random_matrix = np.random.randint(0, colors, (dim, dim))

    visited = np.zeros((dim, dim))

    root = node.Node(random_matrix, get_main_island_rec(random_matrix, visited, 0, 0, random_matrix[0][0]), 0, None,
                     random_matrix[0][0])
    # print(root.visited)

    # print(bfs(root))
    print('Initial state')
    print(random_matrix)
    print('                 ')

    bfs(root)


if __name__ == "__main__":
    main()
