#!/usr/bin/env python
import os
from funcs import *


def int_input(response, max_value):
    try:
        n = int(response)
    except ValueError:
        print("Wrong!!!") # put in loop to allow multiple attempts
        return -1

    if n > max_value:
        print("Out of Bounds!!!")
        return -1

    return n

# loop through first n albums in info.json, print out album and artist name. User enters corresponding indexes to edit
def print_edit_albums(n):
    os.system("clear")
    for i in range(n):
        album = SORTED[i]["album"]
        artist = SORTED[i]["artist"][0]
        print(f"{i}: {album} - {artist}")
        SORTED[i]["status"] = "edited"
    print("Enter album number to edit or 'Done' to finish")

def edit_select():
    edit_index = -1
    while (edit_index == -1):
        response = input()
        if response == "Done":
            return -1

        edit_index = int_input(response, n-1)
    return edit_index

SORTED = load_json(SORTED_FILENAME)
EDITED = load_json(EDITED_FILENAME)

# select how many albums to edit
os.system("clear")
new_entries = len(SORTED)
print(f"You have {new_entries} new entries to edit. How many would you like to edit?")
n = -1
while (n == -1):
    n = int_input(input(), new_entries)

# edit album info
while(1):
    print_edit_albums(n)

    edit_index = edit_select()
    if edit_index == -1:
        break
    
    album_info = SORTED[edit_index]
    album = album_info["album"]
    artist = album_info["artist"][0]

    # print tracklist
    os.system("clear")
    print(f"{album} - {artist}\nTracklist:\n")
    for track in album_info["tracklist"]:
        print(os.path.basename(track))
        
    print("Enter new album name: (Leave blank to keep unchanged)")
    new_album_name = input()
    print("Enter new artist name: (Leave blank to keep unchanged)")
    new_artist_name = input()

    if new_album_name != "":
        album_info["album"] = new_album_name
    if new_artist_name != "":
        album_info["artist"] = [new_artist_name]

# moves data from SORTED to EDITED
move_album_data("edited", SORTED, EDITED);

# changes filenames
for album_info in EDITED:
    success = update_files(DEST, album_info, "edited")

cleandirs(DEST)
write_json(SORTED, SORTED_FILENAME)
write_json(EDITED, EDITED_FILENAME)
