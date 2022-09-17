import numpy as np
import node
import Utils.priorityQueue as priorityQueue
import Utils.priorityQueueGreedy as priorityQueueGreedy
import time
import math
import Utils.fillzoneUtils as fillzoneUtils

movement_cost = 1

colors = 6
dim = [4, 6, 8, 14]


# armo una cola y voy sacando el nodo que hace más tiempo se encuentra en la cola
def bfs_search(root, dimension):
    queue = [root]
    total_nodes = 1
    border_nodes = 1

    while queue:
        actual_node = queue.pop(0)
        border_nodes = border_nodes - 1

        if fillzoneUtils.is_goal(actual_node, dimension):
            return actual_node, border_nodes, total_nodes

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color,
                                                       dimension)
                blank_matrix = np.zeros((dimension, dimension))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                             dimension)
                if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dimension):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    queue.append(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1


def dfs_search(actual_node, dimension, border_nodes_dfs=1, total_nodes_dfs=1):
    border_nodes_dfs = border_nodes_dfs - 1
    # nodo Encontrado
    if fillzoneUtils.is_goal(actual_node, dimension):
        return actual_node, border_nodes_dfs, total_nodes_dfs

    # siguiente nodo
    for color in range(colors):
        if color != actual_node.color:
            new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dimension)
            blank_matrix = np.zeros((dimension, dimension))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                         dimension)
            if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dimension):
                new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                     actual_node, color, island_size)
                next_node, border_nodes, total_nodes = dfs_search(new_node, dimension, border_nodes_dfs + 1,
                                                                  total_nodes_dfs + 1)
                if next_node is not None:
                    return next_node, border_nodes, total_nodes


def dfs_search_iter(root, dimension):
    border_nodes = 1
    total_nodes = 1
    stack = [root]

    while stack:
        actual_node = stack.pop()
        border_nodes = border_nodes - 1
        # nodo Encontrado
        if fillzoneUtils.is_goal(actual_node, dimension):
            return actual_node, border_nodes, total_nodes

        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color,
                                                       dimension)
                blank_matrix = np.zeros((dimension, dimension))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                             dimension)
                if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dimension):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    stack.append(new_node)
                    border_nodes = border_nodes + 1
                    total_nodes = total_nodes + 1
    return None, border_nodes, total_nodes


# funcion heuristica que devuelve la cantidad de colores restantes para poder
# conquistar toda la matriz (no se tiene en cuenta la isla principal)
def heuristic1(actual_node, dimension):
    color_list = []
    for i in range(dimension):
        for j in range(dimension):
            if actual_node.visited[i][j] == 0 and actual_node.state[i][j] not in color_list:
                color_list.append(actual_node.state[i][j])
            if color_list.__len__() == colors:
                break
        if color_list.__len__() == colors:
            break
    return color_list.__len__()


# Relación de cantidad de bloques ganados por cambio de color y
# cantidad de boques ganados al cambiar por color de competidor
def heuristic2(actual_node, dimension):
    domination_left = dimension * dimension - actual_node.island_size
    if domination_left == 0:
        return 0
    percentage = domination_left * (100 / (dimension * dimension))
    range_values = math.ceil(100 / 10)
    value = percentage / range_values
    return value

# Relación de cantidad de bloques ganados por cambio de color y
# cantidad de boques ganados al cambiar por color de competidor
def heuristic3(actual_node, dimension):
    if fillzoneUtils.is_goal(actual_node, dimension):
        return 0

    # los nodos vecinos del padre
    perimetral_colors = []
    father = actual_node.parent

    steps = 3
    num = (colors - 1) / steps
    numerals = [dimension * dimension, dimension * dimension * 0.66, dimension * dimension * 0.33]
    value = numerals[0] / actual_node.island_size

    # miro los otros hijos del padre
    for color in range(colors):
        if color != father.color and color != actual_node.color:
            new_state = fillzoneUtils.change_color(father.state, father.visited, color, dimension)
            blank_matrix = np.zeros((dimension, dimension))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                         dimension)
            if father.island_size < island_size:
                perimetral_colors.append(color)

    sub_value, best_node = fillzoneUtils.get_best_color(actual_node, perimetral_colors, numerals[1], dimension)
    value += sub_value

    sub_sub_value, best_node = fillzoneUtils.get_best_color(best_node, perimetral_colors, numerals[2], dimension)
    value += sub_sub_value

    return value


# Cantidad de bloques restantes
def heuristic4(actual_node, dimension):
    return dimension * dimension - actual_node.island_size


def heuristic5(actual_node, dimension):
    if fillzoneUtils.is_goal(actual_node, dimension):
        return 0

    # los nodos vecinos del padre
    perimetral_colors = []
    father = actual_node.parent

    steps = 3
    num = (colors - 1) / steps
    numerals = [math.ceil(num * 3), math.ceil(num * 2), math.ceil(num)]
    value = numerals[0] / actual_node.island_size

    # miro los otros hijos del padre
    for color in range(colors):
        if color != father.color and color != actual_node.color:
            new_state = fillzoneUtils.change_color(father.state, father.visited, color, dimension)
            blank_matrix = np.zeros((dimension, dimension))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                         dimension)
            # if not is_insignificant_move(father.visited, main_island):
            if father.island_size < island_size:
                perimetral_colors.append(color)

    sub_value, best_node = fillzoneUtils.get_best_color(actual_node, perimetral_colors, numerals[1], dimension)
    value += sub_value

    sub_sub_value, best_node = fillzoneUtils.get_best_color(best_node, perimetral_colors, numerals[2], dimension)
    value += sub_sub_value

    return value


