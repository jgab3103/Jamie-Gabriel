import librosa
from colorsys import rgb_to_hsv, hsv_to_rgb
import music21 as mu
from midi2audio import FluidSynth
import pandas as pd
import numpy as np
import sympy as sp
from IPython.display import HTML, IFrame
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle
from IPython.display import Image
from matplotlib.lines import Line2D
from matplotlib.patches import Patch



def create_sound_file_from_midi(m21_data, file_name):
    m21_data.write('midi', fp = file_name + ".mid")
    fs = FluidSynth()
    fs.midi_to_audio('./' + file_name + ".mid", file_name + '.mp3')
    return(IPython.display.Audio("./" + file_name + ".mp3"))



def complementary(r, g, b):
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


def createMatPlotLibAxisForScore(ax, x_limit, y_limit):    
    ax.set_xticks(range(int(x_limit)))
    ax.set_yticks(range(int(y_limit)))
    [ax.xaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(x_limit))]
    [ax.yaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(y_limit))]
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='k', linestyle='-', linewidth=.5)
    ax.tick_params(axis = "both", which = "both", bottom = False, top = False)
    
    return(ax)


def createScoreFormatting(ax1, yOffset):
    
    # formatting data
    text_kwargs = dict( fontsize=32, color='white')
    
    keyColorCoords = [((0, 1), 80, 1), ((0, 3), 80, 1), ((0, 6), 80, 1), ((0, 8), 80, 1), ((0, 10), 80, 1), 
                 ((0, 13), 80, 1),((0, 15), 80, 1),((0, 18), 80, 1),((0, 20), 80, 1),((0, 22), 80, 1),
                 ((0, 25), 80, 1), ((0, 27), 80, 1), ((0, 30), 80, 1), ((0, 32), 80, 1), ((0, 34), 80, 1),
                 ((0, 37), 80, 1), ((0, 39), 80, 1), ((0, 42), 80, 1), ((0, 44), 80, 1), ((0, 46), 80, 1),
                 ((0, 49), 80, 1), ((0, 51), 80, 1), ((0, 54), 80, 1), ((0, 56), 80, 1), ((0, 58), 80, 1),
                 ((0, 61), 80, 1), ((0, 63), 80, 1), ((0, 66), 80, 1), ((0, 68), 80, 1), ((0, 70), 80, 1),
                 ((0, 73), 80, 1), ((0, 75), 80, 1), ((0, 78), 80, 1), ((0, 80), 80, 1), ((0, 82), 80, 1),
                 ((0, 85), 80, 1), ((0, 87), 80, 1), ((0, 90), 80, 1), ((0, 92), 80, 1), ((0, 94), 80, 1),
                 ((0, 97), 80, 1), ((0, 99), 80, 1), ((0, 102), 80, 1), ((0, 104), 80, 1), ((0, 106), 80, 1),
                 ((0, 109), 80, 1), ((0, 111), 80, 1), ((5, 114), 80, 1), ((0, 116), 80, 1), ((0, 118), 80, 1)]


    
    # Draw black and white keys
    [ax1.add_patch(Rectangle((keyColorCoords[i][0][0],keyColorCoords[i][0][1] - yOffset), keyColorCoords[i][1], keyColorCoords[i][2], color="#EBECF0", zorder = -10)) for i in range(len(keyColorCoords))]

    ax1.add_patch(Rectangle((74, 0), 10, 80, color = "black"))
    

    return(ax1)


def convertDataForScoreVisualisation(scoreDataAsDF, startMeasure, endMeasure):

    df1 = scoreDataAsDF[(scoreDataAsDF.measureNumber >= startMeasure) & (scoreDataAsDF.measureNumber <= endMeasure) & (scoreDataAsDF.midiNumber != -1)]

    offsetForStart = min(df1.offsetAsFloat)
    minMidiNumber = min(df1.midiNumber)
    maxMidiNumber = max(df1.midiNumber)
   
    df2 = df1[["instrument", "part","measureNumber", "offsetAsFloat", "midiNumber", "nameWithOctave", "quarterLengthDurationAsFloat", "partColor"]].copy().reset_index()

    df2['height'] = 1
    heightNormalize = df2.groupby(by=["offsetAsFloat", "midiNumber"]).sum().reset_index()[['offsetAsFloat', 'midiNumber', 'height']]
    new_df = pd.merge(df2, heightNormalize,  how='left', left_on=['offsetAsFloat','midiNumber'], right_on = ['offsetAsFloat','midiNumber'])
    df = new_df.sort_values(by = [ "offsetAsFloat", "midiNumber"]).reset_index()
    df["divider"] = df.groupby((df["height_y"]!=df["height_y"].shift()).cumsum()).cumcount() + 1
    df['divider'] = np.where(df.height_y == 1,1, df.divider)
    df['width'] = df.height_x / df.height_y
    
    
    df['adjustedHeightOffset'] = ((df.height_x / df.height_y) * df.divider) - df.width
    
    df['new_col'] = list(zip(df["offsetAsFloat"]-offsetForStart, (df["midiNumber"] - minMidiNumber) + df['adjustedHeightOffset'] ))
    df['col2'] = list(zip(df["new_col"], df["quarterLengthDurationAsFloat"], df["width"], df["partColor"], df['nameWithOctave']))
    

    coords = df.col2.values

    return([coords, minMidiNumber, maxMidiNumber, df])



