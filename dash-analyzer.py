# coding: utf-8
# Copyright 2014 jeoliva author. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

import errno
import os
import logging
import urllib2
import httplib
import sys
import argparse

import mpd
from bitreader import BitReader

def download_url(uri, range=None):
    print("\tDownloading {url}, Range: {range}".format(url=uri, range=range))

    opener = urllib2.build_opener(m3u8.getCookieProcessor())
    if(range is not None):
        opener.addheaders.append(('Range', range))

    response = opener.open(uri)
    content = response.read()
    response.close()

    return content


# MAIN APP
parser = argparse.ArgumentParser(description='Analyze DASH streams and gets useful information')

parser.add_argument('url', metavar='Url', type=str,
               help='Url of the stream to be analyzed')

parser.add_argument('-s', action="store", dest="segments", type=int, default=1,
               help='Number of segments/fragments to be analyzed per rendition')

parser.add_argument('-l', action="store", dest="frame_info_len", type=int, default=30,
               help='Max number of frames per track whose information will be reported')

args = parser.parse_args()

# Sample url: http://dash.edgesuite.net/envivio/dashpr/clear/Manifest.mpd
mpd_obj = mpd.load(args.url)
