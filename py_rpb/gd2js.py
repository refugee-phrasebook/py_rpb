import scrapesheet as sc
import sys
import string
import sampa2x
from iso6393 import iso6393dic
import json
from data import domaind
#provide a commandline version to scrape google doc and output to either tsv or js
#tabulate from original class was not working at the time of writing

class lexeme():
  def __init__(self,ID,label,orth,iso,sampa,latn,ipa,domain):
    self.ID = ID
    self.label = label
    self.iso6393code = iso
    self.orthographic = orth
    self.transcriptions = sampa2x.getPhoneticStrings(sampa,ipa=ipa)
    self.domain = domain
    if latn:  
      self.transcriptions['Latin'] = latn
    else:  
      self.transcriptions['Latin'] = ''

  

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
         
		    
def s2js(s,languages,typ='',target=0):
	jss = []
	for lg in languages:
			print(lg)
			lg = int(lg)
			name = s.records[0][lg]
			normname = normalizename(name) 
			print("%s --> %s"%(name,normname))
			pairs = getpairs(s.records[1:], lg,target=target)
			lgjs = lg2js(normname, pairs)
			jss.append(lgjs)
	t = "var lgs={\n%s\n}"% '\n,\n'.join(jss)
	targetlg = normalizename(s.records[0][target])
	fn = '%sdata_%s.js'%(typ,targetlg)
	print(fn)
	out = open(fn,'w')
	out.write(t)
	out.close()

	
def s2lxm(s):#only for new short-style sheets
  result = []
  records = s.records
  iso6393code = records[0][2]
  #identify interesting colums
  sampacol = False
  latncol = False
  ipacol = False
  for i,x in enumerate(records[0]):
    y = x.strip()
    if y.endswith('-Qaas'):
      if y.startswith(iso6393code): 
        sampacol = i
      else:
        raise ValueError   
      continue
    if y.endswith('-Qaai'):
      if y.startswith(iso6393code): 
        ipacol = i
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
    ipa = False
    latn = False
    if sampacol:
      sampa = record[sampacol]
    if latncol:
      latn = record[latncol]
    if ipacol:
      ipa = record[latncol]
    orth = record[2]
    #print(sampa, latn, orth, ID, label,iso6393code)
    domain = getDomain(ID)
    lxm = lexeme(ID,label,orth,iso6393code,sampa,latn,ipa,domain) # check for overwriting
    result.append(lxm)
  #print(len(result))
  return result
    
def getDomain(ID):
  try:
    return domaind[ID]
  except KeyError:
    print (ID,"not in domaind")
    
def addtodico(d,lx):
  ID = lx.ID
  #assure the lexeme is in the dict
  if d.get(ID) == None:
    d[ID] = {'label':lx.label,
            'domain':lx.domain,
            'ID':lx.ID,
            'lgs':{'eng':{'orthographic':lx.label,
                          'transcriptions':{'IPA':'',
                                            'SAMPA':'',
                                            'cyrtrans':'',
                                            'arabtrans':''
                                            }
                          }
                  }
    }
  #print(lx.label)
  #add new information
  if d[ID]['lgs'].get(lx.iso6393code) != None:
    print("%s already present in %s, skipping %s"%(ID,lx.iso6393code,lx.orthographic))
    return d
  d[ID]['lgs'][lx.iso6393code] = {'orthographic':lx.orthographic,
'transcriptions':lx.transcriptions,
'label':iso6393dic[lx.iso6393code]['label']
    }
  return d
  

    
