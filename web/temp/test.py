# -*- coding: utf-8 -*-

"""
Парс по isbn http://www.litres.ru/
рабочий
"""

import re
data = 'asasasasasasasaas'

pattern = '^([a-z]{1}|[A-Z].*|[0-9].*'

def checkio(data):
    if len(data) >= 10:
        if re.findall(pattern, data):
            return data

print checkio(data)

"""
if __name__ == '__main__':
    assert checkio('A1213pokl')==False, 'First'
    assert checkio('bAse730onE4')==True, 'Second'
    assert checkio('asasasasasasasaas')==False, 'Third'
    assert checkio('QWERTYqwerty')==False, 'Fourth'
    assert checkio('123456123456')==False, 'Fifth'
    assert checkio('QwErTy911poqqqq')==True, 'Sixth'
    print 'All ok'
"""