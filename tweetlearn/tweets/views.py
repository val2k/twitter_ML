from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Tweet

def index(request):
	tweets = Tweet.objects.all()
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		'tweets': tweets,
	})
	return HttpResponse(template.render(context))

def knn(request):
	tweets = Tweet.objects.filter(category=2)
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		  'tweets': tweets,
	})	
	return HttpResponse(template.render(context))

def bayes(request):
	tweets = Tweet.objects.filter(category=2)
	template = loader.get_template('tweets/bootstrap/index.html')
	context = RequestContext(request, {
		  'tweets': tweets,
	})	
	return HttpResponse(template.render(context))
