# from django import forms
# from django.forms import inlineformset_factory
# from .models import Quiz


# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['text', 'is_correct']


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text']


# class QuizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields = ['title', 'description']

# AnswerFormSet = inlineformset_factory(
#     Quiz 
#     form=AnswerForm, 
#     extra=4,
# )

# QuestionFormSet = inlineformset_factory(
#     Quiz,  
#     form=QuestionForm, 
#     extra=1,
# )
