from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from .models import Quiz, QuizResult, Question


def unauthorized(request):
    return render(request, 'unauthorized.html')


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Teacher').exists()
    

class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


def quiz_list(request):
    quizzes = Quiz.objects.all()
    is_teacher = request.user.groups.filter(name='Teacher').exists() if request.user.is_authenticated else False
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'is_teacher': is_teacher})


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.all()
        return context

@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    
    if request.method == 'POST':
        score = 0
        answers = {}
        
        for question in quiz.questions.all():
            user_answer = request.POST.get(f'question_{question.id}')
            correct_answer = question.correct_answer
            
            answers[question.id] = user_answer
            if user_answer == correct_answer:
                score += 1
        
        
        quiz_result = QuizResult.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            answers=answers
        )
        
        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': quiz.questions.count(),
        })
    
    return render(request, 'quiz/quiz.html', {'quiz': quiz})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Quiz, QuizResult

@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.questions.all()
        answers = {}
        score = 0

        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer: 
                answers[question.id] = selected_answer
                if selected_answer == question.correct_answer:
                    score += 1

        QuizResult.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            answers=answers
        )

        return render(request, 'quiz/quiz_results.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': questions.count(),
        })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='User'))
            login(request, user)
            return redirect('quiz_list')
        error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
        error_message = ''
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})


class CreateQuizView(TeacherRequiredMixin, CreateView):
    model = Quiz
    fields = ['title', 'description']
    
    def form_valid(self, form):
    
        form.instance.user = self.request.user
        quiz = form.save()
        
    
        question_count = len(self.request.POST.getlist('question_text_1')) 
        
        for i in range(question_count):
            question_text = self.request.POST.get(f'question_text_{i+1}')
            answer_1 = self.request.POST.get(f'answer_1_{i+1}')
            answer_2 = self.request.POST.get(f'answer_2_{i+1}')
            answer_3 = self.request.POST.get(f'answer_3_{i+1}')
            answer_4 = self.request.POST.get(f'answer_4_{i+1}')
            correct_answer = self.request.POST.get(f'correct_answer_{i+1}')
            
            
            question = Question(
                quiz=quiz,
                question_text=question_text,
                answer_1=answer_1,
                answer_2=answer_2,
                answer_3=answer_3,
                answer_4=answer_4,
                correct_answer=correct_answer,
            )
            question.save()
        
        
        if self.request.POST.get('add_question'):
            return HttpResponseRedirect(self.request.path)
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_data'] = [] 
        return context
        
class UpdateQuizView(TeacherRequiredMixin, UpdateView):
    model = Quiz
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['question_data'] = self.object.questions.all()
        return context


class DeleteQuizView(TeacherRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/delete_quiz.html'
    success_url = reverse_lazy('quiz_list')
