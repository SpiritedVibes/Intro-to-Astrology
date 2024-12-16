from django.urls import path, include
from . import views
from .views import QuizDetailView, CreateQuizView, DeleteQuizView, UpdateQuizView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('explore-universe/', views.explore_universe, name='universe_explore'),
    path('universe_journey/', views.journey_start, name='universe_journey'),
    path('quiz-answer/', views.quiz_answer, name='quiz_answer'),
    path('planet-info/', views.planet_info, name='planet_info'),
    path('explore-stars/', views.explore_stars, name='stars_explore'),

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