#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import csv
import re

from tweets.models import Tweet
from collections import Counter

class Algos:

    def __init__(self):
	self.cfg = config.Config()



    ####################
    ##### KEYWORDS #####
    ####################


    def classifier_keyw(self, tweet):
	""" Methode de classification d'un tweet via la methode par mots cles
	    : tweet : tweet a classifier
	    @return un tuple (TweetObject, categorie)
	"""

	tmp_tweet = tweet
	neg_count = 0
	pos_count = 0

	with open(config.NEGATIVE_FILE, 'r+') as neg:
	    negatives = neg.read()

	with open(config.POSITIVE_FILE, 'r+') as pos:
	    positives = pos.read()

	tweet = re.findall(r"\w+", tweet.text)

	for word in tweet:
	    if word in negatives:
		neg_count += 1
	    if word in positives:
		pos_count += 1

	res = pos_count - neg_count
	
	# TODO: verifier les valeurs des categories
	if res == 0:
	    return (tmp_tweet, 2)
	elif res > 0:
	    return (tmp_tweet, 4)
	else:
	    return (tmp_tweet, 0)

    def annotation_by_keywords(self):
	""" Cette methode etait utilisee pour classifier des tweets d'une base csv via la methode
	    par mots cles
	    (deprecated)
	"""
        
	with open(config.ANNOTATED_CSV, 'a+') as annotated_csv:
	    csv_writer = csv.writer(annotated_csv)
            with open(config.CLEANED_CSV, 'a+') as cleaned_csv:
	        csv_reader = csv.reader(cleaned_csv)
                for tweet in csv_reader:
	    	    text = tweet[2]
	      	    category = self.process_annotation(text)
	    	    csv_writer.writerow([tweet[0], tweet[1], tweet[2], tweet[3], category])
	    	


    ####################
    ####### KNN ########
    ####################



    def classifier_KNN(self, tweet, k):
	""" Classification d'un tweet via l'algo KNN (K nearest neighbour)
	    : tweet : tweet a classifier
	    : k     : nombre de voisins
	    @return un tuple (TweetObject, categorie)
	"""

	with open(config.ANNOTATED_CSV, 'r+') as annotated_file:
	    csv_reader = csv.reader(annotated_file)

	    # Limite a 250 tweets
	    all_tweets = list(csv_reader)
	    nb_tweets = len(all_tweets)

	    # Creation de la liste des k premiers voisins
	    k_neighbours = all_tweets[1:k]
	    

	    # Dictionnaire ayant pour cle un tuple (tweet.text et categorie) d'un voisin
	    # et a pour valeur sa distance avec le tweet a classifier
	    dist_neighbours = {}
            
	    text_tweet = tweet.text

	    for neighbour in k_neighbours:
		text_neighbour = neighbour[2]
	        cat_neighbour = neighbour[5]

	        dist_t_n = self.distance(text_tweet, text_neighbour)
		dist_neighbours[(text_neighbour, cat_neighbour)] = dist_t_n
	    
	    for i in range(k + 1, nb_tweets - 1):
		dist = self.distance(text_tweet, all_tweets[i][2])

		if dist < any(dist_neighbours.values()):

		    # On supprime la cle du tweet ayant la distance la plus grande
		    higher_dist = max(dist_neighbours.values())
		    key_to_delete = self.key_from_value(dist_neighbours, higher_dist)
		    del dist_neighbours[key_to_delete]
		    
		    # On insere le nouveau tweet au dictionnaire
		    text = all_tweets[i][2]
		    dist_neighbours[(text, all_tweets[i][5])] = dist

	    # TODO
	    vote = self.vote(dist_neighbours)[1]
	    if not vote:
		vote = 2
	    else:
		vote = int(vote)
	
	    return (tweet, vote) 

    def vote(self, dist_neighbours):
	""" Retourne la categorie d'un tweet grace a celles de ses plus
	    proches voisins
	    : dist_neighbours : dictionnaire associant un tuple (text_voisin, categ_voisin)
			        ayant pour valeur la distance avec le tweet a classifier
	    @return la categorie du plus proche voisin
	"""

	counter = Counter(dist_neighbours)
	return self.key_from_value(counter, max(counter.values())) 


    def key_from_value(self, _dict, _value):
	keys = []
	for key, value in _dict.iteritems():
	    if value == _value:
		return key
		#keys.append(key)
	#return keys
		    

    def distance(self, tweet1, tweet2):
	""" Calcule la distance entre deux tweets
	"""

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


   ####################		
   ####### BAYES ######
   ####################


    def classifier_bayes(self, tweet, freq=False, bigramme=False):
	
	proba_neg = self.proba(tweet.text, 'negative', freq=freq, bigramme=bigramme)
	proba_pos = self.proba(tweet.text, 'positive', freq=freq, bigramme=bigramme)
	proba_neu = self.proba(tweet.text, 'neutral', freq=freq, bigramme=bigramme)

	if proba_pos > proba_neu and proba_pos >proba_neg:
	    return (tweet, 4)
	elif proba_neg > proba_pos and proba_neg > proba_neu:
	    return (tweet, 0)
	else:               
	    return (tweet, 2)


    # TODO: Tout mettre en float...
    def get_tweets_from_class(self, _class):
	""" Retourne tous les tweets d'une classe donnee
	"""

	if _class == 'negative':
	    class_id = 0
	elif _class == 'positive':
	    class_id = 4
	elif _class == 'neutral':
	    class_id = 2

	tweets_in_class = Tweet.objects.filter(category=class_id)
	
	return tweets_in_class

    def total_words(self, bigramme=False):
	""" Retourne le nombre de mots total de la base d'apprentissage
	"""

	total_words = 0
	tweets = Tweet.objects.all()
	
	for tweet in tweets:
	    if bigramme:
    	        total_words += len(re.findall(r"\w+ \w+", tweet.text))
            else:	
    	        total_words += len(re.findall(r"\w+", tweet.text))

	return total_words
	    
    def nb_occurence(self, _word, _class, bigramme=False):
	""" Retourne le nombre d'occurences d'un mot dans un classe donnee
	    ainsi que le nombre total de mots dans cette classe
	"""
	# TODO: Calculer tous les mots d'un coup, sinon pas du tout optimise

	count_word = 0
	total_words = 0
	
	tweets = self.get_tweets_from_class(_class)
	total_words = 0

	for tweet in tweets:
	    # TODO: Optimisable ?

	    if bigramme:
		words = re.findall(r"\w+ \w+", tweet.text)
	        total_words += len(words)
	    else:
	        words = re.findall(r"\w+", tweet.text)
		total_words += len(words)

	    for word in words:
		if word == _word:
		    count_word += 1

	return (count_word, total_words)
	
    #### PROBA ####

    def proba_word(self, word, _class, occ_word, freq=False, bigramme=False):
	""" Probabilite d'occurence du mot m dans un texte de la classe c
	    P(m|c)
	"""

	nb_words, total_classwords = self.nb_occurence(word, _class, bigramme=bigramme)
	N = self.total_words(bigramme=bigramme)

	nb_words = float(nb_words)
	total_classwords = float(total_classwords)
	N = float(N)

	if freq:
	    # Frequence
	
 	    return float(nb_words / (total_classwords + N )) ** occ_word
	else:
	    # Presence
	    return float(nb_words / (total_classwords + N ))
	
    def proba_class(self, _class):
	""" Probabilite de la classe	
	    Nombre de tweets de la classe / Nombre de tweets total """
	
	nb_tweets_class = float(len(self.get_tweets_from_class(_class)))
	nb_tweets = float(len(Tweet.objects.all()))
	retuned_value = float(nb_tweets_class / nb_tweets)
	return retuned_value
	
	
    def proba(self, tweet, _class, freq=False, bigramme=False):
	""" Calcul reel de la probabilite: P(classe|t)
	"""

	prob = 0
	proba_class = self.proba_class(_class)

	tweet = tweet.split(" ")
	
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
