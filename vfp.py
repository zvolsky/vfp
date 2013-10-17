# coding: utf8
#-------------------------------------------------------------------------------
# Name:        vfp
# Purpose:     mimics behaviour of some Visual FoxPro functions
#
# Author:      Mirek Zvolsky
#
# Created:     07.12.2011
# Licence:     public domain
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""vfp are few utils, f.e. file utils.
Syntax of some of them is similar to visual foxpro.

.filetostr(filename)                        # read the file AS IS
.strtofile(content, filename, additive)     # write str or encode&write unicode
.strtoutf8file(content, filename, additive) # write unicode or decode&write str
                                            #       into utf8 file
.suredir(path)                              # create dir if not present

- see source code for more parameters and parameters details
"""

ignore_write_errors = False
usual_encoding = 'mbcs'
    # 'mbcs' is machine standard Windows encoding
    # change this outside of Windows), otherwise you will receive errors if
    #   strtofile() is called with unicode content and wo unicode_encoding par
    #   -or- strtoutf8file() is called with str content and wo str_encoding par 

import os

def filetostr(fname):
    """return content of the file"""
    f = open(fname, 'rb')
    content = f.read()
    f.close()
    return content

def strtofile(content, fname, additive=0, unicode_encoding=usual_encoding):
    """writes string to file
    expression - string to output to the fname file
    fname - output filename
    additive - default=rewrite, 1 (or True)=append
        vfp pars nFlag>1 (nFlag ~ additive) not implemented yet"""
            # mbcs in windows is the default encoding,
            #   f.e. in czech windows it means windows-1250
            # on non-windows systems enter 'windows-1250' explicitly
    length = 0
    if content or not additive:
        if type(content)==unicode:
            encoded = content.encode(unicode_encoding)
        else:
            encoded = content
        try:
            suredir(fname, is_filename=True)
            f = open(fname, 'ab' if additive else 'wb')
            f.write(encoded)
            f.close()
            length = len(encoded)
        except:
            if not ignore_write_errors:
                raise IOError, 'cannot write to file'
    return length

def strtoutf8file(content, fname, additive=0, str_encoding=usual_encoding):
    """writes string to file
    expression - string to output to the fname file
    fname - output filename
    additive - default=rewrite+leadingbytes, -1 rewrite-leadingbytes,
               1 (or True)=append               
        vfp pars nFlag>1 (nFlag ~ additive) not implemented yet"""
            # mbcs in windows is the default encoding,
            #   f.e. in czech windows it means windows-1250
            # on non-windows systems enter 'windows-1250' explicitly
    length = 0
    if content or not additive:
        if type(content)==str:
            content = unicode(content, str_encoding)
                    # mbcs in windows is the default encoding,
                    #   f.e. in czech windows it means windows-1250
        if additive:
            encoded = ''
        else:
            encoded = chr(239)+chr(187)+chr(191) # utf8leadingbyte
        encoded += content.encode('utf-8')
        try:
            suredir(fname, is_filename=True)
            f = open(fname, 'ab' if additive else 'wb')
            f.write(encoded)
            f.close()
            length = len(encoded)
        except:
            if not ignore_write_errors:
                raise IOError, 'cannot write to file'
    return length

def suredir(path, is_filename=False):
    '''create directory if it doesn't exist
    with is_filename=True you can have 1st param filename:
        it will create required path
    '''
    if is_filename:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)
