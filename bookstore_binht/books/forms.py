from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "rating": forms.HiddenInput(attrs={"class": "form-control"}),
        }
        labels = {
            "content": "Your review:",
        }
