#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import re
def mixtheregex(*items):
	return '(?:' + '|'.join(items) + ')'

word=r'(?:[\w_\‘\’\'\-\:\\)\(]+)'		#Regex to match words

number=(r'(?:[\+-]?\$?\d+(?:\.\d+)?(?:[eE]-?\d+)?%?)(?![A-Za-z])(?:\\s*/\s*(?:[\+-]?\$?\d+(?:\.\d+)?(?:[eE]-?\d+)?%?)(?![A-Za-z]))?')
											#Regex for numbers(decimals,...)
Punct=r"['\"“”‘’?.!…,:;@/\\]"		#Punctuation	
hashi = r'(?:\#+[\w]+[_\'\-]*[\w]+)'		#Hash regex

mention=r'(?:@[\w_]+)'			#Mention regex
ellipsis=r'(?:\.(?:\s*\.){1,})'		#Ellipsis regex
h_nu=r"""(?:(?:\+?[01][\-\s.]*)?(?:[\(]?\d{3}[\-\s.\)]*)?\d{3}[\-\s.]*\d{4})"""		#Phonenumberregex
brack=r'(?:[(][\w_\'\-\:\\)\(]+[)])'		#Brackets regex
time=(r'\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?')	#Time regex
other=r'(?:\S)'
br=r'(?:[{][\w_\'\-\:\\)\(]+[}])'		#other kindof bracket regex
has=r'(?:[<][\w_\'\-\:\\)\(]+[>])'			#<> regex
sqb=r'(?:[[][\w_\'\-\:\\)\(]+[]])'			#square bracket regex
quotes=r'(?:["][\w_\'\-\:\\)\(]+["])'
url=r'(?:http[s]?:\//[\w]+.[\w]+(?:[\/])*[\w]+)'
email=r'(?:[a-zA-Z(0-9)]+@[a-z]+.[a-z]{3,3})'
t_re=re.compile((mixtheregex(email,url,word,quotes,number,hashi,mention,ellipsis,Punct,time,h_nu,brack,br,has,other,sqb)),re.VERBOSE|re.I|re.UNICODE)

def Tokenize(s):
	
	print s

	s=str(s).decode('utf-8')
	tokens=t_re.findall(s)
	"""
	for k in tokens:	
		print k.encode('utf-8')
	"""	
	return tokens
f=open('train.txt',mode='r')
g=f.readlines()
context={}
transition={}
emit={}
possible_tags=['<s>','</s>']
def hmm():
	prev='<s>'
	for m in g:
		k=m.split()
		if prev not in context.keys():
			context[prev]=1
		else:   
			context[prev]+=1
		tag=k[1]
		word=k[0]
		if prev+" "+tag not in transition.keys():
			transition[prev+" "+tag]=1
		else:
			transition[prev+" "+tag]+=1
		if tag not in context.keys():
			context[tag]=1
			possible_tags.append(tag)
		else:
			context[tag]+=1
		if tag+" "+word not in emit.keys():
			emit[tag+" "+word]=1
		else:
			emit[tag+" "+word]+=1
	
		prev=tag
	transition[prev+" </s>"]=1      
def transpro(a,b):  #p(a/b)
	return math.log(transition[b+" "+a]/float(context[b]))
def emisspro(w,t):  #p(w/t)
	if t+" "+w in emit.keys():
		g=lamb*emit[t+" "+w]/float(context[t])+((1-lamb)*1.0/n)
	else:
		g=(1-lamb)*1.0/n
	return math.log(g)
	
hmm()
"""
lamb=input("input lambda")
n=input("input n")
"""
lamb=0.7
n=10000
te=open('test.txt',mode='r')
m=te.readlines()
for j in m: #j-lines
	#le=len(j)
	best_score={}
	best_edge={}
	best_score["0 <s>"]=0
	best_edge["0 <s>"]=None
	words=Tokenize(j)
	le=len(words)
	print words,le
	le=le+1
	for i in range(le-1):
		for prev in possible_tags:
			for nex in possible_tags:
				if str(i)+" "+prev in best_score.keys() and prev+" "+nex in transition.keys():
					score=best_score[str(i)+" "+prev]-transpro(nex,prev)-emisspro(words[i],nex)
					if str(i+1)+" "+nex not in best_score.keys() or best_score[str(i+1)+" "+nex]>score:
						best_score[str(i+1)+" "+nex]=score
						best_edge[str(i+1)+" "+nex]=str(i)+" "+prev   
	for prev in possible_tags:
		if str(le-1)+" "+prev in best_score.keys() and prev+" </s>" in transition.keys():            
			score=best_score[str(le-1)+" "+prev]-transpro("</s>",prev)
			if str(le)+" "+'</s>' not in best_score.keys() or best_score[str(le)+" "+'</s>']>score:
					best_score[str(le)+" "+'</s>']=score
					best_edge[str(le)+" "+'</s>']=str(le-1)+" "+prev
	tagss=[]
		
	next_edge=best_edge[str(le)+" </s>"]
	
	while next_edge!="0 <s>":   
		#print tagss
		positon=next_edge.split()[0]
		taggy=next_edge.split()[1]
		tagss.append(taggy)
		 
		#print positon,taggy
		next_edge=best_edge[next_edge]
		#print next_edge
	tagss.reverse()
	print " ".join(tagss)                       

"""
print transition
print "HMMMMMMMMMM"
print emit
"""





















