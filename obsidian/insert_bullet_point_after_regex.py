##!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to quickly add a bullet point to your daily note
# TODO: change line 32 to your header of choice (after which the bullet point will be inserted), currently it's ### Thoughts

# arguments:
# 1: <abs-file-path>
# 2: <anchor-regex>: the regex match, after which the string will be appended
# 3: <string-to-append>

import sys
import os
import subprocess

dir = os.path.dirname(__file__) + "/"

file_path = "'" + sys.argv[1] + "'"
anchor_regex = "'" + sys.argv[2] + "'"
string_to_append = "'" + "\n- " + sys.argv[3] + "'"


cmd = "{python} {dir}../utils/insert_after_regex.py {file_path} {anchor_regex} {text}".format(python=sys.executable, dir=dir, file_path=file_path, anchor_regex=anchor_regex, text=string_to_append)
subprocess.check_output(cmd, shell=True)
print(sys.argv[3], end="")