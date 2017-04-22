# -*- coding: utf-8 -*-
# Parses an rss feed and opens the link associated with the feed if its more recent 
# than the last it opened.
import webbrowser
import feedparser
import json
import time
import os.path
from sys import argv

def create_comic_file(filename):
    if os.path.isfile(filename):
        print("{} already exists".format(filename))
        return
    with open(filename, "w") as comic_file:
        structure = {"default_site": "http://www.internetfirstpage.com/", "comic_rss": []}
        comic_file.write(json.dumps(structure, indent=4, separators=(',', ': ')))

def get_comic_data(filename):
    try:
        rss_file = open(filename,"r")
        json_data = json.load(rss_file)
        rss_file.close()
        return json_data        
    except FileNotFoundError as ex:
        print("{} wasn't found".format("filename"))
    

def write_comic_data(data, filename):
    rss_file = open("comics.json","w")
    rss_file.write(json.dumps(data, indent=4, separators=(',', ': ')))
    rss_file.close()

def reset(filename):
    json_data = get_comic_data(filename)

    for i in range(len(json_data["comic_rss"])):
        json_data["comic_rss"][i]["last"] = ""

    write_comic_data(json_data, filename)
    
def change_default(filename, link):
    json_data = get_comic_data(filename)

    json_data["default_site"] = link
        
    write_comic_data(json_data, filename)    

def add(filename, link):
    json_data = get_comic_data(filename)

    json_data["comic_rss"].append({"link": link, "last": ""})
        
    write_comic_data(json_data, filename)

def open_comics(filename):
    json_data = get_comic_data(filename)
    #Opens the browser
    webbrowser.open(json_data["default_site"])
    #Firefox opens new windows when a open_new_tab is called if the first window 
    #didn't have enough time to open
    time.sleep(5)
    updated_links = []
    # for each comics in the json file, parse the feed to see if it was updated. If it was, open
    for i in range(len(json_data["comic_rss"])):
        feed = feedparser.parse(json_data["comic_rss"][i]["link"])
        # Checks the bozo bit
        # Try-Catch because a surprising amount of things can go wrong in an rss feed entry.
        try:
            if not feed.bozo and feed.entries[0].updated != json_data["comic_rss"][i]["last"]:
                json_data["comic_rss"][i]["last"] = feed.entries[0].updated
                updated_links.append(feed.entries[0]["link"])        
        except Exception as e:
            print("Something is wrong with the comic at {}".format(json_data["comic_rss"][i]["link"]))
        
    write_comic_data(json_data, filename)
    #open all the things !!!!!!!!
    for link in updated_links:
        webbrowser.open_new_tab(link)

if __name__ == '__main__':
    usage = """Use with python3
Usage:
  comics.py <json file>
  comics.py <json_file> [--reset | -r]
  comics.py <json_file> [--create | -c]
  comics.py <json_file> [--add | -a] <rss url>
  comics.py <json_file> [--change_default | -d] <url>"""

    if len(argv) == 2:
        if argv[1] == "--help" or argv[1] == "-h":
            print(usage)
        else:
            open_comics(argv[1])
    elif len(argv) == 3:
        if argv[2] == "--reset" or argv[2] == "-r":
            reset(argv[1])
        elif argv[2] == "--create" or argv[2] == "-c":
            create_comic_file(argv[1])
    elif len(argv) == 4:
        if argv[2] == "--add" or argv[2] == "-a":
            add(argv[1], argv[3])
        elif argv[2] == "--change_default" or argv[2] == "-d":
            change_default(argv[1], argv[3])
    else:
        print(usage)