#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EncryptionFileResponse(object):
    def __init__(self):
        self.file_inpath = None
        self.file_outpath = None
        self.encryption_success = False
        self.encryption_message = None
        self.hash_request = False
        self.hash_success = False
        self.hash_message = None
        self.error_occurred = False
        self.error_message = None

