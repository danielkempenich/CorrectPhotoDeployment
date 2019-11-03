from __future__ import print_function
import sys
import argparse
import os
import re
from PIL import Image
from PIL.ExifTags import TAGS


def print_exif_tags(infile):
    with Image.open(infile) as im:
        print(infile, im.format, "%dx%d" % im.size, im.mode)
        info = im._getexif()
        for tagid, value in info.items():
            print ("\t[", TAGS[tagid], "] = ", value)



parser = argparse.ArgumentParser(description='Print photo metadata.')
parser.add_argument('-f', '--file', required=True)

args = parser.parse_args()

print_exif_tags(args.file)

