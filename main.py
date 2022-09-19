import numpy as np
import node
import Utils.priorityQueue as priorityQueue
import Utils.priorityQueueGreedy as priorityQueueGreedy
import time
import math
import Utils.fillzoneUtils as fillzoneUtils

movement_cost = 1

colors = int(input('Enter number of colors: '))
dim = int(input('Enter board dimension: '))

print('Options')
print('1 - DFS')
print('2 - BFS')
print('3 - A*')
print('4 - Greedy')
search_method = int(input('Select a search-method: '))
if search_method == 4 or search_method == 3:
    print('Options')
    print('1 - Amount of resting colors')
    print('2 - blocks left')
    print('3 - Steps non-admisible')
    print('4 - blocks left non-admisible')
    print('5 - Steps')
    heuristic = int(input('Enter heuristic: '))


# armo una cola y voy sacando el nodo que hace más tiempo se encuentra en la cola
def bfs_search(root):
    queue = [root]
    total_nodes = 1
    border_nodes = 1

    while queue:
        actual_node = queue.pop(0)
        border_nodes = border_nodes - 1

        if fillzoneUtils.is_goal(actual_node, dim):
            print('GOAL')
            return actual_node, border_nodes, total_nodes

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dim)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
                if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dim):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    queue.append(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1


def dfs_search(actual_node, border_nodes_dfs=1, total_nodes_dfs=1):
    border_nodes_dfs = border_nodes_dfs - 1
    # nodo Encontrado
    if fillzoneUtils.is_goal(actual_node, dim):
        print('GOAL')
        return actual_node, border_nodes_dfs, total_nodes_dfs

    # siguiente nodo
    for color in range(colors):
        if color != actual_node.color:
            new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dim)
            blank_matrix = np.zeros((dim, dim))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
            if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dim):
                new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                     actual_node, color, island_size)
                next_node, border_nodes, total_nodes = dfs_search(new_node, border_nodes_dfs + 1,
                                                                  total_nodes_dfs + 1)
                if next_node is not None:
                    return next_node, border_nodes, total_nodes


def dfs_search_iter(root):
    border_nodes = 1
    total_nodes = 1
    stack = [root]

    while stack:
        actual_node = stack.pop()
        border_nodes = border_nodes - 1
        # nodo Encontrado
        if fillzoneUtils.is_goal(actual_node, dim):
            print('GOAL')
            return actual_node, border_nodes, total_nodes

        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dim)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
                if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dim):
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


# Relación de cantidad de bloques ganados por cambio de color y
# cantidad de boques ganados al cambiar por color de competidor
def heuristic2(actual_node):
    domination_left = dim * dim - actual_node.island_size
    if domination_left == 0:
        return 0
    percentage = domination_left * (100/(dim*dim))
    range_values = math.ceil(100 / 10)
    return percentage/range_values



# Relación de cantidad de bloques ganados por cambio de color y
# cantidad de boques ganados al cambiar por color de competidor
def heuristic3(actual_node):
    if fillzoneUtils.is_goal(actual_node, dim):
        return 0

    # los nodos vecinos del padre
    perimetral_colors = []
    father = actual_node.parent

    steps = 3
    num = (colors - 1) / steps
    numerals = [dim * dim, dim * dim * 0.66, dim * dim * 0.33]
    value = numerals[0] / actual_node.island_size

    # miro los otros hijos del padre
    for color in range(colors):
        if color != father.color and color != actual_node.color:
            new_state = fillzoneUtils.change_color(father.state, father.visited, color, dim)
            blank_matrix = np.zeros((dim, dim))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
            if father.island_size < island_size:
                perimetral_colors.append(color)

    sub_value, best_node = fillzoneUtils.get_best_color(actual_node, perimetral_colors, numerals[1], dim)
    value += sub_value

    sub_sub_value, best_node = fillzoneUtils.get_best_color(best_node, perimetral_colors, numerals[2], dim)
    value += sub_sub_value

    return value

# Cantidad de bloques restantes
def heuristic4(actual_node):
    return dim * dim - actual_node.island_size

def heuristic5(actual_node):
    if fillzoneUtils.is_goal(actual_node, dim):
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
            new_state = fillzoneUtils.change_color(father.state, father.visited, color, dim)
            blank_matrix = np.zeros((dim, dim))
            main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
            # if not is_insignificant_move(father.visited, main_island):
            if father.island_size < island_size:
                perimetral_colors.append(color)

    sub_value, best_node = fillzoneUtils.get_best_color(actual_node, perimetral_colors, numerals[1], dim)
    value += sub_value

    sub_sub_value, best_node = fillzoneUtils.get_best_color(best_node, perimetral_colors, numerals[2], dim)
    value += sub_sub_value

    return value


