#!/usr/bin/env python

'''
Created on 04-02-2011

@author: Seweryn Niemiec
'''

import analog
from optparse import OptionParser

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-a", "--air", dest="air",
                  help="map-AirA file", metavar="FILE")
    parser.add_option("-c", "--cable", dest="cable",
                  help="map-CableA file", metavar="FILE")
    parser.add_option("-s", "--sorted", dest="sorted",
                  help="file with channels list sorted by you;\
                  each line contains two columns separated by TAB char;\
                  first column contains channel name, second column \
                  contains frequency; channel name can have maximum \
                  5 chars; you can aquire frequencies from your cable \
                  operator or use dumper.py (included in this package)\
                  to dump them from map-AirA or map-CableA", metavar="FILE")
    parser.add_option("-d", "--dest", dest="desc",
                  help="destination directory; this script generates two\
                  files: map-AirA and map-CableA; those scripts will\
                  be saved in given directory", metavar="DIR")

    (options, args) = parser.parse_args()
    if not options.air or \
        not options.cable or \
        not options.sorted or \
        not options.desc:
        parser.error("all options are required; try --help for help")

    str_size = analog._struct.size
    chansC = {}
    chansA = {}
    sortedC = []
    sortedA = []

    # read channels from TV exports files
    file = open(options.cable, "rb")
    line = file.read(str_size)
    while line:
        an = analog.AirCableAnalog(line)
        chansC[an.freq] = an
        line = file.read(str_size)
    file.close()

    file = open(options.air, "rb")
    line = file.read(str_size)
    while line:
        an = analog.AirCableAnalog(line)
        chansA[an.freq] = an
        line = file.read(str_size)
    file.close()

    # read sortedC channels
    file = open(options.sorted)
    lines = file.readlines()
    file.close()

    num = 1
    for line in lines:
        line = line.rstrip()

        # skip empty lines
        if len(line) == 0:
            continue

        name, freq = line.split('\t')

        # channel name can not be longer than 5 chars
        if len(name) > 5:
            name = name[:5]
            print "WARN: truncating too long name; new name: '%s'" % name

        try:
            an = chansC[float(freq)]
            an.name = name
            an.number = num
            sortedC.append(an)

            an = chansA[float(freq)]
            an.name = name
            an.number = num
            sortedA.append(an)
        except KeyError:
            print "no chan for freq: " + str(freq)
        num += 1

    #save
    print "GENERATING map-CableA"
    fout = open(options.desc + "/map-CableA", "wb")
    for an in sortedC:
        print an
        fout.write(an.line)
    zeros = "\0" * 40
    for i in range(1000 - len(sortedC)):
        fout.write(zeros)
    fout.close()

    print "GENERATING map-AirA"
    fout = open(options.desc + "/map-AirA", "wb")
    for an in sortedA:
        print an
        fout.write(an.line)
    zeros = "\0" * 40
    for i in range(1000 - len(sortedC)):
        fout.write(zeros)
    fout.close()
