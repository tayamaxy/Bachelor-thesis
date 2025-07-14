from OrtMate_algorithm import *
import multiprocessing
from functools import partial


def find_ort_star(star: LatinSquare, circle: LatinSquare, n_iter, n_s) -> (float, LatinSquare):
    """ funkci, která realizuje logiku algoritmu 2.2.2, s tím rozdílem, že operace star
    není volena libovolně, ale je předána jako vstupní parametr a vrátí se spolu se skóre """
    import copy
    best_star = copy.deepcopy(star)
    dot = create_ort_operation(star.size)
    score = score_(composition(circle, dot, star))

    if score == 1:
        return 1, best_star

    for _ in range(n_iter):
        neighbors = star.n_random_neighbors(n_s)
        all_scores = np.array([score_(composition(circle, dot, neighbor)) for neighbor in neighbors])
        index = np.argmax(all_scores)
        if all_scores[index] == 1:
            best_star = neighbors[index]
            return 1, best_star
        else:
            star = neighbors[index]
        if all_scores[index] >= score:
            score = all_scores[index]
            best_star = copy.deepcopy(neighbors[index])
            star = neighbors[index]
    return score, best_star


def create_population(list_of_squares: [(float, LatinSquare)], n_r=0) -> [LatinSquare]:
    """ vytvoří novou populaci (algoritmus 2.3.1)
        list_of_squares obsahuje dvojice (skóre, star) """
    import random
    n = len(list_of_squares)
    list_of_squares = random.sample(list(list_of_squares), k=len(list_of_squares))
    regular_weights = [x[0] for x in list_of_squares]
    total = sum(regular_weights)
    normalized_weights = [w / total for w in regular_weights]
    cum_weights = []
    cumulative_sum = 0
    for weight in normalized_weights:
        cumulative_sum += weight
        cum_weights.append(cumulative_sum)

    squares = [x[1] for x in list_of_squares]

    population = random.choices(squares, cum_weights=cum_weights, k=n - n_r - 1)
    population.append(squares[0])
    size = list_of_squares[0][1].size
    for i in range(n_r):
        population.append(create_random_square(size))
    return population


def find_ort_gen(circle: LatinSquare, n_iter: int, m_iter: int, n_s: int, l_p: int, n_r: int) -> LatinSquare:
    """ genetický algoritmus hledání latinského čtverce ortogonálního danému (algoritmus 2.3.2) """
    population = []
    for _ in range(l_p):
        population.append(create_random_square(circle.size))
    for _ in range(m_iter):
        pool = multiprocessing.Pool(processes=l_p)
        partial_find_ort_star = partial(find_ort_star, circle=circle, n_iter=n_iter, n_s=n_s)
        results = np.array(pool.map(partial_find_ort_star, population))
        index = np.argmax(results[:, 0])
        if results[index][0] == 1:
            return results[index, 1]
        population = create_population(results, n_r)
    return population[0]


if __name__ == '__main__':
    #příklad využití algoritmu 2.3.2
    L = LatinSquare(np.array([[0, 1, 2, 3, 4],
                              [4, 0, 1, 2, 3],
                              [3, 4, 0, 1, 2],
                              [2, 3, 4, 0, 1],
                              [1, 2, 3, 4, 0]]))

    L_ort_mate = find_ort_gen(L, n_iter=100, m_iter=10, n_s=50, l_p=10, n_r=2)  # latinský čtverec ortogonální L
    L_ort_mate.print()

