#-------------------------------------------------------------------------------
# Name:        cookbook_reader.py
# Purpose:     Wrapper for reading the cookbook, from whereever it should be
#              stored. Also, verify and map field names.
#
# Author:      Tobias
#
# Created:     29.10.2015
# Copyright:   (c) Tobias 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import yaml
import codecs
import os
from groceries.recipes import Recipe


filename = os.path.join(os.path.dirname(__file__),'cookbook.yaml')

field_mapping = {
    'kategorier': 'tags',
    'tid': 'time',
    'oppskrift': 'how_to',
    'antall personer i oppskrift': 'serves',
    'ingredienser': 'ingredients'
    }

with codecs.open(filename, "r", "utf-8") as fid:
    cookbook_file = yaml.load(fid, Loader=yaml.BaseLoader)
recipes = list()

# Wrapper for recipes, normalizing all tags and split tags:
for recipe in cookbook_file:
    new_dict = {}
    for k, v in cookbook_file[recipe].items():
        assert k in field_mapping
        if field_mapping[k] == 'tags':
            v = [s.strip() for s in v.split(',')]
        elif field_mapping[k] == 'serves':
            v = float(v)
        new_dict[field_mapping[k]] = v
    new_dict['name'] = recipe
    recipes.append(Recipe(**new_dict))
