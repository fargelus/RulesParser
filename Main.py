__author__ = 'dima'

from data import Data
from parser import Parser
from graph import Graph


def main(records):
    facts = Data()
    Parser(records, facts)
    g = Graph(facts)
    g.parse_matrix()




