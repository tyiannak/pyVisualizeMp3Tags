"""! 
@brief main.py
@details This is the main file of pyVisualizeMp3Tags

@author Theodoros Giannakopoulos {tyiannak@gmail.com}
"""

import csv
import sys
import argparse
import os
from tqdm import tqdm
from mutagen.id3 import ID3

def list_mp3_files(path_name, recursively = False):
    """! Lists all audio files in a particular folder

    \param folder path to search for audio files

    \param (\a boolean) (not) recursive search for audio files

    \returns (\a list) of full paths to audio files"""

    extensions = ('.mp3',)
    if recursively:
        audio_files = []
        for root, dirs, files in os.walk(path_name):
            for filename in files:
                if filename.lower().endswith(extensions):
                    audio_files.append(os.path.join(root, filename))
    else:
        audio_files = [os.path.join(path_name, file)
                       for file in os.listdir(path_name) if
                         file.lower().endswith(extensions)]

    return sorted(audio_files)

def get_mp3_tags(file_path):
    """! Gets mp3 tags from an audio file

    \param file_path the path to the input audio file

    \returns dict of mp3 tags"""
    try:
        artist = track = album = ""
        mp3Info = ID3(file_path)
        if ("TPE1" in mp3Info):
            artist = mp3Info["TPE1"].text[0]
        if ("TALB" in mp3Info):
            album = mp3Info["TALB"].text[0]
        if ("TIT2" in mp3Info) :
            track = mp3Info["TIT2"].text[0]        
        return {"artist": artist, "track": track, "album": album}      
    except:
        return {}

def parseArguments():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-i', '--input', nargs=None,
                        help="Input audio paths (list of folders)")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()
    audiopath = args.input

    mp3_paths = list_mp3_files(audiopath, True)
    for mp3_path in tqdm(mp3_paths):
    	print get_mp3_tags(mp3_path)



