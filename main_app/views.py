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
from .models import Quiz, QuizResult, Question, UserProfile, PlanetInfo
from .forms import UserProfileForm


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
    

def explore_universe(request):
    return render(request, 'universe_explore.html')

def journey_start(request):
    return render(request, 'universe_journey.html')

def start_journey(request):
    space_facts = {
        'largest_planet': {
            'title': "The Largest Planet",
            'description': "The largest planet in our solar system is Jupiter! It's a gas giant with a Great Red Spot, which is a massive storm.",
            'more_info': "Jupiter has a diameter of 142,984 km, and it's so large that more than 1,300 Earths could fit inside it!"
        },
        'closest_star': {
            'title': "The Closest Star",
            'description': "The closest star to Earth is the Sun! It's our primary source of light and energy.",
            'more_info': "The Sun is about 93 million miles away from Earth, and it's a medium-sized star, classified as a G-type main-sequence star."
        },
        'closest_galaxy': {
            'title': "The Closest Galaxy",
            'description': "The Andromeda Galaxy is the closest large galaxy to the Milky Way. It's about 2.537 million light-years away.",
            'more_info': "Andromeda is on a collision course with the Milky Way, but don't worry—it will take about 4 billion years before they merge!"
        },
        'black_hole': {
            'title': "What is a Black Hole?",
            'description': "A black hole is a region of space where gravity is so strong that not even light can escape.",
            'more_info': "Black holes are formed when massive stars collapse under their own gravity. Their event horizon is the boundary beyond which nothing can return."
        },
        'sun_fuel': {
            'title': "The Sun's Fuel",
            'description': "The Sun's energy is powered by nuclear fusion of hydrogen atoms into helium in its core.",
            'more_info': "This process releases an enormous amount of energy, which is what powers the Sun and gives us light and warmth."
        },
        'mars': {
            'title': "The Red Planet",
            'description': "Mars is known as the Red Planet due to its reddish appearance, caused by iron oxide (rust) on its surface.",
            'more_info': "Mars has the highest mountain in the solar system, Olympus Mons, and it has two moons, Phobos and Deimos."
        },
        'jupiter_moons': {
            'title': "Moons of Jupiter",
            'description': "Jupiter has 79 moons, the largest of which is Ganymede, which is even larger than the planet Mercury!",
            'more_info': "Jupiter's moons are diverse, and some may even have subsurface oceans that could support life."
        },
        'venus': {
            'title': "The Longest Day",
            'description': "Venus has the longest day of any planet in our solar system. It takes 243 Earth days to complete one full rotation!",
            'more_info': "Interestingly, Venus' day is longer than its year, which only takes 225 Earth days to orbit the Sun."
        },
        'sputnik': {
            'title': "The First Artificial Satellite",
            'description': "Sputnik 1 was the first artificial satellite to orbit the Earth, launched by the Soviet Union in 1957.",
            'more_info': "It marked the beginning of the space race and was a major milestone in space exploration history."
        },
        'milky_way': {
            'title': "The Milky Way",
            'description': "The Milky Way is a spiral galaxy that contains our solar system and billions of stars.",
            'more_info': "It's estimated that there are over 100 billion stars in the Milky Way, and it's just one of the billions of galaxies in the universe."
        },
        'planet_count': {
            'title': "How Many Planets?",
            'description': "There are 8 planets in our solar system. They are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
            'more_info': "Pluto was once considered the 9th planet, but it was reclassified as a dwarf planet in 2006."
        },
        'nebula': {
            'title': "Nebulas and Star Formation",
            'description': "Nebulas are large clouds of gas and dust where new stars are born.",
            'more_info': "The most famous nebula is the Orion Nebula, where thousands of new stars are being formed."
        },
        'galaxies': {
            'title': "Types of Galaxies",
            'description': "There are three main types of galaxies: spiral, elliptical, and irregular.",
            'more_info': "The Milky Way is a spiral galaxy, while the Andromeda Galaxy is also spiral, and galaxies like the Messier 87 are elliptical."
        },
        'event_horizon': {
            'title': "The Event Horizon",
            'description': "The event horizon is the boundary around a black hole beyond which nothing, not even light, can escape.",
            'more_info': "Once something crosses this boundary, it's lost to the black hole forever."
        },
        'first_in_space': {
            'title': "First Human in Space",
            'description': "Yuri Gagarin was the first human to go into space, orbiting the Earth on April 12, 1961.",
            'more_info': "He made just one orbit around Earth in his spacecraft, Vostok 1, and made history as the first space traveler."
        },
    }

    
    selected_fact = request.GET.get('fact')
    fact = "Welcome to your space exploration! Click a button to start your journey."
    more_info = ""

    if selected_fact and selected_fact in space_facts:
        fact = space_facts[selected_fact]['description']
        more_info = space_facts[selected_fact]['more_info']

    return render(request, 'universe_journey.html', {'fact': fact, 'more_info': more_info, 'space_facts': space_facts})

