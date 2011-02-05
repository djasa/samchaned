'''
Created on 04-02-2011

@author: Seweryn Niemiec
'''

import struct

_format = "=ccccccccc h cl h H 12s f cc B B"
_struct = struct.Struct(_format)


class AirCableAnalog(object):
    '''
    This structure comes from
    https://sourceforge.net/apps/phpbb/samygo/viewtopic.php?f=5&t=158&start=80#p7244
    
    Thanks for robert_schl for providing it.
    
    // map-AirA and map-CableA entry format (no header)
    typedef format SCMCHANNEL
    {
       [0] char         Available;         // flag if entry is available for use
       [1] char         Used;            // flag if entry is used
       [2] char         Skip;            // flag if entry is to be skipped by +/-
       [3] char         Source;            // signal source, see enumeration below
       [4] char         Signal;            // signal type, see enumeration below
       [5] char         Modulation;         // modulation, see enumeration below
       [6] char         Locked;            // channel locked (0=open, 1=locked)
       [7] char         Unknown7;         //*14 | 8
       [8] char         Tuned;            //*0 | 1
       [9] short         Number;            //*customized channel number
       [10] char         Unknown11;         //*-1 | 14
       [11] long         Unknown12;         //*0
       [12] short         Preset;            //*pre-assigned channel number
       [13] unsigned short   Length;            // channel name length (in BYTES!)
       [14] unsigned short   Name[6];         // big-endian Unicode characters
       [15] float         Frequency;         // frequency in MHz with fractions
       [16] char         Unknown36;         //* 1
       [17] char         Unknown37;         //*-1
       [18] unsigned char   Favorites;         // favorites, see definitions below
       [19] unsigned char   CRC;
    }
    '''


    def __init__(self, line):
        '''
        Constructor
        '''
        self.line = line
        self.__rawTable = list(_struct.unpack(line))
        index = self.__rawTable[14].index('\0\0')
        self.__name = unicode(self.__rawTable[14][:index], "utf-16-be")

    @property
    def preset(self):
        return self.__rawTable[12]

    @property
    def freq(self):
        return self.__rawTable[15]

    def __getName(self):
        return self.__name
    def __setName(self, name):
        self.__name = name
        nameUTF16 = name.encode("utf-16-be")
        self.__rawTable[13] = 12
        self.__rawTable[14] = nameUTF16 + "\0" * (12 - len(nameUTF16))
        self.__pack()
    name = property(__getName, __setName)

    def __getNumber(self):
        return self.__rawTable[9]
    def __setNumber(self, number):
        self.__rawTable[9] = number
        self.__rawTable[12] = number
        self.__pack()
    number = property(__getNumber, __setNumber)

    def __pack(self):
        self.line = _struct.pack(*self.__rawTable)
        self.__rawTable[19] = self.__crc
        self.line = _struct.pack(*self.__rawTable)

    @property
    def __crc(self):
        sum = 0
        for b in self.line[:-1]:
            sum += ord(b)
        sum = sum % 256
        return sum

    def __repr__(self):
        return "%s\t%g" % (self.name, self.freq)

