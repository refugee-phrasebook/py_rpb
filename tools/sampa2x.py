#from string import maketrans 
import sys
import re
#import pyfribidi

SAMPA =         "abcdefghijklmnopqrstuvwxyzA{6QE@3IO29&U}VYBCDGLJNRSTHZ"
IPA =           "abcdefghijklmnopqrstuvwxyzɑæɐɒɛəɜɪɔøœɶʊʉʌʏβçðɣʎɲŋʁʃθɥʒ"
BALKANCYRLLIC = "абhдeфгхијклмнопкrстуввxизаeааeeeиоeeeuuаибhдгљњnршсуж"
#RUSCYRLLIC = "erfd"
#editors have problems with switching between RTL and LTR 
#in the middle of the line, hence a list over several lines
ARABIC = "".join(["ا",#a
          "ب",#b
          "خ",#c
          "د",#d
          "ي",#e
          "ف",#f
          "گ",#g
          "ح",#h
          "ي",#i
          "ي",#j
          "ك",#k
          "ل",#l
          "م",#m
          "ن",#n
          "و",#o
          "پ",#p
          "ق",#q
          "ر",#r
          "س",#s
          "ت",#t
          "و",#u
          "و",#v
          "و",#w
          "خ",#x
          "ي",#y
          "ظ",#z
          "ا",#A
          "ا",#{
          "ا",#6
          "ا",#Q
          "ي",#E
          "ي",#@
          "ي",#3
          "ي",#I
          "و",#O
          "ي",#2
          "ي",#9
          "ي",#&
          "و",#U
          "و",#}
          "و",#V
          "ي",#Y
          "ب",#B
          "خ",#C
          "ظ",#D
          "ق",#G
          "ل",#L
          "ي",#J
          "ن",#N
          "ر",#R
          "ﺸ",#S
          "س",#T
          "ي",#H
          "ژ",#Z
])

#ARABIC =        "ﻌژﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌژ"
#PERSIAN = "afew"
#print(len(SAMPA))
#print(len(ARABIC))

BALKANREMOVE = ''
#print(SAMPA)
#print(ARABIC)
  
