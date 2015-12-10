from django.db import models

class Tweet(models.Model):

	CATEGORIES = (
		(-1, -1), # NON ANNOTE
		(0, 0), # NEGATIF
		(1, 1), # NEUTRE
		(2, 2)) # POSITIF

	id = models.IntegerField(default=0, primary_key=True)
	user = models.CharField(max_length=30)
	text = models.TextField()
	date = models.DateField(blank=True)
	request = models.CharField(max_length=100, blank=True)
	category = models.IntegerField(choices=CATEGORIES,
                                    default=-1)
