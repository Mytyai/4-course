from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class QuestionCreateForm(forms.Form):
    question_text = forms.CharField(
        label="Текст вопроса",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    choices = forms.CharField(
        label="Варианты ответа (по одному в строке)",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Вариант 1\nВариант 2\nВариант 3"
        })
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]