# Batch51DownmixToStereo

This script uses Tkinter to prompt the user for the directory all the source 5.1 ProTools sessions are in.

Session by session, the WAV files are read into an array. Once verified there are 6 WAV files (to make a 5.1), the array is sent to a function calling 3 FFMPEG subprocesses to interleave the 6 WAV files into 1 6channel WAV file, Downmix to standard Stereo, then adjust the gain down by 6dB.

The intermediary Interleaved and Downmixed WAV files are then discarded.
