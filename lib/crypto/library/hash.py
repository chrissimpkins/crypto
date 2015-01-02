#!/usr/bin/env python
# encoding: utf-8

import hashlib
from Naked.toolshed.file import FileReader

def generate_hash(filepath, hash="sha256"):
    fr = FileReader(filepath)
    data = fr.read_bin()
    if hash == "sha256":
        return calculate_sha256(data)

def calculate_sha256(binary_string):
    return hashlib.sha256(binary_string).hexdigest()
