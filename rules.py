__author__ = 'dima'

import random

class Rules:
    @staticmethod
    def find_objects(string_to_parse):
        pos_first = -1
        pos_last = -1
        objects_to_return = []
        while True:
            pos_first = string_to_parse.find('(', pos_first + 1)
            if pos_first == -1:
                break
            pos_last = string_to_parse.find(')', pos_last + 1)
            if pos_last == -1:
                break
            objects_to_return.append(string_to_parse[pos_first + 1:pos_last])
        return objects_to_return

    @staticmethod
    def find_link_type(string_to_parse):
        link_beg = string_to_parse.find(')')
        link_end = string_to_parse.find('(', link_beg)
        link_type = string_to_parse[link_beg + 1:link_end]
        if link_type.strip() == 'is are':
            link_number = 1
        elif link_type.strip() == 'part of':
            link_number = 2
        elif link_type.strip() == 'consist of':
            link_number = 3
        elif link_type.strip() == 'IN NAME':
            return
        else:
            raise NameError('Процессор способен обрабатывать только три вида связи')
        return link_number

    def __init__(self, graph_):
        self.graph = graph_

        self.matrix = graph_.matrix

        self.size = len(self.matrix)

        self.rules = graph_.rules

        self.parse_rules()

    def print_rules(self):
        for k, v in self.rules.items():
            print(k, ': ', v)

    def parse_rules(self):
        i = 0
        while i <= 3:
            # список условий
            condition = []

            # список выводов
            conclusion = []
            for each_rule in self.rules.values():
                for item in each_rule:
                    vals = item.split('THEN')
                    condition.append(vals[0])
                    conclusion.append(vals[1])

            for antecedent, conc in zip(condition, conclusion):
                ant_objects = list()

                if 'AND' not in antecedent and 'AND' not in conc:
                    type_link_ant = Rules.find_link_type(antecedent)
                    ant_objects = Rules.find_objects(antecedent)
                    type_link_conc = Rules.find_link_type(conc)
                    conc_objects = Rules.find_objects(conc)
                    self.make_simple_rules(ant_objects, type_link_ant, conc_objects, type_link_conc)

                elif 'AND' in antecedent and 'AND' not in conc:
                    all_objects = antecedent.split('AND')
                    links = []
                    for each_side in all_objects:
                        objects = Rules.find_objects(each_side)
                        link = Rules.find_link_type(each_side)
                        ant_objects.append(objects[0])
                        ant_objects.append(objects[1])
                        links.append(link)
                    type_link_conc = Rules.find_link_type(conc)
                    conc_objects = Rules.find_objects(conc)

                    self.make_complex_rules(ant_objects, links, conc_objects, type_link_conc)
            i += 1

    def make_simple_rules(self, objects_from, type_from, objects_to, type_to):
        vals_pos = []
        for obj in objects_from:
            pos = objects_to.index(obj)
            vals_pos.append((obj, pos))

        orig_vals_pos = [(val, pos) for pos, val in enumerate(objects_from)]

        orig_pos_i, orig_pos_j = orig_vals_pos[0][1], orig_vals_pos[1][1]
        pos_i, pos_j = vals_pos[0][1], vals_pos[1][1]

        if type_from:
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == type_from:
                        if orig_pos_i == pos_j and orig_pos_j == pos_i:
                            if self.matrix[i][j] != 0:
                                self.matrix[j][i] = type_to
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if i == j:
                        continue
                    if self.graph.entity[str(i + 1)] in self.graph.entity[str(j + 1)]:
                        if orig_pos_i == pos_j and orig_pos_j == pos_i:
                            if self.matrix[j][i] != 0:
                                self.matrix[j][i] = type_to
                        elif orig_pos_j == pos_j and orig_pos_i == pos_i:
                            if self.matrix[i][j] != 0:
                                self.matrix[i][j] = type_to

    def make_complex_rules(self, objects_from, type_from, objects_to, type_to):
        flag = False
        comma_obj_number = 0
        for item in objects_from:
            if item.count(',') >= 1:
                comma_obj_number += 1

        if 1 <= comma_obj_number <= 2:
            flag = True

        if not flag:
            k = 0
            p = 0
            for i in range(self.size):
                row_str = objects_from[k]
                column_str = objects_from[k + 1]
                for j in range(self.size):
                    if self.matrix[i][j] == type_from[p]:
                        k += 2
                        p += 1
                        if objects_from[k] == row_str and objects_from[k + 1] != column_str:
                            for s in range(self.size):
                                if self.matrix[i][s] == type_from[p]:
                                    self.make_conclusion(row_str, column_str, i, j, s, objects_to, type_to)
                        elif objects_from[k] == column_str and objects_from[k + 1] != row_str:
                            for s in range(self.size):
                                if self.matrix[j][s] == type_from[p]:
                                    self.make_conclusion(row_str, column_str, i, j, s, objects_to, type_to)
                        k = 0
                        p = 0

        else:
            if comma_obj_number == 1:
                print(type_from)
                print(type_to)
                ents = self.graph.entity
                vals_keys = self.graph.data.get_vals_keys()
                mult_objects = [key for key in ents if '*' or '/' in ents[key]]
                for item in mult_objects:
                    val = ents[item]
                    val_list = list()
                    if '*' in val:
                        val_list = val.split('*')
                    if '/' in val:
                        val_list = val.split('/')
                    for each_item in val_list:
                        key = int(vals_keys[each_item.strip()]) - 1
                        for i in range(self.size):
                            if self.matrix[key][i] == 2:
                                if str(i + 1) in mult_objects:
                                    if self.matrix[int(item)-1][i] != 0:
                                        self.matrix[int(item)-1][i] = type_to

            else:
                if type_from[0] == type_from[1]:
                    first_type_list = self.graph.make_vertex_list(type_from[0])
                    out = []
                    in_ = []
                    for i in range(len(first_type_list)):
                        mult_obj = first_type_list[i][0]
                        parts = first_type_list[i][1:]
                        for j in range(len(first_type_list) - 1, -1, -1):
                            if i == j:
                                continue
                        compare_mult_obj = first_type_list[j][0]
                        compare_parts = first_type_list[j][1:]
                        if compare_parts == parts \
                                and mult_obj not in compare_parts and compare_mult_obj not in parts:
                            out.append(mult_obj)
                            in_.append(compare_mult_obj)

                    for key_from, key_to in zip(out, in_):
                        if self.matrix[key_from][key_to] != type_to:
                            self.matrix[key_from][key_to] = type_to

                else:
                    ValueError('Связи должны совпадать')

    def make_conclusion(self, row_str, column_str, i, j, s, objects_to, type_to):
        if objects_to[0] == row_str:
            if objects_to[1] == column_str:
                if self.matrix[i][j] != 0:
                    self.matrix[i][j] = type_to
            else:
                if self.matrix[i][s] != 0:
                    self.matrix[i][s] = type_to
        elif objects_to[0] == column_str:
            if objects_to[1] == row_str:
                if self.matrix[j][i] != 0:
                    self.matrix[j][i] = type_to
            else:
                if self.matrix[j][s] != 0:
                    self.matrix[j][s] = type_to
        else:
            if objects_to[1] == row_str:
                if self.matrix[s][i] != 0:
                    self.matrix[s][i] = type_to
            else:
                if self.matrix[s][j] != 0:
                    self.matrix[s][j] = type_to

    def check_matrix(self, type):
        entity = self.graph.entity
        if 1 <= type <= 3:
            type_str = ""
            if type == 1:
                type_str += ' является '
            elif type == 2:
                type_str += ' часть '
            else:
                type_str += ' состоит из '
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == type:
                        print(entity[str(i + 1)], type_str, entity[str(j+1)])
        else:
            raise ValueError('Несоотвествие типа связи')