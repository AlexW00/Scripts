#!/usr/bin/env python
# -*- coding: utf-8 -*-

# arguments:
# 1: <thought-string>

import sys
import re
import datetime
import subprocess

thought_string = sys.argv[1]

now = datetime.datetime.now()
hh = str(now.hour) if now.hour > 9 else "0" + str(now.hour)
mm = str(now.minute) if now.minute > 9 else "0" + str(now.minute)
text_to_append = "\n- {input} `{hh}:{mm}`".format(input=thought_string, hh=hh, mm=mm)

daily_note_folder = "~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Obs/6_PRIVATE/Daily\ Notes/"
daily_note_filepath = subprocess.check_output("python3 ~/Developer/Scripts/utils/get_latest_file.py " + daily_note_folder, shell=True)

with open(daily_note_filepath, "r+") as f:
	read_data = f.read()
	text = re.sub(r'(###.+Thoughts)', r'\1%s' % text_to_append, read_data)
	f.seek(0)
	f.write(text)
	f.truncate()
	print(text_to_append)