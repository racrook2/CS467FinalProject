
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
all_keywords = {}
keyword_count = {}

for dirname, dirnames, filenames in os.walk('.\data'):
	# print path to all subdirectories first.
#	 for subdirname in dirnames:
#		 print(os.path.join(dirname, subdirname))

	# print path to all filenames.
	for filename in filenames:
		if filename[0] == '.':
			continue

		filepath = os.path.join(dirname, filename)
		if os.path.getsize(filepath) == 0:
			print("Skipping 0-byte file " + filepath)
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

					if noun == "[" or noun == "]":
						continue

					if noun not in nouns:
						nouns[noun] = 1
					else:
						nouns[noun] += 1
			top3 = sorted(nouns, key=lambda key: nouns[key], reverse=True)[:3]
			for i, key in enumerate(top3):
				song['key' + str(i + 1)] = key
				song['frequency' + str(i + 1)] = nouns[key]
				if key not in all_keywords:
					all_keywords[key] = [0 for i in range(2)]
					all_keywords[key][0] = blob.sentiment.polarity
					keyword_count[key] = 1
				else:
					keyword_count[key] += 1
					all_keywords[key][0] = (all_keywords[key][0]*(keyword_count[key] - 1) + blob.sentiment.polarity)/keyword_count[key]
			song['sentiment'] = blob.sentiment.polarity
			if 'key1' in song and 'key2' in song and 'key3' in song:
				song['keywords_appended'] = song['key1'] + ' ' + song['key2'] + ' ' + song['key3']
			songs.append(song)
			# pprint.PrettyPrinter(depth=6).pprint(song);



# In[10]:
# Include the count of songs that mention the keyword
for key in keyword_count:
	all_keywords[key][1] = keyword_count[key]

# Remove all keywords that are only mentioned once
print("Number of keywords:" + str(len(all_keywords)))
for key in keyword_count:
	if keyword_count[key] == 1:
		del(all_keywords[key])

print("Number of keywords with >1 song:" + str(len(all_keywords)))
# pprint.PrettyPrinter(depth=6).pprint(keyword_count);


with open('songs', 'w') as file_name:
	json.dump(songs, file_name, indent=4)

with open('keywords', 'w') as file_name:
	json.dump(all_keywords, file_name, indent=4)

# In[ ]:



# In[ ]:



