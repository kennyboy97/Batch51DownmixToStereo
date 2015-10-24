__author__ = 'kenhansen'

"""
Step 1: ask for the directory where all the 5.1 PT sessions live.
Step 2: Scan through subdirectories to find the WAVs and confirm there are 6 WAVs. Build a list of the input WAVs
changing the PATH structure from UNIX to TERMINAL
Step 3: Reorder the input WAVs to be L, R, C, LFE, LS, RS
Step 4: Run 3 FFMPEG subprocesses in serial; Interleave 6 WAVS to 1 WAV, Downmix 6ch WAV to 2ch WAV, bring gain down of
final DS WAV by 6dB
Step 5: Remove intermediary Interleaved.wav and Downmixed.wav files
NOTE: Using Lo/Ro downmix to Stereo instead of Lt/Rt ProLogic II downmix.
Process takes approx. 4 min. per 60min. file.
"""

import subprocess
import sys, os
import Tkinter as tk
import tkFileDialog

root = tk.Tk()
root.withdraw()

print "Choose the source directory for the MOV files"
directory = tkFileDialog.askdirectory()

def reorder(wavs):
    for i in range (len(wavs)):
        if wavs[i].endswith(".L.wav"):
            L=i
        if wavs[i].endswith(".R.wav"):
            R=i
        if wavs[i].endswith(".C.wav"):
            C=i
        if wavs[i].endswith(".LFE.wav"):
            LFE=i
        if wavs[i].endswith(".LS.wav"):
            LS=i
        if wavs[i].endswith(".RS.wav"):
            RS=i
    wavs = [wavs[L], wavs[R], wavs[C], wavs[LFE], wavs[LS], wavs[RS]]
    return wavs

def RemoveFiles(i, d):
    Int=i.replace("\ "," ")
    Down=d.replace("\ "," ")
    os.remove(Int)
    os.remove(Down)

def StereoDownmix(wavs):
    neworderwavs = reorder(wavs)
    path = os.path.dirname(neworderwavs[0])
    Interleavedwav = os.path.join(path, 'Interleaved.wav')
    Downmixedwav = os.path.join(path, 'Downmixed.wav')
    DS=neworderwavs[0]
    FinalDS=str(DS[:-6]+"-DwnmxdLTRT.wav")
    subprocess.call('ffmpeg -i '+neworderwavs[0]+' -i '+neworderwavs[1]+' -i '+neworderwavs[2]+' -i '+neworderwavs[3]+' -i '+neworderwavs[4]+' -i '+neworderwavs[5]+' -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a]amerge=inputs=6[aout]" -map "[aout]" -acodec pcm_s24le '+Interleavedwav, shell=True)
    subprocess.call('ffmpeg -i '+Interleavedwav+' -ac 2 -acodec pcm_s24le '+Downmixedwav, shell=True)
    subprocess.call('ffmpeg -i '+Downmixedwav+' -af "volume=6dB" -acodec pcm_s24le '+FinalDS, shell=True)
    RemoveFiles(Interleavedwav, Downmixedwav)

for root, dirs, files in os.walk(directory):
    for d in dirs:
        subdir = os.path.join(directory, d)
        for root, dirs, files in os.walk(subdir):
            wavs = []
            for file in files:
                if file.endswith(".wav"):
                    full_file = str(os.path.join(root, file))
                    full_file = full_file.replace(" ","\ ")
                    wavs.append(full_file)
            if len(wavs) == 6:
                StereoDownmix(wavs)
