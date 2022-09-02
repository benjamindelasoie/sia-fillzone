import numpy as np
import node
import Utils.priorityQueue as priorityQueue
import time

colors = 5
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
                    # print('                 ')
                    # print(new_state)
                    new_node = node.Node(new_state, main_island, actual_node.cost + 1, actual_node, color)
                    queue.append(new_node)


def dfs_search(actual_node, limit):
    # nodo Encontrado
    if is_goal(actual_node):
        print('GOAL')
        return actual_node

    # paso el limite
    if limit < 0:
        return None

    # siguiente nodo
    for color in range(colors):
        if color != actual_node.color:
            new_state = change_color(np.copy(actual_node.state), actual_node.visited, color)
            blank_matrix = np.zeros((dim, dim))
            main_island = get_main_island_rec(new_state, blank_matrix, 0, 0, color)
            if not is_insignificant_move(actual_node.visited, main_island):
                new_node = node.Node(new_state, main_island, actual_node.cost + 1, actual_node, color)
                next_node = dfs_search(new_node, limit - 1)
                if next_node is not None:
                    return next_node


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
    return 0


def a_search(root):
    queue = priorityQueue.PriorityQueue()
    queue.insert(root)

    while not queue.isEmpty():
        actual_node = queue.pop()
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

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    else:
                        heuristic_val = heuristic2(new_node)

                    new_node.set_value(new_node.cost + heuristic_val)
                    queue.insert(new_node)


def greedy(root):
    current = root
    while not is_goal(current):
        queue = priorityQueue.PriorityQueue()

        # por cada color veo como queda la matriz al escogerlo
        for color in range(colors):
            if color != current.color:
                aux = np.copy(current.state)
                new_state = change_color(aux, current.visited, color)
                blank_matrix = np.zeros((dim, dim))
                main_island = get_main_island_rec(new_state, blank_matrix, 0, 0, color)
                if not is_insignificant_move(current.visited, main_island):
                    # print('                 ')
                    # print(new_state)
                    new_node = node.Node(new_state, main_island, current.cost + 1, current, color)

                    if heuristic == 1:
                        heuristic_val = heuristic1(new_node)
                    else:
                        heuristic_val = heuristic2(new_node)

                    new_node.set_value(heuristic_val)
                    queue.insert(new_node)
        current = queue.pop()

    print('GOAL')
    return current


def main():
    random_matrix = np.random.randint(0, colors, (dim, dim))

    visited = np.zeros((dim, dim))

    root = node.Node(random_matrix,
                     get_main_island_rec(random_matrix, visited, 0, 0, random_matrix[0][0]), 0, None,
                     random_matrix[0][0])
    # print(root.visited)

    # print(bfs_search(root))
    print('Initial state')
    print(random_matrix)
    print('                 ')

    start = time.time()
    goal = bfs_search(root)
    # goal = dfs_search(root, 100)
    # goal = greedy(root)
    end = time.time()
    print(str(end - start) + ' secs')
    current = goal
    while current is not None:
        # print('#colors=' + str(heuristic1(current)))
        print(current.state)
        print('                 ')
        current = current.parent


if __name__ == "__main__":
    main()
