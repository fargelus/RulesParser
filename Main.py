__author__ = 'dima'

from data import Data
from parser import Parser
from graph import Graph
from rules import Rules


def main(records):
    facts = Data()
    Parser(records, facts)
    g = Graph(facts)
    r = Rules(g)
    vals_keys = facts.get_vals_keys()

    from_target = facts.target["from"]
    to_target = facts.target["to"]
    type_target = facts.target["type"]

    from_ = int(vals_keys[from_target]) - 1
    to = int(vals_keys[to_target]) - 1
    type = Rules.find_link_type(type_target)

    i = 0
    while g.matrix[from_][to] != type:
        r.parse_rules()
        i += 1
    g.parse_matrix()




