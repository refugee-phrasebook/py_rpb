#from string import maketrans 
import sys
import re
#import pyfribidi

SAMPA =         "abcdefghijklmnopqrstuvwxyzA{6QE@3IO29&U}VYBCDGLJNRSTHZ"
IPA =                                     "ɑæɐɒɛəɜɪɔøœɶʊʉʌʏβçðɣʎɲŋʁʃθɥʒʔ"
BALKANCYRLLIC = "абhдeфгхијклмнопкrстуввxизаeааeeeиоeeeuuаибhдгљњnршсуж"
RUSCYRLLIC = "erfd"
ARABIC =        "ﻌژﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌﻌژ"
PERSIAN = "afew"
print(len(SAMPA))
print(len(ARABIC))
  
BALKANREMOVE = '?'

arabd = {
"ﺌ":
{
        "isolated":"ﺋ",
        "initial":"ئ",
        "medial":"ﺌ",
         "final":"ﺃ",
        "label":"Hamza"
},
"ﺒ":
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
"ﺘ":
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
"ﺤ":
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
"ﺴ":
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
"ﻈ":
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
"ﻔ":
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
"ﻜ":
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
"ﻠ":
{
        "isolated":"ﻟ",
        "initial":"ﻟ",
        "medial":"ﻠ",
        "final":"ﻝ",
        "label":"lām"
},
"ﻤ":
{
        "isolated":"ﻣ",
        "initial":"ﻣ",
        "medial":"ﻤ",
        "final":"ﻡ",
        "label":"mim"
},
"ﻨ":
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
"ﻴ":
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
"ﺩ":
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
"ﺭ":
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
"ﻭ":
{
        "isolated":"ﻭ",
        "initial":"ﻭ",
        "medial":"ﻭ",
        "final":"ﻭ",
        "label":"vāv"
},
}
balkantab = str.maketrans(SAMPA,BALKANCYRLLIC,BALKANREMOVE)
#rustab = maketrans(SAMPA,RUSCYRLLIC)
aratab = str.maketrans(SAMPA,ARABIC)
#perstab = maketrans(SAMPA,PERSIAN)

NONWORDS = r"""(^|$|['!"#$%&\'\(\)\*\+,-./:;<=>?@\[\\\]^_`{|}~ \t\n]+)"""

def bidi(s):
    #return pyfribidi.log2vis(s)
    return s
 
def lookupinitial(m):  
  s = m.groups(1)[0]
  result = arabd[s]['initial']
  #print(result)
  return result

def lookupfinal(m):  
  #print(6)
  s = m.groups(1)[0]
  #print(m.groups)
  try:
    result = arabd[s]['final']
  except KeyError:
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
    iso = iso[:pos] + arabd[repl][3] + iso[pos + 1:]
  return iso
  #print(s)
  #print(init)
  #print(fin)
  #print(iso)
  

if __name__ == "__main__":
  s = ' '.join(sys.argv[1:])
  c = s
  print(s.translate(balkantab))
  print(bidi(normalize(s.translate(aratab))))  
  #print(s.translate(perstab))