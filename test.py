__author__ = 'Paulo'
import argparse
import os
import re
import shutil
from ID3 import *

def PrepareFileName(fileName):
    try:
        #remove special symbols
        fileName = re.sub(r'[\\/:"\*?<>|]+', '', fileName, 0, re.UNICODE)
        #remove repeating spaces
        fileName = re.sub(r'[ ]+', ' ', fileName, 0, re.UNICODE)
        fileName = fileName.strip()
    except:
        pass
    return fileName

# command-line args parsing
parser = argparse.ArgumentParser(description='This is a MP3 ID3 parsing tool')

parser.add_argument('--music-dir', action='store', dest='music_dir',
                    help='Set the destination directory')

parser.add_argument('--delete', action='store_true', default=False,
                    dest='boolean_switch',
                    help='Set a switch to true')

results = parser.parse_args()

print 'Destination directory:', results.music_dir

if results.boolean_switch:
    print('The script will delete the file on completion')
else:
    print('The script will NOT delete the file on completion')


for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext == '.mp3':
            try:
                id3info = ID3(filename)
                print id3info
                print 'Title:', id3info['TITLE']
                print 'Artist:', id3info['ARTIST']
                new_name = id3info['ARTIST'] + "-" + id3info['TITLE']
                new_name = PrepareFileName(new_name)

            except InvalidTagError, message:
                print "Invalid ID3 tag:", message

            if new_name:
                try:
                    # Check if the new_name file exists, rename new_name + "1"
                    shutil.copy(
                        os.path.join(dirpath, filename),
                        os.path.join(dirpath, new_name + ".mp3")
                    )
                except:
                    print "Cannot rename file " + filename

            if results.boolean_switch:
                try:
                    os.unlink(filename)
                except:
                    print "Cannot delete file " + filename

