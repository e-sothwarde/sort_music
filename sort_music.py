#!/usr/bin/env python
import os
from tinytag import TinyTag
from funcs import *
import re
import json

def cleanname(name):
    replace_dict = {"/": "_", ".": "", "\"": "", ":": ""}
    # replace any / . in tags
    for i in replace_dict:
        name = name.replace(i, replace_dict[i])

    return name

def getext(file):
    name, ext = os.path.splitext(file)
    return ext

def checktags(tag):
    if tag == None or tag.artist == None or tag.album == None or tag.title == None:
        return 0
    return 1

def ismusic(filename):
    ext = getext(filename)
    if ext in [".mp3", ".flac"]:
        return 1
    return 0

def get_album_name(file):
    tag = TinyTag.get(file)

    if checktags(tag) == 0:
        return 0;

    return cleanname(tag.album)

def get_album_year(file):
    tag = TinyTag.get(file)

    if checktags(tag) == 0:
        return 0;

    return tag.year

def get_info_index(file):
    album = get_album_name(file)
    year = get_album_year(file)
    for i in UNSORTED:
         if i["album"] == album: # and i["year'] == year
             return UNSORTED.index(i)
    return -1

def get_artists(file):
    tag = TinyTag.get(file)

    if checktags(tag) == 0:
        return 0

    separators = " Feat|,|;| & "
    artists = re.split(separators, tag.artist)

    for i in artists:
        i = cleanname(i)

    return artists

# loops through all files, adds to info
def add_info(srcdir):
    album_index = -1
    for f in os.listdir(srcdir):
        file = srcdir + "/" + f

        # check for other filetypes
        if os.path.isdir(file):
            add_info(file)
            continue

        if f[:2] == "._":
            os.remove(file)
            continue

        if getext(file) == ".jpg":
            if album_index != -1:
                UNSORTED[album_index]["cover_image"] = file
            continue

        if ismusic(file) == 0:
            continue

        tag_artists = get_artists(file)
        album_index = get_info_index(file)
        album_name = get_album_name(file)

        if album_index == -1:
            # create new entry, fill with info
            album_year = get_album_year(file)
            album_info = {"album": album_name, "artist": tag_artists, "year": album_year, "tracklist": [file], "cover_image": "", "status": ""}
            album_index = len(UNSORTED)
            UNSORTED.append(album_info)
            continue

        UNSORTED[album_index]["tracklist"].append(file)
        info_artists = UNSORTED[album_index]["artist"]

        if info_artists == "Various Artists":
            continue

        common_artists = list(set(info_artists) & set(tag_artists))
        if common_artists == []:
            UNSORTED[album_index]["artist"] = "Various Artists"
            continue

        UNSORTED[album_index]["artist"] = common_artists


def move_files(destdir):
    for album_info in UNSORTED:
        success = update_files(destdir, album_info, "sorted")
        dest_dir_readable = album_info["artist"][0] + "/" + album_info["album"]
        print(f"Moved {success} files to {dest_dir_readable}")

    move_album_data("sorted", UNSORTED, SORTED);

# checks if all src and dest folders exist, creates them if not
if os.path.isdir(DEST) == 0:
    os.mkdir(DEST)

if os.path.isdir(SRC) == 0:
    os.mkdir(SRC)
    #print("Add files to src folder")
    exit()

UNSORTED = load_json(UNSORTED_FILENAME)
SORTED = load_json(SORTED_FILENAME)

# loop through all files, add to UNSORTED
add_info(SRC)
# loop through UNSORTED, move each file to dest folder
move_files(DEST)

cleandirs(SRC)

write_json(UNSORTED, UNSORTED_FILENAME)
write_json(SORTED, SORTED_FILENAME)

