# encoding: utf-8
# $Id: example.py 4167 2011-08-01 12:27:18Z robert $

import os, sys, tempfile, time

# PROJECT'S MODULES PATH -- NEEDED FOR FREESWITCH MOD_PYTHON
SELF_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SELF_PATH)

# import settings
# if DEBUG: 
#     # freeswitch mod_python doesnt consider module changes without reload
#     import settings
#     reload(settings) 

from fsivr import FsIvrBase, log

class Example(FsIvrBase):
    '''parktec ivr'''
    dnis = '8534449008'
    sounds_path = "/tmp"

    def welcome(self):
        self.answer()
        self.playback("welcome.wav", "bem vindo")
            
    def bye(self):
        self.playback("bye.wav", "obrigado por sua ligação")
        self.hangup()

    def say_time(self):
        t = time.localtime()
        h, m = t.tm_hour, t.tm_min
        self.playback("hora_certa.wav", text="São exatamente:")
        self.playback("%s.wav" % h, text="%s" % h)
        if not m:
            if h==1:
                self.playback("hora.wav", text="hora")
            else:
                self.playback("horas.wav", text="horas")
        else:
            self.playback("horas_e.wav", text="horas, e")
            self.playback("%s.wav" % m, text="%s" % m)
            if m==1:
                self.playback("minuto.wav", text="minuto")
            else:
                self.playback("minutos.wav", text="minutos")
        
    # freeswitch entry point
    def run(self):
        '''Entry point'''
        try:
            self.log('running')
            self.welcome()
            retry = 3
            while self.ready() and retry:
                dtmf = self.menu("menu.wav", "menu-invalid.wav", valid_dtmf="123", sound_text="Para hora certa tecle 1, para puum tecle 2, texto tecle 3")
                self.log(str(dtmf))
                if dtmf=='1':
                    self.say_time()
                elif dtmf=='2':
                    self.playback("pum.wav", text="puuuum puruuumm pum pum, pum prum")
                elif dtmf=='3':
                    self.say("exemplo de como usar o TTS sem especificar um nome de arquivo mas, ainda assim, usando o cache em arquivo local")
                else:
                    retry -= 1
            self.bye()

        except Exception, e:
            self.playback(SERVICO_INDISPONIVEL)
            tb = traceback.format_exc()
            self.log(tb, level='erro')

        '''Entry point'''
        log()
        self.welcome()

# entry point
def handler(session, args):
    ivr = Example("34449058", session, args)
    ivr.debug = True
    ivr.handler()

# test purpose only 
if __name__ == "__main__":
    log("syntax OK")
    DEBUG=True
    Example.test(callerid='8599134000',interactive=True)
