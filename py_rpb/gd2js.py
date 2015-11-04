import scrapesheet as sc
import sys
import string
import sampa2x
import iso6393
import json

#provide a commandline version to scrape google doc and output to either tsv or js
#tabulate from original class was not working at the time of writing

class lexeme():
  def __init__(self,ID,label,orth,iso,sampa,latn,domain):
    self.ID = ID
    self.label = label
    self.iso6393code = iso
    self.orthographic = orth
    self.transcriptions = sampa2x.getPhoneticStrings(sampa)
    self.domain = domain
    if latn:  
      self.transcriptions['Latin'] = latn

  

def normalizename(s):
	h =  str(hash(s))[:3]
	n = ''.join([c for c in s if c in string.ascii_letters])[:10]
	result =  "%s_%s"%(n,h) 
	return result

def outputtsv(normname,pairs): 
			filename = 'data_%s_.tsv' % normname
			print(filename)
			out = open(filename, 'w')
			for p in pairs:
				out.write("\t".join(p))
				out.write("\n")
			out.close()
			
def lg2js(normname,pairs): 
			t = """{
				"target":"%s",
				"source":"%s",
				"phonetic":"%s",
				"domain":""
			}""" 
			result = """ '%s':function (){ 
	return [""" % normname
			result += '\n,\n'.join([t%p for p in pairs])
			result +="""	    ]
    }"""
			return result
 
	
			
def getpairs(records,lg):
  """
  return a tuple of all translations from target to source
  """
  return [(r[0],r[lg]) for r in records if r[lg]!='']
				 
def gettuples(records,languages):
  """
  return a tuple of the ID and all renderings in all selected languages
  """
  languages = [0,3]+languages
  #print(languages)
  return [records[l] for l in languages]
  
def s2tsv(s,languages,typ=''):  
        firstlanguage = languages[0]
        #print(firstlanguage)
        #print(s.records[0])
        #print(s.records[0][firstlanguage])
        name = s.records[0][languages[0]]
        normname = normalizename(name)    
        #print(languages)
        #print([s.records[0][i] for i in languages])
        print(normname)
        #pairs = getpairs(s.records[1:], lg)
        records = s.records[1:]
        tuples =  [gettuples(r,languages) for r in records]
        fn = 'tsv/data_%s_%s.tsv'%(typ,normname)
        #print(fn)
        out = open(fn,'w')
        for t in tuples:
          out.write("\t".join(t))
          out.write("\n")
        out.close()
        
		    
def s2js(s,languages,typ=''):
	jss = []
	for lg in languages:
			print(lg)
			lg = int(lg)
			name = s.records[0][lg]
			normname = normalizename(name) 
			print("%s --> %s"%(name,normname))
			pairs = getpairs(s.records[1:], lg)
			lgjs = lg2js(normname, pairs)
			jss.append(lgjs)
	t = "var lgs={\n%s\n}"% '\n,\n'.join(jss)
	out = open('data_%s.js'%typ,'w')
	out.write(t)
	out.close()
	
	
def s2lxm(s):#only for new short-style sheets
  result = []
  records = s.records
  iso6393code = records[0][2]
  #identify interesting colums
  sampacol = False
  latncol = False
  for i,x in enumerate(records[0]):
    y = x.strip()
    if y.endswith('-Qaas'):
      if y.startswith(iso6393): 
        sampacol = i
      else:
        raise ValueError      
      continue
    if y.endswith('-Latn'):
      if y.startswith(iso6393code): 
        latncol = i
      else:
        raise ValueError      
  #extract information from rows
  for record in s.records[1:]:
    ID, label = record[:2]
    sampa = False
    latn = False
    if sampacol:
      sampa = record[sampacol]
    if latncol:
      latn = record[latncol]
    orth = record[2]
    #print(sampa, latn, orth, ID, label,iso6393code)
    domain = None
    lxm = lexeme(ID,label,orth,iso6393code,sampa,latn,domain) # check for overwriting
    result.append(lxm)
  print(len(result))
  return result
    
def addtodico(d,lx):
  ID = lx.ID
  #assure the lexeme is in the dict
  if d.get(ID) == None:
    d[ID] = {'label':lx.label,
              'domain':lx.domain,
              'lgs':{}
      }
  print(lx.label)
  #add new information
  if d[ID]['lgs'].get(lx.iso6393code) != None:
    print("%s already present in %s, skipping %s"%(ID,lx.iso6393code,lx.orthographic))
    return d
  d[ID]['lgs'][lx.iso6393code] = {'orthographic':lx.orthographic,
            'transcriptions':lx.transcriptions,
            'label':iso6393dic[lx.iso6393code]['label']
    }
  return d
  
