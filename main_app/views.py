from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
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

@login_required
def quiz_result_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_result = QuizResult.objects.filter(quiz=quiz, user=request.user).last()
    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'score': quiz_result.score,
        'total_questions': quiz.questions.count(),
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
    template_name = 'main_app/quiz_form.html'

    def form_valid(self, form):
        # Save the quiz instance
        form.instance.user = self.request.user
        
        # Check if the "Add Another Question" button was clicked
        if 'add_question' in self.request.POST:
            # If the "Add Another Question" button was clicked, we just return without saving
            return self.render_to_response(self.get_context_data(form=form, add_question=True))

        # If the "Save Quiz" button was clicked, save the quiz and process the questions
        response = super().form_valid(form)

        # Process the questions after the form is valid (you can save the questions here if needed)
        question_data = self.request.POST.getlist('question_text')
        answers_1 = self.request.POST.getlist('answer_1')
        answers_2 = self.request.POST.getlist('answer_2')
        answers_3 = self.request.POST.getlist('answer_3')
        answers_4 = self.request.POST.getlist('answer_4')
        correct_answers = self.request.POST.getlist('correct_answer')

        for i in range(len(question_data)):
            Question.objects.create(
                quiz=form.instance,
                question_text=question_data[i],
                answer_1=answers_1[i],
                answer_2=answers_2[i],
                answer_3=answers_3[i],
                answer_4=answers_4[i],
                correct_answer=correct_answers[i]
            )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if we are adding a new question
        if 'add_question' in self.request.POST:
            # If adding a new question, pass the current question data
            question_data = self.request.POST.getlist('question_text')
            context['question_data'] = question_data
        else:
            context['question_data'] = []  # Empty list for creating new questions

        return context

class UpdateQuizView(TeacherRequiredMixin, UpdateView):
    model = Quiz
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching questions related to the quiz
        context['question_data'] = self.object.questions.all()
        return context


class DeleteQuizView(TeacherRequiredMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/delete_quiz.html'
    success_url = reverse_lazy('quiz_list')
