# coding: utf-8
# Copyright 2014 Globo.com Player authors. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

from collections import namedtuple
import os
import posixpath
import errno
import math
import re
import xml.etree.ElementTree as ET
from mediapresentationdescription import MediaPresentationDescription

try:
    import urlparse as url_parser
except ImportError:
    import urllib.parse as url_parser



class Mpd(object):
    DURATION_REGEX_STR = "^(-)?P(([0-9]*)Y)?(([0-9]*)M)?(([0-9]*)D)?(T(([0-9]*)H)?(([0-9]*)M)?(([0-9.]*)S)?)?$"
    DURATION_REGEX = re.compile(DURATION_REGEX_STR)

    def __init__(self, content=None, base_path=None, base_uri=None):
        if content is not None:
            self.manifest = self.parse(content)
        else:
            self.manifest = {}
        self._base_uri = base_uri
        self.base_path = base_path

    def parse(self, content):
        root = ET.fromstring(content)

        manifest = MediaPresentationDescription()
        self.parseRoot(root, manifest)
        return manifest

    def parseRoot(self, mpdRoot, manifest):
        for name, value in mpdRoot.attrib.items():
            if name == "type":
                manifest.dynamic = (value == "dynamic")
            elif name == "mediaPresentationDuration":
                manifest.duration = self.parseDuration(value)
            elif name == "availabilityStartTime":
                manifest.availabilityStartTime = value
            elif name == "maxSegmentDuration":
                manifest.maxSegmentDuration = self.parseDuration(value)
            elif name == "minBufferTime":
                manifest.minBufferTime = self.parseDuration(value)
            elif name == "profiles":
                manifest.profiles = value

    def parseDuration(self, str):
        result = self.DURATION_REGEX.match(str)
        duration = 0
        if result != None:
            negated = not(result.group(1) == None or len(result.group(1)) == 0)
            years = result.group(3)
            if years != None:
                duration += float(years) * 31556908
            months = result.group(5)
            if months != None:
                duration += float(months) * 2629739
            days = result.group(7)
            if days != None:
                duration += float(days) * 86400
            hours = result.group(10)
            if hours != None:
                duration += float(hours) * 3600
            minutes = result.group(12)
            if minutes != None:
                duration += float(minutes) * 60
            seconds = result.group(14)
            if seconds != None:
                duration += float(seconds)
            if negated:
                return -1 * long(duration * 1000)
            else:
                return long(duration * 1000)
        else:
            return long(float(str) * 3600 * 1000)