iso6393dic ={'hbs':{'label':'Serbo-Croatian'}}
    
if __name__ == '__main__': 
    #usage : gd2js.py  1 3 8 12 14 17 19 22 24  
    languages = [int(i) for i in sys.argv[1:]]
    #print(languages)
    sheets = [('Serbo-Croatian','https://docs.google.com/spreadsheets/d/1wweXwpEpHWrFcM46YZ-SVi-gLfywrUyj1wjEf19DWQE/pubhtml'),
                ('Albanian       ','https://docs.google.com/spreadsheets/d/1B9OXDIV4nDUekqpwILbAK6eHIAIP5UePgpYbOWRsTvY/edit?usp=sharing'), 
                ('Urdu   ','https://docs.google.com/spreadsheets/d/1oCRZRBOn6sl8ufJ12OF1gPR_OLj598H45OENqkFfF7U/edit?usp=sharing'), 
                ('Amharic','https://docs.google.com/spreadsheets/d/1ni8FOoW4Nqa1drwVCEoKMh4NqAn5ySSezFL-Mvo0hiY/edit?usp=sharing'), 
                ('Somali ','https://docs.google.com/spreadsheets/d/1SLCVAYupSfjpvMwKiid0Z4JexbJhQsZX19yAzhPIcx0/edit?usp=sharing'), 
                ('Slovenian      ','https://docs.google.com/spreadsheets/d/1fFUM1Vv3EwYKZDFmYDxNTBPTEZAGG4fIWVuLJ3JFOS8/edit?usp=sharing'), 
                ('Spanish','https://docs.google.com/spreadsheets/d/1YPoON25ikaxl47e03rIvP000EWV1Jjb69uYfcKykyVw/edit?usp=sharing'), 
                ('Skandinavian   ','https://docs.google.com/spreadsheets/d/1Nb2EOiFuyYmIVIB5MtUINyflQMOIu8OklgVgWS5zG2w/edit?usp=sharing'), 
                ('Tigrinya       ','https://docs.google.com/spreadsheets/d/1xirVHOFdzJnAk2zHdcyL1qk59R0O9xIKYCpuDOzRCVk/edit?usp=sharing'), 
                ('Arabic ','https://docs.google.com/spreadsheets/d/1OgfvT0-Fu1i7o4voo6hGyijl5PuX3Ao7vaaD290yN3c/edit?usp=sharing'), 
                ('Tamilstill     ','https://docs.google.com/spreadsheets/d/1U5zN3Z8ndAsP-rgAIUYdZ5byStv-MXjiCHPQjmiUYPI/edit?usp=sharing'), 
                ('Vietnamese     ','https://docs.google.com/spreadsheets/d/1nAHfWgRkPl8v3bn2cZdlDzs_z1gTAEsvJDPMftfBozQ/edit?usp=sharing'), 
                ('Turkish','https://docs.google.com/spreadsheets/d/1TxSFbmaWGjbg0jQCDTEQQRtUREMr5FaoDhfQIVpqGuM/edit?usp=sharing'), 
                ('Armenian       ','https://docs.google.com/spreadsheets/d/17GNmqw7p70yeCCgxhX-0B12p4Pr-5Dn3SGEPqVj8SMQ/edit?usp=sharing'), 
                ('Bangla ','https://docs.google.com/spreadsheets/d/14T7_M75eTfuVq3sv90NuAXNL4ANa_S_FiW9UeYzCwzY/edit?usp=sharing'), 
                ('Bulgarian      ','https://docs.google.com/spreadsheets/d/1_IVb4dau9W4Ks2EXeirmKvJcpiv-g5wGvtpuvKWXx2o/edit?usp=sharing'), 
                ('Catalan','https://docs.google.com/spreadsheets/d/1CofyH0zQK5EqreiQHOCmKZ_JBu5IdfeIEvZZEGK0lrQ/edit?usp=sharing'), 
                ('Czech  ','https://docs.google.com/spreadsheets/d/1pvYWmnD1gG-6EJDZjfm_OSRCmmzI0rojRl-WBjjsvkg/edit?usp=sharing'), 
                ('Dari   ','https://docs.google.com/spreadsheets/d/1_DZXAK6qVd3qRFKH-xodl8JnUPGnX8_y_tRuYUM128k/edit?usp=sharing'), 
                ('Dutch  ','https://docs.google.com/spreadsheets/d/1OhE1xpgofuivQDtcWvDeng4XxpyDFteExKwiC-k57wE/edit?usp=sharing'), 
                ('Slovak/ Czech  ','https://docs.google.com/spreadsheets/d/1dOiR8Uicz59p5CvzXHtT3M672R0Iw3ADzFcZANE27pA/edit?usp=sharing'), 
                ('Russian','https://docs.google.com/spreadsheets/d/1WptrC8MhzEDpBma86wyyz2CvVhXyUKIaIaFklkMcC80/edit?usp=sharing'), 
                ('Romanian       ','https://docs.google.com/spreadsheets/d/1ashnd-ZtcyrFEj0fYAl5ksaImSqWyahgHkbZnD_YqMA/edit?usp=sharing'), 
                ('Portuguese     ','https://docs.google.com/spreadsheets/d/1QKIgFbW-R9Zr6fzTuQs-grOPvGp0DcNj1FfkY_bbPqA/edit?usp=sharing'), 
                ('Filipino       ','https://docs.google.com/spreadsheets/d/1_5C3GEZbr34X9nLUADEaCs63Rz3TDkOE4e1DwFMsmcs/edit?usp=sharing'), 
                ('Farsi  ','https://docs.google.com/spreadsheets/d/1S8KfVhmT6oDmJuxL0QFQ9q3j4cnegUWWXOSTUv6r7gY/edit?usp=sharing'), 
                ('Finnish','https://docs.google.com/spreadsheets/d/1VS0gHUD5sHqoQPI65CCbhCykhC5Bb0jx3GXfWbAmwBQ/edit?usp=sharing'), 
                ('French ','https://docs.google.com/spreadsheets/d/1wSR5_gLCMNdGDOLlKuKel35_oaKrzrX5z6pgrlB_T0k/edit?usp=sharing'), 
                ('Polish ','https://docs.google.com/spreadsheets/d/1lNixeQDE3IaGV1-KwGd0QMxDawpj8B2AcRMLnkRXE7I/edit?usp=sharing'), 
                ('Pashto ','https://docs.google.com/spreadsheets/d/1Wz4il9CygqlZW1m7l7DDfXQpqQ-Unk7zmavBO5r5kGI/edit?usp=sharing'), 
                ('German ','https://docs.google.com/spreadsheets/d/1Hu1ikg7AM_OJzbWSwSIzljYTOor4fKLXiUBYSXPm1ks/edit?usp=sharing'), 
                ('Macedonian     ','https://docs.google.com/spreadsheets/d/1kEcuVFHCkt5kUE2dV2jff4UZZBLIZ2mUMVlue4ICQtM/edit?usp=sharing'), 
        ]
    lexemes = []
    for typ, sheet_uri in sheets[:1]:
        print(typ)
        s = sc.SheetScraper(sheet_uri)
        s.fetch() 
        s.select_columns(languages)	
        #s2tsv(s,languages,typ=sh)
        #s2js(s,languages,typ=sh) 
        lexemes += s2lxm(s)
    fulldico = {}
    for lx in lexemes:
      fulldico = addtodico(fulldico,lx)
      
    
        


          #'short':'https://docs.google.com/spreadsheets/d/10Ch8eIACzROPYql5aztkG3_VvdCdkDInnVVK7QPK2E0/pubhtml#gid=418287843&single=true',
          #'long':'https://docs.google.com/spreadsheets/d/1IpkETNzRzletRpLEeLUKAldB2j_O8UJVn1zM_sYg56Y/pubhtml#gid=0',
          #'longcopy': 'https://docs.google.com/spreadsheets/d/1bBesmfse2EcK0n_DpgEM5uGd4EwNkxZW8waRLPSPb4Y/pubhtml?gid=0&single=true'
          #('medical','https://docs.google.com/spreadsheets/d/1wjmRrkN9WVB4KIeKBy8wDDJ8E51Mh2-JxIBy2KNMFRQ/pubhtml')
          #'legal':'https://docs.google.com/spreadsheets/d/1D7jo-tAyQkmfYvVyT27nZ93ZkyFcZg2vEvf4OMbXJ_c/pubhtml#gid=0',
         