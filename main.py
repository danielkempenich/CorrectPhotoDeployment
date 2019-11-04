
from __future__ import print_function
import sys
import argparse
import os
import re
from PIL import Image

#from PIL.ExifTags import TAGS
#print(TAGS[306])
EXIF_TAG_DATETIME = 306
EXIF_TAG_DATETIME_ORIGINAL = 36867
EXIF_TAG_DATETIME_DIGITIZED = 36868

folder_re = re.compile("(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)")

def determine_date_of_image(infile):
    with Image.open(infile) as im:
        #print(infile, im.format, "%dx%d" % im.size, im.mode)
        info = im._getexif()
        datestring = (info.get(EXIF_TAG_DATETIME_ORIGINAL))
        if datestring is None:
            datestring = (info.get(EXIF_TAG_DATETIME_DIGITIZED))
        if datestring is None:
            datestring = (info.get(EXIF_TAG_DATETIME))
        #print ("infile: ", infile, " datestring: ", datestring)
        return datestring.split(" ")[0].split(":")[0:3]

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
            image_yyyy, image_mm, image_dd = determine_date_of_image(fullpath)

            if ((folder_yyyy != image_yyyy) or (folder_mm != image_mm) or (folder_dd != image_dd)):
                newpath = os.path.join(subsubdir, image_yyyy + "-" + image_mm + "-" + image_dd, name)
                renames[fullpath] = newpath
                # print("Image: ", name, " belongs in: ",  newpath, " not: ", fullpath)
            #else:
                # print("Image: ", name, " folder_yyyy: ", folder_yyyy, "image_yyyy: ", image_yyyy)
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
