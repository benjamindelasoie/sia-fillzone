import numpy as np
import node
import Utils.priorityQueue as priorityQueue
import time

colors = 4
dim = 10
heuristic = 1

# arrays para movernos hacia los bloques adyacentes
# index = 0 ---> ARRIBA
# index = 1 ---> IZQUIERDA
# index = 2 ---> DERECHA
# index = 3 ---> ABAJO
row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]
movement_cost = 1


# devuelve una matriz con 1's donde se ubica nuestra isla principal
def get_main_island_rec(matrix, visited, i, j, color, island_size):
    if i < 0 or j < 0 or i >= dim or j >= dim or visited[i][j]:
        return visited, island_size

    if matrix[i][j] == color:
        visited[i][j] = True
        island_size += 1
        new_visited = visited

        for k in range(4):
            new_visited, island_size = get_main_island_rec(matrix, new_visited, i + row[k], j + col[k],
                                                           color, island_size)

        return new_visited, island_size

    return visited, island_size


# cambia el color de la isla principal
def change_color(matrix, visited, color):
    for i in range(dim):
        for j in range(dim):
            if visited[i][j]:
                matrix[i][j] = color
    return matrix


def is_goal(actual_node):
    for i in range(dim):
        for j in range(dim):
            if actual_node.state[i][j] != actual_node.color:
                return False
    return True


def is_insignificant_move(visited, new_visited):
    for i in range(dim):
        for j in range(dim):
            if visited[i][j] != new_visited[i][j]:
                return False
    return True


# armo una cola y voy sacando el nodo que hace más tiempo se encuentra en la cola
def bfs_search(root):
    queue = [root]
    total_nodes = 1
    border_nodes = 1

    while queue:
        actual_node = queue.pop(0)
        border_nodes = border_nodes - 1
        if is_goal(actual_node):
            print('GOAL')
            return actual_node, border_nodes, total_nodes

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = change_color(np.copy(actual_node.state), actual_node.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0)
                if not is_insignificant_move(actual_node.visited, main_island):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    queue.append(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1


def dfs_search(actual_node, limit, border_nodes_dfs=1, total_nodes_dfs=1):
    border_nodes_dfs = border_nodes_dfs - 1
    # nodo Encontrado
    if is_goal(actual_node):
        print('GOAL')
        return actual_node, border_nodes_dfs, total_nodes_dfs

    # paso el límite
    if limit < 0:
        print('limit')
        return None, border_nodes_dfs, total_nodes_dfs

    # siguiente nodo
    for color in range(colors):
        if color != actual_node.color:
            new_state = change_color(np.copy(actual_node.state), actual_node.visited, color)
            blank_matrix = np.zeros((dim, dim))
            main_island, island_size = get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0)
            if not is_insignificant_move(actual_node.visited, main_island):
                new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                     actual_node, color, island_size)
                next_node, border_nodes, total_nodes = dfs_search(new_node, limit - 1, border_nodes_dfs + 1, total_nodes_dfs + 1)
                if next_node is not None:
                    return next_node, border_nodes, total_nodes

# agrego esta opcion de dfs porque la otra no funciona bien con el limite
def dfs_search_2(root, limit, border_nodes_dfs=1, total_nodes_dfs=1):
    border_nodes = 1
    total_nodes = 1
    stack = [root]

    while stack:
        actual_node = stack.pop()
        border_nodes = border_nodes - 1
        # nodo Encontrado
        if is_goal(actual_node):
            print('GOAL')
            return actual_node, border_nodes, total_nodes
        # paso el límite
        if limit < actual_node.cost:
            continue
        for color in range(colors):
            if color != actual_node.color:
                new_state = change_color(np.copy(actual_node.state), actual_node.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0)
                if not is_insignificant_move(actual_node.visited, main_island):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    stack.append(new_node)
                    border_nodes = border_nodes + 1
                    total_nodes = total_nodes + 1
    return None, border_nodes, total_nodes


# funcion heuristica que devuelve la cantidad de colores restantes para poder
# conquistar toda la matriz (no se tiene en cuenta la isla principal)
def heuristic1(actual_node):
    color_list = []
    for i in range(dim):
        for j in range(dim):
            if actual_node.visited[i][j] == 0 and actual_node.state[i][j] not in color_list:
                color_list.append(actual_node.state[i][j])
            if color_list.__len__() == colors:
                break
        if color_list.__len__() == colors:
            break
    return color_list.__len__()


# ¿funcion heuristica?
def heuristic2(actual_node):
    return (dim * dim) - actual_node.island_size


def a_search(root):
    queue = priorityQueue.PriorityQueue()
    queue.insert(root)

    total_nodes = 1
    border_nodes = 1

    while not queue.isEmpty():
        actual_node = queue.pop()
        border_nodes = border_nodes - 1
        if is_goal(actual_node):  # TODO  ver si es esto o poner q la heuristica sea 0
            print('GOAL')
            return actual_node, border_nodes, total_nodes

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = change_color(np.copy(actual_node.state), actual_node.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0)
                if not is_insignificant_move(actual_node.visited, main_island):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    else:
                        heuristic_val = heuristic2(new_node)

                    new_node.set_value(new_node.cost + heuristic_val)
                    queue.insert(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1


def greedy(root):
    current = root
    total_nodes = 1
    border_nodes = 0
    while not is_goal(current):
        queue = priorityQueue.PriorityQueue()

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != current.color:
                aux = np.copy(current.state)
                new_state = change_color(aux, current.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0)
                if not is_insignificant_move(current.visited, main_island):
                    new_node = node.Node(new_state, main_island, current.cost + movement_cost,
                                         current, color, island_size)

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    else:
                        heuristic_val = heuristic2(new_node)

                    new_node.set_value(heuristic_val)
                    queue.insert(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1
        current = queue.pop()
        border_nodes = border_nodes - 1

    print('GOAL')
    return current, border_nodes, total_nodes


def main():
    random_matrix = np.random.randint(0, colors, (dim, dim))

    # random_matrix = [[1,2,1],[2,0,2],[0,0,1]]

    # random_matrix = [[1, 2, 1], [2, 0, 2], [0, 0, 1]]

    # random_matrix = [[0, 1, 1], [2, 2, 2], [1, 1, 1]]

    visited = np.zeros((dim, dim))

    main_island, island_size = get_main_island_rec(random_matrix, visited, 0, 0, random_matrix[0][0], 0)

    root = node.Node(random_matrix, main_island, 0, None,
                     random_matrix[0][0], island_size)

    start = time.time()
    # goal, border_nodes, total_nodes = bfs_search(root)
    goal, border_nodes, total_nodes = dfs_search_2(root, 50)
    # goal, border_nodes, total_nodes = a_search(root)
    end = time.time()

    current = goal
    while current is not None:
        print(current.state)
        print('                 ')
        current = current.parent

    print('Total cost: ' + str(goal.cost))
    print('Total nodes: ' + str(total_nodes))
    print('Border nodes: ' + str(border_nodes))
    print('Processing time: ' + str(end - start) + ' secs')


if __name__ == "__main__":
    main()

    # TODO testear metodos
    # TODO enlasar con front
    # TODO ver heuristicas
    # TODO README
