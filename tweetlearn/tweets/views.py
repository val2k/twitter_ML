from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Tweet
import tlearn

def index(request):
	tweets = Tweet.objects.all()
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		'tweets': tweets,
	})
	return HttpResponse(template.render(context))

def parse_request(request):
	algo = request.POST.get('algo')
	twt_request = request.POST.get('the_search')

	proxy = True if request.POST.get('proxy') else False

	if algo == 'KNN':
	    http_res = knn(request, twt_request, proxy)
	elif algo == 'Keyword':
	    http_res = keyword(request, twt_request, proxy)
	elif ("Bayes" in algo):
	    bigramme = 0
	    frequence = 0

	    if "Unigramme" in algo:
	        if "frequence" in algo:
		    frequence = 1
	    else:
		bigramme = 1
		if "frequence" in algo:
		    frequence = 1
		
	    http_res = bayes(request, twt_request, proxy, frequence, bigramme)

	return http_res 

def knn(request, twt_request, proxy):
	tln = tlearn.TweetLearn(proxy)
	
	tweets = tln.process_classif('KNN', twt_request)
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		  'tweets': tweets,
	})	
	return HttpResponse(template.render(context))

def keyword(request, twt_request, proxy):

	tln = tlearn.TweetLearn(proxy)

	tweets = tln.process_classif('Keyword', twt_request)
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		  'tweets': tweets,
	})	
	return HttpResponse(template.render(context))
	

def bayes(request, twt_request, proxy, freq, big):

	tln = tlearn.TweetLearn(proxy)

	tweets = tln.process_classif('Bayes', twt_request, freq, big)
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		  'tweets': tweets,
	})	
	return HttpResponse(template.render(context))
