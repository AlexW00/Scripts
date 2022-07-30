#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to return the path to the latest created file in a folder

# arguments:
# 1: <path-to-folder>

import glob
import os
import sys
import platform


def creation_date(path_to_file):
	"""
	Try to get the date that a file was created, falling back to when it was
	last modified if that isn't possible.
	See http://stackoverflow.com/a/39501288/1709587 for explanation.
	"""
	if platform.system() == 'Windows':
		return os.path.getctime(path_to_file)
	else:
		stat = os.stat(path_to_file)
		try:
			return stat.st_birthtime
		except AttributeError:
			# We're probably on Linux. No easy way to get creation dates here,
			# so we'll settle for when its content was last modified.
			return stat.st_mtime

def get_latest_file (path_to_folder):
	list_of_files = glob.glob('{path}*'.format(path=path_to_folder))
	latest_file = max(list_of_files, key=lambda file: creation_date(file))
	return latest_file

print(get_latest_file(sys.argv[1]), end="")