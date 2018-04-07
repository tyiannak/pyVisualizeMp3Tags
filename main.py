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
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PyLyrics import *


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


def generate_word_cloud(list_of_tags, output_file, show = False):
    text = " ".join([at["artist"].lower().replace(" ", "_")
                     for at in list_of_tags])

    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_file)
    if show:
        plt.show()


def generate_word_cloud_lyrics(list_of_tags, output_file, show = False):
    text = []
    for at in tqdm(list_of_tags):
        try:
            text.append(PyLyrics.getLyrics(at["artist"], at["track"]))
        except:
            print "Sub not found", at["artist"], at["track"]

    text = " ".join(text).lower()
    n_lyrics_found = len(text)
    if n_lyrics_found == 0:
        print "No lyrics were found for the particular files!"
        return

    print "{} lyrics found for {} mp3 files in total".format(len(text),
                                                             len(list_of_tags))

    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_file)
    if show:
        plt.show()


def get_mp3_tags(file_path):
    """! Gets mp3 tags from an audio file

    \param file_path the path to the input audio file

    \returns dict of mp3 tags"""
    try:
        artist = track = album = ""
        mp3Info = ID3(file_path)
        if "TPE1" in mp3Info:
            artist = mp3Info["TPE1"].text[0]
        if "TALB" in mp3Info:
            album = mp3Info["TALB"].text[0]
        if "TIT2" in mp3Info:
            track = mp3Info["TIT2"].text[0]        
        return {"artist": artist, "track": track, "album": album}      
    except:
        return None


def parseArguments():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-i', '--input', nargs=None, required = True,
                        help="Input audio path (folder that contains mp3)")
    parser.add_argument('-o', '--output', nargs=None, required = True,
                        help="Output figure file")
    parser.add_argument('-l', '--lyrics', action='store_true',
                        help="Also produce lyrics tags (needs time)")
    parser.add_argument('-s', '--show', action='store_true',
                        help="Plot results")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()

    mp3_paths = list_mp3_files(args.input, True)
    all_tags = []
    for mp3_path in tqdm(mp3_paths):
        cur_tag = get_mp3_tags(mp3_path)
        if cur_tag:
            all_tags.append(cur_tag)

    generate_word_cloud(all_tags, args.output, args.show)
    if args.lyrics:
        generate_word_cloud_lyrics(all_tags, "lyrics_" + args.output, args.show)

