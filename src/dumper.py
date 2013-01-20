#!/usr/bin/env python

'''
Created on 05-02-2011

@author: Seweryn Niemiec
'''

import analog
import sys

if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print "USAGE %s map-typeA" % sys.argv[0]
        sys.exit(1)

    str_size = analog._struct.size
    chans = {}

    # read channels from TV export file
    file = open(sys.argv[1], "rb")
    line = file.read(str_size)
    while line:
        an = analog.AirCableAnalog(line)
        chans[an.freq] = an
        if an.freq != 0:
            print an
        line = file.read(str_size)
    file.close()
