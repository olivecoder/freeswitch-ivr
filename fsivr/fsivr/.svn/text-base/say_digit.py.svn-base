#!/usr/bin/env python
# coding: utf-8
# original em: http://code.google.com/p/propython/source/browse/appengine/labtmpbr/extenso.py
from math import log

cardinais = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900]

cardinais_pot1000 = [10**3, 10**6, 10**9, 10**12, 10**15, 10**18, 10**21, 10**24, 10**27, 10**30, 10**33, 10**36, 10**39, 10**42, 10**45, 10**48, 10**51, 10**54, 10**57, 10**60]

cardinais_femininos = [1, 2, 200, 300, 400, 500, 600, 700, 800, 900]

limite = max(cardinais_pot1000)*1000-1

def cardinal999(n, genero='m'):
    assert 0<=n<1000
    if n in cardinais:
        if genero == 'f' and n in cardinais_femininos:
            return str(n) + 'a.wav'
        else:
            return str(n) + '.wav'
    else:
        pot10 = 10**int(log(n, 10))
        cabeca = n/pot10
        corpo =  n%pot10
        redondo = cabeca*pot10
        if redondo == 100:
            prefixo = 'cento.wav'
        else:
            if genero == 'f' and redondo in cardinais_femininos:
                prefixo = str(redondo) + 'a.wav'
            else:
                prefixo = str(redondo) + '.wav'
        return prefixo + ' e.wav ' + cardinal999(corpo, genero)

def scardinal(n, genero='m'):
    if n < 1000:
        return cardinal999(n, genero)
    else:
        pot1000 = 1000**((len(str(n))-1)/3)
        cabeca = n/pot1000
        corpo =  n%pot1000
        if pot1000 == 1000 and cabeca == 1:
            prefixo = '1000.wav'
        else:
            try:
                prefixo = (cardinal999(cabeca, genero) + ' ' +
                           str(pot1000) + '.wav')
            except KeyError:
                raise OverflowError('limite %s ultrapassado' % limite)
            if cabeca != 1:
                prefixo = prefixo.replace('ilhão', 'ilhões')
        if corpo:
            if (0<corpo<100) or (corpo < 1000 and (corpo%100)==0):
                conector = ' e.wav '
            elif prefixo == '1000.wav':
                conector = ' '
            else:
                conector = ' '
            return prefixo + conector + scardinal(corpo, genero)
        else:
            return prefixo

def cardinal(n, genero='m'):
    "genero: m(masculino) f(feminino)"
    return scardinal(n, genero).split()