def visualizeScore(scoreData, fromMeasure = None, toMeasure = None, reduce = False):
    
    coords1 = convertDataForScoreVisualisation(scoreData, fromMeasure, toMeasure)

    text_kwargs = dict( fontsize=10, color='orange')

    legend_elements = [Line2D([0], [0], color='b', lw=4, label='Violin'),
                       Line2D([0], [0], marker='o', color='w', label='Viola',
                              markerfacecolor='g', markersize=15),
                       Patch(facecolor='orange', edgecolor='r',
                             label='Cello')]



    # DRAW NOTES
    fig, (ax1) = plt.subplots(1, 1, figsize=(20, 12))

    ax1 = createMatPlotLibAxisForScore(ax1, 16, (coords1[2] - coords1[1]) + 5)

    t = [ax1.add_patch(Rectangle(coords1[0][i][0], coords1[0][i][1], coords1[0][i][2], color = coords1[0][i][3])) for i in range(len(coords1[0]))]

    u = [ax1.text(coords1[0][j][0][0], coords1[0][j][0][1], coords1[0][j][4], **text_kwargs) for j in range(len(coords1[0]))]


    ax1.legend(handles=legend_elements, loc='upper right')

    f1 = createScoreFormatting(ax1, coords1[1])


def convertScoreToDF(scoreData = None, scoreName = None, scoreMovement = None):
    # examine the list of parts
    partList = scoreData.getElementsByClass(mu.stream.Part)
    pList = []
    for i in range(0, len(partList)):
        pList.append(partList[i])
        
        
    events = []

    currentNumerator = None
    currentDenominator = None
    currentInstrument = None
    currentInstrumentName = None
    currentPartName = None


    for eachPart in pList:


        for el in eachPart.flatten():

            eventDictionary = {}
            eventDictionary['offset'] = el.offset
            eventDictionary['quarterLengthDuration'] = el.duration.quarterLength
            eventDictionary['measureNumber'] = el.measureNumber
            eventDictionary['currentNumerator'] = currentNumerator
            eventDictionary['currentDenominator'] = currentDenominator
            eventDictionary['instrument'] = currentInstrumentName
            eventDictionary['part'] = currentPartName


            currentType = str(type(el))

            if currentType == "<class 'music21.meter.base.TimeSignature'>":

                currentNumerator = el.numerator
                currentDenominator = el.denominator

            if "instrument" in currentType:

                currentInstrumentName = el.instrumentName
                currentPartName = el.partName

            if currentType == "<class 'music21.note.Rest'>":
                #print("REST")
                eventDictionary['nameWithOctave'] = "NA"
                eventDictionary['midiNumber'] = -1
                eventDictionary['fullName'] = "Rest"
                eventDictionary['name'] = "NA"
                eventDictionary['octave'] = "NA"
                events.append(eventDictionary)


            if currentType == "<class 'music21.note.Note'>":
                eventDictionary['nameWithOctave'] = el.nameWithOctave
                eventDictionary['midiNumber'] = el.pitches[0].midi
                eventDictionary['fullName'] = el.pitches[0].fullName
                eventDictionary['name'] = el.pitches[0].name
                eventDictionary['octave'] = el.pitches[0].octave
                events.append(eventDictionary)

            elif currentType == "<class 'music21.chord.Chord'>":
      

                for eachNote in el:
             
                    tempEventDictionary = eventDictionary.copy()

                    tempEventDictionary['nameWithOctave'] = eachNote.nameWithOctave
                    tempEventDictionary['midiNumber'] = eachNote.pitches[0].midi
                    tempEventDictionary['fullName'] = eachNote.pitches[0].fullName
                    tempEventDictionary['name'] = eachNote.pitches[0].name
                    tempEventDictionary['octave'] = eachNote.pitches[0].octave
                    events.append(tempEventDictionary)
           
                    
    scoreEventData = pd.DataFrame(events)
    scoreEventData['offsetAsFloat'] = scoreEventData['offset'].astype(float)
    scoreEventData['quarterLengthDurationAsFloat'] = scoreEventData.quarterLengthDuration.astype(float)
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(scoreEventData.part)))
    scoreEventData['partColor'] = colors.tolist()
    scoreEventData['scoreName'] = scoreName
    scoreEventData['movement'] = scoreMovement
    
    return(scoreEventData)




from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 60  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

for pitch in degrees:
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    time = time + 1

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    
    
#fs = FluidSynth()
#fs.midi_to_audio('./major-scale.mid', 'again.mp3')
#import IPython

#IPython.display.Audio('./again.mp3')