#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to quickly add a bullet point to your daily note
# TODO: change line 32 to your header of choice (after which the bullet point will be inserted), currently it's ### Thoughts

# arguments:
# 1: <abs-file-path>
# 2: <anchor-regex>: the regex match, after which the string will be appended
# 3: <string-to-append>

import re
import os
import sys

file_path = sys.argv[1]
anchor_regex = sys.argv[2]
string_to_append = sys.argv[3]

with open(file_path, "r+") as f:
	read_data = f.read()
	text = re.sub(r'({anchor})'.format(anchor=anchor_regex), r'\1{text}'.format(text=string_to_append), read_data)
	f.seek(0)
	f.write(text)
	f.truncate()
	print(string_to_append)