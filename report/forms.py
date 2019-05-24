from django import forms
from .models import Day, Category, Event

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['category', 'description', 'expense']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = "분류"
        self.fields['description'].label = "내용"
        self.fields['expense'].label = "금액"
        self.fields['description'].widget.attrs = {'placeholder': "사용처 입력"}