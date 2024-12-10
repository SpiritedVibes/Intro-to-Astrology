from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Quiz, Question, Answer


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

def about(request):
    return render(request, 'about.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()


@method_decorator(login_required, name='dispatch')
class QuizView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = self.calculate_score(request, quiz)
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score})

    def calculate_score(self, request, quiz):
        score = 0
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = question.answers.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
        return score


@method_decorator(login_required, name='dispatch')
class QuizResultView(View):
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = self.calculate_score(request, quiz)
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score})

    def calculate_score(self, request, quiz):
        score = 0
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = question.answers.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
        return score


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list') 
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


@user_passes_test(is_admin, login_url='unauthorized')
@login_required
def create_quiz(request):
    if request.method == 'POST':
    
        title = request.POST.get('title')
        description = request.POST.get('description')
        quiz = Quiz.objects.create(title=title, description=description)

        question_count = len(request.POST.getlist('questions'))
        for i in range(question_count):
            question_text = request.POST.get(f'questions[{i}][question]')
            question = Question.objects.create(quiz=quiz, question_text=question_text)

            answer_1 = request.POST.get(f'questions[{i}][answers][0]')
            answer_2 = request.POST.get(f'questions[{i}][answers][1]')
            answer_3 = request.POST.get(f'questions[{i}][answers][2]')
            answer_4 = request.POST.get(f'questions[{i}][answers][3]')

            correct_answer = int(request.POST.get(f'questions[{i}][correct_answer]'))

            Answer.objects.create(
                question=question,
                answer_1=answer_1,
                answer_2=answer_2,
                answer_3=answer_3,
                answer_4=answer_4,
                correct_answer=correct_answer
            )

        return redirect('quiz_list')

    return render(request, 'create_quiz.html')

def unauthorized(request):
    return render(request, 'unauthorized.html')