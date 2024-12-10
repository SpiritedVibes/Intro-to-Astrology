from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct_answer')
    list_filter = ('correct_answer',)
    search_fields = ('question__question_text',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    search_fields = ('question_text',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
