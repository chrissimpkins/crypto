#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# crypto
# Copyright 2014 Christopher Simpkins
# MIT license
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# c.cmd = Primary command (crypto <primary command>)
# c.cmd2 = Secondary command (crypto <primary command> <secondary command>)
#
# c.arg_to_cmd = first positional argument to the primary command
# c.arg_to_cmd2 = first positional argument to the secondary command
#
# c.option(option_string, [bool argument_required]) = test for option with optional positional argument to option test
# c.option_with_arg(option_string) = test for option and mandatory positional argument to option
# c.flag(flag_string) = test for presence of a "option=argument" style flag
#
# c.arg(arg_string) = returns the next positional argument to the arg_string argument
# c.flag_arg(flag_string) = returns the flag assignment for a "--option=argument" style flag
#------------------------------------------------------------------------------------

# Application start
def main():
    import sys
    import getpass
    from Naked.commandline import Command
    from Naked.toolshed.shell import muterun
    from Naked.toolshed.state import StateObject
    from Naked.toolshed.system import dir_exists, directory, filename, file_exists, list_all_files, make_path, stdout, stderr

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------
    # [ Instantiate state object ]
    #------------------------------------------------------------------------------
    state = StateObject()
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

        path_list = [] # user entered paths from command line
        directory_list = [] # directory paths included in the user entered paths from the command line
        file_list = [] # file paths included in the user entered paths from the command line (and inside directories entered)

        # determine if argument is an existing file or directory
        for argument in c.argv:
            if file_exists(argument):
                file_list.append(argument) # if it is a file, add the path to the file_list
            elif dir_exists(argument):
                directory_list.append(argument) # if it is a directory, add path to the directory_list

        # add all file paths from user specified directories to the file_list
        contained_dot_file = False
        contained_crypt_file = False

        if len(directory_list) > 0:
            for directory in directory_list:
                directory_file_list = list_all_files(directory)
                for contained_file in directory_file_list:
                    if contained_file[0] == ".":
                        contained_dot_file = True
                    elif contained_file.endswith('.crypt'):
                        contained_crypt_file = True
                    else:
                        # otherwise add to the list for encryption
                        contained_file_path = make_path(directory, contained_file)
                        file_list.append(contained_file_path)

        # confirm that there are files to be encrypted, if not warn user
        if len(file_list) == 0:
            if contained_dot_file == True or contained_crypt_file == True:
                stderr("There were no files identified for encryption.  crypto does not encrypt dot files or previously encrypted (i.e. .crypt) files")
                sys.exit(1)
            else:
                stderr("Unable to identify the requested path(s) for encryption")
                sys.exit(1)
        else:
        # file_list should contain all filepaths from either user specified file paths or contained in top level of directory, encrypt them
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")
            if passphrase == passphrase_confirm:
                for the_file in file_list:
                    encrypted_filepath = the_file + '.crypt' # modify the encrypted filename with .crypt file suffix
                    system_command = "gpg --batch --force-mdc --cipher-algo AES256 -o " + encrypted_filepath + " --passphrase " + passphrase + " --symmetric " + the_file

                    if ascii_armored == True: # add --armor switch to the command if indicated on the CL
                        system_command = "gpg --batch --armor --force-mdc --cipher-algo AES256 -o " + encrypted_filepath + " --passphrase " + passphrase + " --symmetric " + the_file

                    response = muterun(system_command)

                    if response.exitcode == 0:
                        stdout(encrypted_filepath + " was generated from " + the_file)
                    else:
                        stderr(response.stderr, 0)
                        stderr("Encryption failed")
                        sys.exit(1)

                stdout("Encryption complete")
            else:
                stderr("The passphrases did not match.  Please enter your command again.")
                sys.exit(1)

    elif c.argc == 1:
    # simple single file or directory processing with default settings
        path = c.arg0
        if file_exists(path):
        # it is a file, encrypt the single file with default settings
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")
            if passphrase == passphrase_confirm:
                encrypted_filepath = path + '.crypt' # modify the encrypted filename with .crypt file suffix
                system_command = "gpg --batch --force-mdc --cipher-algo AES256 -o " + encrypted_filepath + " --passphrase " + passphrase + " --symmetric " + path

                response = muterun(system_command)
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""
                # check returned status code
                if response.exitcode == 0:
                    stdout(encrypted_filepath + " was generated from " + path)
                    stdout("Encryption complete")
                else:
                    stderr(response.stderr, 0)
                    stderr("Encryption failed")
                    sys.exit(1)
            else:
                stderr("The passphrases did not match.  Please enter your command again.")
        elif dir_exists(path):
        # it is a directory, encrypt all top level files with default settings
            directory_file_list = list_all_files(path)
            # remove dot files and previously encrypted files (with .crypt suffix) from the list of directory files
            count = 0
            for x in directory_file_list:
                if x[0] == '.' or x.endswith('.crypt'):
                    del directory_file_list[count]
                count += 1
            # confirm that there are still files in the list after the dot files and encrypted files are removed
            if len(directory_file_list) == 0:
                stderr("There are no unencrypted files in the directory.")
                sys.exit(1)
            #prompt for the passphrase
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            if passphrase == passphrase_confirm:
                # encrypt all of the files in the directory
                for filepath in directory_file_list:
                    absolute_filepath = make_path(path, filepath) # combine the directory path and file name into absolute path
                    encrypted_filepath = filepath + '.crypt'
                    encrypted_filepath = make_path(path, encrypted_filepath) # combined original directory path with the file paths
                    system_command = "gpg --batch --force-mdc --cipher-algo AES256 -o " + encrypted_filepath + " --passphrase " + passphrase + " --symmetric " + absolute_filepath
                    response = muterun(system_command)
                    if response.exitcode == 0:
                        stdout(encrypted_filepath + " was generated from " + absolute_filepath)
                    else:
                        stderr(response.stderr, 0)
                        stderr("Encryption failed for " + path, 0)
                        sys.exit(1)
            else:
                # passphrases do not match
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
        sys.exit(1) #exit

if __name__ == '__main__':
    main()
