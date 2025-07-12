from django import forms
from .models import Item, Profile

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'size', 'condition', 'points_required', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
