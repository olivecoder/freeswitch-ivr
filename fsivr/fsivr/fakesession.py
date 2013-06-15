import random
import os

class FakeSession(object):
    '''Emulates freeswitch.session for tests purposes'''

    def __init__(self, interactive = False, sound = False, *args, **kwargs):
        self.interactive = interactive
        self.sound = sound
        self.answered_flag = False
        self.state = 'CS_EXECUTE'
        self.callerid = None
        self.last_attr = ""
        self.ivrlog = None
        random.seed()
        return super(FakeSession, self).__init__(*args, **kwargs)

    def log(self, fname, *args, **kwargs):
        if len(kwargs):
            args = args + (kwargs,)
        msg = "FakeSession: %s%s" % (fname, str(args)) 
        print msg
        if self.ivrlog:
            self.ivrlog(msg)

    def fake_method(self, *args, **kwargs):
        self.log(self.last_attr, *args, **kwargs)
        return True

    def inputDtmf(self, min_digits, max_digits):
        if self.interactive:
            dtmf = raw_input('>>> ')
            self.log("inputDtmf", result=dtmf)
        else:
            dtmf = self.randomDtmf(min_digits, max_digits)
        return  dtmf 

    def streamFile(self, snd):
        if self.sound:
            os.system('play %s 2> /dev/null' % snd)
        self.log("streamFile", snd=snd)

    
    def randomDtmf(self, min_digits, max_digits):
        n = random.randrange(min_digits, max_digits+1)
        dtmf = ''.join([str(random.randrange(10)) for n in range(n)])                    
        self.log("randomDtmf", dtmf=dtmf)
        return dtmf

    def __getattr__(self, varname):
        self.last_attr = varname
        return self.fake_method

    def getVariable(self, varname, *args, **kwargs):
        self.log("getVariable", varname, *args, **kwargs)
        if self.callerid and varname == 'caller_id_number':
            value = self.callerid 
        elif varname == 'sound_prefix':
            value = ''
        else:
            value = self.inputDtmf(10,11)
        return value

    def answer(self, *args, **kwargs):
        self.log("answer", *args, **kwargs)
        self.state = "CS_EXCHANGE_MEDIA"
        self.answered_flag = True
        return True

    def answered(self, *args, **kwargs):
        self.log("answered", *args, **kwargs)
        return self.answered_flag

    def hangup(self, cause, *args, **kwargs):
        self.log("hangup", *args, **kwargs)
        self.state = "CS_HANGUP"
        return True
    
    def getState(self, *args, **kwargs):
        self.log("getState", *args, **kwargs)
        return self.state

    def getDigits(max_digits, *args, **kwargs):
        self.log("getDigits", *args, **kwargs)
        return self.inputDtmf(0, max_digits)
    
    def read(self, min_digits, max_digits, *args, **kwargs):
        self.log("read", max_digits, *args, **kwargs)
        return self.inputDtmf(min_digits, max_digits)

    def playAndGetDigits(self, min_digits, max_digits, max_tries, timeout, terminators, 
                         audio_files, bad_input_audio_file, digits_regex, *args, **kwargs):
        self.log("playAndGetDigits", min_digits, max_digits, max_tries, timeout, terminators, 
                 audio_files, bad_input_audio_file, digits_regex, *args, **kwargs)
        self.streamFile(audio_files)
        return self.inputDtmf(min_digits, max_digits)


if __name__ == "__main__":
    FakeSession().I_Dont_Exist_Anywhere("output shall be: any_method(1, {'d': 2})")
    FakeSession().any_method(1, d=2)