arabd = {
  "ا":
  {
          "isolated":"ﺋ",
          "initial":"ئ",
          "medial":"ﺌ",
          "final":"ﺃ",
          "label":"Hamza"
  },
  "ئ":
  {
          "isolated":"ﺋ",
          "initial":"ئ",
          "medial":"ﺌ",
          "final":"ﺃ",
          "label":"Hamza"
  },
  "ب":
  {
          "isolated":"ﺑ",
          "initial":"ﺑ",
          "medial":"ﺒ",
          "final":"ﺏ",
          "label":"be"
  },
  "پ":
  {
          "isolated":"پ",
          "initial":"ﭘ",
          "medial":"پ",
          "final":"پ",
          "label":"pe"
  },
  "ت":
  {
          "isolated":"ﺗ",
          "initial":"ﺗ",
          "medial":"ﺘ",
          "final":"ﺕ",
          "label":"te"
  },
  "ﺗ":
  {
          "isolated":"ﺗ",
          "initial":"ﺗ",
          "medial":"ﺘ",
          "final":"ﺕ",
          "label":"te"
  },
  "ﺜ":
  {
          "isolated":"ﺛ",
          "initial":"ﺛ",
          "medial":"ﺜ",
          "final":"ﺙ",
          "label":"s̱e"
  },
  "ﺠ":
  {
          "isolated":"ﺞ",
          "initial":"ﺟ",
          "medial":"ﺠ",
          "final":"ﺝ",
          "label":"jim"
  },
  "چ":
  {
          "isolated":"ﭻ",
          "initial":"ﭼ",
          "medial":"چ",
          "final":"ﭺ",
          "label":"che"
  },
  "ح":
  {
          "isolated":"ﺢ",
          "initial":"ﺣ",
          "medial":"ﺤ",
          "final":"ﺡ",
          "label":"ḥe"
  },
  "ﺨ":
  {
          "isolated":"ﺦ",
          "initial":"ﺧ",
          "medial":"ﺨ",
          "final":"ﺥ",
          "label":"khe"
  },
  "خ":
  {
          "isolated":"ﺦ",
          "initial":"ﺧ",
          "medial":"ﺨ",
          "final":"ﺥ",
          "label":"khe"
  },
  "ﺳ":
  {
          "isolated":"ﺳ",
          "initial":"ﺳ",
          "medial":"ﺴ",
          "final":"ﺱ",
          "label":"sin"
  },
  "س":
  {
          "isolated":"ﺳ",
          "initial":"ﺳ",
          "medial":"ﺴ",
          "final":"ﺱ",
          "label":"sin"
  },
  "ﺸ":
  {
          "isolated":"ﺷ",
          "initial":"ﺷ",
          "medial":"ﺸ",
          "final":"ﺵ",
          "label":"šin"
  },
  "ﺼ":
  {
          "isolated":"ﺻ",
          "initial":"ﺻ",
          "medial":"ﺼ",
          "final":"ﺹ",
          "label":"ṣād"
  },
  "ﻀ":
  {
          "isolated":"ﺿ",
          "initial":"ﺿ",
          "medial":"ﻀ",
          "final":"ﺽ",
          "label":"z̤ād"
  },
  "ﻄ":
  {
          "isolated":"ﻃ",
          "initial":"ﻃ",
          "medial":"ﻄ",
          "final":"ﻁ",
          "label":"ṭā"
  },
  "ظ":
  {
          "isolated":"ﻇ",
          "initial":"ﻇ",
          "medial":"ﻈ",
          "final":"ظ",
          "label":"ẓā"
  },
  "ﻌ":
  {
          "final":"ع",
          "initial":"ﻋ",
          "medial":"ﻌ",
          "isolated":"ﻉ",
          "label":"ʿeyn"
  },
  "ﻐ":
  {
          "isolated":"ﻏ",
          "initial":"ﻏ",
          "medial":"ﻐ",
          "final":"ﻍ",
          "label":"ġeyn"
  },
  "ف":
  {
          "isolated":"ﻓ",
          "initial":"ﻓ",
          "medial":"ﻔ",
          "final":"ﻑ",
          "label":"fe"
  },
  "ﻗ":
  {
          "isolated":"ﻗ",
          "initial":"ﻕ",
          "medial":"ﻗ",
          "final":"ﻕ",
          "label":"qāf"
  },
  "ﻚ":
  {
          "isolated":"ﻛ",
          "initial":"ﻚ",
          "medial":"ﻜ",
          "final":"ﻙ",
          "label":"kāf"
  },
  "ك":
  {
          "isolated":"ﻛ",
          "initial":"ﻚ",
          "medial":"ﻜ",
          "final":"ﻙ",
          "label":"kāf"
  },
  "گ":
  {
          "isolated":"گ",
          "initial":"ﮔ",
          "medial":"گ",
          "final":"گ",
          "label":"gāf"
  },
  "ل":
  {
          "isolated":"ﻟ",
          "initial":"ﻟ",
          "medial":"ﻠ",
          "final":"ﻝ",
          "label":"lām"
  },
  "م":
  {
          "isolated":"ﻣ",
          "initial":"ﻣ",
          "medial":"ﻤ",
          "final":"ﻡ",
          "label":"mim"
  },
  "ﻧ":
  {
          "isolated":"ﻧ",
          "initial":"ﻧ",
          "medial":"ﻨ",
          "final":"ﻥ",
          "label":"nun"
  },
  "ن":
  {
          "isolated":"ﻧ",
          "initial":"ﻧ",
          "medial":"ﻨ",
          "final":"ﻥ",
          "label":"nun"
  },
  "ﻬ":
  {
          "isolated":"ﻫ",
          "initial":"ﻪ",
          "medial":"ﻬ",
          "final":"ﻩ",
          "label":"he"
  },
  "ﻲ":
  {
          "isolated":"ﻳ",
          "initial":"ﻲ",
          "medial":"ﻴ",
          "final":"ﻱ",
          "label":"ye"
  },
  "ي":
  {
          "isolated":"ﻳ",
          "initial":"ﻲ",
          "medial":"ﻴ",
          "final":"ﻱ",
          "label":"ye"
  },
  "ﺍ":
  {
          "isolated":"ﺍ",
          "initial":"ﺍ",
          "medial":"ﺍ",
          "final":"ﺍ",
          "label":"ʾalef"
  },
  "د":
  {
          "isolated":"ﺩ",
          "initial":"ﺩ",
          "medial":"ﺩ",
          "final":"ﺩ",
          "label":"dāl"
  },
  "ﺫ":
  {
          "isolated":"ﺫ",
          "initial":"ﺫ",
          "medial":"ﺫ",
          "final":"ﺫ",
          "label":"ẕāl"
  },
  "ر":
  {
          "isolated":"ﺭ",
          "initial":"ﺭ",
          "medial":"ﺭ",
          "final":"ﺭ",
          "label":"re"
  },
  "ﺯ":
  {
          "isolated":"ﺯ",
          "initial":"ﺯ",
          "medial":"ﺯ",
          "final":"ﺯ",
          "label":"ze"
  },
  "ژ":
  {
          "isolated":"ژ",
          "initial":"ژ",
          "medial":"ژ",
          "final":"ژ",
          "label":"že"
  },
  "و":
  {
          "isolated":"ﻭ",
          "initial":"ﻭ",
          "medial":"ﻭ",
          "final":"ﻭ",
          "label":"vāv"
  },
  ":": #length sign
  {
          "isolated":"ـ",
          "initial":"ـ",
          "medial":"ـ",
          "final":"ـ",
          "label":"phonetic length"
  },
  "ـ": #length sign
  {
          "isolated":"ـ",
          "initial":"ـ",
          "medial":"ـ",
          "final":"ـ",
          "label":"phonetic length"
  }
}
balkantab = str.maketrans(SAMPA,BALKANCYRLLIC,BALKANREMOVE)
#rustab = maketrans(SAMPA,RUSCYRLLIC)
aratab = str.maketrans(SAMPA,ARABIC)
ipatab = str.maketrans(SAMPA,IPA)
#perstab = maketrans(SAMPA,PERSIAN)

