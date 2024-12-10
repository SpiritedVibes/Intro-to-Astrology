from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Quiz

def home(request):
    return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')

def about(request):
    return render(request, 'about.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

class QuizView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        
        return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0
        
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer and user_answer == question.correct_answer:
                score += 1

        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': len(questions)
        })
