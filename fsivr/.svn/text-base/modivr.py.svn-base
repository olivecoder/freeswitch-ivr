# encoding: utf-8
# modivr.py
# Robert, 2010.05.10

import StringIO
import traceback, inspect
import random, os
from decimal import Decimal

global in_freeswitch
try:
    from freeswitch import *
except:
    in_freeswitch = False
else:
    in_freeswitch = True

# local 
from fakesession import FakeSession
from ivrbase import IvrBase
from say_digit import cardinal

class FsIvrBase(IvrBase):
    '''Freeswitch mod_python IVR Base Class'''
    in_freeswitch = in_freeswitch
    
    def __init__(self, dnis=None, session=None, args=None):
        self.session  = session
        self.args     = args
        self.userid   = None
        super(FsIvrBase, self).__init__(dnis)
        if in_freeswitch:
            consoleLog("warning","FSIVR: writing log to %s" % self.log_filename)
        if self.session:
            self.sounds_path = os.path.join(self.sound_prefix, self.sounds_path)
        self.log("incoming call")

    def log(self, msg="CheckPoint", level="info"):
        msg = super(FsIvrBase,self).log(msg, level)
        if in_freeswitch:
            consoleLog(level, msg)

    @property
    def callerid(self):
        return self.clean_phone(self.session.getVariable("caller_id_number"))

    @property
    def sound_prefix(self):
        return self.session.getVariable("sound_prefix")

    @classmethod
    def test(ivr_class, callerid=None, interactive = False, sound = False, **kwargs):
        session = FakeSession(interactive = interactive, sound = sound)
        if callerid:
            session.callerid = callerid
        testivr = ivr_class("fakeDnis", session, None)
        for k in kwargs:
            setattr(testivr, k, kwargs[k])
        testivr.debug = True
        testivr.handler()
        return testivr.debug

    def answer(self):
        self.session.answer()
        self.session.sleep(1000)

    def playback(self, sound_file, text=None):
        snd = self.get_sound(sound_file, text)
        snd = str(snd) # see http://wiki.freeswitch.org/wiki/Mod_python#String_Substitution_in_Functions, for understand this
        self.session.streamFile(snd)

    def play_number(self, number, gender='m'):
        number = cardinal(number, gender)
        for parts in number:
            self.playback(parts)
 
    def hangup(self,cause=None):
        if cause==None:
            if self.session.answered():
                cause="NORMAL_CLEARING"
            else:
                cause="USER_BUSY"
        if self.debug:
            line=inspect.currentframe().f_back.f_lineno
            self.log("hangup(%s): called by line %i" % (cause, line))
        self.session.hangup(cause)

    def menu(self, sound, invalid_sound, valid_dtmf="0123456789*#", retry=None, timeout=None, 
             sound_text=None, invalid_sound_text="opção inválida"):
        retry = retry or self.retry
        timeout = timeout or self.timeout
        sound = self.get_sound(sound, sound_text)
        invalid_sound = self.get_sound(invalid_sound, invalid_sound_text)
        valid_regex = '['+','.join(valid_dtmf)+']'
        return self.session.playAndGetDigits(1, 1, retry, timeout, "", sound, invalid_sound, valid_regex)

    def input(self, sound, invalid_sound, min_length, max_length, retry=None, timeout=None, valid_regex=None, 
              sound_text=None, invalid_sound_text="valor inválido"):
        retry = retry or self.retry
        timeout = timeout or self.timeout
        sound = self.get_sound(sound, sound_text)
        invalid_sound = self.get_sound(invalid_sound, invalid_sound_text)
        if not valid_regex:
            valid_regex = '\\d{%i,%i}' % (min_length, max_length)
        return self.session.playAndGetDigits(min_length, max_length, retry, timeout, "#", sound, invalid_sound, valid_regex)


if __name__ == "__main__":
    DEBUG=True
    ModIvr.run()
