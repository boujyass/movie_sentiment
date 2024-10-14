from django.shortcuts import render, redirect
from .nlp_model import SentimentAnalyzer
from .models import Review

analyzer = SentimentAnalyzer()

def analyze_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text', '')
        sentiment, score = analyzer.analyze_sentiment(review_text)
        
        # Save to database
        Review.objects.create(text=review_text, sentiment=sentiment, score=score)
        
        context = {
            'sentiment': sentiment,
            'score': score,
            'review': review_text,
            'explanation': get_explanation(sentiment, score)
        }
        return render(request, 'result.html', context)
    return render(request, 'input.html')

def get_explanation(sentiment, score):
    if sentiment == 'Positive':
        return f"The review is positive with a confidence of {score:.2f}. This suggests the movie was well-received."
    elif sentiment == 'Negative':
        return f"The review is negative with a confidence of {score:.2f}. This suggests the movie was not well-received."
    else:
        return f"The review is neutral with a confidence of {score:.2f}. This suggests mixed feelings about the movie."

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_list.html', {'reviews': reviews})


import json
from django.shortcuts import render
from django.db.models import Avg
from django.db.models.functions import TruncDate
from .models import Review

def trend_analysis(request):
    daily_sentiments = Review.objects.annotate(date=TruncDate('created_at')) \
                              .values('date') \
                              .annotate(avg_score=Avg('score')) \
                              .order_by('date')
    
    dates = [item['date'].strftime('%Y-%m-%d') for item in daily_sentiments]
    scores = [float(item['avg_score']) for item in daily_sentiments]
    
    context = {
        'dates_json': json.dumps(dates),
        'scores_json': json.dumps(scores),
    }
    
    return render(request, 'trend_analysis.html', context)

import requests

def get_movie_info(title):
    api_key = '1d11e782'  # Get this from http://www.omdbapi.com/
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def analyze_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text', '')
        movie_title = request.POST.get('movie_title', '')
        sentiment, score = analyzer.analyze_sentiment(review_text)
        aspects = analyzer.aspect_based_analysis(review_text)
        movie_info = get_movie_info(movie_title)
        
        Review.objects.create(text=review_text, sentiment=sentiment, score=score)
        
        context = {
            'sentiment': sentiment,
            'score': score,
            'review': review_text,
            'aspects': aspects,
            'movie_info': movie_info
        }
        return render(request, 'result.html', context)
    return render(request, 'input.html')