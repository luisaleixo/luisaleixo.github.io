# -*- Coding: UTF-8 -*-
#coding: utf-8

import generateImage
import json

shapes_array = []

def available_shapes():
    shapes = generateImage.available_shapes()

    shapes_json = []
    for shape in shapes:
        shape_append = {'shape':shape, 'index':shapes.index(shape)}
        if shape_append not in shapes_json:
            shapes_json.append(shape_append)

    return shapes_json

def all_shapes(json_file):
    shapes_array.append(json_file)

    return shapes_array
