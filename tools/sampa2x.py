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
          "ك",#c
          "د",#d
          "ﻋ",#e
          "ﻔ",#f
          "گ",#g
          "ح",#h
          "ي",#i
          "ي",#j
          "ك",#k
          "ﻠ",#l
          "م",#m
          "ن",#n
          "و",#o
          "پ",#p
          "ق",#q
          "ر",#r
          "ﺴ",#s
          "ت",#t
          "و",#u
          "و",#v
          "و",#w
          "ﺨ",#x
          "ي",#y
          "ﺯ",#z
          "ا",#A
          "ﻋ",#{
          "ا",#6
          "ا",#Q
          "ﻋ",#E
          "ﻋ",#@
          "ﻋ",#3
          "ي",#I
          "و",#O
          "ﻋ",#2
          "ﻋ",#9
          "ﻋ",#&
          "و",#U
          "ﻋ",#}
          "ﻋ",#V
          "ﻋ",#Y
          "ب",#B
          "ح",#C
          "ض",#D
          "ﻐ",#G
          "ل",#L
          "ن",#J
          "ن",#N
          "ﻐ",#R
          "ﺸ",#S
          "ث",#T
          "ي",#H
          "ج",#Z
])

#ARABIC =        "ﻌژﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌژ"
#PERSIAN = "afew"
#print(len(SAMPA))
#print(len(ARABIC))

BALKANREMOVE = ''
#print(SAMPA)
#print(ARABIC)
  
arabd = {
  "ء":
  {
          "initial":"ٴ",
          "isolated":"ء",
          "medial":"ٴ",
          "final":"ٴ",
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
          "medial":"ـپـ",
          "final":"پ",
          "label":"pe"
  },
  "ت":
  {
          "initial":"ﺗ",
          "isolated":"ت",
          "medial":"ﺘ",
          "final":"ﺕ",
          "label":"te"
  },
  "ﺜ":
  {
          "isolated":"ﺙ",
          "initial":"ﺛ",
          "medial":"ﺜ",
          "final":"ﺙ",
          "label":"s̱e"
  },
  "ﺠ":
  {
          "final":"ـﺞ",
          "initial":"ﺟ",
          "medial":"ﺠ",
          "isolated":"ﺝ",
          "label":"jim"
  },
  "چ":
  {
          "final":"ﭻ",
          "initial":"ﭼ",
          "medial":"ـچـ",
          "isolated":"ﭺ",
          "label":"che"
  },
  "ح":
  {
          "final":"ـﺢ",
          "initial":"ﺣ",
          "medial":"ﺤ",
          "isolated":"ﺡ",
          "label":"ḥe"
  },
  "ﺨ":
  {
          "final":"ـﺦ",
          "initial":"ﺧ",
          "medial":"ﺨ",
          "isolated":"ﺥ",
          "label":"khe"
  },
  "ﺴ":
  {
          "isolated":"س",
          "initial":"ﺳ",
          "medial":"ﺴ",
          "final":"ﺱ",
          "label":"sin"
  },
  "ﺸ":
  {
          "isolated":"ﺵ",
          "initial":"ﺷ",
          "medial":"ﺸ",
          "final":"ش",
          "label":"šin"
  },
  "ﺼ":
  {
          "isolated":"ﺹ",
          "initial":"ﺻ",
          "medial":"ﺼ",
          "final":"ـص",
          "label":"ṣād"
  },
  "ﻀ":
  {
          "isolated":"ﺽ",
          "initial":"ﺿ",
          "medial":"ﻀ",
          "final":"ـض",
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
          "final":"ـغ",
          "initial":"ﻏ",
          "medial":"ﻐ",
          "isolated":"ﻍ",
          "label":"ġeyn"
  },
  "ﻔ":
  {
          "final":"ف",
          "initial":"ﻓ",
          "medial":"ﻔ",
          "isolated":"ﻑ",
          "label":"fe"
  },
  "ﻗ":
  {
          "isolated":"ﻕ",
          "initial":"ﻕ",
          "medial":"ﻗ",
          "final":"ـق",
          "label":"qāf"
  },
  "ك":
  {
          "initial":"ﻛ",
          "final":"ﻚ",
          "medial":"ﻜ",
          "isolated":"ﻙ",
          "label":"kāf"
  },
  "گ":
  {
          "isolated":"گ",
          "initial":"ﮔ",
          "medial":"ـگـ",
          "final":"ـگ",
          "label":"gāf"
            
  },
  "ﻠ":
  {
          "final":"ﻟ",
          "initial":"ﻟ",
          "medial":"ﻠ",
          "isolated":"ﻝ",
          "label":"lām"
  },
  "م":
  {
          "isolated":"ﻡ",
          "initial":"ﻣ",
          "medial":"ﻤ",
          "final":"ـم",
          "label":"mim"
  },
  "ن":
  {
          "isolated":"ﻥ",
          "initial":"ﻧ",
          "medial":"ﻨ",
          "final":"ن",
          "label":"nun"
  },
  "ﻬ":
  {
          "initial":"ﻫ",
          "final":"ﻪ",
          "medial":"ﻬ",
          "isolated":"ﻩ",
          "label":"he"
  },
  "ي":
  {
          "initial":"ﻳ",
          "final":"ﻲ",
          "medial":"ﻴ",
          "isolated":"ي",
          "label":"ye"
  },
  "ا":
  {
          "isolated":"ﺍ",
          "initial":"ﺍ",
          "medial":"ا",
          "final":"ـا",
          "label":"ʾalef"
  },
  "ﻋ":
  {
          "isolated":"ﻉ",
          "initial":"ﻋ",
          "medial":"ـعـ",
          "final":"ـع",
          "label":"ʿeyn"
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
          "final":"ـذ",
          "label":"ẕāl"
  },
  "ر":
  {
          "isolated":"ﺭ",
          "initial":"ﺭ",
          "medial":"ر",
          "final":"ـر",
          "label":"re"
  },
  "ﺯ":
  {
          "isolated":"ﺯ",
          "initial":"ﺯ",
          "medial":"ز",
          "final":"ز",
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
          "medial":"و",
          "final":"و",
          "label":"vāv"
  }
  #":": #length sign
  #{
          #"isolated":"ـ",
          #"initial":"ـ",
          #"medial":"ـ",
          #"final":"ـ",
          #"label":"phonetic length"
  #},
  #"ـ": #length sign
  #{
          #"isolated":"ـ",
          #"initial":"ـ",
          #"medial":"ـ",
          #"final":"ـ",
          #"label":"phonetic length"
  #}
}
balkantab = str.maketrans(SAMPA,BALKANCYRLLIC,BALKANREMOVE)
#rustab = maketrans(SAMPA,RUSCYRLLIC)
aratab = str.maketrans(SAMPA,ARABIC,':')
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
<<<<<<< Updated upstream
  #for pos,repl in isos:    #check for ـproblem FIXME
=======
  #for pos,repl in isos:    
>>>>>>> Stashed changes
    #iso = iso[:pos] + arabd[s[pos]]['isolated'] + iso[pos + 1:]    
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