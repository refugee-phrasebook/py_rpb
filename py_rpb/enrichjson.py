from iso6393 import iso6393dic
import json
#import sys
from subprocess import call, check_output
import os


f = open('lexemes.json')
c = f.read() 
f.close()

d = json.loads(c)
print(len(d))

for ID in d:
  #print(ID)
  for lg in d[ID]['lgs']:
    #print(' ',lg)
    try:
      espeaklg = iso6393dic[lg]['for_espeak']
    except KeyError:
      continue
    if espeaklg.strip()=='':
      continue
    text = d[ID]['lgs'][lg]['orthographic']
    #syscall  = syscalltemplate % (lg,espeaklg,lg,IipaD,text)
    try:
      os.mkdir('wav/%s'%lg)
    except FileExistsError:
      pass    
    syscall = ['espeak', '--ipa', '-v', espeaklg, '-w', 'wav/%s/%s.wav'%(lg,ID), '"%s"'%text]  
    ipa = check_output(syscall).decode('utf8')
    d[ID]['lgs'][lg]['transcriptions']['IPA']=ipa
    #print(len(retval),retval)

out = open('lexemes2.json', 'w')
out.write(json.dumps(d, sort_keys=True, indent=4))
out.close()

