from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.models = {
            'bert': pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"),
            'roberta': pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"),
            'distilbert': pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        }

    def analyze_sentiment(self, text, model='bert'):
        result = self.models[model](text)[0]
        label = result['label']
        score = result['score']
        
        if model == 'bert':
            stars = int(label.split()[0])
            if stars <= 2:
                sentiment = 'Negative'
            elif stars == 3:
                sentiment = 'Neutral'
            else:
                sentiment = 'Positive'
        elif model in ['roberta', 'distilbert']:
            sentiment = label.lower().capitalize()
        
        return sentiment, score

    def get_sentiment_score(self, text, model='bert'):
        _, score = self.analyze_sentiment(text, model)
        return score

    def aspect_based_analysis(self, text):
        aspects = {'acting': [], 'plot': [], 'visuals': [], 'soundtrack': []}
        words = text.lower().split()
        
        for i, word in enumerate(words):
            for aspect in aspects:
                if aspect in words[max(0, i-5):i+5]:
                    aspects[aspect].append(word)
        
        results = {}
        for aspect, aspect_words in aspects.items():
            if aspect_words:
                sentiment, score = self.analyze_sentiment(' '.join(aspect_words))
                results[aspect] = {'sentiment': sentiment, 'score': score}
        
        return results