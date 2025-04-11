
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'subject', 'feedback_text', 'email', 'future_projects_likelihood']