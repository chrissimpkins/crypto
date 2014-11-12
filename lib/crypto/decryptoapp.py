#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# decrypto
# Copyright 2014 Christopher Simpkins
# MIT license
#------------------------------------------------------------------------------

# Application start
def main():
    import os
    import sys
    import getpass
    from Naked.commandline import Command
    from Naked.toolshed.shell import execute, muterun
    #from Naked.toolshed.state import StateObject
    from Naked.toolshed.system import dir_exists, directory, filename, file_exists, list_all_files, make_path, stdout, stderr

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------
    # [ Instantiate state object ]
    #------------------------------------------------------------------------------
    # state = StateObject()
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
        use_standard_output = False # print to stdout flag
        use_file_overwrite = False # overwrite existing files

        # set user option flags
        if c.option('--stdout') or c.option('-s'):
            use_standard_output = True
        if c.option('--overwrite') or c.option('-o'):
            use_file_overwrite = True

        directory_list = [] # directory paths included in the user entered paths from the command line
        file_list = [] # file paths included in the user entered paths from the command line (and inside directories entered)

        for argument in c.argv:
            if file_exists(argument): # user included a file, add it to the file_list for decryption
                if argument.endswith('.crypt'):
                    file_list.append(argument) # add .crypt files to the list of files for decryption
                elif argument.endswith('.gpg'):
                    file_list.append(argument)
                elif argument.endswith('.asc'):
                    file_list.append(argument)
                elif argument.endswith('.pgp'):
                    file_list.append(argument)
                else:
                    # cannot identify as an encrypted file, give it a shot anyways but warn user
                    file_list.append(argument)
                    stdout("Could not confirm that '" + argument + "' is encrypted based upon the file type.  Attempting decryption.  Keep your fingers crossed...")
            elif dir_exists(argument): # user included a directory, add it to the directory_list
                directory_list.append(argument)
            else:
                if argument[0] == "-":
                    pass # if it is an option, do nothing
                else:
                    stdout("'" + argument + "' does not appear to be an existing file or directory.  Will not attempt decryption for this argument.")

        # unroll the contained directory files into the file_list IF they are encrypted file types
        if len(directory_list) > 0:
            for directory in directory_list:
                directory_file_list = list_all_files(directory)
                for contained_file in directory_file_list:
                    if contained_file.endswith('.crypt'):
                        file_list.append(make_path(directory, contained_file)) # include the file with a filepath 'directory path/contained_file path'
                    elif contained_file.endswith('.gpg'):
                        file_list.append(make_path(directory, contained_file))
                    elif contained_file.endswith('asc'):
                        file_list.append(make_path(directory, contained_file))
                    elif contained_file.endswith('.pgp'):
                        file_list.append(make_path(directory, contained_file))


        # confirm that there are files for encryption, if not abort
        if len(file_list) == 0:
            stderr("Could not identify files for encryption")
            sys.exit(1)

        # get passphrase used to symmetrically decrypt the file
        passphrase = getpass.getpass("Please enter your passphrase: ")
        passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

        if passphrase == passphrase_confirm:
            # begin decryption of each requested file.  the directory path was already added to the file path above
            for encrypted_file in file_list:
                # create the decrypted file name
                decrypted_filename = ""
                if encrypted_file.endswith('.crypt'):
                    decrypted_filename = encrypted_file[0:-6]
                elif encrypted_file.endswith('.gpg') or encrypted_file.endswith('.asc') or encrypted_file.endswith('.pgp'):
                    decrypted_filename = encrypted_file[0:-4]
                else:
                    decrypted_filename = encrypted_file + '.decrypt' # if it was a file without a known encrypted file type, add the .decrypt suffix

                # determine whether file overwrite will take place with the decrypted file
                skip_file = False # flag that indicates this file should not be encrypted
                created_tmp_files = False
                if not use_standard_output: # if not writing a file, no need to check for overwrite
                    if file_exists(decrypted_filename):
                        if use_file_overwrite: # rename the existing file to temp file which will be erased or replaced (on decryption failures) below
                            tmp_filename = decrypted_filename + '.tmp'
                            os.rename(decrypted_filename, tmp_filename)
                            created_tmp_files = True
                        else:
                            stdout("The file path '" + decrypted_filename + "' already exists.  This file was not decrypted.")
                            skip_file = True

                # begin decryption
                if not skip_file:
                    if use_standard_output:
                        system_command = "gpg --batch --passphrase " + passphrase + " -d " + encrypted_file
                        successful_execution = execute(system_command) # use naked execute function to directly push to stdout, rather than return stdout

                        if not successful_execution:
                            stderr("Unable to decrypt file '" + encrypted_file + "'", 0)
                            if created_tmp_files: # restore the moved tmp file to original if decrypt failed
                                tmp_filename = decrypted_filename + '.tmp'
                                if file_exists(tmp_filename):
                                    os.rename(tmp_filename, decrypted_filename)
                        else: # decryption successful but we are in stdout flag so do not include any other output from decrypto
                            pass
                    else:
                        system_command = "gpg --batch -o " + decrypted_filename + " --passphrase " + passphrase + " -d " + encrypted_file
                        response = muterun(system_command)

                        if response.exitcode == 0:
                            stdout("'" + encrypted_file + "' decrypted to '" + decrypted_filename + "'")
                        else: # failed decryption
                            if created_tmp_files:# restore the moved tmp file to original if decrypt failed
                                tmp_filename = decrypted_filename + '.tmp'
                                if file_exists(tmp_filename):
                                    os.rename(tmp_filename, decrypted_filename)
                            # report the error
                            stderr(response.stderr)
                            stderr("Decryption failed for " + encrypted_file)

                # cleanup: remove the tmp file
                if created_tmp_files:
                    tmp_filename = decrypted_filename + '.tmp'
                    if file_exists(tmp_filename):
                        os.remove(tmp_filename)

            # overwrite the entered passphrases
            passphrase = ""
            passphrase_confirm = ""

        else:# overwrite user entered passphrases
            passphrase = ""
            passphrase_confirm = ""
            stderr("The passphrases did not match.  Please enter your command again.")
            sys.exit(1)

    elif c.argc == 1:
    # simple single file or directory processing with default settings
        path = c.arg0
        if file_exists(path): ## SINGLE FILE
            check_existing_file = False # check for a file with the name of new decrypted filename in the directory

            if path.endswith('.crypt'):
                new_filename = path[0:-6] # remove the .crypt suffix
                check_existing_file = True
            elif path.endswith('.gpg') or path.endswith('.pgp') or path.endswith('.asc'):
                new_filename = path[0:-4]
                check_existing_file = True
            else:
                new_filename = path + ".decrypt" #if there is not a standard file type, then add a .decrypt suffix to the decrypted file name
                stdout("Could not confirm that the requested file is encrypted based upon the file type.  Attempting decryption.  Keep your fingers crossed...")

            # confirm that the decrypted path does not already exist, if so abort with warning message to user
            if check_existing_file == True:
                if file_exists(new_filename):
                    stderr("Your file will be decrypted to '" + new_filename + "' and this file path already exists.  Please move the file or use the --overwrite option with your command if you intend to replace the current file.")
                    sys.exit(1)

            # get passphrase used to symmetrically decrypt the file
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            # confirm that the passphrases match
            if passphrase == passphrase_confirm:
                system_command = "gpg --batch -o " + new_filename + " --passphrase " + passphrase + " -d " + path
                response = muterun(system_command)
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""

                if response.exitcode == 0:
                    stdout("Decryption complete")
                    sys.exit(0)
                else:
                    stderr(response.stderr, 0)
                    stderr("Decryption failed")
                    sys.exit(1)
            else:
                stderr("The passphrases did not match.  Please enter your command again.")
                sys.exit(1)
        elif dir_exists(path):  ## SINGLE DIRECTORY
            dirty_directory_file_list = list_all_files(path)
            directory_file_list = [x for x in dirty_directory_file_list if (x.endswith('.crypt') or x.endswith('.gpg') or x.endswith('.pgp') or x.endswith('.asc'))]

            # if there are no encrypted files found, warn and abort
            if len(directory_file_list) == 0:
                stderr("There are no encrypted files in the directory")
                sys.exit(1)

            #prompt for the passphrase
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            if passphrase == passphrase_confirm:
                # decrypt all of the encypted files in the directory
                for filepath in directory_file_list:
                    absolute_filepath = make_path(path, filepath) # combine the directory path and file name into absolute path

                    # remove file suffix from the decrypted file path that writes to disk
                    if absolute_filepath.endswith('.crypt'):
                        decrypted_filepath = absolute_filepath[0:-6] # remove the .crypt suffix
                    elif absolute_filepath.endswith('.gpg') or absolute_filepath.endswith('.pgp') or absolute_filepath.endswith('.asc'):
                        decrypted_filepath = absolute_filepath[0:-4]

                    # confirm that the file does not already exist
                    if file_exists(decrypted_filepath):
                        stdout("The file path '" + decrypted_filepath + "' already exists.  This file was not decrypted.")
                    else:
                        system_command = "gpg --batch -o " + decrypted_filepath + " --passphrase " + passphrase + " -d " + absolute_filepath
                        response = muterun(system_command)

                        if response.exitcode == 0:
                            stdout("'" + absolute_filepath + "' decrypted to '" + decrypted_filepath + "'")
                        else:
                            stderr(response.stderr)
                            stderr("Decryption failed for " + absolute_filepath)
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""
            else:
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
