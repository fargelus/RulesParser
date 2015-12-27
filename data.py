__author__ = 'dima'

# простой разделяемый класс данных


class Data:
    def __init__(self, entity_=None, rels_=None, rules_=None, target_=None):
        self.entity = entity_
        self.rels = rels_
        self.rules = rules_
        self.target = target_

    def get_vals_keys(self):
        return {self.entity[key]: key for key in self.entity.keys()}

    def get_multiple_obj(self):
        return [int(key) - 1 for key in self.entity if self.entity[key].count(' ') >= 1]











