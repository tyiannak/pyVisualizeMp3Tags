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


def get_mp3_tags(file_path):
    """! Gets mp3 tags from an audio file

    \param file_path the path to the input audio file

    \returns dict of mp3 tags"""
    return {}



def parseArguments():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-i', '--input', nargs='+',
                        help="Input audio paths (list of folders)")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()
    audiopaths = args.input

    print audiopaths
