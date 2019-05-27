from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Work, Card


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class DateInput(forms.DateInput):
    """마감기한 입력 시 달력 위젯 사용"""
    input_type = 'date'


class WorkPriorityInput(forms.Select):
    """우선 순위 입력 시 높음, 중간, 낮음에서 선택하는 select 위젯 사용"""
    choices = Work.WORK_PRIORITY


class CardPriorityInput(forms.Select):
    """우선 순위 입력 시 높음, 중간, 낮음에서 선택하는 select 위젯 사용"""
    choices = Card.CARD_PRIORITY


class CardForm(ModelForm):
    """TODO (Card model) 생성, 수정 시 사용되는 Form"""
    class Meta:
        model = Card
        fields = ['name', 'description', 'deadline', 'priority', 'done']
        widgets = {
            'deadline': DateInput(),
            'priority': CardPriorityInput(),
        }


"""Work 생성 시 Card도 생성 할 수 있음"""
CardInlineFormSet = inlineformset_factory(
                        Work,
                        Card,
                        form=CardForm,
                        can_delete=False,
                        extra=1)


class WorkForm(ModelForm):
    """TODO (Work model) 생성, 수정 시 사용되는 Form"""
    class Meta:
        model = Work
        fields = ['name', 'description', 'deadline', 'priority', 'done']
        widgets = {
            'deadline': DateInput(),
            'priority': WorkPriorityInput(),
        }
