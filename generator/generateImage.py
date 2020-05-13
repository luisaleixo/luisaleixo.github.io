from music21 import *
import cairo, sys, argparse, copy, math, random
import numpy as np
import colorsys
import math
import json
float_gen = lambda a, b: random.uniform(a, b)

def getTimeSignature(event):
    return event.numerator / event.denominator

def getVolume(event):
    return event.volume.getRealized()

def getDurations(bwv):
    for el in bwv.flat:
        print(el.duration.quarterLength)

def getOffsetInMeasure(measure):
    offsets = []
    for element in measure.flat:
        offsets.append(element.offset)

    return offsets

def getMeasureOffset(bwv):
    offsets = []
    for element in bwv.parts:
        for event in element.getElementsByClass("Measure"):
            if event.number <= 32:
                if event not in offsets:
                    offsets.append(event.offset)
    return offsets

def getBackgroundLuminance(bwv_c):
    background = bwv_c.flat.getElementsByClass(tempo.MetronomeMark)[0].number
    #print(background)
    if background < 60:
        return 0
    elif background >= 60 and background < 70:
        return 0.1
    elif background >= 70 and background < 80:
        return 0.2
    elif background >= 80 and background< 90:
        return 0.3
    elif background >= 90 and background< 100:
        return 0.4
    elif background >= 100 and background < 110:
        return 0.5
    elif background >= 110 and background < 120:
        return 0.6
    elif background >= 120 and background < 130:
        return 0.7
    elif background >= 130 and background < 140:
        return 0.8
    elif background >= 140 and background < 150:
        return 0.9
    elif background >= 150:
        return 1

def getResizableSize(event):
    base = 50
    if event.number < 60:
        return base
    elif event.number >= 60 and event.number < 70:
        base = base - (2 * 1)
        return base
    elif event.number >= 70 and event.number < 80:
        base = base - (2 * 2)
        return base
    elif event.number >= 80 and event.number< 90:
        base = base - (2 * 3)
        return base
    elif event.number >= 90 and event.number< 100:
        base = base - (2 * 4)
        return base
    elif event.number >= 100 and event.number < 110:
        base = base - (2 * 5)
        return base
    elif event.number >= 110 and event.number < 120:
        base = base - (2 * 6)
        return base
    elif event.number >= 120 and event.number < 130:
        base = base - (2 * 7)
        return base
    elif event.number >= 130 and event.number < 140:
        base = base - (2 * 8)
        return base
    elif event.number >= 140 and event.number < 150:
        base = base - (2 * 9)
        return base
    elif event.number >= 150:
        base = base - (2 * 10)
        return base

def get_Chords_per_measure(c_bwv):
    measures_elements = []
    for m in c_bwv.getElementsByClass('Measure'):
        if m.number <= 32:
            try:
                measures_elements.append(m.analyze("key").name)
            except:
                print("An Exception Occured!")
                measures_elements.append("C major")

    return measures_elements

def getVolumeChords(c_bwv):
    chords_volume = []
    for m in c_bwv.getElementsByClass('Measure'):
        if m.number <= 32:
            volumes = 0
            n = 0
            for el in m.flat.getElementsByClass("Chord"):
                volumes += el.volume.getRealized()
                n += 1
            chords_volume.append(volumes/(n + 0.000001))

    return chords_volume

def getLuminanceChords(c_bwv):
    chords_luminance = []
    for m in c_bwv.getElementsByClass('Measure'):
        if m.number <= 32:
            for el in m.flat.getElementsByClass("Chord"):
                chords_luminance.append(getLuminance(el.root()))
    return chords_luminance

