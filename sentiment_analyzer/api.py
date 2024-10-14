from rest_framework.views import APIView
from rest_framework.response import Response
from .nlp_model import SentimentAnalyzer

analyzer = SentimentAnalyzer()

class SentimentAnalysisAPI(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        model = request.data.get('model', 'bert')
        sentiment, score = analyzer.analyze_sentiment(text, model)
        aspects = analyzer.aspect_based_analysis(text)
        return Response({
            'overall_sentiment': sentiment,
            'overall_score': score,
            'aspect_analysis': aspects
        })