def quiz_answer(request):
    if request.method == 'POST':
        selected_planet = request.POST.get('planet')
        
        if selected_planet == 'Mercury':
            quiz_feedback = "Correct! Mercury is indeed the closest planet to the Sun."
        else:
            quiz_feedback = "Oops! The correct answer is Mercury."
        
        return render(request, 'universe_explore.html', {'quiz_feedback': quiz_feedback})

def planet_info(request):
    planet_name = request.POST.get('planet')
    planet_info = None

    planet_data = {
        'mercury': {
            'name': 'Mercury',
            'description': 'Mercury is the closest planet to the Sun and the smallest in our solar system.',
            'image_url': 'main_app/static/images/mercury.jpg'
        },
        'venus': {
            'name': 'Venus',
            'description': 'Venus is the second planet from the Sun and has a thick, toxic atmosphere.',
            'image_url': 'main_app/static/images/Venus.webp'
        },
        'earth': {
            'name': 'Earth',
            'description': 'Earth is our home planet and the only one known to support life.',
            'image_url': 'main_app/static/images/Earth.jpg'
        },
        'mars': {
            'name': 'Mars',
            'description': 'Mars is the 4th planet from the Sun and is known for its reddish appearance.',
            'image_url': 'main_app/static/images/Mars.webp'
        },
        'jupiter': {
            'name': 'Jupiter',
            'description': 'Jupiter is the largest planet in our solar system, with a massive storm called the Great Red Spot.',
            'image_url': 'main_app/static/images/Jupiter.jpeg'
        },
        'saturn': {
            'name': 'Saturn',
            'description': 'Saturn is known for its stunning rings made of ice and rock particles.',
            'image_url': 'main_app/static/images/Saturn.jpg'
        },
        'uranus': {
            'name': 'Uranus',
            'description': 'Uranus is a pale blue planet that rotates on its side, making it unique in our solar system.',
            'image_url': 'main_app/static/images/Uranus.jpg'
        },
        'neptune': {
            'name': 'Neptune',
            'description': 'Neptune is a deep blue planet known for its strong winds and storms.',
            'image_url': 'main_app/static/images/Uranus.jpg'
        },
        'pluto': {
            'name': 'Pluto',
            'description': 'Pluto, once considered the ninth planet, is now classified as a dwarf planet.',
            'image_url': 'main_app/static/images/Pluto.jpg'
        }
    }

    if planet_name and planet_name.lower() in planet_data:
        planet = planet_data[planet_name.lower()]
        planet_info = PlanetInfo(
            name=planet['name'],
            description=planet['description'],
            image_url=planet['image_url']
        )

    return render(request, 'universe_explore.html', {'planet_info': planet_info})



def explore_stars(request):
    return render(request, 'stars_explore.html')

def quantum_mechanics(request):
    return render(request, 'quantum_mechanics.html')

def max_planck(request):
    return render(request, 'max_planck.html')

def einstein_quantum(request):
    return render(request, 'einstein_quantum.html')

def bohr_quantum(request):
    return render(request, 'bohr_quantum.html')

def schrodinger_quantum(request):
    return render(request, 'schrodinger_quantum.html')

def heisenberg_quantum(request):
    return render(request, 'heisenberg_quantum.html')

@login_required
def user_dashboard(request):
    user_results = QuizResult.objects.filter(user=request.user).select_related('quiz')
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'user_dashboard.html', {
        'user_results': user_results,
        'user_profile': user_profile
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})

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
