from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# class Quiz(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.title

# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
#     question_text = models.CharField(max_length=255)

#     def __str__(self):
#         return self.question_text

# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Answer for question: {self.question}'

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    question_text = models.CharField(max_length=255)
    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    answer_4 = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('quiz_list')

class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    score = models.IntegerField()
    answers = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.user.username} in {self.quiz.title}"

