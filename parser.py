__author__ = 'dima'

import json


class Parser:
    def __init__(self, text_, data):
        self.text = text_
        self.data_to_fill = data

        self.parse_base()

    def parse_base(self):
        json_str = str()
        for line in self.text:
            json_str += line

        parse_data = json.loads(json_str)
        self.data_to_fill.entity = parse_data["Entity"]
        self.data_to_fill.rels = parse_data["Rels"]
        self.data_to_fill.rules = parse_data["Rules"]
        self.data_to_fill.target = parse_data["Target"]
