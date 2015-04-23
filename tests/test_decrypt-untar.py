#!/usr/bin/env python
# encoding: utf-8

import unittest
import shutil
import os
import pexpect
from Naked.toolshed.system import file_exists, dir_exists


class CryptoUntarArchiveTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.testdir = 'testdir10'
        self.sourcedir = os.path.join(self.testdir, 'sourcedir')
        self.nofile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'nofile.tar.crypt')
        self.nofile_encrypted_archive_destpath = os.path.join(self.testdir, 'nofile.tar.crypt')
        self.singlefile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'singlefile.tar.crypt')
        self.singlefile_encrypted_archive_destpath = os.path.join(self.testdir, 'singlefile.tar.crypt')
        self.multifile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'multifile.tar.crypt')
        self.multifile_encrypted_archive_destpath = os.path.join(self.testdir, 'multifile.tar.crypt')
        self.subdirs_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'subdirs.tar.crypt')
        self.subdirs_encrypted_archive_destpath = os.path.join(self.testdir, 'subdirs.tar.crypt')

        # cleanup old test files if they are present
        if file_exists(self.nofile_encrypted_archive_destpath):
            os.remove(self.nofile_encrypted_archive_destpath)

        if file_exists(self.singlefile_encrypted_archive_destpath):
            os.remove(self.singlefile_encrypted_archive_destpath)

        if file_exists(self.multifile_encrypted_archive_destpath):
            os.remove(self.multifile_encrypted_archive_destpath)

        if file_exists(self.subdirs_encrypted_archive_destpath):
            os.remove(self.subdirs_encrypted_archive_destpath)

        if file_exists(os.path.join(self.testdir, 'nofile.tar')):
            os.remove(os.path.join(self.testdir, 'nofile.tar'))

        if file_exists(os.path.join(self.testdir, 'nofile.tar.crypt')):
            os.remove(os.path.join(self.testdir, 'nofile.tar.crypt'))

        if dir_exists(os.path.join(self.testdir, 'nofile')):
            shutil.rmtree(os.path.join(self.testdir, 'nofile'))

        if file_exists(os.path.join(self.testdir, 'singlefile.tar')):
            os.remove(os.path.join(self.testdir, 'singlefile.tar'))

        if file_exists(os.path.join(self.testdir, 'singlefile.tar.crypt')):
            os.remove(os.path.join(self.testdir, 'singlefile.tar.crypt'))

        if dir_exists(os.path.join(self.testdir, 'singlefile')):
            shutil.rmtree(os.path.join(self.testdir, 'singlefile'))

        if file_exists(os.path.join(self.testdir, 'multifile.tar')):
            os.remove(os.path.join(self.testdir, 'multifile.tar'))

        if file_exists(os.path.join(self.testdir, 'multifile.tar.crypt')):
            os.remove(os.path.join(self.testdir, 'multifile.tar.crypt'))

        if dir_exists(os.path.join(self.testdir, 'multifile')):
            shutil.rmtree(os.path.join(self.testdir, 'multifile'))

        if file_exists(os.path.join(self.testdir, 'subdirs.tar')):
            os.remove(os.path.join(self.testdir, 'subdirs.tar'))

        if file_exists(os.path.join(self.testdir, 'subdirs.tar.crypt')):
            os.remove(os.path.join(self.testdir, 'subdirs.tar.crypt'))

        if dir_exists(os.path.join(self.testdir, 'subdirs')):
            shutil.rmtree(os.path.join(self.testdir, 'subdirs'))

    def submit_same_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        return child

    def test_crypto_untar_no_file_archive_cwd(self):
        shutil.copyfile(self.nofile_encrypted_archive_sourcepath, self.nofile_encrypted_archive_destpath)
        # execute with testdir as the working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto nofile.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory write occurs in the proper spot
            self.assertTrue(dir_exists('nofile'))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('nofile.tar'))
            self.assertTrue(file_exists('nofile.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('nofile')
            os.remove('nofile.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_nofile_archive_notcwd(self):
        shutil.copyfile(self.nofile_encrypted_archive_sourcepath, self.nofile_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/nofile.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory write occurs in the proper spot
        self.assertTrue(dir_exists('testdir10/nofile'))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/nofile.tar'))
        self.assertTrue(file_exists('testdir10/nofile.tar.crypt'))
        # there is no directory written to the current working directory
        self.assertFalse(dir_exists('nofile'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/nofile')
        os.remove(os.path.join('testdir10', 'nofile.tar.crypt'))

    def test_crypto_untar_singlefile_archive_cwd(self):
        shutil.copyfile(self.singlefile_encrypted_archive_sourcepath, self.singlefile_encrypted_archive_destpath)
        # execute with testdir as the working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto singlefile.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory write occurs in the proper spot
            self.assertTrue(dir_exists('singlefile'))
            # unpacked decrypted directory contains single file
            self.assertTrue(file_exists(os.path.join('singlefile', 'test.txt')))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('singlefile.tar'))
            self.assertTrue(file_exists('singlefile.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('singlefile')
            os.remove('singlefile.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_singlefile_archive_notcwd(self):
        shutil.copyfile(self.singlefile_encrypted_archive_sourcepath, self.singlefile_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/singlefile.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory write occurs in the proper spot
        self.assertTrue(dir_exists('testdir10/singlefile'))
        # unpacked decrypted directory contains single file
        self.assertTrue(file_exists(os.path.join('testdir10', 'singlefile', 'test.txt')))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/singlefile.tar'))
        self.assertTrue(file_exists('testdir10/singlefile.tar.crypt'))
        # there is no directory written to the current working directory
        self.assertFalse(dir_exists('singlefile'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/singlefile')
        os.remove(os.path.join('testdir10', 'singlefile.tar.crypt'))

    def test_crypto_untar_multifile_archive_cwd(self):
        shutil.copyfile(self.multifile_encrypted_archive_sourcepath, self.multifile_encrypted_archive_destpath)
        # execute with testdir as the working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto multifile.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory write occurs in the proper spot
            self.assertTrue(dir_exists('multifile'))
            # unpacked decrypted directory contains correct multiple files
            self.assertTrue(file_exists(os.path.join('multifile', 'test.txt')))
            self.assertTrue(file_exists(os.path.join('multifile', 'test2.txt')))
            self.assertTrue(file_exists(os.path.join('multifile', 'test3.txt')))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('multifile.tar'))
            self.assertTrue(file_exists('multifile.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('multifile')
            os.remove('multifile.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_multifile_archive_notcwd(self):
        shutil.copyfile(self.multifile_encrypted_archive_sourcepath, self.multifile_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/multifile.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory write occurs in the proper spot
        self.assertTrue(dir_exists('testdir10/multifile'))
        # unpacked decrypted directory contains single file
        self.assertTrue(file_exists(os.path.join('testdir10', 'multifile', 'test.txt')))
        self.assertTrue(file_exists(os.path.join('testdir10', 'multifile', 'test2.txt')))
        self.assertTrue(file_exists(os.path.join('testdir10', 'multifile', 'test3.txt')))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/multifile.tar'))
        self.assertTrue(file_exists('testdir10/multifile.tar.crypt'))
        # there is no directory written to the current working directory
        self.assertFalse(dir_exists('multifile'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/multifile')
        os.remove(os.path.join('testdir10', 'multifile.tar.crypt'))

    def test_crypto_untar_subdirs_archive_cwd(self):
        shutil.copyfile(self.subdirs_encrypted_archive_sourcepath, self.subdirs_encrypted_archive_destpath)
        # execute with testdir as the working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto subdirs.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory write occurs in the proper spot
            self.assertTrue(dir_exists('subdirs'))
            # unpacked decrypted directory contains unpacked subdirectories
            self.assertTrue(dir_exists(os.path.join('subdirs', 'dir1')))
            self.assertTrue(dir_exists(os.path.join('subdirs', 'dir2')))
            # unpacked decrypted directory contains the correct path for unpacked file in subdirectory
            self.assertTrue(file_exists(os.path.join('subdirs', 'dir1', 'test.txt')))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('subdirs.tar'))
            self.assertTrue(file_exists('subdirs.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('subdirs')
            os.remove('subdirs.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_subdirs_archive_notcwd(self):
        shutil.copyfile(self.subdirs_encrypted_archive_sourcepath, self.subdirs_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/subdirs.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory write occurs in the proper spot
        self.assertTrue(dir_exists('testdir10/subdirs'))
        # unpacked decrypted directory contains unpacked subdirectories
        self.assertTrue(dir_exists(os.path.join('testdir10', 'subdirs', 'dir1')))
        self.assertTrue(dir_exists(os.path.join('testdir10', 'subdirs', 'dir2')))
        # unpacked decrypted directory contains the correct path for unpacked file in subdirectory
        self.assertTrue(file_exists(os.path.join('testdir10', 'subdirs', 'dir1', 'test.txt')))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/subdirs.tar'))
        self.assertTrue(file_exists('testdir10/subdirs.tar.crypt'))
        # there is no directory written to the current working directory
        self.assertFalse(dir_exists('subdirs'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/subdirs')
        os.remove(os.path.join('testdir10', 'subdirs.tar.crypt'))

    def test_crypto_untar_multitar_archives_cwd(self):
        shutil.copyfile(self.subdirs_encrypted_archive_sourcepath, self.subdirs_encrypted_archive_destpath)
        shutil.copyfile(self.singlefile_encrypted_archive_sourcepath, self.singlefile_encrypted_archive_destpath)
        # execute with testdir not working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto subdirs.tar.crypt singlefile.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory writes occur in the proper spot
            self.assertTrue(dir_exists('subdirs'))
            self.assertTrue(dir_exists('singlefile'))
            # unpacked decrypted singlefile directory contains single file
            self.assertTrue(file_exists(os.path.join('singlefile', 'test.txt')))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('singlefile.tar'))
            self.assertTrue(file_exists('singlefile.tar.crypt'))
            # unpacked decrypted subdirs directory contains unpacked subdirectories
            self.assertTrue(dir_exists(os.path.join('subdirs', 'dir1')))
            self.assertTrue(dir_exists(os.path.join('subdirs', 'dir2')))
            # unpacked decrypted subdirs directory contains the correct path for unpacked file in subdirectory
            self.assertTrue(file_exists(os.path.join('subdirs', 'dir1', 'test.txt')))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('subdirs.tar'))
            self.assertTrue(file_exists('subdirs.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('subdirs')
            shutil.rmtree('singlefile')
            os.remove('subdirs.tar.crypt')
            os.remove('singlefile.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_multitar_archives_notcwd(self):
        shutil.copyfile(self.subdirs_encrypted_archive_sourcepath, self.subdirs_encrypted_archive_destpath)
        shutil.copyfile(self.singlefile_encrypted_archive_sourcepath, self.singlefile_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/subdirs.tar.crypt testdir10/singlefile.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory writes occur in the proper spot
        self.assertTrue(dir_exists('testdir10/subdirs'))     # write occurs in testdir10
        self.assertTrue(dir_exists('testdir10/singlefile'))
        self.assertFalse(dir_exists('subdirs'))              # not in cwd
        self.assertFalse(dir_exists('singlefile'))
        # unpacked decrypted singlefile directory contains single file
        self.assertTrue(file_exists(os.path.join('testdir10', 'singlefile', 'test.txt')))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/singlefile.tar'))
        self.assertTrue(file_exists('testdir10/singlefile.tar.crypt'))
        # unpacked decrypted subdirs directory contains unpacked subdirectories
        self.assertTrue(dir_exists(os.path.join('testdir10', 'subdirs', 'dir1')))
        self.assertTrue(dir_exists(os.path.join('testdir10', 'subdirs', 'dir2')))
        # unpacked decrypted subdirs directory contains the correct path for unpacked file in subdirectory
        self.assertTrue(file_exists(os.path.join('testdir10', 'subdirs', 'dir1', 'test.txt')))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/subdirs.tar'))
        self.assertTrue(file_exists('testdir10/subdirs.tar.crypt'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/subdirs')
        shutil.rmtree('testdir10/singlefile')
        os.remove('testdir10/subdirs.tar.crypt')
        os.remove('testdir10/singlefile.tar.crypt')


# TODO: overwrite existing files tests with --overwrite switch

# TODO: do not untar if user has --nountar switch