def a_search(root, dimension, heuristic):
    queue = priorityQueue.PriorityQueue()
    queue.insert(root)

    if fillzoneUtils.is_goal(root, dimension):
        return root, 1, 1

    total_nodes = 1
    border_nodes = 1

    while not queue.isEmpty():
        actual_node = queue.pop()
        border_nodes = border_nodes - 1

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color,
                                                       dimension)
                blank_matrix = np.zeros((dimension, dimension))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                             dimension)
                if actual_node.island_size < island_size:
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node, dimension)

                        # print(heuristic_val)

                    elif heuristic == 2:
                        heuristic_val = heuristic2(new_node, dimension)
                    elif heuristic == 3:
                        heuristic_val = heuristic3(new_node, dimension)
                    elif heuristic == 4:
                        heuristic_val = heuristic4(new_node, dimension)
                    else:
                        heuristic_val = heuristic5(new_node)

                    new_node.set_value(heuristic_val)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1

                    if heuristic_val == 0:
                        return new_node, border_nodes, total_nodes
                    queue.insert(new_node)


def greedy(root, dimension, heuristic):
    current = root
    total_nodes = 1
    border_nodes = 0
    while not fillzoneUtils.is_goal(current, dimension):
        queue = priorityQueueGreedy.PriorityQueue()

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != current.color:
                aux = np.copy(current.state)
                new_state = fillzoneUtils.change_color(aux, current.visited, color, dimension)
                blank_matrix = np.zeros((dimension, dimension))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                             dimension)
                if not fillzoneUtils.is_insignificant_move(current.visited, main_island, dimension):
                    new_node = node.Node(new_state, main_island, current.cost + movement_cost,
                                         current, color, island_size)

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node, dimension)
                    elif heuristic == 2:
                        heuristic_val = heuristic2(new_node, dimension)
                    elif heuristic == 3:
                        heuristic_val = heuristic3(new_node, dimension)
                    elif heuristic == 4:
                        heuristic_val = heuristic4(new_node, dimension)
                    else:
                        heuristic_val = heuristic5(new_node, dimension)

                    new_node.set_value(heuristic_val)
                    queue.insert(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1
        current = queue.pop()
        border_nodes = border_nodes - 1

    return current, border_nodes, total_nodes


def run_all():
    for dimension in dim:
        random_matrix = np.random.randint(0, colors, (dimension, dimension))

        print("--------------------------------------------------------------")
        print("DIM = " + str(dimension))
        print()
        print()
        print(random_matrix)

        visited = np.zeros((dimension, dimension))

        main_island, island_size = fillzoneUtils.get_main_island_rec(random_matrix, visited, 0, 0,
                                                                     random_matrix[0][0], 0, dimension)

        root = node.Node(random_matrix, main_island, 0, None,
                         random_matrix[0][0], island_size)

        goals = [None] * 10
        border_nodes = [0] * 10
        total_nodes = [0] * 10
        total_times = [0] * 10  

        prints = ["A* HEURISTIC 1", "A* HEURISTIC 2", "A* HEURISTIC 3", "A* HEURISTIC 4", "GREEDY HEURISTIC 1",
                  "GREEDY HEURISTIC 2", "GREEDY HEURISTIC 3", "GREEDY HEURISTIC 4", "DFS", "BFS"]

        iteration = 0
        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = a_search(root, dimension, 1)
        total_times[iteration] = time.time() - timer
        iteration += 1

        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = a_search(root, dimension, 2)
        total_times[iteration] = time.time() - timer
        iteration += 1
        
        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = a_search(root, dimension, 3)
        total_times[iteration] = time.time() - timer
        iteration += 1

        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = a_search(root, dimension, 4)
        total_times[iteration] = time.time() - timer
        iteration += 1
        #        goals[1], border_nodes[1], total_nodes[1] = a_search(root, dimension, 5)


        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = greedy(root, dimension, 1)
        total_times[iteration] = time.time() - timer
        iteration += 1

        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = greedy(root, dimension, 2)
        total_times[iteration] = time.time() - timer
        iteration += 1

        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = greedy(root, dimension, 3)
        total_times[iteration] = time.time() - timer
        iteration += 1

        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = greedy(root, dimension, 4)
        total_times[iteration] = time.time() - timer
        iteration += 1
        #       goals[2], border_nodes[2], total_nodes[2] = greedy(root, dimension, 5)


        timer = time.time()
        goals[iteration], border_nodes[iteration], total_nodes[iteration] = dfs_search(root, dimension=dimension)
        total_times[iteration] = time.time() - timer
        iteration += 1


        timer = time.time()
       #  goals[iter], border_nodes[iter], total_nodes[iter] = bfs_search(root, dimension)
        total_times[iteration] = time.time() - timer

        for i in range(9):
            print(prints[i])
            print(total_times[i])

            print('Total cost: ' + str(goals[i].cost))
            print('Total nodes: ' + str(total_nodes[i]))
            print('Border nodes: ' + str(border_nodes[i]))
            print()
            print()


if __name__ == '__main__':
    run_all()
