#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import csv
import re

from tweetlearn.tweets.models import Tweet
from collections import Counter

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

	    all_tweets = list(csv_reader)
	    nb_tweets = len(all_tweets)
	    k_neighbours = all_tweets[1:k]

	    dist_k_neighbours = {}
	    print dist_k_neighbours
	    
	    for neighbour in k_neighbours:
		neighbour = neighbour[2]
		dist_k_neighbours[neighbour] = self.distance(tweet, neighbour)
		#dist_k_neighbours[k_neighbours[i][2]] = self.distance(tweet, k_neighbours[i])

	    
	    for i in range(k + 1, nb_tweets - 1):
		dist = self.distance(tweet, all_tweets[i])

		if dist < any(dist_k_neighbours.values()):

		    higher_dist = max(dist_k_neighbours.values())

		    key_to_delete = self.key_from_value(dist_k_neighbours, higher_dist)
		    del dist_k_neighbours[key_to_delete]
		    
		    text = all_tweets[i][2]
		    dist_k_neighbours[text] = dist
		    print dist_k_neighbours

	    return self.vote(dist_k_neighbours)

    def vote(self, dist_k_neighbours):
	counter = Counter(dist_k_neighbours.values())
	# TODO: Gerer le cas ou il y a plusieurs valeurs identiques
	# Choisir la key la plus basse
	# Retourner la category !! Faire un tuple (text, category) dans dist_k_neighbours ?
	return self.key_from_value(counter, max(counter.values()))


    def key_from_value(self, _dict, _value):
	for key, value in _dict.iteritems():
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
	
	#############
	### BAYES ###
	#############

    # TODO: To mettre en float...

    def get_tweets_from_class(self, _class):
	# Retourne tous les tweets d'une classe donnee

	if _class == 'negative':
	    class_id = 0
	elif _class == 'positive':
	    class_id = '2'
	elif _class == 'neutral':
	    class_id = '1'
	else:
	    return -1    

	tweets_in_class = Tweet.objects.filter(category=class_id)
	return tweets_in_class

    def total_words(self):
	# Retourne le nombre total de mots de la base de tweets
	# Independemment des classes
	total_words = 0
	tweets = Tweet.objects.all()
	
	for tweet in tweets:
    	    total_words += len(re.findall(r"\w+", tweet.text))

	return total_words
	    
    def nb_occurence(self, _word, _class):
	# Retourne le nombre d'occurences d'un mot dans un classe donnee
	# Ainsi que le nombre total de mots dans cette classe
	# TODO: Calculer tous les mots d'un coup, sinon pas du tout optimise

	count_word = 0
	total_words = 0
	
	tweets = self.get_tweets_from_class(_class)
	total_words = len(tweets)

	for tweet in tweets:
	    # TODO: Optimisable ?
	    words = re.findall(r"\w+", tweet.text)

	    for word in words:
		if word == _word:
		    count_word += 1

	return (count_word, total_words)
	
    #### PROBA ####

    def proba_word(self, word, _class, occ_word, freq=0, bigramme=False):
	# P(m|c)
	# Probabilite d'occurence du mot m dans un texte de la classe c

	nb_words, total_classwords = self.nb_occurence(word, _class)
	N = self.total_words()

	if freq:
	    # Frequence
 	    return ((nb_words + 1) / (total_classwords + N)) ** occ_word
	else:
	    # Presence
	    return (nb_words + 1) / (total_classwords + N)
	
    def proba_class(self, _class):
	# Probabilite de la classe	
	# Nombre de tweets de la classe / Nombre de tweets total
	
	nb_tweets_class = len(self.get_tweets_from_class(_class))
	nb_tweets = len(Tweet.objects.all())

	return (nb_tweets_class / nb_tweets)
	
    def proba(self, tweet, _class, freq=0, bigramme=False):
	# Calcul reel de la proba: P(classe|t)
	prob = 0
	proba_class = self.proba_class(_class)

	tweet = tweet.split(" ")
	
	### bigramme ###
	if bigramme:
            tmp_tweet = []
	    
	    cpt = 0
	    while cpt < len(tweet) - 1:
		tmp_tweet.append(" ".join([tweet[cpt], tweet[cpt + 1]]))
                cpt += 1
            
	    tweet = tmp_tweet

	for word in tweet:
	    if len(word) > 3:
	        occ_word = tweet.count(word)
	        prob += self.proba_word(word, _class, occ_word) * proba_class
	
	return prob

    def classifier(self, tweet, freq=0, bigramme=False):
	
	proba_neg = self.proba(tweet, 'negative', freq=freq, bigramme=bigramme)
	proba_pos = self.proba(tweet, 'positive', freq=freq, bigramme=bigramme)
	proba_neu = self.proba(tweet, 'neutral', freq=freq, bigramme=bigramme)

	if proba_pos > proba_neg and proba_pos > proba_neu:
	    return 4
	elif proba_neg > proba_pos and proba_neg > proba_neu:
	    return 0
	else:
	    return 2

if __name__ == "__main__":
    alg = Algos()
    print(alg.classifier("Je mange du pain et de la viande  ", bigramme=True))
	
