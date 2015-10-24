import scrapesheet as sc
import sys
import string

#provide a commandline version to scrape google doc and output to either tsv or js
#tabulate from original class was not working at the time of writing

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
				"phonetic":"",
				"domain":""
			}""" 
			result = """ '%s':function (){ 
	return [""" % normname
			result += '\n,\n'.join([t%p for p in pairs])
			result +="""	    ]
    }"""
			return result
 
	
			
def getpairs(records,lg):
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
	
			

if __name__ == '__main__': 
	#usage : gd2js.py  1 3 8 12 14 17 19 22 24  
	languages = [int(i) for i in sys.argv[1:]]
	#print(languages)
	sheets = {
	  #'short':'https://docs.google.com/spreadsheets/d/10Ch8eIACzROPYql5aztkG3_VvdCdkDInnVVK7QPK2E0/pubhtml#gid=418287843&single=true',
	  #'long':'https://docs.google.com/spreadsheets/d/1IpkETNzRzletRpLEeLUKAldB2j_O8UJVn1zM_sYg56Y/pubhtml#gid=0',
	  #'longcopy': 'https://docs.google.com/spreadsheets/d/1bBesmfse2EcK0n_DpgEM5uGd4EwNkxZW8waRLPSPb4Y/pubhtml?gid=0&single=true'
	  'medical':'https://docs.google.com/spreadsheets/d/1wjmRrkN9WVB4KIeKBy8wDDJ8E51Mh2-JxIBy2KNMFRQ/pubhtml',
	  #'legal':'https://docs.google.com/spreadsheets/d/1D7jo-tAyQkmfYvVyT27nZ93ZkyFcZg2vEvf4OMbXJ_c/pubhtml#gid=0',
	  }
	for sh in sheets:
	    sheet_uri = sheets[sh]
	    s = sc.SheetScraper(sheet_uri)
	    s.fetch() 
	    s.select_columns(languages)	
	    s2tsv(s,languages,typ=sh)
	    #s2js(s,languages,typ=sh) 
    
