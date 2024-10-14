from django.urls import path
from . import views
from sentiment_analyzer.api import SentimentAnalysisAPI
urlpatterns = [
    path('', views.analyze_review, name='analyze_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('api/analyze/', SentimentAnalysisAPI.as_view(), name='api_analyze'),
    path('trends/', views.trend_analysis, name='trend_analysis'),
]