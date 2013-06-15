# ivrbase.py

import pycurl
import urllib
import StringIO
import traceback
import gettext
import inspect
import os
import re
from urllib import urlencode
from tempfile import mktemp

from fakesession import FakeSession
from tts import GoogleTts

class IvrBaseMeta(type):
    def __new__(cls, name, bases, dct):
        if not dct.has_key('sounds_path'):
            dct['sounds_path'] = name.lower() 
        return super(IvrBaseMeta, cls).__new__(cls, name, bases, dct)


class IvrBase(object):
    '''Independent IVR Base Class'''
    __metaclass__ = IvrBaseMeta
    debug = False
    timeout = 3000 # ms
    retry = 3 
    land_phone_regex = "0?[1-9][1-9][2-9][0-9]{7}"
    mobile_phone_regex = "0?[1-9][1-9][5-9][0-9]{7}"
    tts = GoogleTts

    def __init__(self, dnis=None):
        self.dnis = dnis
        self.log_tag = self.__class__.__name__.lower()
        if self.callerid:
            self.log_filename = "/tmp/%s.%s.log" % (self.log_tag, self.callerid)
        else:
            self.log_filename = "/tmp/%s.log" % self.log_tag

    @property
    def callerid(self):
        return None

    def answer(self):
        raise NotImplementedError

    def hangup(self):
        raise NotImplementedError

    def input(self, sound, invalid_sound, min_length, max_length, retry=None, timeout=None, valid_regex=None):
        raise NotImplementedError

    def playback(self, sound_file, text=None):
        raise NotImplementedError

    def say(self, text, sound_file=None):
        if not sound_file:
            sound_file = self.tts.slugify(text)+".wav"
        self.playback(sound_file, text)
 
    def input_phone(self, sound, invalid_sound):
        phone = self.input(sound, invalid_sound, 10, 11, valid_regex=land_phone_regex)
        phone = self.clean_phone(phone)
        return phone

    def input_mobilephone(self, sound, invalid_sound):
        phone = self.input(sound, invalid_sound, 10, 11, valid_regex=mobile_phone_regex)
        phone = self.clean_phone(phone)
        return phone

    def run(self):
        '''Start Ivr'''
        try:
            self.handler()
        except Exception, e:
            tb = traceback.format_exc()
            self.log(tb)
        
    def handler(self):
        '''start ivr'''
        try:
            self.run()
        except Exception, e:
            tb = traceback.format_exc()
            self.log(tb)

    def write_log_file(self, msg):
        f = open(self.log_filename, 'a')
        f.write(msg+"\n")
        f.close()

    def log(self, msg="CheckPoint", level="info"):
        line = inspect.currentframe().f_back.f_lineno
        msg = "%s(%i): %s: %s" % (self.log_tag.upper(), line, level.upper(), msg)
        if self.debug or level=="error":
            print msg
            self.write_log_file(msg)
        return msg

    def get_sound(self, sound_file_name, text=None):
        '''add sounds_path and localizate sound name'''
        p = gettext.gettext(self.sounds_path)
        f = gettext.gettext(sound_file_name)
        snd = os.path.join(p, f)
        if text and not os.path.exists(snd):
            assert self.tts().synthesize(text, snd)
        return os.path.join(p, f)
            
    def clean_phone(self, phone, valid_length=10):
        cleaned_phone = ''.join([n for n in phone if n>='0' and n<='9']) # extract only digits
        if cleaned_phone[:1] == '0':  # discard first 0 digit
            cleaned_phone = cleaned_phone[1:]
        if len(cleaned_phone) != valid_length:
            self.log("clean_phone: invalid: "+phone)
            cleaned_phone = None
        return cleaned_phone


