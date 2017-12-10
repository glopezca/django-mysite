from django import formsfrom django.utils import timezonefrom datetime import datefrom .models import Questionfrom django.conf import settings
class QuestionCreateForm(forms.ModelForm):    question_text = forms.CharField(required=True, label ='Pregunta')    #pub_date = forms.DateField(required=True, initial=date.today(), widget=forms.HiddenInput) # Este valor lo genero en la vista    choice1 = forms.CharField(required=True, label='Opción 1')    choice2 = forms.CharField(required=True, label='Opción 2')    choice3 = forms.CharField(required=True, label='Opción 3')    class Meta:
       model = Question
       fields = ['question_text',]
       #fields = ['question_text', 'pub_date'] # Solo exijo el título de la pregunta