def color_note(event):
    if event.name == note.Note("C").name:
        color = (255, 0, 0)

    elif event.name == note.Note("C#").name:
        color = (255, 0, 125)

    elif event.name == note.Note("D-").name:
        color = (255, 0, 125)

    elif event.name == note.Note("D").name:
        color = (255, 0, 255)

    elif event.name == note.Note("D#").name:
        color = (125, 0, 255)

    elif event.name == note.Note("E-").name:
        color = (125, 0, 255)

    elif event.name == note.Note("E").name:
        color = (0, 0, 255)

    elif event.name == note.Note("F").name:
        color = (0, 125, 255)

    elif event.name == note.Note("F#").name:
        color = (0, 255, 255)

    elif event.name == note.Note("G-").name:
        color = (0, 255, 255)

    elif event.name == note.Note("G").name:
        color = (0, 255, 125)

    elif event.name == note.Note("G#").name:
        color = (0, 255, 0)

    elif event.name == note.Note("A-").name:
        color = (0, 255, 0)

    elif event.name == note.Note("A").name:
        color = (125, 255, 0)

    elif event.name == note.Note("A#").name:
        color = (255, 255, 0)

    elif event.name == note.Note("B-").name:
        color = (255, 255, 0)

    elif event.name == note.Note("B").name:
        color = (255, 125, 0)

    ###nao esta no circulo
    elif event.name == note.Note("C-").name:
        color = (255, 125, 0)

    elif event.name == note.Note("F-").name:
        color = (0, 0, 255)

    elif event.name == note.Note("E#").name:
        color = (0, 125, 255)

    elif event.name == note.Note("B#").name:
        color = (255, 0, 0)

    elif event.name == note.Note("B--").name:
        color = (125, 255, 0)

    elif event.name == note.Note("E--").name:
        color = (255, 0, 255)

    elif event.name == note.Note("F##").name:
        color = (0, 255, 125)

    elif event.name == note.Note("C##").name:
        color = (255, 0, 255)

    elif event.name == note.Note("D##").name:
        color = (0, 0, 255)

    luminance = getLuminance(event)
    volume = getVolume(event)
    color_hls = colorsys.rgb_to_hls(color[0] / 255, color[1] / 255, color[2] / 255)
    color_rgb = colorsys.hls_to_rgb(color_hls[0], luminance, volume)
    return color_rgb

def get_chords_colors(c_key, luminance, volume):
    if c_key == "C major":
        color = (255, 0, 0)

    elif c_key == "A minor":
        color = (255, 0, 0)

    elif c_key == "G major":
        color = (255, 0, 125)

    elif c_key == "E minor":
        color = (255, 0, 125)

    elif c_key == "D major":
        color = (255, 0, 255)

    elif c_key == "B minor":
        color = (255, 0, 255)

    elif c_key == "A major":
        color = (255, 0, 255)

    elif c_key == "F# minor":
        color = (255, 0, 255)

    elif c_key == "E major":
        color = (0, 0, 255)

    elif c_key == "C# minor":
        color = (0, 0, 255)

    elif c_key == "B major":
        color = (0, 125, 255)

    elif c_key == "G# minor":
        color = (0, 125, 255)

    elif c_key == "G- major":
        color = (0, 255, 255)

    elif c_key == "F# major":
        color = (0, 255, 255)

    elif c_key == "E- minor":
        color = (0, 255, 255)

    elif c_key == "D- major":
        color = (0, 255, 125)

    elif c_key == "B- minor":
        color = (0, 255, 125)

    elif c_key == "A- major":
        color = (0, 255, 0)

    elif c_key == "F minor":
        color = (0, 255, 0)

    elif c_key == "E- major":
        color = (125, 255, 0)

    elif c_key == "C minor":
        color = (125, 255, 0)

    elif c_key == "B- major":
        color = (255, 255, 0)

    elif c_key == "G minor":
        color = (255, 255, 0)

    elif c_key == "F major":
        color = (255, 125, 0)

    elif c_key == "D minor":
        color = (255, 125, 0)

    ####nao estao na roda

    elif c_key == "C# minor":
        color = (248, 155, 124)

    elif c_key == "C minor":
        color = (103, 203, 160)

    elif c_key == "C# major":
        color = (254, 248, 101)

    color_hls = colorsys.rgb_to_hls(color[0] / 255, color[1] / 255, color[2] / 255)
    color_rgb = colorsys.hls_to_rgb(color_hls[0], luminance, volume)
    return color_rgb

