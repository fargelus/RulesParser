__author__ = 'dima'


class Graph:
    def __init__(self, data_):
        self.data = data_

        self.entity = data_.entity
        self.rels = data_.rels
        self.rules = data_.rules
        self.target = data_.target

        self.empty = float('inf')

        self.size = len(self.entity)
        self.matrix = [[self.empty] * self.size for i in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    self.matrix[i][j] = 0

        self.parse_rels()

    def parse_rels(self):
        for key in sorted(self.rels):
            for val in self.rels[key]:
                if val['type'] == 'is are':
                    to = int(val['to']) - 1
                    from_ = int(key) - 1
                    self.matrix[from_][to] = 1
                elif val['type'] == 'part of':
                    to = int(val['to']) - 1
                    from_ = int(key) - 1
                    self.matrix[from_][to] = 2
                elif val['type'] == 'consist of':
                    to = int(val['to']) - 1
                    from_ = int(key) - 1
                    self.matrix[from_][to] = 3
                else:
                    raise NameError('Процессор способен обрабатывать только три вида связи')

    def print_matrix(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.matrix[i][j], end=' ')
            print()

    def make_vertex_list(self, type):
        # создадим списки всех изменяющихся вершин
        verts = []
        if type == 1:
            for i in range(self.size):
                vertices_list = []
                for j in range(self.size):
                    if self.matrix[i][j] == 1:
                        if i not in vertices_list:
                            vertices_list.append(i)
                        vertices_list.append(j)

                if vertices_list:
                    verts.append(vertices_list)
        elif type == 2:
            for i in range(self.size):
                part_of_list = []
                for j in range(self.size):
                    if self.matrix[i][j] == 2:
                        if i not in part_of_list:
                            part_of_list.append(i)
                        part_of_list.append(j)

                if part_of_list:
                    verts.append(part_of_list)

        else:
            for i in range(self.size):
                contains_of_list = []
                for j in range(self.size):
                    if self.matrix[i][j] == 3:
                        if i not in contains_of_list:
                            contains_of_list.append(i)
                        contains_of_list.append(j)

                if contains_of_list:
                    verts.append(contains_of_list)
        return verts

    def parse_matrix(self):
        """ фун-ия парсит матрицу и выводит данные в файл """
        output_filename = '/home/dima/Рабочий стол/productionSystem(2 module)/output.txt'
        output = open(output_filename, 'w')

        target_filename = '/home/dima/Рабочий стол/productionSystem(2 module)/target.txt'
        target = open(target_filename, 'w')
        is_are = ' является '
        part_of = ' часть '
        contains_of = ' состоит из '

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 1:
                    from_ = self.entity[str(i+1)]
                    to = self.entity[str(j+1)]
                    output.write(from_ + is_are + to + '\n')
                elif self.matrix[i][j] == 2:
                    from_ = self.entity[str(i+1)]
                    to = self.entity[str(j+1)]
                    output.write(from_ + part_of + to + '\n')
                elif self.matrix[i][j] == 3:
                    from_ = self.entity[str(i+1)]
                    to = self.entity[str(j+1)]
                    output.write(from_ + contains_of + to + '\n')
                else:
                    pass

        str_to_find = self.target["from"]
        vals_keys = self.data.get_vals_keys()
        key = int(vals_keys[str_to_find]) - 1
        for j in range(self.size):
            if self.matrix[key][j] == 1:
                val = self.entity[str(j+1)]
                if val == self.target["to"]:
                    to = self.entity[str(j+1)]
                    target.write(str_to_find + is_are + to + '\n')

    def make_new_objects(self, obj):
        self.size += 1
        self.entity[str(self.size)] = obj
        prev_matrix = self.matrix
        self.matrix = [[self.empty] * self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    self.matrix[i][j] = 0

        for i in range(self.size):
            if i < self.size - 1:
                for j in range(self.size):
                    if j < self.size - 1:
                        self.matrix[i][j] = prev_matrix[i][j]

