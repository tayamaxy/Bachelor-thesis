import numpy as np
from Latin_square import LatinSquare


def create_ort_operation(n: int) -> dict:
    """ vytvoří binární operaci na množině {0, 1, ..., n-1}, která je ortogonální vůči libovolnému latinskému čtverci (operace 'tečka' z příkladu 2.1.3)
        a uloží ji do slovníku, jehož klíče jsou souřadnice políčka Cayleyho tabulky a hodnota je jeho obsah """
    dict = {}
    for x in range(n):
        for y in range(n):
            dict[(x, y)] = {y}
    return dict


def composition(circle: LatinSquare, dot: dict, star: LatinSquare) -> np.ndarray:
    """ spočte složení třech binarních operací dle definice 2.1.2 """
    order = circle.size
    result = np.empty((order, order), dtype=object)
    for x in range(order):
        for y in range(order):
            result[x, y] = next(iter(star.incidence_dict[(next(iter(circle.incidence_dict[(x, y)])), next(iter(dot[(x, y)])))]))
    return result


def create_random_square(order: int) -> LatinSquare:
    symbols = range(order)
    first_row = np.array(symbols)
    circulant_matrix = np.zeros((order, order), dtype=int)
    for i in range(order):
        circulant_matrix[i] = np.roll(first_row, i)

    circulant_latinsquare = LatinSquare(circulant_matrix)
    k = 1500
    circulant_latinsquare.jm_algorithm(k)
    return circulant_latinsquare


def score_(operation: np.ndarray) -> float:
    """ spočte skóre binární operace (algoritmus 2.2.1) """
    size = operation.shape[0]
    score = 0
    for i in range(size):
        score += 2 * size - len(set(operation[:, i])) - len(set(operation[i, :]))
    return round(1-score/(size*(size-1)), 3)


def find_ort(circle: LatinSquare, n_iter, n_s, apply_jm=0, k=2) -> LatinSquare:
    """  základní algoritmus hledání latinského čtverce ortogonálního danému (algoritmus 2.2.2)

         pokud apply_jm > 0 a nejlepší skóre se po dobu apply_jm iterací nezmění,
         na star se aplikue algoritmus Jacobsona a Matthewse s parametrem k>1 """
    order = circle.size
    dot = create_ort_operation(order)
    star = create_random_square(order)
    score = score_(composition(circle, dot, star))
    prev_score = score
    best_approximation = LatinSquare(composition(circle, dot, star))

    if score == 1:
        return best_approximation
    c = 0 # počítadlo změn skóre v iterací

    for i in range(n_iter):
        if apply_jm != 0 and c > apply_jm:
            star.jm_algorithm(k)
            score = score_(composition(circle, dot, star))
            c = 0

        neighbors = star.n_random_neighbors(n_s)

        all_scores = np.array([score_(composition(circle, dot, neighbors)) for neighbors in neighbors])
        index = np.argmax(all_scores)
        if all_scores[index] == 1:
            best_approximation = LatinSquare(composition(circle, dot, neighbors[index]))
            return best_approximation
        else:
            star = neighbors[index]
        if all_scores[index] >= score:
            score = all_scores[index]
            best_approximation = LatinSquare(composition(circle, dot, neighbors[index]))
            star = neighbors[index]
        if prev_score == score:
            c += 1
        else:
            c = 0
        prev_score = score
    return best_approximation


if __name__ == '__main__':
    #příklad využití algoritmu 2.2.2
    L = LatinSquare(np.array([[0, 1, 2, 3, 4],
                              [4, 0, 1, 2, 3],
                              [3, 4, 0, 1, 2],
                              [2, 3, 4, 0, 1],
                              [1, 2, 3, 4, 0]]))

    L_ort_mate = find_ort(L,  n_iter=5000, n_s=50) #latinský čtverec ortogonální L
    L_ort_mate.print()



