import os
import json

# filenames
#home = os.path.dirname(os.path.realpath(__file__))
home, tail = os.path.split(os.path.dirname(os.path.realpath(__file__)))
UNSORTED_FILENAME = home + "/.config/unsorted.json"
SORTED_FILENAME = home + "/.config/sorted.json"
EDITED_FILENAME = home + "/.config/edited.json"

SRC = home + "/share/src"
DEST = home + "/share/dest"

# write INFO to info.json
def write_json(data, data_filename):
    info_json = json.dumps(data)
    f = open(data_filename, "w")
    f.write(info_json)

# load INFO
def load_json(filename):
    if os.path.isfile(filename) == 0:
        return []
    else:
        f = open(filename, "r")
        return json.loads(f.read())

def move_album_data(condition, src, dest):
    for i in reversed(range(len(src))):
        if src[i]["status"] == condition:
            # search edited before adding
            dest.append(src[i])
            src.remove(src[i])

# moves file to destdir
def move_file(file, dest_dir):
    dest = dest_dir + "/" + os.path.basename(file)
    if os.path.isfile(dest):
        return -1

    os.rename(file, dest)

# updates tags based on album_info
# cannot be done with tinytag!
def update_tags(file, album_info): 
    artists = album_info["artist"]
    artist = ""
    if len(artists) > 1:
        for i in artists:
            artist = artist + " & " + i
    artist = artists[0]
    album = album_info["album"]
    year = album_info["year"]

# moves all tracks in album_info to destdir based on artist and album names, updates tag info
def update_files(destdir, album_info, status):
    success = 0
    dest_dir = destdir + "/" + album_info["artist"][0] + "/" + album_info["album"] 
    tracklist = album_info["tracklist"]
    for i in range(len(tracklist)):
        file = tracklist[i]
        if os.path.isdir(dest_dir) == 0:
            os.makedirs(dest_dir)

        if move_file(file, dest_dir) == -1:
            continue
        success += 1
        album_info["tracklist"][i] = dest_dir + "/" + os.path.basename(file)
        #update_tags(file, album_info)

    cover_image = album_info["cover_image"]
    if cover_image != "":
        move_file(cover_image, dest_dir)
    album_info["status"] = status

    return success

# checks if directory is empty, removes it if it is
def deldir(dirpath):
    if len(list(os.scandir(dirpath))) == 0:
        os.rmdir(dirpath)
        return 1
    print("Directory not deleted\n\t {}".format(dirpath))
    return 0

# removes all empty directories
def cleandirs(src):
    for i in os.listdir(src):
        path = src + "/" + i
        if os.path.isdir(path):
            cleandirs(path)
        else:
            return

    if len(os.listdir(src)) == 0:
        os.rmdir(src)
