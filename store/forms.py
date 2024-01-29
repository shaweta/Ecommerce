from django import forms
from store.models import ReviewRatings

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRatings
        fields = ['subject', 'review', 'rating']