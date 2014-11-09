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
    from Naked.toolshed.system import dir_exists, directory, filename, file_exists, make_path, stdout, stderr

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
    # [ Command Suite Validation ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    #------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from crypto.settings import usage as crypto_usage
        print(crypto_usage)
        sys.exit(1)
    #------------------------------------------------------------------------------------------
    # [ NAKED FRAMEWORK COMMANDS ]
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
    # [ PRIMARY COMMAND LOGIC ]
    #
    #------------------------------------------------------------------------------------------
    elif c.argc > 1:
    # code for multi-file processing
        pass
    elif c.argc == 1:
    # simple single file or directory processing with default settings
        path = c.arg0
        if file_exists(path):
            # it is a file
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")
            if passphrase == passphrase_confirm:
                encrypted_filepath = path + '.crypt' # modify the encrypted filename with .crypt file suffix
                system_command = "gpg --batch --force-mdc --cipher-algo AES256 -o " + encrypted_filepath + " --passphrase " + passphrase + " --symmetric " + path
                response = muterun(system_command)
                if response.exitcode == 0:
                    stdout(encrypted_filepath + " was generated")
                    stdout("Encryption complete")
                else:
                    stderr(response.stderr, 0)
                    stderr("Encryption failed")
            else:
                stderr("The passphrases did not match.  Please enter your command again.")
            pass
        elif dir_exists(path):
            # it is a directory
            stdout("Dir success")
            pass
        else:
            # error message, not a file or directory.  user entry error
            stderr("The path that you entered does not appear to be an existing file or directory.  Please try again.")



    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        print("Could not complete your request.  Please try again.")
        sys.exit(1) #exit

if __name__ == '__main__':
    main()
