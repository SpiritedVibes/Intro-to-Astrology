from django.urls import path
from . import views
from .views import QuizResultView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.QuizView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/result/', QuizResultView.as_view(), name='quiz_result'),
    path('accounts/signup/', views.signup, name='signup'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    # path('horoscopes/', views.horoscopes, name='horoscopes'),
    # path('birth_chart/', views.birth_chart, name='birth_chart'),
    # path('contact/', views.contact, name='contact'),
]