def deform(shape, iterations, variance):
    for i in range(iterations):
        for j in range(len(shape)-1, 0, -1):
            midpoint = ((shape[j-1][0] + shape[j][0])/2 + float_gen(-variance, variance),
                        (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            #para cada um dos lados, encontra o seu midpoint e adiciona-o
            shape.insert(j, midpoint)
    return shape

def polygon(sides, radius=1, rotation=0, translation=None):
    one_segment = math.pi * 2 / sides

    points = [
        (math.sin(one_segment * i + rotation) * radius,
         math.cos(one_segment * i + rotation) * radius)
        for i in range(sides)]

    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
                  for point in points]

    points.append(points[0])
    return points

def circle(centerX, centerY, radius, angle_start, angle_end):
    points = []

    for degree in range(angle_start, angle_end):
        radians = degree * math.pi / 180
        x = centerX + radius * math.cos(radians)
        y = centerY + radius * math.sin(radians)
        points.append((x, y))

    return points

def getMeasureTime(bwv):
    return bwv.parts[0].getElementsByClass("Measure")[0].seconds

def getOverallTime(bwv):
    return bwv.flat.seconds

def getDimensions(bwv):
    measureTime = getMeasureTime(bwv)
    overallTime = getOverallTime(bwv)

    return overallTime * 100 / 4, measureTime * 1000

def rhombus(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)

    oct = []

    oct.append((x, y))

    x += d / 1.5
    y += d * 1.5
    oct.append((x, y))

    x -= d / 1.5
    y += d * 1.5
    oct.append((x, y))

    x -= d / 1.5
    y -= d * 1.5
    oct.append((x, y))

    x += d / 1.5
    y -= d * 1.5
    oct.append((x, y))

    return oct

def octagon(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)

    oct = []

    oct.append((x, y))

    x += side
    oct.append((x, y))

    x += d
    y += d
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= d
    y += d
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= d
    y -= d
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += d
    y -= d
    oct.append((x, y))

    return oct

def rectangle(x_orig, y_orig, side):
    x = x_orig
    y = y_orig

    oct = []

    oct.append((x, y))

    x += side / 1.5
    oct.append((x, y))

    y += side * 2
    oct.append((x, y))

    x -= side / 1.5
    oct.append((x, y))

    y -= side * 2
    oct.append((x, y))

    return oct

def getShape(cr, instr, event, location_x, location_y, size, colors, shapealpha):
    if instr.midiProgram >= 0 and instr.midiProgram <= 7:
        shape_points = circle(location_x, location_y, size / 2, 0, 360)

    elif instr.midiProgram >= 8 and instr.midiProgram <= 15:
        shape_points = circle(location_x, location_y, size / 4, 0, 360)  # smaller circle

    elif instr.midiProgram >= 16 and instr.midiProgram <= 23:
        shape_points = rectangle(location_x, location_y, size)

    elif instr.midiProgram >= 24 and instr.midiProgram <= 31:
        cr.set_source_rgba(colors[0], colors[1], colors[2], shapealpha / 2)
        shape = rectangle(location_x, location_y, size / 4)
        baseshape = deform(shape, 8, 6)
        for i in range(len(baseshape)):
            cr.line_to(baseshape[i][0], baseshape[i][1])
        cr.fill()
        return

    elif instr.midiProgram >= 32 and instr.midiProgram <= 39:
        cr.set_source_rgba(colors[0], colors[1], colors[2], shapealpha / 2)
        shape = rectangle(location_x, location_y, size)
        baseshape = deform(shape, 8, 6)
        for i in range(len(baseshape)):
            cr.line_to(baseshape[i][0], baseshape[i][1])
        cr.fill()
        return

    elif instr.midiProgram >= 40 and instr.midiProgram <= 47:
        shape = octagon(location_x, location_y, size / 2)
        baseshape = deform(shape, basedeforms, initial)
        cr.set_source_rgba(colors[0], colors[1], colors[2], 0.04)

        for j in range(random.randint(minshapes, maxshapes)):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
        return

    elif instr.midiProgram >= 48 and instr.midiProgram <= 55:
        rotation = random.randint(0, 20)
        shape_points = polygon(12, size, (rotation / 10) * math.pi, [location_x, location_y])

    elif instr.midiProgram >= 56 and instr.midiProgram <= 63:
        rotation = random.randint(0, 20)
        shape_points = polygon(4, size, (rotation / 10) * math.pi, [location_x, location_y])

    elif instr.midiProgram >= 64 and instr.midiProgram <= 71:
        rotation = random.randint(0, 20)
        shape_points = polygon(4, size, (rotation / 10) * math.pi, [location_x, location_y])
        shape_points = deform(shape_points, 8, 4)

    elif instr.midiProgram >= 72 and instr.midiProgram <= 79:
        shape_points = rhombus(location_x, location_y, size / 2)

    elif instr.midiProgram >= 80:
        rotation = random.randint(0, 20)
        shape_points = polygon(3, size, (rotation / 10) * math.pi, [location_x, location_y])

    if isinstance(event, chord.Chord):
        if event.isConsonant is False:
            shape_points = deform(shape_points, 5, 5)

    shape_points = deform(shape_points, 2, 2)
    cr.set_source_rgba(colors[0], colors[1], colors[2], shapealpha)
    for i in range(len(shape_points)):
        cr.line_to(shape_points[i][0], shape_points[i][1])
    cr.fill()
    return

def getLuminance(event):
    if event.octave <= 0:
        return 0.1
    elif event.octave == 1:
        return 0.2
    elif event.octave == 2:
        return 0.3
    elif event.octave == 3:
        return 0.4
    elif event.octave == 4:
        return 0.5
    elif event.octave == 5:
        return 0.6
    elif event.octave >= 6:
        return 0.7

def finalDraw(bwv, bwv_c, name):
    width, height = 2700, 1600

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.rectangle(0, 0, width, height)

    background_color = colorsys.hls_to_rgb(0, getBackgroundLuminance(bwv_c), 0)

    cr.set_source_rgb(background_color[0], background_color[1], background_color[2])
    cr.fill()

    lg2 = cairo.LinearGradient(0.0, 0.0, width, 0)

    measures_elements = get_Chords_per_measure(bwv_c)
    measures = len(measures_elements)

    chords_luminance = getLuminanceChords(bwv_c)
    chords_volume = getVolumeChords(bwv_c)

    count = 0
    i = 0
    step = 1 / (measures)
    while count < measures:
        #print(measures_elements[count])
        chord_color = get_chords_colors(measures_elements[count], chords_luminance[count], chords_volume[count])
        lg2.add_color_stop_rgba(i, chord_color[0], chord_color[1], chord_color[2], 0.5)
        i = i + step
        count = count + 1

    cr.rectangle(0, 0, width, height)

    cr.set_source(lg2)
    cr.fill()

    ######## BACKGROUND END #########

    cr.set_line_width(20)

    horizontal_offset = getMeasureOffset(bwv)
    horizontal_offset_norm = [float(i) / (max(horizontal_offset) + 0.1) * width * 0.975 for i in
                              horizontal_offset]  # posição horizontal

    for part in bwv.parts:

        print("Instrument: " + part.getElementsByClass("Instrument")[0].instrumentName + " " + str(
            part.getElementsByClass("Instrument")[0].midiProgram))

        # Now, since we already found the instruments, we're going to see if we're dealing with chords or notes.

        for measure_i in part.getElementsByClass("Measure"):
            if measure_i.number <= 32:

                print("        Measure: " + str(measure_i.number))

                vertical_offset = getOffsetInMeasure(measure_i)
                vertical_offset_norm = [(float(i)) / (max(vertical_offset) + 0.1) * height * 0.975 if len(
                    vertical_offset) > 1 else height / 2 for i in vertical_offset]

                # Now, we're inside the measures, so lets try to find the notes, chords and rest notes
                for event in measure_i.flat:

                    print("                Event: " + str(event))

                    # case it has a metronome tempo
                    if isinstance(event, tempo.MetronomeMark):
                        resizableSize = getResizableSize(event)

                    if isinstance(event, meter.TimeSignature):
                        timeSignature = getTimeSignature(event)

                    if isinstance(event, note.Note) or isinstance(event, chord.Chord) or isinstance(event, note.Rest):

                        # polygon(sides, radius=1, rotation=0, translation=None)

                        location_x = horizontal_offset_norm[event.measureNumber - 1] + 0.01 * width
                        location_y = vertical_offset_norm[measure_i.flat.index(event)] + 0.025 * height

                        # Case it is a note:
                        if isinstance(event, note.Note):
                            # color
                            colors = color_note(event)

                            # shapealpha can either be the duration or the octave
                            # shapealpha = event.duration.quarterLength
                            shapealpha = 1 - getLuminance(event)  # the higher the song, the less solid it is.
                            # shapealpha = getLuminance(event)
                            # shapealpha = 1 - event.beatStrength
                            # shapealpha = 0.9
                            # shapealpha = getVolume(event)

                            # size
                            size = ((event.duration.quarterLength) * resizableSize + resizableSize) * (
                                        1 / timeSignature)
                            # size = (event.beatStrength * 100)

                            # points
                            getShape(cr, part.getElementsByClass("Instrument")[0], event, location_x, location_y, size,
                                     colors, shapealpha)

                        if isinstance(event, chord.Chord):

                            # size of the chord
                            size = event.duration.quarterLength
                            size_step = len(event)

                            for chord_event in event:
                                # color
                                colors = color_note(chord_event)

                                # shapealpha can either be the duration or the octave
                                # shapealpha = event.duration.quarterLength
                                shapealpha = 1 - getLuminance(chord_event)  # the higher the song, the less solid it is.
                                # shapealpha = getLuminance(chord_event)
                                # shapealpha = chord_event.beatStrength
                                # shapealpha = 0.9
                                # shapealpha = 1

                                # size
                                size = ((chord_event.duration.quarterLength) * resizableSize + resizableSize) * (
                                            1 / timeSignature)

                                # points
                                getShape(cr, part.getElementsByClass("Instrument")[0], event, location_x, location_y,
                                         size, colors, shapealpha)

                                # resize
                                size = size / size_step

        '''cr.translate(width/2, height/2) #point (0, 0) in the center of the canvas 
        cr.rotate(math.radians(360/len(bwv.parts)))
        cr.translate(-width/2, -height/2)'''
    finalName = "static/" + name + str(random.randint(0, 500)) + '.png'
    ims.write_to_png(finalName)

    return finalName


initial = 40
deviation = 20

basedeforms = 1
finaldeforms = 3

minshapes = 20
maxshapes = 25

def available_shapes():
    shapes = ['circle', 'smaller circle', 'rectangle', 'rectanguar spot', 'bigger rectangular spot', 'circle spot', 'square', 'irregular square', 'rhombus']
    return shapes

def main(music_file, shape):

    bwv = converter.parse("static/music_files/" + music_file)
    #bwv.show("text")
    bwv_c = bwv.chordify()

    print(shape)
    for el in shape:
        print(json.loads(el)['midi'])

    #return finalDraw(bwv, bwv_c, music_file)
    return 0