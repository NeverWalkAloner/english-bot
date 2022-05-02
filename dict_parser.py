from string import ascii_letters
import json
import re

re_rus = re.compile(r'')

dictionary = []
with open('dict.txt', mode='r') as f:
    for line in f.readlines():
        eng, rus = line.split('  ')
        rus = ' '.join(word for word in rus.split(' ') if not word.startswith(('[', '_')))
        rus = ''.join(ch for ch in rus if ch not in ascii_letters + '()._')
        if ''.join(e for e in rus if e.isalpha()) and len(eng) > 2:
            dictionary.append({'eng': eng.strip(), 'rus': rus.strip()})
            # print('{} > {}'.format(eng, rus))

with open('dict_db', mode='w') as f:
    f.write(json.dumps(dictionary))