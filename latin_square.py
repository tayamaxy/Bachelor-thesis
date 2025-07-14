import numpy as np
import random
import copy


def create_dict(incidence_matrix):
    """ vytvoří slovník, jehož klíče jsou souřadnice políčka a hodnota je jeho obsah """
    dict = {}
    for i in range(incidence_matrix.shape[0]):
        for j in range(incidence_matrix.shape[0]):
            dict[(i, j)] = {incidence_matrix[i, j]}
    return dict


class LatinSquare:
    def __init__(self, incidence_matrix: np.ndarray):
        self.incidence_matrix = np.vectorize(lambda x: {x})(incidence_matrix)
        self.size = incidence_matrix.shape[0]
        self.symbols = set(incidence_matrix[1, :])
        self.incidence_dict = create_dict(incidence_matrix)
        self.is_proper = True #True, pokud je vlastní, False jinak
        self.imp_cell_pos = () #souřadnice nevlstního políčka
        self.imp_value = None  #nevlastní symbol
        self.imp_element_pos_ver = [(), ()]
        self.imp_element_pos_hor = [(), ()]

    def __eq__(self, other):
        return np.array_equal(self.incidence_matrix, other.incidence_matrix)

    def __hash__(self):
        matrix = self.incidence_matrix.flatten()
        matrix_tuple = tuple([next(iter(x)) for x in matrix])
        return hash(matrix_tuple)

    def print(self):
        if self.is_proper:
            print(np.vectorize(lambda x: next(iter(x)))(self.incidence_matrix))
        else:
            print(self.incidence_matrix)

    def get_rid_of_impropriety(self):
        self.is_proper = True
        self.imp_cell_pos = ()
        self.imp_value = None
        self.imp_element_pos_ver = [(), ()]
        self.imp_element_pos_hor = [(), ()]

    def set_impropriety(self, position: tuple, second_value: set):
        self.is_proper = False
        self.imp_cell_pos = position
        self.imp_value = second_value

        imp_element_pos_hor = []
        imp_element_pos_ver = []
        for i in range(self.size):
            if self.incidence_dict[(i, position[1])] == second_value and i != position[0]:
                imp_element_pos_hor.append((i, position[1]))
            if self.incidence_dict[(position[0], i)] == second_value and i != position[1]:
                imp_element_pos_ver.append((position[0], i))

        self.imp_element_pos_hor = imp_element_pos_hor
        self.imp_element_pos_ver = imp_element_pos_ver

    def choose_subsquare(self) -> list:
        p1 = random.choice(self.imp_element_pos_hor)
        p2 = random.choice(self.imp_element_pos_ver)
        return [p1, p2, self.imp_cell_pos, (p1[0], p2[1])]

    def choose_value(self) -> set:
        return {random.choice(list(self.incidence_dict[self.imp_cell_pos]))}

    def make_move(self, subsquare=None, value=None):
        """ aplikuje na latinský čtverec náhodně zvolenou latinskou záměnu """
        if self.is_proper:
            position = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            value = {random.choice(list(self.symbols.difference(self.incidence_dict[position])))}
            origin_value = self.incidence_dict[position]
            self.incidence_dict[position] = value
            self.incidence_matrix[position] = value

            x, y = 0, 0
            for i in range(self.size):
                if self.incidence_dict[(i, position[1])] == value and i != position[0]:
                    self.incidence_dict[(i, position[1])] = origin_value
                    self.incidence_matrix[i, position[1]] = origin_value
                    x = i
                if self.incidence_dict[(position[0], i)] == value and i != position[1]:
                    self.incidence_dict[(position[0], i)] = origin_value
                    self.incidence_matrix[position[0], i] = origin_value
                    y = i
            opposite_position = (x, y)
            if self.incidence_dict[opposite_position] == origin_value:
                self.incidence_dict[opposite_position] = value
                self.incidence_matrix[opposite_position] = value
            else:
                self.incidence_dict[opposite_position] = self.incidence_dict[opposite_position].union(value)
                self.incidence_matrix[opposite_position] = self.incidence_dict[opposite_position].union(value)
                self.set_impropriety(opposite_position, origin_value)

        else:
            if not (subsquare and value):
                subsquare = self.choose_subsquare()
                value = self.choose_value()

            second_value = self.incidence_dict[self.imp_cell_pos].difference(value)

            for position in subsquare:
                if position in self.imp_element_pos_hor or position in self.imp_element_pos_ver:
                    self.incidence_dict[position] = value
                    self.incidence_matrix[position] = value
                elif position == self.imp_cell_pos:
                    self.incidence_dict[position] = second_value
                    self.incidence_matrix[position] = second_value
                else:
                    if value == self.incidence_dict[position]:
                        self.incidence_dict[position] = self.imp_value
                        self.incidence_matrix[position] = self.imp_value
                        self.get_rid_of_impropriety()
                    else:
                        self.incidence_dict[position] = self.incidence_dict[position].union(self.imp_value)
                        self.incidence_matrix[position] = self.incidence_dict[position].union(self.imp_value)
                        self.set_impropriety(position, value)

    def n_random_neighbors(self, n: int):
        """ vratí n náhyných (vlastních) sousedů """
        sousede = set()
        current_ls = copy.deepcopy(self)
        hit = 0
        while len(sousede) < n:
            while not hit:
                self.make_move()
                if self.is_proper and (self != current_ls):
                    sousede.add(self)
                    hit = 1
            hit = 0
            self = current_ls
            current_ls = copy.deepcopy(self)
        return list(sousede)

    def jm_algorithm(self, k):
        """ algoritmus Jacobsona a Matthewse """
        if k < 2:
            raise Exception("Only k > 1 is allowed")
        hit = 1
        while hit < k:
            self.make_move()
            if self.is_proper:
                hit += 1


if __name__ == '__main__':
    #příklad vytváření instanci třídy LatinSquare
    L = LatinSquare(np.array([[0, 1, 2, 3],
                              [3, 0, 1, 2],
                              [2, 3, 0, 1],
                              [1, 2, 3, 0]]))

    L.jm_algorithm(2)
    L.print()


