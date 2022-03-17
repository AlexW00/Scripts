#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os

daily_note_folder = "~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Obs/6_PRIVATE/Daily\ Notes/"
daily_note_filepath = subprocess.check_output("python3 ~/Developer/Scripts/utils/get_latest_file.py " + daily_note_folder, shell=True)
subprocess.check_call(["open", "-a", "/Applications/Setapp/Focused.app", daily_note_filepath])