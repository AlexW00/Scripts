#!/Library/Frameworks/Python.framework/Versions/Current/bin/python3
# -*- coding: utf-8 -*-

# arguments:
# 1: <path-to-folder>

import glob
import os
import sys

def get_latest_file (path_to_folder):
	list_of_files = glob.glob('{path}*'.format(path=path_to_folder))
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

print(get_latest_file(sys.argv[1]), end="")