#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from crypto.library.cryptor import Cryptor

class CryptoCompressionCheckTest(unittest.TestCase):

    def setUp(self):
        self.pdf_file = "test.pdf"
        self.mp3_file = "test.mp3"
        self.gz_file = "test.tar.gz"
        self.png_file = "test.png"
        self.jpg_file = "test.jpg"
        self.txt_file = "test.txt"
        self.py_file = "test.py"
        self.nosuffix_file = "test"

    def tearDown(self):
        pass
    
    # TODO: add file types with different length suffixes
    
    # binary file checks
    
    def test_binary_pdf_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.pdf_file)
        response_txt = c._is_common_text(self.pdf_file)
        self.assertTrue(response_bin)
        self.assertFalse(response_txt)
        
    def test_binary_mp3_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.mp3_file)
        response_txt = c._is_common_text(self.mp3_file)
        self.assertTrue(response_bin)
        self.assertFalse(response_txt)
        
    def test_binary_gz_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.gz_file)
        response_txt = c._is_common_text(self.gz_file)
        self.assertTrue(response_bin)
        self.assertFalse(response_txt)
        
    def test_binary_png_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.png_file)
        response_txt = c._is_common_text(self.png_file)
        self.assertTrue(response_bin)
        self.assertFalse(response_txt)
        
    def test_binary_jpg_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.jpg_file)
        response_txt = c._is_common_text(self.jpg_file)
        self.assertTrue(response_bin)
        self.assertFalse(response_txt)
        
    # text file checks
    
    def test_text_txt_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.txt_file)
        response_txt = c._is_common_text(self.txt_file)
        self.assertFalse(response_bin)
        self.assertTrue(response_txt)
        
    def test_text_py_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.py_file)
        response_txt = c._is_common_text(self.py_file)
        self.assertFalse(response_bin)
        self.assertTrue(response_txt)
        
    # test is_common_binary & _is_common_text function with file without file type suffix in the file name
        
    def test_binary_nosuffix_check(self):
        c = Cryptor("passphrase")
        response_bin = c._is_common_binary(self.nosuffix_file)
        self.assertFalse(response_bin)
        
    def test_text_nosuffix_check(self):
        c = Cryptor("passphrase")
        response_txt = c._is_common_text(self.nosuffix_file)
        self.assertFalse(response_txt)       
        
        
        