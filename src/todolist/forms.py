from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Work, Card


class DateInput(forms.DateInput):
    input_type = 'date'


class WorkPriorityInput(forms.Select):
    choices = Work.WORK_PRIORITY


class CardPriorityInput(forms.Select):
    choices = Card.CARD_PRIORITY


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'description', 'deadline', 'priority', 'done']
        widgets = {
            'deadline': DateInput(),
            'priority': CardPriorityInput(),
        }


CardInlineFormSet = inlineformset_factory(
                        Work,
                        Card,
                        form=CardForm,
                        can_delete=False,
                        extra=1)


class WorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ['name', 'description', 'deadline', 'priority', 'done']
        widgets = {
            'deadline': DateInput(),
            'priority': WorkPriorityInput(),
        }
