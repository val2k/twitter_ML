#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import csv
import re

class Algos:

    def __init__(self):
	self.cfg = config.Config()

    ##### KEYWORDS #####
    def annotation_by_keywords(self):
	# Ouverture du fichier csv nettoye
	# On bouche sur la liste de tweets
	# On effectue le process
	# Ecrire du tweet dans le nouveau fichier
        
	with open(config.ANNOTATED_CSV, 'a+') as annotated_csv:
	    csv_writer = csv.writer(annotated_csv)
            with open(config.CLEANED_CSV, 'a+') as cleaned_csv:
	        csv_reader = csv.reader(cleaned_csv)
                for tweet in csv_reader:
	    	    text = tweet[2]
	      	    category = self.process_annotation(text)
	    	    csv_writer.writerow([tweet[0], tweet[1], tweet[2], tweet[3], category])
	    	
    def process_annotation(self, tweet):
	neg_count = 0
	pos_count = 0

	with open(config.NEGATIVE_FILE, 'r+') as neg:
	    negatives = neg.read()

	with open(config.POSITIVE_FILE, 'r+') as pos:
	    positives = pos.read()

	for word in tweet:
	    if word in negatives:
		neg_count += 1
	    if word in positives:
		pos_count += 1

	res = pos_count - neg_count
	
	if res == 0:
	    return 2
	elif res > 0:
	    return 4
	else:
	    return 0

    ####################
    ####### KNN ########
    ###################

    def KNN(self, tweet, k):
	# tweet: tweet a etiqueter
	#     k: nombre de voisins
	# TODO: methode "vote" a implementer

	with open(config.ANNOTATED_CSV, 'r+') as annotated_file:
	    csv_reader = csv.reader(annotated_file)
	    csv_reader = list(csv_reader)
	    nb_tweets = len(csv_reader)
	    k_neighbours = csv_reader[1:k]

	    dist_k_neighbours = {}
	    
	    for neighbour in k_neighbours:
		neighbour = neighbour[2]
		dist_k_neighbours[neighbour] = self.distance(tweet, neighbour)
		#dist_k_neighbours[k_neighbours[i][2]] = self.distance(tweet, k_neighbours[i])

	    
	    for i in range(k + 1, nb_tweets - 1):
		dist = self.distance(tweet, csv_reader[i])

		if dist < any(dist_k_neighbours.values()):

		    higher_dist = max(dist_k_neighbours.values())
		    key_to_delete = key_from_value(dist_k_neighbours, higher_dist)
		    del dist_k_neighbours[key_to_delete]
		    dist_k_neighbours[k_neighbours[i]] = value


    def key_from_value(self, _dict, _value):
	for key, value in _dict:
	    if value == _value:
		return key
		    

    def distance(self, tweet1, tweet2):
    # TODO: implementer d'autres distances
	if isinstance(tweet1, list):
	    tweet1 = tweet1[2]
	if isinstance(tweet2, list): 
	    tweet2 = tweet2[2]

	common_words = 0
	total_words = len(re.findall(r"\w+", tweet1)) + \
		      len(re.findall(r"\w+", tweet2))
	
	tweet1 = tweet1.split(" ")
	tweet2 = tweet2.split(" ")

	for word in tweet1:
	    if word in tweet2:
		common_words += 1
	
	return float(float(total_words - common_words) / total_words)
	
	
if __name__ == "__main__":
    alg = Algos()
    print(alg.KNN("test", 10))
    print(alg.distance("lol lol lol", "bla bla bla"))
    print(alg.distance("lol lol lol", "lol lol lol"))
	

	