NONWORDS = r"""(^|$|['!"#$%&\'\(\)\*\+,-./:;<=>?@\[\\\]^_`{|}~ \t\n]+)"""

def bidi(s):
    #return pyfribidi.log2vis(s)
    return s
 
def lookupinitial(m):  
  s = m.groups(1)[0]
  try:
    result = arabd[s]['initial']
  except KeyError:
    print("could not translate %s in %s" % (s,m))
    result = s
  #print(result)
  return result

def lookupfinal(m):  
  #print(6)
  s = m.groups(1)[0]
  #print(m.groups)
  try:
    result = arabd[s]['final']
  except KeyError:
    print("could not translate %s in %s" % (s,m))    
    result = s
  #print(result)
  return result
 
def normalize(s):
  tmp = s
  #find isolated glyphs
  isos = []
  for m in re.finditer(r"(?<!\B)([^ ])(?!\B)", s):
    isos.append((m.start(),m.group(0)))   
  init = re.sub(r'(?<=\b)([^ ])',lookupinitial, tmp)
  fin = re.sub(r'([^ ])(?=\b)',lookupfinal, init)
  iso = fin 
  for pos,repl in isos:    
    iso = iso[:pos] + arabd[repl]['isolated'] + iso[pos + 1:]    
  return iso
  #print(s)
  #print(init)
  #print(fin)
  #print(iso)
 
def getPhoneticStrings(sampa,ipa=False): 
  if sampa:
    d ={'IPA':sampa.translate(ipatab),
      'SAMPA':sampa,
      'cyrtrans':sampa.translate(balkantab),
      'arabtrans':bidi(normalize(sampa.translate(aratab)))
      }
  elif ipa:
    d ={'IPA':ipa,
      'SAMPA':'',
      'cyrtrans':'',
      'arabtrans':''
      }
  else:
    d ={'IPA':'',
      'SAMPA':'',
      'cyrtrans':'',
      'arabtrans':''
      }
      
  return d

if __name__ == "__main__":
  s = ' '.join(sys.argv[1:])
  c = s
  print(s.translate(balkantab))
  print(bidi(normalize(s.translate(aratab))))  
  print(s.translate(ipatab))
  print(getPhoneticStrings(s))