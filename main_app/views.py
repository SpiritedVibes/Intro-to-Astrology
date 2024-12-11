from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from .models import Quiz, QuizResult, Answer, Question
from django.http import Http404
from .forms import QuizForm


def is_group_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    is_teacher = request.user.groups.filter(name='Teacher').exists() if request.user.is_authenticated else False
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'is_teacher': is_teacher})


@method_decorator(login_required, name='dispatch')
class QuizView(View):
    template_name = 'quiz/quiz.html'
    result_template = 'quiz/quiz_result.html'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return render(request, self.template_name, {'quiz': quiz, 'questions': quiz.questions.all()})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = self.calculate_score(request, quiz)
        return render(request, self.result_template, {'quiz': quiz, 'score': score})

    def calculate_score(self, request, quiz):
        score = sum(
            1 for question in quiz.questions.all()
            if (selected := request.POST.get(f'question_{question.id}')) and \
               question.answers.filter(id=selected, is_correct=True).exists()
        )
        return score

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'

@login_required
def quiz_result_view(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        questions = quiz.questions.all()
        
        
        score = 0
        user_answers = []
        answers_data = {} 
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                user_answers.append({
                    'question': question,
                    'selected_answer': selected_answer,
                    'is_correct': selected_answer.correct_answer == int(selected_answer_id),
                })

                
                if selected_answer.correct_answer == int(selected_answer_id):
                    score += 1

                answers_data[question.id] = selected_answer_id

        quiz_result = QuizResult.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            answers=answers_data
        )

      
        context = {
            'quiz': quiz,
            'score': score,
            'user_answers': user_answers,
            'total_questions': questions.count(),
            'quiz_result': quiz_result 
        }

        return render(request, 'quiz/quiz_result.html', context)

    else:
        raise Http404("Invalid request")


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


def unauthorized(request):
    return render(request, 'unauthorized.html')


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_group_member(self.request.user, 'Teacher')

class CreateQuizView(TeacherRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/create_quiz.html'
    success_url = reverse_lazy('quiz_list')

def form_valid(self, form):
    print("POST data:", self.request.POST) 
    return super().form_valid(form)

def form_invalid(self, form):
    print("Form errors:", form.errors)
    return super().form_invalid(form)


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class UpdateQuizView(TeacherRequiredMixin, UpdateView):
    model = Quiz
    fields = ['title', 'description']
    template_name = 'quiz/update_quiz.html'
    success_url = reverse_lazy('quiz_list')

class DeleteQuizView(TeacherRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/delete_quiz.html'
    success_url = reverse_lazy('quiz_list')
