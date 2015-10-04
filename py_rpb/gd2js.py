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
 
	
			
def getpairs(records,lg,target=0):
	return [(r[target],r[lg]) for r in records if r[lg]!='']
  				 


def s2tsv(s,languages):
	for lg in languages:
			print(lg)
			lg = int(lg)
			name = s.records[0][lg]
			normname = normalizename(name) 
			print(normname)
			pairs = getpairs(s.records[1:], lg)
		    
def s2js(s,languages,typ=''):
	jss = []
	for lg in languages:
			print(lg)
			lg = int(lg)
			name = s.records[0][lg]
			normname = normalizename(name) 
			print("%s --> %s"%(name,normname))
			pairs = getpairs(s.records[1:], lg,target=31)
			lgjs = lg2js(normname, pairs)
			jss.append(lgjs)
	t = "var lgs={\n%s\n}"% '\n,\n'.join(jss)
	out = open('%sdata_%s.js'%(typ,s.records[0][lg]),'w')
	out.write(t)
	out.close()
	
			

if __name__ == '__main__': 
	#usage : gd2js.py  1 3 8 12 14 17 19 22 24   
	languages = sys.argv[1:] 
	print(languages) 
	sheets = {
	  'short':'https://docs.google.com/spreadsheets/d/10Ch8eIACzROPYql5aztkG3_VvdCdkDInnVVK7QPK2E0/pubhtml#gid=418287843&single=true',
	  #'long':'https://docs.google.com/spreadsheets/d/1IpkETNzRzletRpLEeLUKAldB2j_O8UJVn1zM_sYg56Y/pubhtml#gid=0&single=true',
	  #'medical':'https://docs.google.com/spreadsheets/d/1wjmRrkN9WVB4KIeKBy8wDDJ8E51Mh2-JxIBy2KNMFRQ/pubhtml#gid=0&single=true',
	  #'legal':'https://docs.google.com/spreadsheets/d/1D7jo-tAyQkmfYvVyT27nZ93ZkyFcZg2vEvf4OMbXJ_c/pubhtml#gid=0&single=true',
	  }
	for sh in sheets:
	    sheet_uri = sheets[sh]
	    print(sh,sheet_uri)
	    s = sc.SheetScraper(sheet_uri)
	    s.fetch() 
	    s.select_columns(languages)	
	    s2js(s,languages,typ=sh)     
