#!/usr/bin/env python
# encoding: utf-8

import os
import tarfile
from Naked.toolshed.file import FileReader
from Naked.toolshed.system import make_path, stdout, stderr

#------------------------------------------------------------------------------
# PUBLIC
#------------------------------------------------------------------------------
def generate_tar_files(file_list):
    """Public function that reads a list of local folders (or files) and generates tar archives from it"""
    # this initial check may be removed as we previously already checked, if this file exists
    # and if the user has moved it in the meantime, we will fail below anyway
    for f in file_list:
        if not os.path.exists(f):
            stderr("Expected file/folder for tar archive creation did not exist.")
            return False

    tar_file_list = []

    for f in file_list:
        if _generate_tar(f):
            tar_file_list.append(f+'.tar')

    return tar_file_list

def remove_tar_files(file_list):
    for f in file_list:
        if not os.path.exists(f) or not f.endswith('.tar'):
            stderr("Expected tar archive not found.")
            #continue
        else:
            os.remove(f)

#------------------------------------------------------------------------------
# PRIVATE
#------------------------------------------------------------------------------
def _generate_tar(filepath):
    """Private function that reads a local folder (or file) and generates a tar archive from it"""
    try:
        with tarfile.open(filepath+'.tar', 'w') as tar:
            tar.add(filepath)
    except tarfile.TarError, e:
        stderr("Error: TAR file creation failed [" + str(e) + "]")
        return False

    return True