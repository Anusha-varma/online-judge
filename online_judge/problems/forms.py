from django import forms
from .models import CodeSubmission, Problem, Contest

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
]


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title',
            'description',
            'difficulty',
            'sample_input',
            'sample_output',
            'test_input',   
            'expected_output',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'sample_input': forms.Textarea(attrs={'rows': 3}),
            'sample_output': forms.Textarea(attrs={'rows': 3}),
            'test_input': forms.Textarea(attrs={'rows': 3}),
            'expected_output': forms.Textarea(attrs={'rows': 3}),
        }

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'description', 'problems', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        


