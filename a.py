#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import brown
t=1
for wor in brown.tagged_words():
	if t<=50000:
		print wor[0].encode('utf-8'),wor[1].encode('utf-8')
	else:
		break
	t+=1
#print brown.tagged_words()
