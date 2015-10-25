#from string import maketrans 
import sys

SAMPA =         "abcdefghijklmnopqrstuvwxyzA{6QE@3IO29&U}VYBCDGLJNRSTHZ"
IPA =                                     "ɑæɐɒɛəɜɪɔøœɶʊʉʌʏβçðɣʎɲŋʁʃθɥʒʔ"
BALKANCYRLLIC = "абhдeфгхијклмнопкrстуввxизаeааeeeиоeeeuuаибhдгљњnршсуж"
RUSCYRLLIC = "erfd"
ARABIC = "twe3"
PERSIAN = "afew"
  
BALKANREMOVE = '?'

arabd = {
"ـﺌـ":
{
        "isolated":"ـﺋ",
        "initial":"ﺊـ",
        "medial":"ـﺌـ",
         "final":"ﺃ",
        "label":"Hamza"
},
"ـﺒـ":
{
        "isolated":"ـﺑ",
        "initial":"ﺑ",
        "medial":"ـﺒـ",
        "final":"ﺏ",
        "label":"be"
},
"ـپـ":
{
        "isolated":"ـپ",
        "initial":"ﭘ",
        "medial":"ـپـ",
        "final":"پ",
        "label":"pe"
},
"ـﺘـ":
{
        "isolated":"ـﺗ",
        "initial":"ﺗ",
        "medial":"ـﺘـ",
        "final":"ﺕ",
        "label":"te"
},
"ـﺜـ":
{
        "isolated":"ـﺛ",
        "initial":"ﺛ",
        "medial":"ـﺜـ",
        "final":"ﺙ",
        "label":"s̱e"
},
"ـﺠـ":
{
        "isolated":"ﺞ",
        "initial":"ﺟ",
        "medial":"ـﺠـ",
        "final":"ﺝ",
        "label":"jim"
},
"ـچـ":
{
        "isolated":"ﭻ",
        "initial":"ﭼ",
        "medial":"ـچـ",
        "final":"ﭺ",
        "label":"che"
},
"ـﺤـ":
{
        "isolated":"ﺢ",
        "initial":"ﺣ",
        "medial":"ـﺤـ",
        "final":"ﺡ",
        "label":"ḥe"
},
"ـﺨـ":
{
        "isolated":"ﺦ",
        "initial":"ﺧ",
        "medial":"ـﺨـ",
        "final":"ﺥ",
        "label":"khe"
},
"ـﺴـ":
{
        "isolated":"ـﺳ",
        "initial":"ﺳ",
        "medial":"ـﺴـ",
        "final":"ﺱ",
        "label":"sin"
},
"ـﺸـ":
{
        "isolated":"ـﺷ",
        "initial":"ﺷ",
        "medial":"ـﺸـ",
        "final":"ﺵ",
        "label":"šin"
},
"ـﺼـ":
{
        "isolated":"ـﺻ",
        "initial":"ﺻ",
        "medial":"ـﺼـ",
        "final":"ﺹ",
        "label":"ṣād"
},
"ـﻀـ":
{
        "isolated":"ـﺿ",
        "initial":"ﺿ",
        "medial":"ـﻀـ",
        "final":"ﺽ",
        "label":"z̤ād"
},
"ـﻄـ":
{
        "isolated":"ـﻃ",
        "initial":"ﻃ",
        "medial":"ـﻄـ",
        "final":"ﻁ",
        "label":"ṭā"
},
"ـﻈـ":
{
        "isolated":"ـﻇ",
        "initial":"ﻇ",
        "medial":"ـﻈـ",
        "final":"ﻅ",
        "label":"ẓā"
},
"ـﻌـ":
{
        "isolated":"ـﻋ",
        "initial":"ﻋ",
        "medial":"ـﻌـ",
        "final":"ﻉ",
        "label":"ʿeyn"
},
"ـﻐـ":
{
        "isolated":"ـﻏ",
        "initial":"ﻏ",
        "medial":"ـﻐـ",
        "final":"ﻍ",
        "label":"ġeyn"
},
"ـﻔـ":
{
        "isolated":"ـﻓ",
        "initial":"ﻓ",
        "medial":"ـﻔـ",
        "final":"ﻑ",
        "label":"fe"
},
"ـﻗ":
{
        "isolated":"ـﻗ",
        "initial":"ﻕ",
        "medial":"ـﻗ",
        "final":"ﻕ",
        "label":"qāf"
},
"ـﻜـ":
{
        "isolated":"ـﻛ",
        "initial":"ﻚـ",
        "medial":"ـﻜـ",
        "final":"ﻙ",
        "label":"kāf"
},
"ـگـ":
{
        "isolated":"ـگ",
        "initial":"ﮔ",
        "medial":"ـگـ",
        "final":"گ",
        "label":"gāf"
},
"ـﻠـ":
{
        "isolated":"ـﻟ",
        "initial":"ﻟ",
        "medial":"ـﻠـ",
        "final":"ﻝ",
        "label":"lām"
},
"ـﻤـ":
{
        "isolated":"ـﻣ",
        "initial":"ﻣ",
        "medial":"ـﻤـ",
        "final":"ﻡ",
        "label":"mim"
},
"ـﻨـ":
{
        "isolated":"ـﻧ",
        "initial":"ﻧ",
        "medial":"ـﻨـ",
        "final":"ﻥ",
        "label":"nun"
},
"ـﻬـ":
{
        "isolated":"ـﻫ",
        "initial":"ﻪـ",
        "medial":"ـﻬـ",
        "final":"ﻩ",
        "label":"he"
},
"ـﻴـ":
{
        "isolated":"ـﻳ",
        "initial":"ﻲـ",
        "medial":"ـﻴـ",
        "final":"ﻱ",
        "label":"ye"
},
"ﺍ":
{
        "isolated":"ـﺍ",
        "initial":"ﺍ",
        "medial":"ـﺍ",
        "final":"ﺍ",
        "label":"ʾalef"
},
"ﺩ":
{
        "isolated":"ـﺩ",
        "initial":"ﺩ",
        "medial":"ـﺩ",
        "final":"ﺩ",
        "label":"dāl"
},
"ﺫ":
{
        "isolated":"ـﺫ",
        "initial":"ﺫ",
        "medial":"ـﺫ",
        "final":"ﺫ",
        "label":"ẕāl"
},
"ﺭ":
{
        "isolated":"ـﺭ",
        "initial":"ﺭ",
        "medial":"ـﺭ",
        "final":"ﺭ",
        "label":"re"
},
"ﺯ":
{
        "isolated":"ـﺯ",
        "initial":"ﺯ",
        "medial":"ـﺯ",
        "final":"ﺯ",
        "label":"ze"
},
"ژ":
{
        "isolated":"ـژ",
        "initial":"ژ",
        "medial":"ـژ",
        "final":"ژ",
        "label":"že"
},
"ﻭ":
{
        "isolated":"ـﻭ",
        "initial":"ﻭ",
        "medial":"ـﻭ",
        "final":"ﻭ",
        "label":"vāv"
},
}
balkantab = str.maketrans(SAMPA,BALKANCYRLLIC,BALKANREMOVE)
#rustab = maketrans(SAMPA,RUSCYRLLIC)
#aratab = maketrans(SAMPA,ARABIC)
#perstab = maketrans(SAMPA,PERSIAN)

NONWORDS = r"""(^|$|['!"#$%&\'\(\)\*\+,-./:;<=>?@\[\\\]^_`{|}~ \t\n]+)"""

def bidi(s):
   return pyfribidi.log2vis(s)
 
def lookupinitial(m):  
  s = m.groups(1)[0]
  result = arabd[s][0]
  #print(result)
  return result

def lookupfinal(m):  
  #print(6)
  s = m.groups(1)[0]
  #print(m.groups)
  try:
    result = arabd[s][2]
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
  print(s)
  print(init)
  print(fin)
  print(iso)
  

if __name__ == "__main__":
  s = ' '.join(sys.argv[1:])
  c = s
  print(s.translate(balkantab))
  print(bidi(normalize(s.translate(aratab))))  
  #print(s.translate(perstab))