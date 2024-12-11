from django.urls import path, include
from . import views
from .views import QuizDetailView, CreateQuizView, UpdateQuizView, DeleteQuizView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result_view, name='quiz_result'),

    path('quiz/create/', CreateQuizView.as_view(), name='create_quiz'),
    path('quiz/<int:pk>/update/', UpdateQuizView.as_view(), name='update_quiz'),
    path('quiz/<int:pk>/delete/', DeleteQuizView.as_view(), name='delete_quiz'), 
    
    path('accounts/signup/', views.signup, name='signup'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('accounts/', include('django.contrib.auth.urls')), 
]