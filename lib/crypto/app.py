#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# crypto
# Copyright 2015 Christopher Simpkins
# MIT license
#------------------------------------------------------------------------------

# Application start
def main():
    import sys
    import getpass
    from Naked.commandline import Command
    from Naked.toolshed.shell import muterun
    from Naked.toolshed.system import dir_exists, directory, filename, file_exists, list_all_files, make_path, stdout, stderr

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------------------
    # [ VALIDATION LOGIC ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    #------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from crypto.settings import usage as crypto_usage
        print(crypto_usage)
        sys.exit(1)
    #------------------------------------------------------------------------------------------
    # [ HELP, VERSION, USAGE LOGIC ]
    # Naked framework provides default help, usage, and version commands for all applications
    #   --> settings for user messages are assigned in the lib/crypto/settings.py file
    #------------------------------------------------------------------------------------------
    if c.help():      # User requested crypto help information
        from crypto.settings import help as crypto_help
        print(crypto_help)
        sys.exit(0)
    elif c.usage():   # User requested crypto usage information
        from crypto.settings import usage as crypto_usage
        print(crypto_usage)
        sys.exit(0)
    elif c.version(): # User requested crypto version information
        from crypto.settings import app_name, major_version, minor_version, patch_version
        version_display_string = app_name + ' ' + major_version + '.' + minor_version + '.' + patch_version
        print(version_display_string)
        sys.exit(0)
    #------------------------------------------------------------------------------------------
    # [ APPLICATION LOGIC ]
    #
    #------------------------------------------------------------------------------------------
    elif c.argc > 1:
    # code for multi-file processing and commands that include options
        ## ASCII ARMOR SWITCH
        ascii_armored = False
        if c.option('--armor') or c.option('-a'):
            ascii_armored = True

        ## MAX COMPRESS / COMPRESS ALL SWITCH
        max_compress = False
        if c.option('--space'):
            max_compress = True

        ## NO COMPRESSION SWITCH
        no_compress = False
        if c.option('--speed'):
            no_compress = True

        ## SECURE HASH DIGEST REPORT SWITCH
        report_checksum = False
        if c.option('--hash'):
            report_checksum = True

        path_list = [] # user entered paths from command line
        directory_list = [] # directory paths included in the user entered paths from the command line
        file_list = [] # file paths included in the user entered paths from the command line (and inside directories entered)

        # dot and .crypt file flags for exclusion testing
        contained_dot_file = False
        contained_crypt_file = False

        # determine if argument is an existing file or directory
        for argument in c.argv:
            if file_exists(argument):
                if argument.endswith('.crypt'): # do not include previously encrypted files
                    contained_crypt_file = True
                else:
                    file_list.append(argument) # add appropriate file paths to the file_list
            elif dir_exists(argument):
                directory_list.append(argument) # if it is a directory, add path to the directory_list

        # add all file paths from user specified directories to the file_list
        if len(directory_list) > 0:
            for directory in directory_list:
                directory_file_list = list_all_files(directory)
                for contained_file in directory_file_list:
                    if contained_file[0] == ".":
                        contained_dot_file = True # change the flag + is not included in file_list intentionally (no dot files)
                    elif contained_file.endswith('.crypt'):
                        contained_crypt_file = True # change the flag + is not included in file_list intentionally (no previously encrypted files)
                    else:
                        # otherwise add to the list for encryption
                        contained_file_path = make_path(directory, contained_file)
                        file_list.append(contained_file_path)

        # confirm that there are files to be encrypted, if not warn user
        if len(file_list) == 0:
            if contained_dot_file == True or contained_crypt_file == True:
                stderr("There were no files identified for encryption.  crypto does not encrypt dot files or previously encrypted '.crypt' files.")
                sys.exit(1)
            else:
                stderr("Unable to identify files for encryption")
                sys.exit(1)
        else:
        # file_list should contain all filepaths from either user specified file paths or contained in top level of directory, encrypt them
            passphrase = getpass.getpass("Please enter your passphrase: ")
            if len(passphrase) == 0: # confirm that user entered a passphrase
                stderr("You did not enter a passphrase. Please repeat your command and try again.")
                sys.exit(1)
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")
            if passphrase == passphrase_confirm:
                from crypto.library.cryptor import Cryptor
                the_cryptor = Cryptor(passphrase)

                # run encryption based upon any passed switches
                if ascii_armored:
                    if max_compress:
                        the_cryptor.encrypt_files(file_list, force_nocompress=False, force_compress=True, armored=True, checksum=report_checksum)
                    elif no_compress:
                        the_cryptor.encrypt_files(file_list, force_nocompress=True, force_compress=False, armored=True, checksum=report_checksum)
                    else:
                        the_cryptor.encrypt_files(file_list, force_nocompress=False, force_compress=False, armored=True, checksum=report_checksum)
                else:
                    if max_compress:
                        the_cryptor.encrypt_files(file_list, force_nocompress=False, force_compress=True, armored=False, checksum=report_checksum)
                    elif no_compress:
                        the_cryptor.encrypt_files(file_list, force_nocompress=True, force_compress=False, armored=False, checksum=report_checksum)
                    else:
                        the_cryptor.encrypt_files(file_list, force_nocompress=False, force_compress=False, armored=False, checksum=report_checksum)

                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""
                the_cryptor.cleanup()
            else:
                # passphrases did not match, report to user and abort
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""
                stderr("The passphrases did not match. Please enter your command again.")
                sys.exit(1)

    elif c.argc == 1:
    # simple single file or directory processing with default settings
        path = c.arg0
        if file_exists(path):
        # it is a file, encrypt the single file with default settings
            # confirm that it is not already encrypted, abort if so
            if path.endswith('.crypt'):
                stderr("You are attempting to encrypt an encrypted file.  Please delete the .crypt file and repeat encryption with the original file if this is your intent.")
                sys.exit(1)
            # if passes test above, obtain passphrase from the user
            passphrase = getpass.getpass("Please enter your passphrase: ")
            if len(passphrase) == 0: # confirm that user entered a passphrase
                stderr("You did not enter a passphrase. Please repeat your command and try again.")
                sys.exit(1)
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            if passphrase == passphrase_confirm:
                from crypto.library.cryptor import Cryptor
                the_cryptor = Cryptor(passphrase)
                the_cryptor.encrypt_file(path)
                the_cryptor.cleanup()
            else:
                stderr("The passphrases did not match.  Please enter your command again.")
                sys.exit(1)
        elif dir_exists(path):
        # it is a directory, encrypt all top level files with default settings
            dirty_directory_file_list = list_all_files(path)
            # remove dot files and previously encrypted files (with .crypt suffix) from the list of directory files
            clean_directory_file_list = [x for x in dirty_directory_file_list if x[0] != "." and x.endswith(".crypt") == False] # remove dotfiles and .crypt files

            # confirm that there are still files in the list after the dot files and encrypted files are removed
            if len(clean_directory_file_list) == 0:
                stderr("There are no unencrypted files in the directory.")
                sys.exit(1)

            # create relative file paths for each file in the clean_directory_file_list
            clean_directory_file_list_relpaths = []
            for clean_file in clean_directory_file_list:
                new_file_path = make_path(path, clean_file)
                clean_directory_file_list_relpaths.append(new_file_path)

            #prompt for the passphrase
            passphrase = getpass.getpass("Please enter your passphrase: ")
            if len(passphrase) == 0: # confirm that user entered a passphrase
                stderr("You did not enter a passphrase. Please repeat your command and try again.")
                sys.exit(1)
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            if passphrase == passphrase_confirm:
                from crypto.library.cryptor import Cryptor
                the_cryptor = Cryptor(passphrase)
                the_cryptor.encrypt_files(clean_directory_file_list_relpaths) #encrypt the list of directory files
                the_cryptor.cleanup()
            else:
            # passphrases do not match
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""
                stderr("The passphrases did not match.  Please enter your command again.")
                sys.exit(1)
        else:
            # error message, not a file or directory.  user entry error
            stderr("The path that you entered does not appear to be an existing file or directory.  Please try again.")
            sys.exit(1)

    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        print("Could not complete your request.  Please try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
