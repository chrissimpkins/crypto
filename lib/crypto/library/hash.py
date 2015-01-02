#!/usr/bin/env python
# encoding: utf-8

import hashlib
from Naked.toolshed.file import FileReader

#------------------------------------------------------------------------------
# PUBLIC
#------------------------------------------------------------------------------
def generate_hash(filepath):
    fr = FileReader(filepath)
    data = fr.read_bin()
    return _calculate_sha256(data)


#------------------------------------------------------------------------------
# PRIVATE
#------------------------------------------------------------------------------
def _calculate_sha256(binary_string):
    return hashlib.sha256(binary_string).hexdigest()

