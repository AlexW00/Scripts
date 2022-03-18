#!/Library/Frameworks/Python.framework/Versions/Current/bin/python3
# -*- coding: utf-8 -*-

# Script to quickly add a bullet point to your daily note
# TODO: change line 32 to your header of choice (after which the bullet point will be inserted), currently it's ### Thoughts

# arguments:
# 1: <thought-string>

import sys
import re
import datetime
import subprocess
import os
import yaml

thought_string = sys.argv[1]

dir = os.path.dirname(__file__) + "/"
config_yaml = open(dir + '../CONFIG.yaml')
config = yaml.load(config_yaml, Loader=yaml.FullLoader)
daily_note_folder = config["dailyNote"]["dailyNoteFolder"]
daily_note_filepath = subprocess.check_output("python3 ~/Developer/Scripts/utils/get_latest_file.py " + daily_note_folder, shell=True)

now = datetime.datetime.now()
hh = str(now.hour) if now.hour > 9 else "0" + str(now.hour)
mm = str(now.minute) if now.minute > 9 else "0" + str(now.minute)
text_to_append = "\n- {input} `{hh}:{mm}`".format(input=thought_string, hh=hh, mm=mm)

with open(daily_note_filepath, "r+") as f:
	read_data = f.read()
	text = re.sub(r'(###.+Thoughts)', r'\1%s' % text_to_append, read_data)
	f.seek(0)
	f.write(text)
	f.truncate()
	print(text_to_append)