if __name__ == '__main__':  
    #usage : gd2js.py  1 3 8 12 14 17 19 22 24  
    languages = [int(i) for i in sys.argv[1:]]
    #print(languages)
    sheets = [('German','https://docs.google.com/spreadsheets/d/1Hu1ikg7AM_OJzbWSwSIzljYTOor4fKLXiUBYSXPm1ks/pubhtml'), 
                ('Serbo-Croatian','https://docs.google.com/spreadsheets/d/1wweXwpEpHWrFcM46YZ-SVi-gLfywrUyj1wjEf19DWQE/pubhtml'),
                ('Albanian','https://docs.google.com/spreadsheets/d/1B9OXDIV4nDUekqpwILbAK6eHIAIP5UePgpYbOWRsTvY/pubhtml'), 
                ('Urdu','https://docs.google.com/spreadsheets/d/1oCRZRBOn6sl8ufJ12OF1gPR_OLj598H45OENqkFfF7U/pubhtml'), 
                ('Amharic','https://docs.google.com/spreadsheets/d/1ni8FOoW4Nqa1drwVCEoKMh4NqAn5ySSezFL-Mvo0hiY/pubhtml'), 
                ('Somali','https://docs.google.com/spreadsheets/d/1SLCVAYupSfjpvMwKiid0Z4JexbJhQsZX19yAzhPIcx0/pubhtml'), 
                ('Slovenian','https://docs.google.com/spreadsheets/d/1fFUM1Vv3EwYKZDFmYDxNTBPTEZAGG4fIWVuLJ3JFOS8/pubhtml'), 
                ('Spanish','https://docs.google.com/spreadsheets/d/1YPoON25ikaxl47e03rIvP000EWV1Jjb69uYfcKykyVw/pubhtml'), 
                ('Tigrinya','https://docs.google.com/spreadsheets/d/1xirVHOFdzJnAk2zHdcyL1qk59R0O9xIKYCpuDOzRCVk/pubhtml'), 
                ('Arabic','https://docs.google.com/spreadsheets/d/1OgfvT0-Fu1i7o4voo6hGyijl5PuX3Ao7vaaD290yN3c/pubhtml'), 
                ('Tamil','https://docs.google.com/spreadsheets/d/1U5zN3Z8ndAsP-rgAIUYdZ5byStv-MXjiCHPQjmiUYPI/pubhtml'), 
                ('Vietnamese','https://docs.google.com/spreadsheets/d/1nAHfWgRkPl8v3bn2cZdlDzs_z1gTAEsvJDPMftfBozQ/pubhtml'), 
                ('Turkish','https://docs.google.com/spreadsheets/d/1TxSFbmaWGjbg0jQCDTEQQRtUREMr5FaoDhfQIVpqGuM/pubhtml'), 
                ('Armenian','https://docs.google.com/spreadsheets/d/17GNmqw7p70yeCCgxhX-0B12p4Pr-5Dn3SGEPqVj8SMQ/pubhtml'), 
                ('Bangla','https://docs.google.com/spreadsheets/d/14T7_M75eTfuVq3sv90NuAXNL4ANa_S_FiW9UeYzCwzY/pubhtml'), 
                ('Bulgarian','https://docs.google.com/spreadsheets/d/1_IVb4dau9W4Ks2EXeirmKvJcpiv-g5wGvtpuvKWXx2o/pubhtml'), 
                ('Catalan','https://docs.google.com/spreadsheets/d/1CofyH0zQK5EqreiQHOCmKZ_JBu5IdfeIEvZZEGK0lrQ/pubhtml'), 
                ('Czech','https://docs.google.com/spreadsheets/d/1pvYWmnD1gG-6EJDZjfm_OSRCmmzI0rojRl-WBjjsvkg/pubhtml'), 
                ('Dari','https://docs.google.com/spreadsheets/d/1_DZXAK6qVd3qRFKH-xodl8JnUPGnX8_y_tRuYUM128k/pubhtml'), 
                ('Dutch','https://docs.google.com/spreadsheets/d/1OhE1xpgofuivQDtcWvDeng4XxpyDFteExKwiC-k57wE/pubhtml'), 
                ('Slovak','https://docs.google.com/spreadsheets/d/1dOiR8Uicz59p5CvzXHtT3M672R0Iw3ADzFcZANE27pA/pubhtml'), 
                ('Russian','https://docs.google.com/spreadsheets/d/1WptrC8MhzEDpBma86wyyz2CvVhXyUKIaIaFklkMcC80/pubhtml'), 
                ('Romanian','https://docs.google.com/spreadsheets/d/1ashnd-ZtcyrFEj0fYAl5ksaImSqWyahgHkbZnD_YqMA/pubhtml'), 
                ('Portuguese','https://docs.google.com/spreadsheets/d/1QKIgFbW-R9Zr6fzTuQs-grOPvGp0DcNj1FfkY_bbPqA/pubhtml'), 
                ('Filipino','https://docs.google.com/spreadsheets/d/1_5C3GEZbr34X9nLUADEaCs63Rz3TDkOE4e1DwFMsmcs/pubhtml'), 
                ('Farsi','https://docs.google.com/spreadsheets/d/1S8KfVhmT6oDmJuxL0QFQ9q3j4cnegUWWXOSTUv6r7gY/pubhtml'), 
                ('Finnish','https://docs.google.com/spreadsheets/d/1VS0gHUD5sHqoQPI65CCbhCykhC5Bb0jx3GXfWbAmwBQ/pubhtml'), 
                ('French','https://docs.google.com/spreadsheets/d/1wSR5_gLCMNdGDOLlKuKel35_oaKrzrX5z6pgrlB_T0k/pubhtml'), 
                ('Polish','https://docs.google.com/spreadsheets/d/1lNixeQDE3IaGV1-KwGd0QMxDawpj8B2AcRMLnkRXE7I/pubhtml'), 
                ('Pashto','https://docs.google.com/spreadsheets/d/1Wz4il9CygqlZW1m7l7DDfXQpqQ-Unk7zmavBO5r5kGI/pubhtml'), 
                ('Macedonian','https://docs.google.com/spreadsheets/d/1kEcuVFHCkt5kUE2dV2jff4UZZBLIZ2mUMVlue4ICQtM/pubhtml'),
                ('Lithuanian','https://docs.google.com/spreadsheets/d/1ozMIw30k-r8DzANLR66QWHWR7rdbkiJi_PfjU2zgIVE/pubhtml'),
                ('Greek','https://docs.google.com/spreadsheets/d/1L2QEC-TpWDEhUfQERConudQO12kx54zEy8poesFmo1c/pubhtml'),
                ('Sorani','https://docs.google.com/spreadsheets/d/1eFm_HeVZYmibwUElJ88wroTANMMFBLVkF9b4G5w4Ksk/pubhtml'),
                ('Hungarian','https://docs.google.com/spreadsheets/d/1fHcCEKf7utsT6L_LY7iDaSMKpSkwLSbqTKD96Bi1Bvw/pubhtml'),
                ('Icelandic','https://docs.google.com/spreadsheets/d/1mfVsGJqVp9iJ0rLXsqqZ5EDdgMdAbKh4mY7D7m8zQHA/pubhtml'),
                ('Kurmanji','https://docs.google.com/spreadsheets/d/1mfVsGJqVp9iJ0rLXsqqZ5EDdgMdAbKh4mY7D7m8zQHA/pubhtml'),
                ('Italian','https://docs.google.com/spreadsheets/d/1sTtzVugGrOL3ZplTRejSr5G2UAcv7JSEqYDiISzZbJM/pubhtml'),
                ('Swedish','https://docs.google.com/spreadsheets/d/1v4LtKee6U1booU92P0UOUrrL4W9nWaiyzx4g-9v20gI/pubhtml'),
                ('Norwegian','https://docs.google.com/spreadsheets/d/1Nb2EOiFuyYmIVIB5MtUINyflQMOIu8OklgVgWS5zG2w/pubhtml'),
                ('Danish','https://docs.google.com/spreadsheets/d/1Cd8H5-wle6ea32alCPdoSIzrbTu_Il48zGzq8XokV3o/pubhtml') 
        ]
    #accumulate lexemes
    lexemes = []
    for typ, sheet_uri in sheets:
        print(typ)
        s = sc.SheetScraper(sheet_uri)
        s.fetch() 
        s.select_columns(languages)	
        #s2tsv(s,languages,typ=sh)
        #s2js(s,languages,typ=sh) 
        lexemes += s2lxm(s)
    fulldico = {}
    #store lexemes in dictionary
    for lx in lexemes:
      fulldico = addtodico(fulldico,lx)
    jd = json.dumps(fulldico,indent=4)
    out = open('lexemes.json','w')
    out.write(jd)
    out.close()
      
    
        


          #'short':'https://docs.google.com/spreadsheets/d/10Ch8eIACzROPYql5aztkG3_VvdCdkDInnVVK7QPK2E0/pubhtml#gid=418287843&single=true',
          #'long':'https://docs.google.com/spreadsheets/d/1IpkETNzRzletRpLEeLUKAldB2j_O8UJVn1zM_sYg56Y/pubhtml#gid=0',
          #'longcopy': 'https://docs.google.com/spreadsheets/d/1bBesmfse2EcK0n_DpgEM5uGd4EwNkxZW8waRLPSPb4Y/pubhtml?gid=0&single=true'
          #('medical','https://docs.google.com/spreadsheets/d/1wjmRrkN9WVB4KIeKBy8wDDJ8E51Mh2-JxIBy2KNMFRQ/pubhtml')
          #'legal':'https://docs.google.com/spreadsheets/d/1D7jo-tAyQkmfYvVyT27nZ93ZkyFcZg2vEvf4OMbXJ_c/pubhtml#gid=0',
          
