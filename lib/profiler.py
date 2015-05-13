#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile, pstats, StringIO

def profile():
    # ------------------------------------------------------------------------------
    # Setup a profile
    # ------------------------------------------------------------------------------
    pr = cProfile.Profile()
    # ------------------------------------------------------------------------------
    # Enter setup code below
    # ------------------------------------------------------------------------------
        # Optional: include setup code here
        
    # import os
    # from crypto.library.cryptor import Cryptor
    # from Naked.toolshed.system import list_all_files, make_path
    # c = Cryptor("test")
    # test_dir = make_path(os.path.expanduser('~'), 'Desktop', 'profiletests')
    # the_file_list = list_all_files(test_dir)
    # x = 0
    # for i in the_file_list:
        # the_file_list[x] = make_path(test_dir, i)
        # x += 1

    # ------------------------------------------------------------------------------
    # Start profiler
    # ------------------------------------------------------------------------------
    pr.enable()

    # ------------------------------------------------------------------------------
    # BEGIN profiled code block
    # ------------------------------------------------------------------------------
        # include profiled code here

    # c.encrypt_files(the_file_list)
    # ------------------------------------------------------------------------------
    # END profiled code block
    # ------------------------------------------------------------------------------
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.strip_dirs().sort_stats("time").print_stats()
    print(s.getvalue())

if __name__ == '__main__':
    profile()