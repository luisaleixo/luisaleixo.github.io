from music21 import *

def getInstrument(bwv):
    bwv_file = converter.parse("music_files/" + bwv)

    instruments = []
    for part in bwv_file.parts:
        if {'name': part.getElementsByClass("Instrument")[0].instrumentName} not in instruments:
            instruments.append({'name': part.getElementsByClass("Instrument")[0].instrumentName})
    return instruments