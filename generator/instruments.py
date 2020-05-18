# -*- Coding: UTF-8 -*-
#coding: utf-8

from music21 import *
import shapes

def getInstrument(bwv):
    bwv_file = converter.parse("static/music_files/" + bwv)

    availabe_shapes = shapes.available_shapes()

    instruments = []
    for part in bwv_file.parts:
        json_obj = {'name': part.getElementsByClass("Instrument")[0].instrumentName,
                    'midi': part.getElementsByClass("Instrument")[0].midiProgram,
                    'shapes': availabe_shapes}

        if json_obj not in instruments:
            instruments.append(json_obj)

    return instruments