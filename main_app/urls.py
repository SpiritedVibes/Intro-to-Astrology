from django.urls import path, include
from . import views
from .views import QuizDetailView, CreateQuizView, DeleteQuizView, UpdateQuizView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    path('explore-universe/', views.explore_universe, name='universe_explore'),
    path('universe_journey/', views.journey_start, name='universe_journey'),
    path('quiz-answer/', views.quiz_answer, name='quiz_answer'),
    path('planet-info/', views.planet_info, name='planet_info'),
    path('explore-stars/', views.explore_stars, name='stars_explore'),
    path('quantum-mechanics/', views.quantum_mechanics, name='quantum_mechanics'),

    path('max-planck/', views.max_planck, name='max_planck'),
    path('einstein-quantum/', views.einstein_quantum, name='einstein_quantum'),
    path('bohr-quantum/', views.bohr_quantum, name='bohr_quantum'),
    path('schrodinger-quantum/', views.schrodinger_quantum, name='schrodinger_quantum'),
    path('heisenberg-quantum/', views.heisenberg_quantum, name='heisenberg_quantum'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),

    path('quiz/create/', CreateQuizView.as_view(), name='create_quiz'),
    path('quiz/<int:pk>/update/', UpdateQuizView.as_view(), name='update_quiz'),
    path('quiz/<int:pk>/delete/', DeleteQuizView.as_view(), name='delete_quiz'), 
    
    path('accounts/signup/', views.signup, name='signup'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('accounts/', include('django.contrib.auth.urls')), 
]