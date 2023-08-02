from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'recommendation']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '5'}),
            'recommendation': forms.RadioSelect()
        }
        labels = {
            'content': '',
            'recommendation': 'Would you recommend this anime?'
        }