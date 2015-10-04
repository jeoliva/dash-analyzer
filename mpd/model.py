# coding: utf-8
# Copyright 2014 Globo.com Player authors. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

from collections import namedtuple
import os
import posixpath
import errno
import math

try:
    import urlparse as url_parser
except ImportError:
    import urllib.parse as url_parser



class Mpd(object):

    def __init__(self, content=None, base_path=None, base_uri=None):
        if content is not None:
            self.data = self.parse(content)
        else:
            self.data = {}
        self._base_uri = base_uri
        self.base_path = base_path


    def parse(self, content):
        pass
