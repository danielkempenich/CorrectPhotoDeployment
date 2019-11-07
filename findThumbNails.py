
from __future__ import print_function
import sys
import argparse
import os
import re
from PIL import Image

#from PIL.ExifTags import TAGS
#print(TAGS[306])

folder_re = re.compile("(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)")

def determine_image_dimensions(infile):
    with Image.open(infile) as im:
        return im.size[0:2]

def determine_date_of_folder(subdir):
    match = folder_re.fullmatch(subdir)
    if match:
        #print ("subdir: ", subdir, " groups: ", match.groups())
        return match.groups()
    else:
        raise Exception("No match")


parser = argparse.ArgumentParser(description='Sort photos in a directory.')
parser.add_argument('-d', '--directory', required=True)
parser.add_argument('--dryrun', action='store_true')
# Using the recommended thumbnail size from youtube guide to define the size of
# which everything below this x,y value is considered a thumbnail
parser.add_argument('-x', default=1280, type=int)
parser.add_argument('-y', default=720, type=int)

args = parser.parse_args()

renames = {}

processedCount = 0
for root, dirs, files in os.walk(args.directory, topdown=False):
    for name in files:
        try:
            processedCount += 1
            if (0 == (processedCount % 1000)):
                print("Processed: ", processedCount, " Current file: ", name, file=sys.stderr)
            subsubdir, subdir = os.path.split(root)
            fullpath = os.path.join(root, name)
            folder_yyyy, folder_mm, folder_dd = determine_date_of_folder(subdir)
            image_xx, image_yy = determine_image_dimensions(fullpath)
            #print("Image: ", fullpath, "xx:", image_xx, " yy:", image_yy)
            if ((image_xx <= args.x) and (image_yy <= args.y)):
                newpath = os.path.join(subsubdir, "thumbnails", name)
                renames[fullpath] = newpath
                #print("Image: ", name, " belongs in: ",  newpath, " not: ", fullpath)
            #else:
                #print("Image: ", name, " (xx=", image_xx, " > ", args.x, " or yy=", image_yy, " > ", args.y, ")")
        except (Exception, IOError):
            pass
        
        
for old, new in renames.items():
    if (args.dryrun):
        print("rename: ", old, ", ", new)
    else:
        basedir, file = os.path.split(new)
        try:
            os.makedirs(basedir, exist_ok=True)
            os.rename(old, new)
        except OSError as ex:
            print(ex)
