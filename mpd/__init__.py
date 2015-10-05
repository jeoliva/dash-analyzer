# coding: utf-8
# Copyright 2014 jeoliva author. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

import sys
PYTHON_MAJOR_VERSION = sys.version_info

import os
import posixpath
import re
from cookielib import CookieJar

try:
    import urlparse as url_parser
    import urllib2
    cj = CookieJar()
    cookieProcessor = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookieProcessor)
    urlopen = opener.open
except ImportError:
    import urllib.parse as url_parser
    from urllib.request import urlopen as url_opener
    urlopen = url_opener

from mpd import Mpd

def load(uri):
    if is_url(uri):
        return _load_from_uri(uri)
    else:
        return _load_from_file(uri)

def getCookieProcessor():
    return cookieProcessor

# Support for python3 inspired by https://github.com/szemtiv/m3u8/
def _load_from_uri(uri):
    resource = urlopen(uri)
    base_uri = _parsed_url(_url_for(uri))
    if PYTHON_MAJOR_VERSION < (3,):
        content = _read_python2x(resource)
    else:
        content = _read_python3x(resource)
    return Mpd(content, base_uri=base_uri)

def _url_for(uri):
    return urlopen(uri).geturl()

def _parsed_url(url):
    parsed_url = url_parser.urlparse(url)
    prefix = parsed_url.scheme + '://' + parsed_url.netloc
    base_path = posixpath.normpath(parsed_url.path + '/..')
    return url_parser.urljoin(prefix, base_path)

def _read_python2x(resource):
    return resource.read().strip()

def _read_python3x(resource):
    return  resource.read().decode(resource.headers.get_content_charset(failobj="utf-8"))

def _load_from_file(uri):
    with open(uri) as fileobj:
        raw_content = fileobj.read().strip()
    base_uri = os.path.dirname(uri)
    return Mpd(raw_content, base_uri=base_uri)

def is_url(uri):
    return re.match(r'https?://', uri) is not None
