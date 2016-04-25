
# coding: utf-8

# In[1]:

import os
#from textblob import Blobber
#from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob
import nltk
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()
import json
import pprint
#tb = Blobber(analyzer=NaiveBayesAnalyzer())

# In[2]:

def list_files(dir):																								  
	r = []																											
	subdirs = [x[0] for x in os.walk(dir)]																			
	for subdir in subdirs:																							
		files = (subdir)[1]																			 
		if (len(files) > 0):																						  
			for file in files:																						
				r.append(subdir + "/" + file)																		 
	return r   


# In[3]:

# for dirname, dirnames, filenames in os.walk('.\data'):
	# print path to all subdirectories first.
#	 for subdirname in dirnames:
#		 print(os.path.join(dirname, subdirname))

	# print path to all filenames.
#	 for filename in filenames:
#		 print(os.path.join(dirname, filename))


# In[4]:

# os.listdir('data')


# In[14]:

artist_count = 0;
song_count = 0;
songs = []

for dirname, dirnames, filenames in os.walk('.\data'):
	# print path to all subdirectories first.
#	 for subdirname in dirnames:
#		 print(os.path.join(dirname, subdirname))

	# print path to all filenames.
	for filename in filenames:
		if filename[0] == '.':
			continue
		"""
		if artist_count > 0:
			break
			
		if song_count > 0:
			break
		"""
		song_count+=1
		
		songname = filename[:-4]
		songname = songname.replace("-", " ")
		artistname = dirname[7:]
		artistname = artistname.replace("-", " ")
		
#		 index = 0
#		 i = 0
# #		 while (i != -1):
#			 index = i
# #			 i = dirname.find("-", index, len(dirname))

# #		 artistname = dirname[index:]
		
		
		#print("Path:", os.path.join(dirname, filename))
		filepath = os.path.join(dirname, filename)
		#print(filepath)
		#print("dirname:", dirname)
		#print("filename:", filename)
		#print("songname:", songname)
		#print("artistname:", artistname)
		
		song = {}
		song['name'] = songname
		song['artist'] = artistname
		
		#print(song['artist'], song['name'])
		
		
		with open(filepath, 'r') as myfile:
			songtext=myfile.read()#.replace('\n', '')
			#print(songtext)
		if (songtext != ""):
			blob = TextBlob(unicode(songtext, "utf-8"))
			nouns = {}
			tags = None
			tokens = nltk.word_tokenize(unicode(songtext, "utf-8"))
			tags = nltk.tag._pos_tag(tokens, tags, tagger)
			for tag in tags:
				if tag[1][0] == 'N':
					noun = tag[0].encode('utf-8').strip().lower()
					if noun not in nouns:
						nouns[noun] = 1
					else:
						nouns[noun] += 1
			keywords = {}
			top3 = sorted(nouns, key=lambda key: nouns[key], reverse=True)[:3]
			for i, key in enumerate(top3):
				#keywords[key] = nouns[key]
				keywords['key' + str(i + 1)] = key
				keywords['frequency' + str(i + 1)] = nouns[key]
			song['keywords'] = keywords
			song['sentiment'] = blob.sentiment.polarity
			songs.append(song)
			pprint.PrettyPrinter(depth=6).pprint(song);

# In[10]:

with open('songs', 'w') as file_name:
	json.dump(songs, file_name, indent=4)


# In[ ]:




# In[ ]:



