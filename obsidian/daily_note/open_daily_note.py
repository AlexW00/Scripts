#!/Library/Frameworks/Python.framework/Versions/Current/bin/python3
# -*- coding: utf-8 -*-

# Script to quickly open your daily note in a markdown editor of your choice

import subprocess
import os
import sys
import yaml


print("version:", sys.version)
dir = os.path.dirname(__file__) + "/"
print("dir:", dir)
config_yaml = open(dir + '../CONFIG.yaml')
config = yaml.load(config_yaml, Loader=yaml.FullLoader)

daily_note_folder = config["dailyNote"]["dailyNoteFolder"]
daily_note_app = config["dailyNote"]["dailyNoteOpenAppPath"]

daily_note_filepath = subprocess.check_output("python3 " + dir + "../../utils/get_latest_file.py " + daily_note_folder, shell=True)
subprocess.check_call(["open", "-a", daily_note_app, daily_note_filepath])