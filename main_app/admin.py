from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3 
    fields = ['text', 'is_correct']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
