#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path
from crypto.library import hash

class CryptoHashDigestTest(unittest.TestCase):

    def setUp(self):
        self.test_py_crypt_hash = "c386b46760da6416a9584e9809929f54c357362d00f8e1698447a9af6c4e548c" # value from shasum command
        self.test_py_crypt_path = "testdir8/test.py.crypt"
        self.test_py2_crypt_hash = "b58bd8e5a3c1eb1a97625dd6205579369d9551410e3bed291db7271e1cb0018c" #value from shasum command
        self.test_py2_crypt_path = "testdir8/test2.py.crypt"

    def tearDown(self):
        pass

    def submit_same_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        return child

    # confirm that the hash.generate_hash(path) function creates an accurate, expected SHA256 hash value
    def test_unit_hash_expected_value(self):
        generated_hash = hash.generate_hash(self.test_py_crypt_path)
        self.assertEqual(generated_hash, self.test_py_crypt_hash)

    # confirm that a modification to the original file alters the generated hash digest value
    def test_unit_hash_unexpected_value(self):
        generated_hash = hash.generate_hash(self.test_py2_crypt_path) # hash generated from slightly modified file
        self.assertEqual(generated_hash, self.test_py2_crypt_hash) # confirm that the appropriate hash value was generated for modified file
        self.assertNotEqual(generated_hash, self.test_py_crypt_hash) # compare with hash generated from the original expected file