reduce_color = 3
# cantidad de movimientos necesarios para llegar al goal en una matriz equivalente a la
# actual pero de 2 o 3 colores (depende de reduce_color)
def heuristic6(actual_node):
    two_color_matrix = np.copy(actual_node.state)
    for i in range(dim):
        for j in range(dim):
            two_color_matrix[i][j] = two_color_matrix[i][j] % reduce_color

    visited = np.zeros((dim, dim))

    main_island, island_size = fillzoneUtils.get_main_island_rec(two_color_matrix, visited, 0, 0, two_color_matrix[0][0], 0,
                                                                 dim)

    root = node.Node(two_color_matrix, main_island, 0, None,
                     two_color_matrix[0][0], island_size)

    queue = [root]

    while queue:
        actual_node = queue.pop(0)

        if fillzoneUtils.is_goal(actual_node, dim):
            return actual_node.cost

        # por cada color veo como queda la matriz al escogerlo
        for color in range(reduce_color):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dim)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0,
                                                                             dim)
                if not fillzoneUtils.is_insignificant_move(actual_node.visited, main_island, dim):
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    queue.append(new_node)


def a_search(root):
    queue = priorityQueue.PriorityQueue()
    queue.insert(root)

    total_nodes = 1
    border_nodes = 1

    while not queue.isEmpty():
        actual_node = queue.pop()
        border_nodes = border_nodes - 1
        if fillzoneUtils.is_goal(actual_node, dim):
            print('GOAL')
            return actual_node, border_nodes, total_nodes

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != actual_node.color:
                new_state = fillzoneUtils.change_color(np.copy(actual_node.state), actual_node.visited, color, dim)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
                if actual_node.island_size < island_size:
                    new_node = node.Node(new_state, main_island, actual_node.cost + movement_cost,
                                         actual_node, color, island_size)
                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    elif heuristic == 2:
                        heuristic_val = heuristic2(new_node)
                    elif heuristic == 3:
                        heuristic_val = heuristic3(new_node)
                    else:
                        heuristic_val = heuristic7(new_node)

                    new_node.set_value(heuristic_val)

                    if fillzoneUtils.is_goal(new_node, dim):
                        print('GOAL')
                        return actual_node, border_nodes, total_nodes

                    queue.insert(new_node)
                    total_nodes = total_nodes + 1
                    border_nodes = border_nodes + 1


def greedy(root):
    current = root
    total_nodes = 1
    border_nodes = 0
    while not fillzoneUtils.is_goal(current, dim):
        queue = priorityQueueGreedy.PriorityQueue()

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != current.color:
                aux = np.copy(current.state)
                new_state = fillzoneUtils.change_color(aux, current.visited, color, dim)
                blank_matrix = np.zeros((dim, dim))
                main_island, island_size = fillzoneUtils.get_main_island_rec(new_state, blank_matrix, 0, 0, color, 0, dim)
                if not fillzoneUtils.is_insignificant_move(current.visited, main_island, dim):
                    new_node = node.Node(new_state, main_island, current.cost + movement_cost,
                                         current, color, island_size)

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    elif heuristic == 2:
                        heuristic_val = heuristic2(new_node)
                    elif heuristic == 3:
                        heuristic_val = heuristic3(new_node)
                    else:
                        heuristic_val = heuristic4(new_node)

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

    visited = np.zeros((dim, dim))

    main_island, island_size = fillzoneUtils.get_main_island_rec(random_matrix, visited, 0, 0, random_matrix[0][0], 0, dim)

    root = node.Node(random_matrix, main_island, 0, None,
                     random_matrix[0][0], island_size)

    start = time.time()

    if search_method == 2:
        goal, border_nodes, total_nodes = bfs_search(root)
    elif search_method == 3:
        goal, border_nodes, total_nodes = a_search(root)
    elif search_method == 4:
        goal, border_nodes, total_nodes = greedy(root)
    else:
        goal, border_nodes, total_nodes = dfs_search(root)

    end = time.time()

    current = goal
    while current is not None:
        print('Chosen color: ' + str(current.color))
        print(current.state)
        print('                 ')
        current = current.parent

    print('Total cost: ' + str(goal.cost))
    print('Total nodes: ' + str(total_nodes))
    print('Border nodes: ' + str(border_nodes))
    print('Processing time: ' + str(end - start) + ' secs')



def main2():
    random_matrix = np.random.randint(0, colors, (dim, dim))

    visited = np.zeros((dim, dim))

    main_island, island_size = fillzoneUtils.get_main_island_rec(random_matrix, visited, 0, 0, random_matrix[0][0], 0,
                                                                 dim)

    root = node.Node(random_matrix, main_island, 0, None,
                     random_matrix[0][0], island_size)

    print("%d" % (heuristic6(root)))



if __name__ == "__main__":
    main()

