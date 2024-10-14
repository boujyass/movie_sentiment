from django.db import models

class Review(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=10)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sentiment} ({self.score}): {self.text[:50]}..."