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
				 

def s2tsv(s,languages):
	for lg in languages:
			print(lg)
			lg = int(lg)
			name = s.records[0][lg]
			normname = normalizename(name) 
			print(normname)
			pairs = getpairs(s.records[1:], lg)
		    
def s2js(s,languages):
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
	out = open('data.js','w')
	out.write(t)
	out.close()
	
			

if __name__ == '__main__': 
	#usage : gd2js.py  1 3 8 12 14 17 19 22 24  
	languages = sys.argv[1:]
	print(languages)
	sheet_uri = 'https://docs.google.com/spreadsheets/d/10Ch8eIACzROPYql5aztkG3_VvdCdkDInnVVK7QPK2E0/pubhtml?gid=418287843&single=true'
	s = sc.SheetScraper(sheet_uri, to_row=106)#106
	s.fetch() 
	s.select_columns(languages)	
	jss = []
	#s2tsv(s,languages)
	s2js(s,languages) 
    